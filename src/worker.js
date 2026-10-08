import { Container } from "@cloudflare/containers";
import { guardAnalysis } from "./size-guard.mjs";
import { VisitorAnalytics } from "./visitor-store.mjs";
import { dashboardHtml } from "./analytics-dashboard.mjs";
import world from "./analytics-world.json";

export { VisitorAnalytics };

function dashboardAuthorized(request, env) {
  if (!env.DASHBOARD_PASSWORD) return false;
  const header = request.headers.get("Authorization") || "";
  if (!header.startsWith("Basic ") || header.length > 500) return false;
  try {
    const decoded = atob(header.slice(6));
    const expected = `admin:${env.DASHBOARD_PASSWORD}`;
    if (decoded.length !== expected.length) return false;
    let diff = 0;
    for (let i = 0; i < decoded.length; i++) diff |= decoded.charCodeAt(i) ^ expected.charCodeAt(i);
    return diff === 0;
  } catch { return false; }
}

function privateHeaders(extra = {}) {
  return { "Cache-Control": "private, no-store", "X-Robots-Tag": "noindex, nofollow", ...extra };
}

function dashboardChallenge() {
  return new Response("Sign in to view SaveFromNet analytics.", {
    status: 401,
    headers: privateHeaders({ "WWW-Authenticate": 'Basic realm="SaveFromNet analytics", charset="UTF-8"' }),
  });
}

async function visitorHash(request, secret) {
  const day = new Date().toISOString().slice(0, 10);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const agent = (request.headers.get("User-Agent") || "").slice(0, 256);
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const bytes = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${day}|${ip}|${agent}`));
  return [...new Uint8Array(bytes)].map(byte => byte.toString(16).padStart(2, "0")).join("");
}

function record(env, event, platform = "unknown", tool = "unknown", format = "", status = 0) {
  const clean = (value, pattern) => typeof value === "string" && pattern.test(value) ? value : "unknown";
  try {
    env.EVENTS?.writeDataPoint({
      blobs: [clean(event, /^[a-z_]{1,40}$/), clean(platform, /^(youtube|instagram|tiktok|facebook|pinterest|reddit|threads|dailymotion|unknown)$/),
        clean(tool, /^[a-z0-9-]{1,60}$/), clean(format, /^(mp3|mp4|m4a|webm|jpg|jpeg|png|gif|webp|heic|unknown|)$/), String(status)],
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
    if (pathname === "/analytics" || pathname === "/analytics/") {
      if (request.method !== "GET") return new Response("Method not allowed", { status: 405 });
      if (!dashboardAuthorized(request, env)) return dashboardChallenge();
      return new Response(dashboardHtml, {
        headers: privateHeaders({ "Content-Type": "text/html; charset=utf-8", "Content-Security-Policy": "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'" }),
      });
    }
    if (pathname === "/api/analytics" || pathname === "/api/analytics/world") {
      if (request.method !== "GET") return new Response("Method not allowed", { status: 405 });
      if (!dashboardAuthorized(request, env)) return dashboardChallenge();
      if (pathname.endsWith("/world")) return Response.json(world, { headers: privateHeaders() });
      const response = await env.VISITOR_ANALYTICS.getByName("global").fetch("https://analytics.internal/stats");
      const headers = new Headers(response.headers);
      for (const [key, value] of Object.entries(privateHeaders())) headers.set(key, value);
      return new Response(response.body, { status: response.status, headers });
    }
    if (pathname === "/api/visit") {
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
      const origin = request.headers.get("Origin");
      if (origin && origin !== new URL(request.url).origin) return new Response("Forbidden", { status: 403 });
      if (!env.VISITOR_HASH_KEY) return new Response("Analytics unavailable", { status: 503 });
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const { success } = await env.EVENT_LIMIT.limit({ key: `visit:${ip}` });
      if (!success) return new Response("Too many visits", { status: 429 });
      const body = await smallJson(request);
      if (!['page', 'heartbeat'].includes(body.kind)) return new Response("Invalid visit", { status: 400 });
      const country = /^[A-Z]{2}$/.test(request.cf?.country || "") ? request.cf.country : "XX";
      const visitor = await visitorHash(request, env.VISITOR_HASH_KEY);
      return env.VISITOR_ANALYTICS.getByName("global").fetch("https://analytics.internal/visit", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ visitor, country, kind: body.kind }),
      });
    }
    if (request.method === "POST" && pathname === "/api/image/process") {
      if (Number(request.headers.get("content-length") || 0) > 9 * 1024 * 1024) {
        return new Response(JSON.stringify({ error: "Choose an image under 8 MB." }),
          { status: 413, headers: { "Content-Type": "application/json" } });
      }
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const { success } = await env.DOWNLOAD_LIMIT.limit({ key: `image:${ip}` });
      if (!success) {
        record(env, "rate_limited", "unknown", "image", "", 429);
        return new Response(JSON.stringify({ error: "Too many image requests. Please try again in a minute." }),
          { status: 429, headers: { "Content-Type": "application/json", "Retry-After": "60" } });
      }
    }
    const body = request.method === "POST" && (pathname === "/api/analyze" || pathname === "/api/download" || pathname === "/api/event") ? await smallJson(request) : {};
    if (request.method === "POST" && (pathname === "/api/download" || pathname === "/api/analyze" || pathname === "/api/transcript" || pathname === "/api/event")) {
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const limiter = pathname === "/api/download" ? env.DOWNLOAD_LIMIT :
        pathname === "/api/analyze" || pathname === "/api/transcript" ? env.ANALYZE_LIMIT : env.EVENT_LIMIT;
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
    if (pathname === "/api/event" && request.method === "POST" && ["tool_page_view", "download_failed"].includes(body.event)) {
      if (typeof body.tool !== "string" || !/^[a-z0-9-]{1,60}$/.test(body.tool) ||
          !["youtube", "instagram", "tiktok", "facebook", "pinterest", "reddit", "threads", "dailymotion", "unknown"].includes(body.platform)) {
        return new Response(JSON.stringify({ error: "Invalid event context." }),
          { status: 400, headers: { "Content-Type": "application/json" } });
      }
      record(env, body.event, body.platform, body.tool, body.format || "", 200);
      return new Response(JSON.stringify({ ok: true }),
        { status: 200, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
    }
    const response = await env.DOWNLOADER.getByName("multi-primary").fetch(request);
    if (pathname === "/api/transcript" && request.method === "POST") {
      record(env, response.ok ? "transcript_successful" : "transcript_failed", "youtube", "youtube-to-transcript", "", response.status);
    }
    if (pathname === "/api/image/process" && request.method === "POST") {
      record(env, response.ok ? "image_processed" : "image_failed", "unknown", "image", "", response.status);
    }
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
        record(env, "download_started", result.platform, result.tool, result.format, response.status);
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
