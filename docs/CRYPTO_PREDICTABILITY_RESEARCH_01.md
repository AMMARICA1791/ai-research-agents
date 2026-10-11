# Research experiment 01 — cryptocurrency predictability

**Status:** Protocol defined; literature and outcomes NOT yet verified.

## Research question
Do machine-learning methods predict cryptocurrency price direction better than transparent classical baselines **out of sample**, and does any predictive edge survive realistic transaction costs?

## Why this case
Uses public published studies and openly available historical market datasets; no dependency on deleted Factory300 repository, wallet, trade records, keys, or capital.

## One-pass laboratory evaluation
1. Discover up to eight public academic works via existing Crossref discovery; record DOI, retrieval date, and metadata-only status.
2. Review accessible primary texts, verify exact quotations, dataset period, target horizon, data availability, evaluation method, transaction-cost assumptions, and limitations. If texts cannot be accessed, mark claims **unverified**, not supported.
3. Compare claimed ML results against simple baselines: majority direction, previous-return sign, and buy-and-hold when applicable. Do not confuse classification accuracy with trading returns.
4. Check time-series splits, leakage, look-ahead bias, fees, spread, slippage, overfitting, regime shifts, and multiple-testing bias.
5. Produce one report: evidence table, contradictory findings, confidence, unresolved gaps, and whether any reported advantage is economically actionable.

## Acceptance criteria
- At least three primary papers reviewed at passage level, or explicitly state why this threshold was not met.
- Each quantitative claim traceable to its own primary source and experimental assumptions.
- No fabricated performance numbers, no live trading, no new trading bot, no new model benchmarking.
- Report distinguishes *research discovery*, *source-grounded claims*, *predictive accuracy*, and *net trading performance*.

## Initial hypotheses, not conclusions
H1: Some ML methods outperform simple prediction baselines in selected historical samples.
H2: Out-of-sample performance and realistic transaction costs weaken or eliminate some apparent advantage.
H3: Results vary materially by asset, time horizon, market regime, and dataset construction.

## Existing lab entry point
Use `.github/workflows/scholarly-discovery.yml` with public topic:
`cryptocurrency price prediction machine learning out of sample trading costs`.
Its Crossref output is **metadata only**; it does not verify scientific claims.

## Scope change
The historical Factory300 study is parked as an incomplete case because its repository and wallet were deleted and its realized transaction record is unavailable. It is not evidence that its trading strategy had negative expected value.
