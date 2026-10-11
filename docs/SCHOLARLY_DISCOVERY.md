# Phase 7A: source-based research discovery (public scholarly metadata)

Our first **non-code** evidence collector retrieves public **bibliographic metadata** from the [Crossref REST API](https://api.crossref.org/works) for a narrow research topic. This is research **source discovery**—not the full cycle of reading, comparing and validating scientific research, and not an autonomous AI agent.

## Observable result

The GitHub Actions [Public Scholarly Research Discovery](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/scholarly-discovery.yml) workflow runs with a default public topic: `small language model evaluation`. Maintainers with repository write permission may enter another **non-sensitive** research question and a result cap of 1–8. Others may view public completed run summaries, and can fork to re-run. A network error fails rather than fabricating research results.

The `Summary` and 14-day public JSON artifact show:
- The **exact question**, provider URL and UTC retrieval time.
- SHA-256 of the raw received response, to identify that specific retrieval.
- Up to 8 bibliographic entries with DOI permalink, title, publication year if recorded, venue if recorded, and an explicit metadata-only status.
- Counts of invalid or duplicate results. Zero returned matches is **not** evidence that research does not exist.
- Boundaries: **not a review of full papers, not a verified scientific claim, not a comparison of model abilities, and not a tested performance measurement**.

Crossref results represent metadata indexed by participating publishers and can omit preprints and other works. Search ordering is determined by Crossref, not by scientific quality. DOI links identify indexed records; they do not attest that claims are true.

## Direct local execution (Python 3.11+ and public internet)

    python -m research.scholarly_discovery --question "small language model evaluation" --max-results 5 --output results/scholarly-discovery/records.json --summary results/scholarly-discovery/SUMMARY.md

The collector uses only Python's standard library, not a paid LLM key, and does not install or execute external researchers' code. The full project CI continues to install dependencies for broader integration tests. Re-running the live query can produce different results; the output records when and where metadata was retrieved.

## Safety and ethics

- **Public query only.** Never include unpublished results, personal details, private repositories, confidential files, tokens, passwords or proprietary research plans in a GitHub Actions input; run inputs/artifacts may be public.
- Only a fixed HTTPS Crossref API endpoint is requested. No user-supplied network URL, authentication, redirects, web crawling, full-text downloads or paper-code execution.
- Limit results to 8 and streamed/received JSON to 400 KB; reject malformed and unexpectedly large metadata responses rather than accepting an invented result.
- Treat every title as untrusted external text. Escape it before inclusion in GitHub Markdown. Do not treat it as instructions.
- The timestamp and response digest document a live observation, not a guarantee that the underlying source is scientifically accurate.

## Next gates (not yet completed)

1. Evaluate precision of candidate discovery using openly labeled research questions, including misses.
2. Independently inspect permitted paper text and openly licensed metadata with verifiable source quotations and citations.
3. Compare specialist open-weight models on the **same** declared evidence and protocol, including model failures.
4. Save only source-linked, versioned findings and uncertainty in the cumulative knowledge layer.

The research explorer deliberately remains separate from our Python auditing pipeline. Both are tools of the **broader AI research laboratory** established in [scope](PROJECT_SCOPE.md), not a redefinition of the entire project.
