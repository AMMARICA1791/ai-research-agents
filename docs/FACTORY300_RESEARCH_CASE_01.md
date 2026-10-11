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
