# Batch Pro payment setup

The existing batch converter remains free for five images. Batch Pro is an optional one-time purchase that raises the per-batch count to ten for 30 days. The 20 MB input, 32 MB ZIP, image dimensions, and request rate limits still apply. No payment button appears until the integration is configured and enabled.

## Dodo setup status

- Live brand: `SaveFromNet` (`brnd_0NpI4ufDWP1ZWaJJfvsJ8`), enabled and verified.
- Live one-time product: `SaveFromNet Batch Pro - 30 Days` (`pdt_0NpI4zo1fXThFVN3XHyuU`), $2.99 USD before applicable tax.
- Live webhook: `ep_3KPW9VN7f9r8DRR8vEzJUupiUER` at `https://savefromnet.fun/api/batch-pass/webhook`, subscribed to `payment.succeeded`, `refund.succeeded`, and `dispute.lost`. It is disabled until the new Worker and processing container are deployed and tested.
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
| `BATCH_PASS_ENABLED` | `true` only after the new Worker and container image are deployed and the payment flow is verified |

`BATCH_TIER_SIGNING_KEY` is passed from the Worker secret to the container by `DownloaderContainer.envVars`. The Worker strips client-supplied tier headers and signs the paid tier. Flask verifies the signature and rejects forged or old headers. This requires a new container image built from this source; the currently pinned image does not contain the ten-image code.

## Release and verification

1. Build and publish a new Cloudflare Container image from this source, and pin its immutable image reference in `wrangler.jsonc`. The current machine has no Docker installation, so use the repository's GitHub Actions container workflow after the code is committed and pushed.
2. Build static pages with `python generate_static.py`, then deploy the Worker. Keep `BATCH_PASS_ENABLED` off for the initial deployment.
3. Verify a free five-image ZIP, rejection of six images before purchase, hosted checkout, signed webhook delivery, ten-image ZIP after purchase, recovery-code redemption in another browser, and loss of paid access after a refund. Use a separate Dodo test-mode product and key for test transactions, or a small live purchase and refund with the owner's involvement.
4. Enable the webhook and set `BATCH_PASS_ENABLED=true` only after the deployed container and fulfillment path have been verified.

The pass is represented by a secure, HttpOnly, first-party cookie. Buyers can reveal and save a recovery code to use the pass in another browser. The code grants access; they should keep it private. Cloudflare Durable Object storage retains the order and pass state for about 45 days and removes it automatically afterward. Payment confirmation comes only from a verified Dodo webhook. A redirect query string cannot grant access.

Official references: [Dodo checkout sessions](https://docs.dodopayments.com/developer-resources/checkout-session), [Dodo webhook integration](https://docs.dodopayments.com/developer-resources/integration-guide), [Dodo metadata](https://docs.dodopayments.com/api-reference/metadata), [Cloudflare container secrets](https://developers.cloudflare.com/containers/examples/env-vars-and-secrets/).
