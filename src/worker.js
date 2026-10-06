import { Container } from "@cloudflare/containers";

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
    if (request.method === "POST" && new URL(request.url).pathname === "/api/download") {
      const ip = request.headers.get("CF-Connecting-IP") || "unknown";
      const { success } = await env.DOWNLOAD_LIMIT.limit({ key: ip });
      if (!success) {
        return new Response(JSON.stringify({ error: "Too many requests. Please try again shortly." }), {
          status: 429,
          headers: { "Content-Type": "application/json", "Retry-After": "60" },
        });
      }
    }
    return env.DOWNLOADER.getByName("flask-primary").fetch(request);
  },
};
