import { Container } from "@cloudflare/containers";
import { guardAnalysis } from "./size-guard.mjs";

function record(env, event, platform = "unknown", tool = "unknown", format = "", status = 0) {
  const clean = (value, pattern) => typeof value === "string" && pattern.test(value) ? value : "unknown";
  try {
    env.EVENTS?.writeDataPoint({
      blobs: [clean(event, /^[a-z_]{1,40}$/), clean(platform, /^(youtube|instagram|tiktok|facebook|pinterest|reddit|threads|dailymotion|unknown)$/),
        clean(tool, /^[a-z0-9-]{1,60}$/), clean(format, /^(mp3|mp4|m4a|webm|jpg|jpeg|png|gif|webp|unknown|)$/), String(status)],
      doubles: [1],
      indexes: ["savefromnet"],
    });
  } catch (error) {
    console.error("Could not record aggregate event", error);
  }
}

async function smallJson(request) {
  if (Number(request.headers.get("content-length") || 0) > 4096) return {};
  const reader = request.clone().body?.getReader();
  if (!reader) return {};
  const chunks = [];
  let length = 0;
  try {
    while (length <= 4096) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > 4096) return {};
      chunks.push(value);
    }
    const buffer = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) { buffer.set(chunk, offset); offset += chunk.byteLength; }
    const parsed = JSON.parse(new TextDecoder().decode(buffer));
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch {
    return {};
  } finally {
    reader.cancel().catch(() => {});
  }
}

export class DownloaderContainer extends Container {
  defaultPort = 8080;
  sleepAfter = "5m";

  async onActivityExpired() {
    try {
      const response = await this.containerFetch("http://localhost:8080/api/activity");
      if (response.ok && (await response.json()).active > 0) {
        this.renewActivityTimeout();
        return;
      }
    } catch (error) {
      console.error("Unable to check active downloads", error);
    }
    await this.stop();
  }
}

export default {
  async fetch(request, env) {
    const pathname = new URL(request.url).pathname;
    const body = request.method === "POST" && (pathname === "/api/analyze" || pathname === "/api/download" || pathname === "/api/event") ? await smallJson(request) : {};
    if (request.method === "POST" && (pathname === "/api/download" || pathname === "/api/analyze" || pathname === "/api/event")) {
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const limiter = pathname === "/api/download" ? env.DOWNLOAD_LIMIT :
        pathname === "/api/analyze" ? env.ANALYZE_LIMIT : env.EVENT_LIMIT;
      const { success } = await limiter.limit({ key: ip });
      if (!success) {
        record(env, "rate_limited", "unknown", "unknown", "", 429);
        return new Response(JSON.stringify({ error: "Too many requests. Please try again shortly." }), {
          status: 429,
          headers: { "Content-Type": "application/json", "Retry-After": "60" },
        });
      }
    }
    if (request.method === "GET" && pathname.startsWith("/api/file/")) {
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const { success } = await env.FILE_LIMIT.limit({ key: ip });
      if (!success) {
        record(env, "rate_limited", "unknown", "file", "", 429);
        return new Response(JSON.stringify({ error: "Too many file requests. Please try again shortly." }), {
          status: 429,
          headers: { "Content-Type": "application/json", "Retry-After": "60" },
        });
      }
    }
    if (pathname === "/api/analyze" && request.method === "POST") {
      record(env, "url_submitted", "unknown", "unknown");
    }
    const response = await env.DOWNLOADER.getByName("multi-primary").fetch(request);
    if (pathname === "/api/analyze" && request.method === "POST") {
      if (response.ok) {
        try {
          const result = await response.clone().json();
          const safeResult = guardAnalysis(result);
          if (!safeResult.formats.length) {
            record(env, "analysis_failed", result.platform, result.tool, "", 422);
            const headers = new Headers(response.headers);
            headers.delete("Content-Length");
            return new Response(JSON.stringify({ code: "no_formats", error: "No available format fits the 512 MB download limit." }),
              { status: 422, headers });
          }
          record(env, "platform_detected", result.platform, result.tool, "", response.status);
          record(env, "analysis_successful", result.platform, result.tool, "", response.status);
          const headers = new Headers(response.headers);
          headers.delete("Content-Length");
          return new Response(JSON.stringify(safeResult), { status: response.status, headers });
        } catch { record(env, "analysis_failed", "unknown", "unknown", "", 500); }
      } else {
        record(env, "analysis_failed", "unknown", "unknown", "", response.status);
      }
    } else if (pathname === "/api/download" && request.method === "POST" && response.ok) {
      try {
        const result = await response.clone().json();
        record(env, "download_clicked", result.platform, result.tool, result.format, response.status);
      } catch { /* The Flask response still reaches the browser. */ }
    } else if (pathname === "/api/event" && request.method === "POST" && response.ok) {
      if (["format_selected", "error_occurred"].includes(body.event)) {
        record(env, body.event, body.platform, body.tool, body.format || "", response.status);
      }
    } else if (request.method === "GET" && pathname.startsWith("/api/file/") && response.status === 200 && response.body) {
      const platform = response.headers.get("X-SFN-Platform") || "unknown";
      const tool = response.headers.get("X-SFN-Tool") || "unknown";
      const format = response.headers.get("X-SFN-Format") || "";
      const headers = new Headers(response.headers);
      headers.delete("X-SFN-Platform");
      headers.delete("X-SFN-Tool");
      headers.delete("X-SFN-Format");
      const stream = response.body.pipeThrough(new TransformStream({
        flush() { record(env, "download_completed", platform, tool, format, response.status); },
      }));
      return new Response(stream, { status: response.status, statusText: response.statusText, headers });
    }
    return response;
  },
};
