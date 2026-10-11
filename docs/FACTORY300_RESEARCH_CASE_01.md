# Factory300 — Research case study 01

**Status:** Research initiated; hypotheses not verified. **No live trades or wallet access.**

## Research question

Can a small-capital, spot-only cryptocurrency trading system generate positive **realized net returns** after all execution costs, and what explains the gap between technically successful automation and economic performance?

## Case boundary

Factory300-Scalp used Solana/Jupiter/Phantom with a nominal **10 USDC per position**, intended take-profit **+0.8%**, stop-loss **−1.2%**, and periodic GitHub Actions execution. These are *reported strategy settings*, not audited evidence of executed trades. No claim is made about realized profit, loss, trade count, or wallet balances until transaction hashes, wallet transfers, and logs are reconciled. No secrets, private keys, or personal account details should be copied here.

## Competing hypotheses

- H1: Two-way execution costs (swap route fees, network fees, price impact, spread and realized slippage) erase a nominal +0.8% target on small orders.
- H2: Scheduled polling and delayed settlement miss price triggers; successful CI runs do not imply executed swaps.
- H3: Signal quality and market regime, not only execution costs, explain the lack of consistent realized profits.
- H4: Incomplete durable trade state, confirmation and accounting make observed P&L unreliable even if transactions execute.

## Falsifiable protocol — one integrated research pass

1. **Audit evidence, not assumptions.** Collect redacted public repository source/workflow history, confirmed transaction signatures and their chain confirmations, timestamped quotes and execution amounts, and available trading logs. Mark absent evidence as *unknown*, never zero.
2. **Reconstruct realized P&L.** For each closed position, reconcile opening/closing token quantities and USDC cash flows, network and platform costs, route price impact, and actual fills. Separate deposits/withdrawals and open holdings from realized trading return.
3. **Test cost feasibility.** For a 10 USDC entry, nominal +0.8% is **0.08 USDC gross** before costs; −1.2% is **0.12 USDC gross loss** before costs. These are hypothetical targets, not measured outcomes. Calculate break-even **round-trip** costs and sensitivity across execution-cost assumptions without pretending slippage tolerance equals realized slippage.
4. **Compare counterfactuals.** Hold execution cost assumptions fixed while testing signal vs. no-signal baseline and delayed polling; avoid look-ahead bias, and separate in-sample from out-of-sample.
5. **Review independent literature.** Extract exact text-backed claims and limitations, recording whether the evidence concerns retail vs institutional scale, CEX vs DEX, historical vs contemporary market structure, and assumed vs observed costs.
6. **Deliver one report.** Findings by confidence level; confirmed facts, unsupported hypotheses, competing explanations, data gaps, and a go/no-go research conclusion. No new trading bot, no live trading, and no additional model comparisons.

## Initial external sources (candidates, not validated evidence for Factory300)

- Manahov, *The rapid growth of cryptocurrencies: How profitable is trading in digital money?* International Journal of Finance & Economics, DOI: https://doi.org/10.1002/ijfe.2778 — finds profitability under its own sample and cost/capital assumptions; **not transferable without validation** to 10-USDC Solana spot swaps.
- *Wish or reality? On the exploitability of triangular arbitrage in cryptocurrency markets*, Finance Research Letters, DOI: https://doi.org/10.1016/j.frl.2024.106508 — reports apparent arbitrage opportunities can disappear after costs and order-book limits; **different strategy and venue**.
- Jupiter Metis Swap API documentation: https://developers.jup.ag/docs/guides/how-to-build-a-custom-swap-with-metis — specifies quotes, price impact, slippage tolerance, priority fees and transaction landing; API behavior/version must be matched to Factory300's historical code and dates.

## Initial findings

- **Confirmed arithmetic:** +0.8% of 10 USDC = 0.08 USDC gross; −1.2% = 0.12 USDC gross.
- **Unverified:** Factory300 trade history, all-in realized fees, closed P&L, the cause(s) of failure, and any positive expected value.
- **Decision:** Investigate historical records first. Do not deploy capital or claim profitability from CI success, simulated trades, literature abstracts or NLI classifications.

**Evidence discipline:** Bibliographic metadata is discovery only. Scientific conclusions require inspected source passages, exact citations, independent reasoning, and explicit human review.

## Audit update — 2026-10-11

### Access and verification
Attempted to read `AMMARICA1791/Factory300-Scalp/executor.py` through the connected GitHub integration; the request returned **404**. A repository search for Factory300 under the owner returned no results. This is an **access/identity gap**, not proof that the repository was deleted or that no trades occurred. Historical transaction counts and realized P&L remain **unknown**.

### Execution-cost distinction (official Jupiter documentation)
Jupiter's quote `outAmount` reflects the quoted routed output (including AMM/platform fees as described by the API), while `otherAmountThreshold` is a minimum acceptable output under the specified slippage tolerance. **Tolerance is not incurred slippage.** The `priceImpactPct` quote is an estimate, not a historical fill. Quote, built transaction, submission, network confirmation, and realized token balance deltas must be separately reconciled. Official docs: https://developers.jup.ag/docs/guides/how-to-build-a-custom-swap-with-metis and https://developers.jup.ag/docs/api-reference/swap/v1/swap. Current docs describe newer endpoints; historical implementation must be assessed against its own API version.

### Break-even sensitivity (illustrative, NOT historical Factory300 fees)

For a 10 USDC position with a nominal 0.08 USDC gross winning move, if **total round-trip execution cost** is:

| Assumed all-in cost | Net winning trade |
| --- | --- |
| 0.01 USDC | +0.07 USDC |
| 0.04 USDC | +0.04 USDC |
| 0.08 USDC | 0.00 USDC |
| 0.10 USDC | −0.02 USDC |

These scenarios isolate **cost feasibility**, not the probability of winning, loss magnitude, or expected value. With a +0.08 gross win and −0.12 gross loss, and a *fixed symmetric* round-trip cost C, the break-even win rate is `(0.12 + C) / 0.20`, provided fills and sizing match the assumptions: 60% at C=0, 65% at C=0.01, 80% at C=0.04, and 100% at C=0.08. No actual Factory300 win rate is established.

### Next evidence gate
Obtain the **correct historical repository identity or exported redacted transaction records**. Without this, stop at transparent cost arithmetic and source-methodology findings. Do not assert real-world strategy failure mechanisms as proven.

## Research scope decision — 2026-10-11

**Paused, not pursued for the first lab validation.** The original Factory300 repository and wallet were deleted; primary execution records have not been verified. No further time will be spent reconstructing the deleted system during the first laboratory test. The new independent public-data study is [Cryptocurrency Predictability Research 01](CRYPTO_PREDICTABILITY_RESEARCH_01.md). This pause is not a scientific finding that the strategy failed economically.
