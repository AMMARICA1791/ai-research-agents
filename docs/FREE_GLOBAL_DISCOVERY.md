# Free Global Discovery Sources

The radar now has 21 configured feed endpoints (12 original, 4 experimental third-party X feeds, and 5 new feeds). This is a **configuration count**, not proof that every endpoint currently responds.

## Added
- GDELT DOC 2.0 RSS: two targeted global news queries on AI research and scientific discoveries. This is public, keyless, best-effort metadata discovery; no claim of full GDELT firehose access.
- arXiv RSS: quantum physics and robotics.
- Nature RSS: published research updates.

## Existing
- Hacker News AI RSS, original arXiv computer science categories, W3C, GitHub Blog, Google Research, and other public feeds.
- Four experimental third-party X profile RSS endpoints (see [X Social Discovery](X_SOCIAL_DISCOVERY.md)).

## Limits and verification
- A successful workflow is not proof of successful ingestion from every feed.
- Inspect the `rapid-radar-report` workflow artifact for `successful_feeds`, `feed_errors`, and `signals[*].source`.
- GDELT and other public services may rate-limit, return empty results, or change endpoints. Feed parsing currently supports RSS item entries only.
- GitHub Actions cron is best-effort and is not a real-time push transport.
- The radar selects up to 40 items per run by a keyword score; it does not yet guarantee fair representation across sources or verify scientific novelty.
- No subscription, credentials, API key, or paid usage is configured.

Sources: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ and https://blog.gdeltproject.org/new-gdelt-article-list-rss-feeds-images-links-social-media-and-mobile-urls/
