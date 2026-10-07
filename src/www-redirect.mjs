/** Permanently consolidate www and plain HTTP onto the HTTPS apex. */
export default {
  fetch(request) {
    const url = new URL(request.url);
    const isWww = url.hostname === "www.savefromnet.fun";
    const isHttpApex = url.hostname === "savefromnet.fun" && url.protocol === "http:";
    if (!isWww && !isHttpApex) {
      return new Response("Not found", { status: 404 });
    }
    url.protocol = "https:";
    url.hostname = "savefromnet.fun";
    return Response.redirect(url.toString(), 301);
  },
};
