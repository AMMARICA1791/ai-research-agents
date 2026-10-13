# Live AI news research: first conversational prototype

This is an experimental, **not independently verified**, news-reading pipeline.
It retrieves public RSS/Atom headlines, attempts to retrieve a few linked HTML
articles, and lets a locally running Qwen model discuss the saved excerpts.
It does **not** establish whether the news claims are true.

## Run (Python 3.11+)

From the repository root:

```sh
python -m research.news_research_pipeline --output research_output/news_research.json
```

Inspect the resulting JSON. If `article_cases` is empty or every case has
`ARTICLE_NOT_RETRIEVED`, no evidence-backed model answer is possible.
Feeds and sites may block automated requests, redirect, or be temporarily offline.

Install and start Ollama separately and download `qwen2.5:0.5b` once.
Then run:

```sh
python -m research.news_chat --dossier research_output/news_research.json --model qwen2.5:0.5b
```

Ask a question, then follow up. Enter `exit` to stop. The model is local;
no paid LLM API key is required, but running Ollama needs compatible hardware.

## GitHub Actions

[AI News Collection Pilot](../.github/workflows/ai-news-collection.yml)
is scheduled daily and also has manual workflow dispatch. It produces
`ai_news.json` and `news_research.json` as downloadable artifacts.
**GitHub Actions does not run the interactive Ollama chat.** Chat runs on
a machine with Ollama installed.

## Scientific and security limitations

- RSS titles are **unverified leads**, not confirmed facts.
- Retrieved publisher text is **not independent corroboration**.
- The model may still misinterpret sources or invent citations. Verify URLs.
- The system does not access authenticated X/Reddit content.
- Only public HTTPS URLs are accepted; redirects are disabled. This may cause
  some legitimate sites to fail, intentionally.
- No persistent user memory, hosted chat UI, or autonomous fact checking yet.
- Do not enter secrets or private data into public workflow inputs/artifacts.

## Success criterion for the next milestone

Demonstrate one real retrieved article, a source-grounded answer, and a
follow-up question, with the exact source URL and recorded run evidence.
