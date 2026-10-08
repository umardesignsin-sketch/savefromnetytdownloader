# Batch Pro payment setup

The existing batch converter remains free for five images. Batch Pro is an optional one-time purchase that raises the per-batch count to ten for 30 days. The 20 MB input, 32 MB ZIP, image dimensions, and request rate limits still apply. No payment button appears until the integration is configured and enabled.

## Dodo setup status

- Live brand: `SaveFromNet` (`brnd_0NpI4ufDWP1ZWaJJfvsJ8`), enabled and verified.
- Live one-time product: `SaveFromNet Batch Pro - 30 Days` (`pdt_0NpI4zo1fXThFVN3XHyuU`), $2.99 USD before applicable tax.
- Live webhook: `ep_3KPW9VN7f9r8DRR8vEzJUupiUER` at `https://savefromnet.fun/api/batch-pass/webhook`, subscribed to `payment.succeeded`, `refund.succeeded`, and `dispute.lost`. It is enabled on the live site.
- A live checkout session was created without payment to verify the product and hosted checkout URL. No paid fulfillment has been tested.

Create separate test-mode credentials and a test product if test transactions are needed. Do not reuse the live key in test mode.

## Cloudflare configuration

Set these on the SaveFromNet Worker through Cloudflare's secret manager. Do not put key or signing-secret values in source files or chat messages.

| Name | Value |
| --- | --- |
| `DODO_API_KEY` | Dodo test or live API key |
| `DODO_BATCH_PRODUCT_ID` | Product ID for that same mode |
| `DODO_WEBHOOK_SECRET` | Signing secret for the configured webhook endpoint |
| `BATCH_TIER_SIGNING_KEY` | A separate random secret, at least 32 bytes, shared with the processing container through its environment |
| `DODO_MODE` | `live` for the configured product and key |
| `BATCH_PASS_ENABLED` | `true` on the live Worker after the backend and hosted checkout checks |

`BATCH_TIER_SIGNING_KEY` is passed from the Worker secret to the container by `DownloaderContainer.envVars`. The Worker strips client-supplied tier headers and signs the paid tier. Flask verifies the signature and rejects forged or old headers. The live container image is pinned to `4a7b3dc85c2911c846d4362029c08bc86e6113c7` and contains the ten-image code.

## Deployed release and verification

- The Worker and container are live on `savefromnet.fun` with Batch Pro enabled. The source image tag is `4a7b3dc85c2911c846d4362029c08bc86e6113c7`.
- Live checks passed: one-image conversion returned a ZIP, six images were rejected at the free five-image limit, the checkout API created a secure hosted Dodo session and pending pass cookie, an unsigned webhook request was rejected, and a signed no-op probe returned 200 using Dodo's current webhook secret.
- A real paid transaction, automatic pass fulfillment, recovery in another browser, and refund revocation still need an owner-controlled purchase and refund to verify end to end. No charge was made during deployment.
- For a future image rebuild, generate short-lived Cloudflare registry credentials with Wrangler, store them as encrypted GitHub Actions secrets `CF_REGISTRY_USERNAME` and `CF_REGISTRY_PASSWORD`, run the manual `build-container.yml` workflow, pin its commit tag in `wrangler.jsonc`, then deploy. Remove the temporary GitHub secrets after a successful build.

The pass is represented by a secure, HttpOnly, first-party cookie. Buyers can reveal and save a recovery code to use the pass in another browser. The code grants access; they should keep it private. Cloudflare Durable Object storage retains the order and pass state for about 45 days and removes it automatically afterward. Payment confirmation comes only from a verified Dodo webhook. A redirect query string cannot grant access.

Official references: [Dodo checkout sessions](https://docs.dodopayments.com/developer-resources/checkout-session), [Dodo webhook integration](https://docs.dodopayments.com/developer-resources/integration-guide), [Dodo metadata](https://docs.dodopayments.com/api-reference/metadata), [Cloudflare container secrets](https://developers.cloudflare.com/containers/examples/env-vars-and-secrets/).
