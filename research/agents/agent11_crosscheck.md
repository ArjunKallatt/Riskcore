# Cross-check: external "Mini-Aladdin" reports vs Riskcore research

Date: 2026-10-02. This compares two reports from another AI research tool against agents 1–10.

**The inputs**, stored in [`../external/`](../external/):
- A chat transcript pasted by the user (the "first report").
- A later Markdown report with four CSVs (the "second report").

**How the new claims were checked:** repo READMEs and LICENSE files on raw.githubusercontent.com, and package metadata from PyPI JSON. Other sites are still blocked from this environment.

## 1. Verdict in one paragraph

The second report broadly agrees with our findings. Both conclude:
- Build an auditable, India-first analytics layer, not an Aladdin clone.
- Use a common data model, a run/result ledger, and effective-dated regulatory rules.
- Treat licences as architecture (vectorbt's Commons Clause, GPL).

The first report contains several errors. The most consequential is that it treats the **RBI 2026 ECL floors as v2 requirements**. Those Directions cover commercial banks, not NBFCs.

Neither external report notices that **most small NBFCs are not on Ind AS 109**, so it still stands as our main correction to the original plan.

The external reports add some useful leads:
- **baselkit**, an Apache-2.0 credit-risk library with Ind AS 109 and RBI IRAC code.
- **A reference DuckDB + Streamlit VaR platform.**
- **Three regulatory items we had not seen:**
  - a SEBI MF Master Circular dated Mar 2026;
  - RBI 2026 amendments to NBFC concentration and provisioning rules;
  - RBI NBFC ALM Directions 2025.
- **Two good design ideas:** a per-metric "Why?" drawer, and a rule-registry schema.

## 2. New open-source leads (verified here)

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ankitjha67/baselkit (PyPI: `creditriskengine`) | Credit risk / ECL | not seen | PyPI 0.31.0 (2026-07-10); first release 0.2.0 (2026-03-24); 18 releases | Apache-2.0 (LICENSE file read). PyPI licence field is empty | Python | Very broad: Basel RWA/IRB, IFRS 9/CECL/**Ind AS 109 + RBI IRAC** (`classify_irac`, `irac_to_ifrs9_stage`, `rbi_minimum_provision`), overlays, PD/LGD/EAD, Vasicek, stress, TLAC/MREL, IRRBB, many jurisdictions | Very active, single author, about 4 months old. Its README shows a "coverage 100%" badge that links nowhere | **M** | **Use as a cross-check oracle and reference** for the IRAC and Ind AS functions, not as a core dependency until you have read its code. The scope (dozens of regimes in 4 months) is unusually broad for one author, so validate every formula against the primary RBI text before relying on it | https://github.com/ankitjha67/baselkit | LIC, README, PyPI |
| husaam-atq/volatility-risk-forecasting-platform | VaR platform (reference) | not seen | README dated 2026-05 | MIT (LICENSE file read) | Python | DuckDB + Streamlit market-risk platform: EWMA/GARCH/HAR forecasts, VaR/ES, Kupiec and Christoffersen backtests, regime labels, SQL validation views | New | M | Architecture reference for the "results in DuckDB + backtest page" design. Its own README reports a 4.76% average breach rate at 95% VaR | https://github.com/husaam-atq/volatility-risk-forecasting-platform | LIC, README |
| cvxgrp/cvxportfolio | Optimisation / backtest | not seen | PyPI 1.5.1 (2025-07-06) | **GPL-3.0** (LICENSE file read) | Python | Multi-period optimisation and backtesting (Boyd group) | Maintained | L (licence) | Methodology reference only | https://github.com/cvxgrp/cvxportfolio | LIC, PyPI |
| microsoft/qlib | Quant research platform | not seen | PyPI pyqlib 0.9.7 (2025-08-15) | MIT (LICENSE file read) | Python | AI-oriented quant research, data and backtest platform | Maintained | L | Out of scope for a risk tool | https://github.com/microsoft/qlib | LIC, PyPI |
| AI4Finance-Foundation/FinRL | RL trading | not seen | PyPI 0.3.7 (2024-04-12) | MIT (LICENSE file read) | Python | Reinforcement learning for trading | PyPI release is stale | L | Not relevant to risk | https://github.com/AI4Finance-Foundation/FinRL | LIC, PyPI |

The baselkit README independently cites **"RBI ECL Master Direction 2026 (RBI/DOR/2026-27/398) … effective April 1, 2027"**. That matches the reference number Agent 8 saw in one secondary result and marked unverified. A second source raises the likelihood that it is correct, but it is still not the primary text.

## 3. Errors and contradictions in the external reports

| # | External claim | Where | Our evidence | Verdict |
|---|---|---|---|---|
| X1 | "RBI ECL Master Direction 2026: PD floor 0.03%, LGD floor 70% unsecured, regulatory floor 5% EAD", listed as **P0 for v2** | First report §6 and §10 | The 2026 Directions apply to **commercial banks** (excluding RRBs, SFBs and payments banks) from 1 Apr 2027 (agents 2 and 8). The baselkit README lists "PD 0.03% / LGD 65%-70%-30% backstops". **"5% EAD" appears nowhere.** | **Wrong for NBFC v2.** Keep it only as an optional bank floor-table preset. The numbers are second-hand (from a library README) and need the primary text |
| X2 | Ind AS 109 ECL as the P0 v2 feature for small and mid NBFCs | Both reports | The MCA roadmap limits Ind AS to listed NBFCs or those with net worth ≥ ₹250 cr (agents 8 and 10) | **Missing nuance.** For most small NBFCs, IRACP provisioning is P0 |
| X3 | "RBI NBFC ALM Directions 2025 mandate stress testing … for NBFCs above ₹100 crore" | First report §1 and §6; called "Draft Directions" in its own search trail | Not found by our agents. **[BK]** The ₹100 cr asset-size threshold matches RBI's 2019 Liquidity Risk Management Framework for NBFCs | **Plausible lead, not verified**, and its draft vs final status is unclear. Verify before mapping features |
| X4 | "Jio BlackRock bringing Aladdin to India" as a product for Indian institutions | First report §1–2 | Not covered by our agents. **[BK]** Jio BlackRock is an asset-management joint venture that said it would use Aladdin's technology for its own business | **Mischaracterised.** It is not a commercial Aladdin offering for Indian institutions. Verify before citing |
| X5 | Stars: Riskfolio 3.1k, PyPortfolioOpt 4.9k, skfolio 2.0k, QuantLib 5.9k | First report §3 | GitHub API on 2026-10-02: 4.5k / 6.1k / 2.5k / 7.6k (agent 4). The second report's ~4.5k / ~6.1k / ~2.4k / ~7.6k matches ours | **Stale numbers** in the first report |
| X6 | vectorbt licence "Apache-2.0" | First report §3 and its CSV | LICENSE file read: Apache-2.0 **+ Commons Clause** (agent 4). The second report gets this right | **Wrong** in the first report |
| X7 | Must-read "The $10 Trillion OpenBB Copilot validation (2025)" | First report §4 | A blog post (didierlopes.beehiiv.com), not research | **Drop it** from the paper list |
| X8 | Must-read "NFRA findings on ECL under Ind AS 109 (2026)" | First report §4 | A news report about a regulator's findings, not a paper. NFRA audit-quality findings on ECL would still be **useful evidence** for the "auditability" thesis | Keep as a **regulatory signal to verify**, not a paper |
| X9 | Christoffersen (1998) DOI `10.1016/S0304-4076(97)00064-7` | Second report papers CSV | Christoffersen (1998) appeared in the *International Economic Review* 39(4): DOI `10.2307/2527341` (agent 5, verified). The DOI given has the Journal of Econometrics prefix | **Wrong DOI** |
| X10 | Rockafellar & Uryasev (2002) DOI `10.21314/JOR.2002.024` | Second report papers CSV | "CVaR for General Loss Distributions" is in the *Journal of Banking & Finance* 26(7): DOI `10.1016/S0378-4266(02)00271-6` (agent 5, verified). The `10.21314/JOR` prefix belongs to the Journal of Risk, where the **2000** paper appeared | **Wrong DOI** |
| X11 | Merton (1974) DOI `10.2307/2326104`; Kupiec SSRN 702397; Rockafellar-Uryasev (2000) JSTOR 2699986 | Second report papers CSV | Agent 5 verified Merton as `10.1111/j.1540-6261.1974.tb03058.x`, Kupiec as SSRN 7065 / DOI `10.3905/jod.1995.407942`, and R-U 2000 via its Semantic Scholar record | **Unverified identifiers.** Use agent 5's |
| X12 | Basel stress-testing principles linked as `bcbs155` | Second report §6 | bcbs155 is the 2009 version. It was superseded by **d450 (Oct 2018)** (agents 5 and 8) | **Outdated link** |
| X13 | "Basel III concentration … granularity (0.2% retail threshold)" | First report §6 | **[BK]** 0.2% is the standardised-approach *regulatory retail* granularity criterion (no single exposure above 0.2% of the retail portfolio). It is a classification test, not a concentration limit | **Misframed.** It is fine as a check in the loan-tape validator |
| X14 | Data licences: jugaad-data "Public", AMFI "Public", Lending Club "Public / free CSV" | First report §5 | NSE's ToS bans automated collection (agent 6). AMFI has no explicit open licence. LendingClub stopped publishing public data around 2020 (agent 6, unverified) | **Overstated.** Data rights are the binding constraint |
| X15 | Commercial lists omit the Indian NBFC ECL vendors | Both reports | Agent 2 found ICRA Analytics ECL 3.0, Acies Kepler, ECL Square, Crediwatch and Roopya (snippet-level) | Our coverage is broader for the v2 market |
| X16 | Roadmap keeps the optimiser (PyPortfolioOpt / Riskfolio) as P0/P2, plus FastAPI and QuantStats | Both reports | Agent 10 cut the optimiser (crowding, overfitting, SEBI IA/RA advice risk) and deferred FastAPI | **Keep our cut.** User-driven what-if covers the need without suggesting target weights |

## 4. Claims the external reports corroborate (confidence raised)

- **The AMFI NAV-history old-format cut-off on 30 Sep 2026, and the 90-day download window.** The second report cites the AMFI page itself, independently of agent 6's snippet. **Treat the change as real.** v1 should use MFapi.in or captn3m0/historical-mf-data as the history source.
- **The RBI ECL Directions reference RBI/DOR/2026-27/398, effective 1 Apr 2027** (via the baselkit README).
- **RBI 2026 amendments to NBFC provisioning and income-recognition rules.** The second report lists these, which matches agent 8's KNM India snippet. **This raises the priority of verify-item #1** (whether any ECL or provisioning change now applies to NBFCs).
- vectorbt's Commons Clause, Backtrader's GPL, QuantLib's BSD licence and PyPortfolioOpt's move to the `PyPortfolio` org.
- Aladdin as a common data language with API-first Studio, Data Cloud on Snowflake, and a Java/Kafka/Snowflake stack from job ads.

## 5. New items to add to the verification list

1. **SEBI Master Circular for Mutual Funds, March 2026**
   https://www.sebi.gov.in/legal/master-circulars/mar-2026/master-circular-for-mutual-funds_100208.html
   It would supersede the Jun 2024 master circular that agent 8 cited, for riskometer, PRC and debt-fund stress-testing rules.
2. **RBI NBFC concentration-risk directions and the 2026 amendment.** Check the current single- and group-exposure limits by layer.
3. **RBI NBFC ALM / liquidity directions (2025).** Check stress-testing and gap-analysis requirements, the asset-size threshold, and whether they are draft or final.
4. **The NFRA 2026 observations on ECL under Ind AS 109.**
5. **Jio BlackRock's actual use of Aladdin.** This is context only.

## 6. Design ideas worth adopting from the second report

- **A "Why?" drawer on every metric.** It shows method, window, horizon, valuation date, data cut, missing-price coverage, top contributors and a plain-English interpretation. This makes "explainability" concrete and cheap to build in Streamlit.
- **A regulatory rule registry as data.** Each rule records jurisdiction, regulator, entity type, product type, effective_from/to, threshold or formula, source document and version. This is the same idea as agent 8's dated parameter tables, with a cleaner schema.
- **Scenario and Result as first-class objects** (`snapshot + scenario + model_version → result`). This is the same as agent 7's run_id rule.
- **Acceptance tests.** A re-upload reproduces identical results. A missing price never silently changes a number. Every shock declares what it shocks.
