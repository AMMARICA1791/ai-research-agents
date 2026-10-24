# Experimental X Social Discovery — Zero Cost

The public radar includes four **best-effort** X profile feeds through FxEmbed's third-party RSS gateway:

- NASA — `https://fxtwitter.com/NASA/feed.xml?count=20`
- Google DeepMind — `https://fxtwitter.com/GoogleDeepMind/feed.xml?count=20`
- Hugging Face — `https://fxtwitter.com/huggingface/feed.xml?count=20`
- arXiv — `https://fxtwitter.com/arxiv/feed.xml?count=20`

These are not official X API connections and require no account, API key, or payment. They do **not** provide X-wide search, real-time guarantees, comprehensive account coverage, or independent scientific verification. This gateway may become unavailable, lag, or change its behavior. Only public material is considered.

The radar logs per-feed failures in `feed_errors` and continues processing other sources. Its existing keyword heuristic ranks the merged feed entries, retaining up to 40 per run. A social post is a discovery lead, **not** a validated research result.

Provider documentation: https://docs.fxembed.com/guide/advanced/rss-atom-feeds/

Official X API access currently uses paid consumption-based billing. No billing, login, credentials, scraping bypass, or paid integration is configured.

To verify actual coverage, inspect the latest `Rapid Project Radar` workflow artifact `rapid-radar-report` and check `successful_feeds`, `feed_errors`, and the `source` field of captured signals. A green workflow alone does not prove any X posts were retrieved.
