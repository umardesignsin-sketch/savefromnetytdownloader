# Transcript API billing setup

The public `/api/v1/youtube/transcript` preview and browser transcript tool remain available. The authenticated `/api/v2/youtube/transcript` endpoint uses a separate account store. A subscription is **$5 per month for 1,000 successful transcript responses**, with four request attempts per minute and two concurrent extractions per account. Failed requests do not consume the monthly allowance.

## Dodo configuration required before checkout is enabled

1. Create a **recurring monthly subscription product** in the existing live Dodo business for USD 5.00, quantity one, with no free trial. Confirm its term extends across many monthly billing cycles rather than expiring after one month. Record its `pdt_...` ID.
2. Create a separate Dodo webhook to `https://savefromnet.fun/api/developer/webhook` subscribed to `payment.succeeded`, `subscription.active`, `subscription.renewed`, `subscription.updated`, `subscription.on_hold`, `subscription.failed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `refund.succeeded`, and `dispute.lost`.
3. Set `DODO_TRANSCRIPT_PRODUCT_ID` to the new product ID and `DODO_TRANSCRIPT_WEBHOOK_SECRET` to that webhook's signing secret using `wrangler secret put`. Keep the existing Batch Pro product and webhook unchanged. Existing `DODO_API_KEY` and `DODO_MODE=live` are reused.
4. Open `/developers`, start a real checkout, and confirm that its Dodo webhook activates the account. Test a paid key against a public video with available captions, then a URL with no captions; only the successful response should increment the dashboard.

Checkout is intentionally disabled unless all bindings and secrets are present. The key is shown only when first generated or rotated; the owner can restore browser access with a recovery code. The dashboard opens Dodo's customer portal for billing changes and cancellation. The account store holds hashes of the owner token and API key, aggregate usage counts, Dodo IDs and period timestamps. It does not store submitted YouTube URLs or transcript text.

An API key looks like `sfn_<account-id>_<random-secret>`. The account ID routes the key to its Durable Object; the secret is checked by hash. Subscription webhooks are signed and checked against Dodo's API, the exact product, account metadata, checkout session and subscription ID. A subscription cannot grant access from an unsigned return URL.

### Deployment limitation

The Dodo product and webhook must be created in the merchant account. They cannot be inferred from the existing one-time Batch Pro product. Until configured, the developer dashboard honestly reports that checkout is unavailable; the paid endpoint grants no entitlement.
