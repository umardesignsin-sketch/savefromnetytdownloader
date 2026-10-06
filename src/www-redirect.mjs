/** Permanently consolidate the www hostname onto the canonical site. */
export default {
  fetch(request) {
    const url = new URL(request.url);
    if (url.hostname !== "www.savefromnet.fun") {
      return new Response("Not found", { status: 404 });
    }
    url.protocol = "https:";
    url.hostname = "savefromnet.fun";
    return Response.redirect(url.toString(), 301);
  },
};
