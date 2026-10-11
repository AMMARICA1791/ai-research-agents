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

## First literature extraction — 2026-10-11

**Provenance:** Manual examination of public publisher/author pages in this research session. These results have NOT been produced by an end-to-end GitHub Actions research workflow, nor independently reproduced from underlying market data. Numbers below are **author-reported**, not independently verified trading returns.

| Primary study | Source | Author-reported evidence | Transferability / caution |
| --- | --- | --- | --- |
| Jaquart, Köpke & Weinhardt (2022), *Machine learning for cryptocurrency market prediction and trading* | https://doi.org/10.1016/j.jfds.2022.12.001 | Publisher abstract reports mean daily direction accuracy **52.9–54.1%** for top-100 cryptocurrencies, **57.5–59.5%** for the highest-confidence 10% of predictions, and net-of-cost out-of-sample Sharpe **3.23** (LSTM) and **3.12** (GRU) versus **1.33** buy-and-hold. | Long-short portfolio; author-reported historical backtest; not a small-capital spot-only live deployment. |
| Wei, Sermpinis & Stasinakis (2023), *Forecasting and trading Bitcoin with machine learning techniques and a hybrid volatility/sentiment leverage* | https://doi.org/10.1002/for.2922 | Authors report forecasting improvement for ML and present trading performance, but **section 5.1 explicitly excludes transaction costs**. | Gross results cannot be read as executable net returns; leveraged/short strategies not equivalent to spot-only. |
| Bysik & Ślepaczuk (2026), *Machine Learning-Based Bitcoin Trading Under Transaction Costs: Evidence From Walk-Forward Forecasting* | https://doi.org/10.2139/ssrn.6795938 ; https://arxiv.org/abs/2606.00060 | Author preprint reports approximately **70,000 hourly observations**, **27 walk-forward folds**, and collapse of naive high-turnover strategies after **10 bps** assumed costs; selective cost-aware XGBoost is positive in some settings. | **Preprint**, not treated as peer-reviewed; BTC/USDT **futures**, not spot; assumptions and regimes may not transfer. The authors caution that Sharpe dominance over buy-and-hold is not statistically established. |
| Berger & Koubová (2024), *Forecasting Bitcoin returns: Econometric time series analysis vs. machine learning* | https://doi.org/10.1002/for.3165 | Publisher article identified as an additional classical-vs-ML comparison. | Full methods and numerical outcomes not yet extracted; **candidate only**, no conclusion drawn. |

### Cross-study synthesis (provisional)

1. **Predictability is not profitability.** Statistical direction accuracy of ~53% may or may not overcome costs, turnover, and risk.
2. **Cost assumptions change conclusions.** One primary article expressly omits fees; another finds frequent trading can become uneconomic under a 10-basis-point assumption.
3. **No evidence yet that a small, spot-only retail trader can reproduce the published portfolio/futures backtests.** Results are conditional on data period, venue, position size, risk, and implementation.
4. **Competing evidence exists:** at least one study reports strong net-of-cost portfolio Sharpe while another finds naive trading strategies collapse under costs. This is not a contradiction until strategies, markets, and assumptions are aligned.

### Verification status

- **3 primary studies identified and key publicly accessible abstract/section-level claims inspected.**
- **Not yet completed:** exact passage-by-passage audit of all full texts, independent backtest reproduction, source-to-claim ledger generated by the repository pipeline, and cost-normalized like-for-like comparison.
- No claim of an automated laboratory run or independently replicated returns is made.
