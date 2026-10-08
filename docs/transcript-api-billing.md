# Transcript API billing setup

The public `/api/v1/youtube/transcript` preview and browser transcript tool remain available. The authenticated `/api/v2/youtube/transcript` endpoint uses a separate account store. A subscription is **$5 per month for 1,000 successful transcript responses**, with four request attempts per minute and two concurrent extractions per account. Failed requests do not consume the monthly allowance.

## Live Dodo configuration

- Live product: `SaveFromNet Transcript API - 1,000 per Month` (`pdt_0NpJ368Pi87wjeiYqAHMF`). The price is USD 5.00 every month, with no trial and a 20-year subscription term so monthly renewals continue.
- Live webhook: `ep_3KQ8RrsphIjOM5Kdlz9jKmCZGhA` at `https://savefromnet.fun/api/developer/webhook`. It is enabled for `payment.succeeded`, `subscription.active`, `subscription.renewed`, `subscription.updated`, `subscription.on_hold`, `subscription.failed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `refund.succeeded`, and `dispute.lost`.
- Cloudflare Worker secrets `DODO_TRANSCRIPT_PRODUCT_ID` and `DODO_TRANSCRIPT_WEBHOOK_SECRET` are installed. Existing `DODO_API_KEY`, `DODO_MODE=live`, and the separate Batch Pro product and webhook remain in use.
- Live checks passed: `/api/developer/status` reports `available: true`; an unpaid `/api/developer/checkout` request created a Dodo hosted checkout and set the account cookie; an unsigned webhook was rejected with HTTP 400; a signed no-op probe using this webhook's signing key returned HTTP 200. No payment was made.
- A real paid transaction, webhook account activation, API-key issuance, monthly quota behavior, and cancellation/refund handling still need an owner-controlled purchase and subsequent verification.

Checkout is intentionally disabled unless all bindings and secrets are present. The key is shown only when first generated or rotated; the owner can restore browser access with a recovery code. The dashboard opens Dodo's customer portal for billing changes and cancellation. The account store holds hashes of the owner token and API key, aggregate usage counts, Dodo IDs and period timestamps. It does not store submitted YouTube URLs or transcript text.

An API key looks like `sfn_<account-id>_<random-secret>`. The account ID routes the key to its Durable Object; the secret is checked by hash. Subscription webhooks are signed and checked against Dodo's API, the exact product, account metadata, checkout session and subscription ID. A subscription cannot grant access from an unsigned return URL.

### Billing safety

Checkout availability alone does not grant API access. The paid endpoint requires an active subscription confirmed through Dodo's signed webhook and product lookup. Keep the product ID and signing secret in Cloudflare's secret manager; never put the signing secret in source control.
