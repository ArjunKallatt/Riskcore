# Agent 4: GitHub and open-source hunt for Riskcore

Research date: 2026-10-02. Scope: Riskcore v1 (investment portfolio risk: VaR/CVaR, factors, stress, optimisation, Indian market data) and v2 (NBFC loan-book risk: PD/LGD/EAD, IFRS 9 / Ind AS 109 ECL, concentration, stress).

## Method and provenance (read first)

| Data point | Source | How to read the "verified" column |
|---|---|---|
| Stars, last push date (`pushed_at`), GitHub licence (SPDX), language, archived flag | GitHub REST search API, reached through the GitHub MCP connector on 2026-10-02. The figures were copied from the raw JSON. | **GH**: the API returned it on 2026-10-02. Stars are as seen that day. The director later said not to use GitHub MCP tools, so nothing after that note came from them. If you need independent verification, treat stars as point-in-time and unaudited. |
| Latest release version and date, PyPI licence/classifier, project URL | `https://pypi.org/pypi/<pkg>/json`, fetched with curl | **PyPI**: verified via PyPI. |
| Licence text | `raw.githubusercontent.com/<repo>/<branch>/LICENSE*`, fetched with curl | **LIC**: I read the licence file itself. |
| Features and README claims | READMEs fetched from raw.githubusercontent.com or with WebFetch | **README**: I opened and read the README. |

Tool limits I hit:
- `api.github.com` returned 403 through both the proxy and WebFetch.
- The session's WebSearch budget was already used up (200/200) when I started, so discovery went through GitHub repo search, awesome-quant, and README cross-links.
- The `open-risk/*` repos all show a `pushed_at` of 2026-09-28. That looks like an org-wide bulk push. PyPI releases for transitionMatrix, concentrationMetrics, and correlationMatrix stop at 2022-02-21, so treat them as **slow or stale**.

Reuse scale:
- **H**: put it in the core stack.
- **M**: use for one specific module, or as a reference implementation.
- **L**: reference only, or avoid.

---

## (a) Main table

### A. Portfolio optimisation and risk measures

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse in Riskcore | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dcajasn/Riskfolio-Lib | Optimisation / risk | 4,532 | push 2026-10-01; PyPI 7.3.0 (2026-05-31) | BSD-3-Clause | Python (+C++ ext) | Mean-risk optimisation over about 24 risk measures (CVaR, EVaR, CDaR, MDD, etc.), risk parity, HRP/HERC, Black-Litterman, factor models, risk-contribution plots | Active | **H** | Main v1 optimisation and risk engine. Use `rp.Portfolio` for CVaR/EVaR optimisation, `rp.RiskFunctions` for stand-alone VaR/CVaR/EVaR/CDaR, and the `plot_risk_con`/`plot_frontier` figures, which work in Streamlit through `st.pyplot` | https://github.com/dcajasn/Riskfolio-Lib | GH, PyPI |
| skfolio/skfolio | Optimisation / risk / stress | 2,456 | push 2026-10-01; PyPI 1.4.10 (2026-09-30) | BSD-3-Clause | Python | scikit-learn-style portfolio optimisation with cross-validation, factor models, Entropy Pooling, vine/bivariate copulas, and synthetic-data **stress tests and factor stress tests** | Very active | **H** | Use for stress and scenario generation (`SyntheticData` + vine copula, Entropy Pooling views) and walk-forward validation of optimisers. The sklearn API makes pipelines simple | https://github.com/skfolio/skfolio | GH, PyPI, README |
| PyPortfolio/PyPortfolioOpt | Optimisation | 6,071 | push 2026-07-07; PyPI 1.6.0 (2026-02-26) | MIT | Python | Efficient frontier, Black-Litterman, HRP, Ledoit-Wolf and other covariance shrinkage, discrete allocation | Active. The repo moved from `robertmartin8/` to the `PyPortfolio` org | **H** | Simple MVO/BL for "quick optimise" UI and `risk_models.CovarianceShrinkage`. `DiscreteAllocation` converts weights into whole Indian share lots | https://github.com/PyPortfolio/PyPortfolioOpt | GH, PyPI |
| cvxpy/cvxpy | Convex optimisation | 6,355 | push 2026-10-02; PyPI 1.9.3 (2026-09-19) | Apache-2.0 | Python/C++ | Modelling language for convex problems. Riskfolio, skfolio and PyPortfolioOpt depend on it | Very active | **H** | Write custom constraints for SEBI/RBI-style limits (sector caps, single-issuer caps, turnover) when the libraries above can't express them | https://github.com/cvxpy/cvxpy | GH, PyPI |
| oxfordcontrol/Clarabel.rs | Solver (dependency, level 2) | 614 | push 2026-04-13; PyPI clarabel 0.11.1 (2025-06-11) | Apache-2.0 | Rust | Interior-point conic solver, the default for cvxpy/skfolio | Active | M | Pin it as the cvxpy solver. Avoids commercial MOSEK | https://github.com/oxfordcontrol/Clarabel.rs | GH, PyPI |
| osqp/osqp | Solver (dependency, level 2) | 2,205 | push 2026-01-12; PyPI 1.1.3 (2026-06-12) | Apache-2.0 | C | Fast QP solver used by cvxpy | Active | M | Use for fast QP (MVO, tracking error) | https://github.com/osqp/osqp | GH, PyPI |
| convexfi/riskparity.py | Risk parity | 325 | push 2026-08-31; PyPI riskparityportfolio 0.6.0 (2024-05-26) | MIT | Python | Fast risk-budgeting portfolios (HKUST, Palomar) | Moderate | M | Risk-budget allocation if Riskfolio's version is too slow | https://github.com/convexfi/riskparity.py | GH, PyPI |
| fortitudo-tech/fortitudo.tech | Stress / CVaR / Entropy Pooling | 311 | push 2026-08-20; PyPI 1.2.5 (2026-08-20) | **GPL-3.0-or-later** | Python | Entropy Pooling views and stress testing combined with CVaR optimisation | Active | M (licence) | Reference for scenario-probability stress (Meucci). skfolio's Entropy Pooling (BSD) avoids the GPL | https://github.com/fortitudo-tech/fortitudo.tech | GH, PyPI |
| ArturSepp/OptimalPortfolios | Optimisation / backtest | 97 | push 2026-10-02; PyPI 7.10.2 (2026-10-01) | MIT | Python | Multi-asset construction, covariance estimation, rolling optimisation and backtest | Very active, small user base | L/M | Reference for rolling-covariance plus rebalancing pipelines | https://github.com/ArturSepp/OptimalPortfolios | GH, PyPI |
| ArturSepp/QuantInvestStrats (`qis`) | Perf. analytics / factsheets | 642 | push 2026-10-02; PyPI qis 5.33.2 (2026-10-01) | MIT | Python | Performance analytics, risk analysis, PDF factsheet reporting | Very active | M | Template for an Aladdin-style "fund factsheet" export (PDF/PNG) | https://github.com/ArturSepp/QuantInvestStrats | GH, PyPI |
| fmilthaler/FinQuant | Portfolio mgmt | 1,827 | push 2023-11-04; PyPI 0.7.0 (2023-09-04) | MIT | Python | Simple portfolio build, MC efficient frontier | Stale | L | Teaching reference only | https://github.com/fmilthaler/FinQuant | GH, PyPI |
| tradytics/eiten | Strategies | 3,305 | push 2022-07-30 | **GPL-3.0** | Python | Eigen / min-var / genetic portfolios | Stale | L | Avoid. GPL and stale. The PyPI `eiten` 1.0.1 lists homepage "test.com", so it may not be the official package | https://github.com/tradytics/eiten | GH, PyPI |
| jankrepl/deepdow | DL optimisation | 1,184 | push 2024-01-24; PyPI 0.2.3 (2024-01-24) | Apache-2.0 | Python | Portfolio optimisation with deep learning | Stale | L | Not needed | https://github.com/jankrepl/deepdow | GH, PyPI |
| Marigold/universal-portfolios | Online portfolio selection | 864 | push 2026-07-31; PyPI 0.4.17 (2026-07-30) | "Feedback MIT" (MIT plus a feedback request) | Python | OLPS algorithms | Maintained | L | Not core | https://github.com/Marigold/universal-portfolios | GH, PyPI, LIC |

### B. Performance and risk analytics (tear sheets)

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ranaroussi/quantstats | Perf. / risk analytics | 7,677 | push 2026-09-27; PyPI 0.0.86 (2026-09-27) | Apache-2.0 | Python | Sharpe, Sortino, VaR/CVaR, drawdowns, rolling stats, HTML tear sheets vs benchmark | Active (revived 2025-26) | **H** | Use `qs.stats.*` for KPI tiles. Use `qs.reports.html()` for a "download tear sheet" button against a NIFTY 50 / NIFTY 500 TRI benchmark | https://github.com/ranaroussi/quantstats | GH, PyPI |
| stefan-jansen/empyrical-reloaded | Risk metrics | 124 | push 2025-12-12; PyPI 0.5.12 (2025-06-01) | Apache-2.0 | Python | Maintained fork of empyrical: alpha/beta, VaR, CVaR, capture ratios, tail ratio | Maintained, slow | M/H | Lightweight, well-tested metric functions. Cross-check against quantstats in unit tests | https://github.com/stefan-jansen/empyrical-reloaded | GH, PyPI |
| quantopian/empyrical | Risk metrics | 1,514 | push 2024-07-26; PyPI 0.5.5 (2020-10-13) | Apache-2.0 | Python | Original | **Stale** (Quantopian closed) | L | Use the -reloaded fork | https://github.com/quantopian/empyrical | GH, PyPI |
| stefan-jansen/pyfolio-reloaded | Tear sheets | 616 | push 2025-12-15; PyPI 0.9.9 (2025-06-02) | Apache-2.0 | Python | Returns, positions, transactions and round-trip tear sheets | Maintained, slow | M | Reuse ideas from the positions/exposure tear sheet (sector exposure, gross/net leverage). matplotlib-based, so wrap with `st.pyplot` | https://github.com/stefan-jansen/pyfolio-reloaded | GH, PyPI |
| quantopian/pyfolio | Tear sheets | 6,428 | push 2023-12-23; PyPI 0.9.2 (2019-04-15) | Apache-2.0 | Python | Original | **Stale** | L | Use the fork | https://github.com/quantopian/pyfolio | GH, PyPI |
| stefan-jansen/alphalens-reloaded | Factor analysis | 660 | push 2025-12-15; PyPI 0.4.6 (2025-06-02) | Apache-2.0 | Python | Factor IC, quantile returns, turnover | Maintained, slow | M | Validate custom factor signals (value/momentum on NSE universe) before they go into the factor-exposure module | https://github.com/stefan-jansen/alphalens-reloaded | GH, PyPI |
| quantopian/alphalens | Factor analysis | 4,461 | push 2024-02-12; PyPI 0.4.0 (2020) | Apache-2.0 | Python | Original | Stale | L | Use the fork | https://github.com/quantopian/alphalens | GH, PyPI |
| pmorissette/ffn | Financial functions | 2,679 | push 2026-10-01; PyPI 1.2.2 (2026-09-17) | MIT | Python | Perf. stats, drawdowns, rebasing, `calc_stats` | Active | M | Convenience perf. stats. Overlaps with quantstats | https://github.com/pmorissette/ffn | GH, PyPI |
| JerBouma/FinanceToolkit | Fundamentals + risk | 5,393 | push 2026-10-01; PyPI 2.2.1 (2026-10-01) | MIT | Python | 150+ ratios plus risk/performance/technicals/fixed-income modules. README describes a "Risk" module (volatility etc.) | Very active | M | Fundamental factor inputs (P/E, ROE, leverage) for the factor-exposure page. Needs a FinancialModelingPrep key for most data, so check Indian coverage | https://github.com/JerBouma/FinanceToolkit | GH, PyPI, README |
| cloudQuant/fincore | Risk analytics | 5 | push 2026-09-20; PyPI 0.5.1 (2026-09-20) | MIT | Python | Claims 150+ metrics; listed in awesome-quant as an empyrical successor | New, tiny | L | Watch only | https://github.com/cloudQuant/fincore | GH, PyPI |
| braverock/PerformanceAnalytics | Perf. analytics (R) | 239 | push 2026-04-13 | GPL (no SPDX on GitHub; unverified) | R | The reference R implementation of risk/performance measures (modified VaR, ES) | Maintained | L | Formula reference for Cornish-Fisher modified VaR. Do not port the code (GPL) | https://github.com/braverock/PerformanceAnalytics | GH (licence unverified) |

### C. Backtesting engines

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| polakowo/vectorbt | Vectorised backtest | 9,258 | push 2026-09-26; PyPI 1.1.1 (2026-09-26) | **Apache-2.0 + Commons Clause** | Python | Very fast numba-vectorised backtests and portfolio stats | Active | M (licence) | Fine for internal research. **Commons Clause bans "selling" a product whose value derives substantially from vectorbt**, so keep it out of a commercial Riskcore SaaS | https://github.com/polakowo/vectorbt | GH, PyPI, LIC |
| pmorissette/bt | Strategy backtest | 2,993 | push 2026-10-02; PyPI 1.2.3 (2026-09-12) | MIT | Python | Tree-of-algos backtester for allocation strategies (built on ffn) | Active | M | Backtest optimiser outputs (monthly rebalance of Riskfolio weights). MIT, so safe for commercial use | https://github.com/pmorissette/bt | GH, PyPI |
| stefan-jansen/zipline-reloaded | Event-driven backtest | 1,948 | push 2026-01-06; PyPI 3.1.1 (2025-07-19) | Apache-2.0 | Python | Maintained Zipline fork | Maintained, slow | L | Too heavy (bundles, calendars) for Riskcore | https://github.com/stefan-jansen/zipline-reloaded | GH, PyPI, README |
| quantopian/zipline | Event-driven backtest | 20,137 | push 2024-02-13; PyPI 1.4.1 (2020) | Apache-2.0 | Python | Original | Stale | L | Don't use | https://github.com/quantopian/zipline | GH, PyPI |
| mementum/backtrader | Event-driven backtest | 23,374 | push 2024-08-19; PyPI 1.9.78.123 (2023-04-19) | **GPL-3.0** | Python | Popular event-driven backtester | Stale | L | Avoid: GPL plus no maintenance | https://github.com/mementum/backtrader | GH, PyPI |
| QuantConnect/Lean | Trading engine | 21,841 | push 2026-10-02; PyPI `lean` CLI 1.0.229 (2026-08-28) | Apache-2.0 | C# | Institutional-grade engine with a Python API | Very active | L | Architecture reference (risk-management models, universe selection). Overkill to embed | https://github.com/QuantConnect/Lean | GH, PyPI |
| nautechsystems/nautilus_trader | Trading engine | 29,556 | push 2026-10-02; PyPI 1.231.0 (2026-08-02) | **LGPL-3.0** | Rust/Python | Production event-driven trading engine | Very active | L | Out of scope (execution). LGPL is fine if used unmodified as a library | https://github.com/nautechsystems/nautilus_trader | GH, PyPI |
| santoshlite/EigenLedger | Backtest / analytics | 1,083 | push 2025-09-14; PyPI 2.1.6 (2024-10-28) | Apache-2.0 on GitHub, but **PyPI classifier says "Other/Proprietary"** | Python | Portfolio backtest plus risk report | Slow | L | Licence ambiguous, so skip | https://github.com/santoshlite/EigenLedger | GH, PyPI |

### D. Pricing, fixed income and enterprise risk engines

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| lballabio/QuantLib | Pricing library | 7,643 | push 2026-10-02; PyPI QuantLib 1.43 (2026-07-14) | Modified BSD (PyPI: BSD-3-Clause) | C++ | Industry-standard pricing: bonds, curves, swaps, options, day counts, calendars | Very active | M/H | Price Indian G-secs, SDLs and corporate bonds, then compute duration, convexity and KRDs for the fixed-income part of v1 and rate-shock stress. Install with `pip install QuantLib` (no compile needed) | https://github.com/lballabio/QuantLib | GH, PyPI, LIC |
| lballabio/QuantLib-SWIG | Python bindings | 402 | push 2026-10-02 | Modified BSD | SWIG | Builds the `QuantLib` Python wheel | Very active | M | Comes in through the `QuantLib` wheel | https://github.com/lballabio/QuantLib-SWIG | GH |
| OpenSourceRisk/Engine (ORE, Acadia) | Enterprise risk engine | 795 | push 2026-09-15; PyPI open-source-risk-engine 1.8.17.0 (2026-09-15) | Modified BSD (per README) | C++ | Built on QuantLib: XVA (CVA/DVA/FVA), exposure simulation, VaR, SIMM, sensitivities | Active | L/M | The closest open-source "Aladdin-like" analytics engine. Very heavy XML configuration. Use as a methodology reference for exposure simulation and parametric/historical VaR reports, or call the Python wheel for complex OTC books. Not needed for v1/v2 | https://github.com/OpenSourceRisk/Engine | GH, PyPI, README |
| domokane/FinancePy | Derivatives / FI pricing | 3,168 | push 2026-10-02; PyPI 1.1.2 (2026-08-21) | **GPL-3.0-or-later** | Python | Pure-Python pricing (bonds, CDS, swaptions, options) with numba | Active | M (licence) | Readable formula reference. **Do not import into a closed-source commercial Riskcore** (GPL); prefer QuantLib | https://github.com/domokane/FinancePy | GH, PyPI |
| attack68/rateslib | Fixed income / curves | 365 | push 2026-05-20; PyPI 2.7.1 (2026-04-04) | **Source-available, non-commercial. Commercial use needs a paid licence** | Python/Rust | Curves, bonds, bond futures, IRS/XCS, AD risk | Active | L (licence) | Avoid for a commercial product. The README says it is "source-available, **not** open source" | https://github.com/attack68/rateslib | GH, PyPI, README |
| google/tf-quant-finance | Pricing (TensorFlow) | 5,517 | push 2026-08-06; PyPI 0.0.1.dev34 (2022-08-19) | Apache-2.0 | Python | GPU pricing models | **README: "no longer maintained and has been archived"** | L | Don't use | https://github.com/google/tf-quant-finance | GH, PyPI, README |
| goldmansachs/gs-quant | Risk toolkit | 13,030 | push 2026-10-01; PyPI 2.1.18 (2026-10-01) | Apache-2.0 | Python | GS risk/structuring toolkit. README: API access needs a GS **institutional client** id and secret | Active | L | API-design reference only. Most functionality is gated behind Marquee | https://github.com/goldmansachs/gs-quant | GH, PyPI, README |
| auto-differentiation/QuantLib-Risks-Py | AAD risk for QuantLib | 22 | push 2026-04-02 | **AGPL-3.0** | Python | Fast AAD sensitivities over QuantLib | Active | L (licence) | Avoid in SaaS (AGPL network clause) | https://github.com/auto-differentiation/QuantLib-Risks-Py | GH, LIC |

### E. Econometrics, statistics, tail and dependence modelling

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bashtage/arch | Volatility / VaR | 1,583 | push 2026-09-27; PyPI 8.0.0 (2025-10-21) | NCSA (permissive, BSD-like) | Python | GARCH/EGARCH/GJR with Student-t/skew-t, filtered historical simulation, bootstrap, unit-root tests | Active | **H** | GARCH-filtered VaR/CVaR (conditional VaR), volatility forecasts, bootstrap CIs on VaR. Kupiec/Christoffersen backtests can be built on its residuals | https://github.com/bashtage/arch | GH, PyPI, LIC |
| statsmodels/statsmodels | Econometrics | 11,669 | push 2026-10-02; PyPI 0.15.0 (2026-08-27) | BSD-3-Clause | Python | OLS/robust regression, logit, time series, VAR | Very active | **H** | Factor regressions (Fama-French-style / Barra-lite exposures), logistic PD models, macro satellite models (PD ~ GDP, repo rate) for ECL forward-looking overlays | https://github.com/statsmodels/statsmodels | GH, PyPI |
| bashtage/linearmodels | Panel / asset-pricing | 1,072 | push 2026-09-28; PyPI 7.0 (2025-10-21) | NCSA | Python | Panel OLS, Fama-MacBeth, linear factor models (GMM) | Active | M | Cross-sectional factor-risk-premium estimation for the factor-exposure module | https://github.com/bashtage/linearmodels | GH, PyPI |
| scikit-learn/scikit-learn | ML | 67,451 | push 2026-10-02; PyPI 1.9.1 (2026-09-10) | BSD-3-Clause | Python | Ledoit-Wolf/OAS covariance, PCA, logistic regression, GBMs | Very active | **H** | Covariance shrinkage, statistical (PCA) factor model, PD classifiers for v2 | https://github.com/scikit-learn/scikit-learn | GH, PyPI |
| CamDavidsonPilon/lifelines | Survival analysis | 2,613 | push 2026-03-07; PyPI 0.30.3 (2026-03-05) | MIT | Python | Kaplan-Meier, Cox PH, AFT models | Maintained | **H (v2)** | **Lifetime PD term structures** for Stage 2/3 ECL (survival curve to marginal PDs), prepayment curves | https://github.com/CamDavidsonPilon/lifelines | GH, PyPI |
| georgebv/pyextremes | EVT | 280 | push 2026-02-19; PyPI 2.5.0 (2026-02-19) | MIT | Python | Block-maxima/POT, GEV/GPD fits | Maintained | M | EVT VaR/ES for fat-tailed small-cap Indian equities, as an "advanced VaR" option | https://github.com/georgebv/pyextremes | GH, PyPI |
| DanielBok/copulae | Copulas | 164 | push 2025-02-07; PyPI 0.8.0 (2025-02-07) | MIT | Python | Elliptical and Archimedean copulas | Slow | M | t-copula Monte Carlo VaR. Also a correlated-default simulation for loan books | https://github.com/DanielBok/copulae | GH, PyPI |
| sdv-dev/Copulas | Copulas | 653 | push 2026-09-21; PyPI 0.14.1 (2026-02-05) | **Business Source License 1.1** | Python | Multivariate copulas for synthetic data | Active | L (licence) | BSL bars offering a "Synthetic Data Creation Service". Probably fine for risk use, but prefer copulae (MIT) or skfolio | https://github.com/sdv-dev/Copulas | GH, PyPI, LIC |
| hudson-and-thames/mlfinlab | Financial ML | 4,932 | push 2023-10-02; not on PyPI (404) | **Proprietary** licence agreement | Python | AFML (de Prado) implementations | Commercialised | L | **Avoid**: the licence file is a paid licensing agreement | https://github.com/hudson-and-thames/mlfinlab | GH, LIC |

### F. Credit risk, scorecards and IFRS 9 / ECL (v2)

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| guillermo-navas-palencia/optbinning | Scorecard / binning | 532 | push 2026-09-29; PyPI 1.0.0 (2026-09-12) | Apache-2.0 | Python | Mathematically optimal monotonic binning (WoE/IV), `Scorecard`, scorecard monitoring (PSI), batch/stream binning, counterfactuals | Active | **H (v2)** | Core of the PD application/behavioural scorecard. `BinningProcess` + `Scorecard` + `ScorecardMonitoring` (PSI/CSI) for model monitoring on NBFC data | https://github.com/guillermo-navas-palencia/optbinning | GH, PyPI, README |
| ShichenXie/scorecardpy | Scorecard | 806 | push 2026-07-28; PyPI 0.1.9.7 (2023-07-29) | MIT | Python | WoE binning, IV, scorecard points, PSI, perf plots (port of the R `scorecard` package) | Repo active; PyPI release old | M/H | Quick alternative or cross-check to optbinning; `perf_eva`, `perf_psi` | https://github.com/ShichenXie/scorecardpy | GH, PyPI |
| amphibian-dev/toad | Scorecard | 529 | push 2026-06-16; PyPI 0.1.7 (2026-05-18) | MIT | Python | End-to-end scorecard tooling: EDA, binning, selection, stepwise, scorecard, PSI | Active | M | Feature-selection utilities (`toad.selection.select`, IV/correlation filters) | https://github.com/amphibian-dev/toad | GH, PyPI, README |
| itlubber/scorecardpipeline | Scorecard pipeline | 263 | push 2026-09-05; PyPI 0.1.39 (2026-06-21) | MIT | Python | sklearn-pipeline scorecards with Excel reporting (Chinese docs) | Active | L/M | Reference for Excel model-documentation output | https://github.com/itlubber/scorecardpipeline | GH, PyPI |
| boredbird/woe | WoE | 254 | push 2019-10-29; PyPI 0.1.4 (2018) | MIT | Python | WoE transforms | Stale | L | Superseded by optbinning | https://github.com/boredbird/woe | GH, PyPI |
| open-risk/transitionMatrix | Rating migration | 88 | push 2026-09-28 (bulk); PyPI 0.5.1 (2022-02-21) | Apache-2.0 | Python | Cohort and duration (Aalen-Johansen) transition-matrix estimators, generators, rating mapping | Slow / semi-stale | **H (v2)** | Estimate **DPD-bucket / stage migration matrices** (0, 1-30, 31-60, 61-90, 90+), then multiply matrices to get lifetime PD for Ind AS 109 staging. Pin the version or vendor the estimators | https://github.com/open-risk/transitionMatrix | GH, PyPI, README |
| open-risk/concentrationMetrics | Concentration | 44 | push 2026-09-28 (bulk); PyPI 0.6.0 (2022-02-21) | MIT | Python | HHI, Gini, Shannon, Theil, Atkinson, concentration ratio, bootstrap CIs | Slow | **H** | Single-name, sector, geography and product concentration on the NBFC book (and issuer concentration in v1). The formulas are small enough to vendor | https://github.com/open-risk/concentrationMetrics | GH, PyPI, README |
| open-risk/correlationMatrix | Correlation | 15 | push 2026-09-28 (bulk); PyPI 0.2.0 (2022-02-21) | Apache-2.0 | Python | Correlation estimation, stressing and repair of correlation matrices | Stale | L/M | Reference for nearest-PSD repair of stressed correlation matrices | https://github.com/open-risk/correlationMatrix | GH, PyPI, README |
| open-risk/openLGD | LGD | 25 | push 2026-09-28 (bulk) | Apache-2.0 | Python | LGD model estimation, standalone or federated (README: "early alpha") | Alpha | L/M | Reference for LGD model structure. Build workout-LGD yourself | https://github.com/open-risk/openLGD | GH, README |
| open-risk/portfolioAnalytics | Credit portfolio loss | 34 | push 2026-09-28 (bulk) | **GPL-2.0** | Python | Vasicek finite/asymptotic pool loss (EL, UL, quantile) | Slow | M (formula only) | Vasicek/ASRF loss distribution for the v2 credit stress and economic-capital page. **Re-implement from public formulas**; don't copy GPL code | https://github.com/open-risk/portfolioAnalytics | GH, README |
| open-risk/openNPL | Loan data platform | 35 | push 2026-09-28 (bulk) | MIT | (Django/JS per GitHub lang: JavaScript) | Loan-tape data model based on EBA NPL templates | Slow | M | Borrow the **loan-tape schema** (counterparty, loan, collateral, enforcement entities) for the v2 data model | https://github.com/open-risk/openNPL | GH |
| open-risk/openRiskScore | Risk scoring | 52 | push 2026-09-28 (bulk) | none detected | Python | Risk-scoring framework | Slow | L | Reference only (no licence) | https://github.com/open-risk/openRiskScore | GH |
| naenumtou/ifrs9 | IFRS 9 ECL reference | 130 | push 2025-11-08 | **None (all rights reserved)** | Jupyter | Full IFRS 9 impairment notebooks: staging, PD/LGD/EAD, forward-looking macro | Maintained | M (read-only) | Methodology walkthrough to mirror. **No licence, so don't copy code** | https://github.com/naenumtou/ifrs9 | GH, README |
| ShrishDhuria/IFRS9_ECL | IFRS 9 ECL engine | 2 | push 2026-06-10 | MIT | Python | PD term structures, 3-stage SICR waterfall, macro scenarios, Vasicek PIT PD, probability-weighted ECL, **Streamlit dashboard**, tests | New, small | M | Closest open template to Riskcore v2's ECL page (Python + Streamlit + MIT). Use as a design checklist; validate before relying on it | https://github.com/ShrishDhuria/IFRS9_ECL | GH, README |
| sebastian-gm/credit_risk_IFRS9_ECL_model | IFRS 9 ECL notebook | 8 | push 2025-02-16 | None | Jupyter | PD/LGD/EAD ECL project | Hobby | L | Reference only | https://github.com/sebastian-gm/credit_risk_IFRS9_ECL_model | GH |
| arnobotha/LifetimePD-TermStructure-Multistate | Lifetime PD (research) | 5 | push 2026-01-22 | MIT | R | Multi-state lifetime PD term structure (paper code) | Research | L/M | Methodology for multi-state (Markov) lifetime PD; pairs with transitionMatrix | https://github.com/arnobotha/LifetimePD-TermStructure-Multistate | GH |
| arnobotha/IFRS9-SICR-Definitions-Logit | SICR research | 8 | push 2026-01-22 | MIT | R | Comparing SICR definitions with logit models | Research | L/M | Ideas for SICR trigger calibration (DPD > 30 backstop + PD-ratio test) | https://github.com/arnobotha/IFRS9-SICR-Definitions-Logit | GH |
| rkhuran/CECL-Modelling-Implementation | CECL | 14 | push 2019-09-15 | None | Python | Loan-level PD/LGD/EAD lifetime loss (mortgage) | Stale | L | Reference | https://github.com/rkhuran/CECL-Modelling-Implementation | GH |
| eddyzzl/marvis-risk-agent | Credit-risk agent | 477 | push 2026-09-19 | MIT | Python | LLM agent for credit model development and validation | New | L | Optional future "AI validator" idea | https://github.com/eddyzzl/marvis-risk-agent | GH |
| mourarthur/awesome-credit-modeling | Awesome list | 177 | push 2024-02-01 | CC0-1.0 | n/a | Papers and resources on credit modelling | Slow | M | Reading list for PD/LGD methodology | https://github.com/mourarthur/awesome-credit-modeling | GH |

### G. Indian market data and calendars

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| jugaad-py/jugaad-data | NSE/BSE/RBI data | 583 | push 2026-09-23; PyPI 0.35.9 (2026-09-23) | "YOLO licence" = **public domain** | Python | Historical/live NSE stocks, F&O, index OHLC + P/E + TRI, bhavcopy, RBI rates, caching, CLI | Active, tracks NSE site changes | **H** | Primary free EOD price, index-TRI and RBI-rate source. Wrap in a cached adapter with retries, because scraping breaks when NSE changes its site | https://github.com/jugaad-py/jugaad-data | GH, PyPI, LIC, README |
| RuchiTanmay/nselib | NSE data | 179 | push 2026-07-18; PyPI 2.5.1 (2026-05-01) | Apache-2.0 (GitHub) | Python | Bhavcopy, deliverables, bulk/block deals, **VaR margins**, F&O OI, index constituents, holiday calendar, India VIX | Active | **H** | Index constituents (for benchmarks), NSE-published VaR margins (sanity check), India VIX for regime/stress | https://github.com/RuchiTanmay/nselib | GH, PyPI, README |
| NayakwadiS/mftool | Indian MF NAVs (AMFI) | 257 | push 2026-09-21; PyPI 3.4 (2026-09-21) | MIT | Python | AMFI scheme codes, latest and historical NAVs | Active | **H** | Mutual-fund holdings in client portfolios (NAV history gives returns, VaR) | https://github.com/NayakwadiS/mftool | GH, PyPI, README |
| aeron7/nsepython | NSE data | 368 | push 2026-03-07; PyPI 2.97 (2025-05-26) | **GPL-3.0** | Python | NSE and NIFTY Indices API wrapper (separate "server edition" repo) | Active | M (licence) | Useful features, but **GPL**. Call it as a separate process/service or replace with nselib/jugaad | https://github.com/aeron7/nsepython | GH, PyPI, README |
| vsjha18/nsetools | NSE live quotes | 907 | push 2025-03-18; PyPI 2.0.1 (2025-03-18) | MIT | Python | Real-time NSE quotes, index lists | Slow | M | Live quote fallback | https://github.com/vsjha18/nsetools | GH, PyPI |
| sdabhi23/bsedata | BSE data | 116 | push 2026-01-08; PyPI 0.6.0 (2024-03-14) | MIT | Python | BSE quotes, gainers/losers, indices | Slow | L/M | BSE-only scrips | https://github.com/sdabhi23/bsedata | GH, PyPI |
| swapniljariwala/nsepy | NSE data | 808 | push 2023-12-24; PyPI 0.8 (2020-03-07) | LGPL-3.0 (LICENSE file) | Python | Old-site NSE scraper | **Deprecated** (README deprecation notice points to jugaad-data) | L | Do not use | https://github.com/swapniljariwala/nsepy | GH, PyPI, LIC, README |
| zerodha/pykiteconnect | Broker API | 1,314 | push 2026-09-15; PyPI kiteconnect 5.2.2 (2026-09-15) | MIT | Python | Official Zerodha Kite Connect client (holdings, positions, historical) | Active | M | Optional "import my holdings" connector (needs a paid Kite Connect app). Official and ToS-clean, unlike scraping | https://github.com/zerodha/pykiteconnect | GH, PyPI |
| ranaroussi/yfinance | Global prices | 25,409 | push 2026-09-30; PyPI 1.7.0 (2026-08-26) | Apache-2.0 | Python | Yahoo Finance prices (`.NS`/`.BO` tickers), FX | Very active | **H (prototype)** | Fast prototyping and global/FX data. Yahoo ToS is personal-use only, so don't rely on it for a commercial product | https://github.com/ranaroussi/yfinance | GH, PyPI |
| pydata/pandas-datareader | Data readers | 3,271 | push 2026-07-21; PyPI 0.11.1 (2026-06-24) | BSD-3-Clause | Python | FRED, Fama-French library, OECD, etc. | Maintained | M | Global macro (FRED) for stress scenarios; Fama-French factors for methodology tests | https://github.com/pydata/pandas-datareader | GH, PyPI, LIC |
| gerrymanoim/exchange_calendars | Calendars | 670 | push ~2026-09; PyPI 4.13.2 (2026-03-10) | Apache-2.0 | Python | Exchange calendars including **XBOM (Bombay SE)** | Active | **H** | Indian trading-day calendar for return alignment, VaR horizons and holding periods | https://github.com/gerrymanoim/exchange_calendars | GH, PyPI, README |
| rsheftel/pandas_market_calendars | Calendars | 1,001 | push 2026-07-12; PyPI 5.4.0 (2026-05-27) | MIT | Python | Market calendars (wraps exchange_calendars) | Active | M | Alternative wrapper | https://github.com/rsheftel/pandas_market_calendars | GH, PyPI |
| OpenBB-finance/OpenBB (API reports owner `openbq-org/OpenBB`) | Data platform | 73,742 | push 2026-10-02; PyPI openbb 5.0.0 (2026-09-29) | Apache-2.0 (LICENSE file: "All files in this repository are licensed under the Apache License, Version 2.0") | Python | "Open Data Platform": unified data connectors to Python, REST, Excel and MCP | Very active | M | Optional data-abstraction layer (FRED, ECB, OECD, FMP, etc.). Heavy dependency; Indian coverage is thin. Earlier OpenBB versions were AGPL, so pin ≥ the Apache-licensed release | https://github.com/OpenBB-finance/OpenBB | GH, PyPI, LIC, README |

### H. Dashboards, Aladdin-like apps and UI references

| Repo | Category | Stars | Last updated | License | Language | Purpose | Maintenance | Reuse | How to reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|
| streamlit/streamlit | Dashboard framework | 45,871 | push 2026-10-02; PyPI 1.64.0 (2026-09-15) | Apache-2.0 | Python | Data-app framework | Very active | **H** | Riskcore UI (already chosen) | https://github.com/streamlit/streamlit | GH, PyPI |
| plotly/dash | Dashboard framework | 24,440 | push 2026-10-02; PyPI 4.4.1 (2026-07-21) | MIT | Python | Callback-based dashboards | Very active | L/M | Migration path if Streamlit hits multi-user or state limits. Use Plotly figures inside Streamlit either way | https://github.com/plotly/dash | GH, PyPI |
| ghostfolio/ghostfolio | Wealth mgmt app | 9,390 | push 2026-10-02 | **AGPL-3.0** | TypeScript | Self-hosted wealth tracker (holdings, allocation, X-ray risk checks) | Very active | L | UX reference only (allocation and X-ray screens). **AGPL means don't copy code** | https://github.com/ghostfolio/ghostfolio | GH |
| portfolio-performance/portfolio | Portfolio tracker | 4,084 | push 2026-10-02 | EPL-1.0 | Java | Desktop performance tracker (TTWROR, IRR) | Very active | L | Reference for performance-attribution definitions (TTWROR vs IRR) | https://github.com/portfolio-performance/portfolio | GH |
| MBKraus/Python_Portfolio__VaR_Tool | VaR app | 124 | (updated 2026-07-28) | No LICENSE file found (404) | Python | wxPython widget: historical, parametric and MC VaR vs benchmark | Hobby | L | VaR method cross-check only | https://github.com/MBKraus/Python_Portfolio__VaR_Tool | GH (minimal) |

### I. Awesome lists and meta-resources (for level-2 discovery)

| Repo | Category | Stars | Last updated | License | Purpose | Reuse | Link | Verified |
|---|---|---|---|---|---|---|---|---|
| wilsonfreitas/awesome-quant | Awesome list | 29,923 | push 2026-10-02 | none detected | Master list. I read the sections "Portfolio Optimization & Risk Analysis", "Factor Analysis", "Calendars" and "Market Data". Level-2 finds: fincore, fortitudo.tech, riskparity.py, QuantLib-Risks-Py, OptimalPortfolios, mlfinlab, exchange_calendars, jugaad-data, nsetools | M (discovery) | https://github.com/wilsonfreitas/awesome-quant | GH, README |
| mourarthur/awesome-credit-modeling | Awesome list | 177 | 2024-02-01 | CC0 | Credit-risk reading list | M | https://github.com/mourarthur/awesome-credit-modeling | GH |
| open-risk/awesome-sustainable-finance | Awesome list | 82 | bulk 2026-09-28 | CC0 | Climate/ESG risk resources (possible v3 climate stress) | L | https://github.com/open-risk/awesome-sustainable-finance | GH |
| stefan-jansen/machine-learning-for-trading | Book code | 21,196 | updated 2026-10-02 | (not checked) | ML4T 3rd ed. code; parent of the *-reloaded forks | L | https://github.com/stefan-jansen/machine-learning-for-trading | GH |

Total distinct repos assessed: **about 85**.

---

## (b) Recommended core stack for Riskcore

All of the following have permissive licences (MIT, BSD, Apache or NCSA) and were actively maintained as of 2026-09/10.

| Layer | Library (pin) | Role in Riskcore |
|---|---|---|
| UI | `streamlit` 1.64, `plotly` | Pages, KPI tiles, interactive charts |
| Data: India | `jugaad-data` 0.35.9, `nselib` 2.5.1, `mftool` 3.4; `kiteconnect` (optional, official) | EOD prices, index TRI, constituents, India VIX, MF NAVs, RBI rates. Put them behind one `DataProvider` interface with on-disk Parquet cache and fallback order jugaad → nselib → yfinance |
| Data: global/macro | `yfinance` (prototype only), `pandas-datareader` (FRED) | FX, global indices, macro series for stress |
| Calendars | `exchange_calendars` 4.13 (XBOM) | Trading-day alignment, horizon scaling |
| Core numerics | `numpy`, `pandas`, `scipy`, `scikit-learn` 1.9 | Covariance shrinkage (Ledoit-Wolf), PCA factors |
| VaR/CVaR and vol | own code (historical, parametric, MC) + `arch` 8.0 (GARCH/FHS) + `pyextremes` (EVT, optional) + `copulae` (t-copula MC, optional) | VaR engine with Kupiec/Christoffersen backtests |
| Perf. / risk KPIs | `quantstats` 0.0.86 (+ `empyrical-reloaded` as test oracle) | Sharpe, Sortino, drawdown, tear-sheet export |
| Factor exposure | `statsmodels` 0.15 (+ `linearmodels` 7.0 for Fama-MacBeth) | Time-series and cross-sectional factor regressions on Indian factors (market, SMB, HML, momentum built from NSE data) |
| Optimisation | `riskfolio-lib` 7.3 (primary), `skfolio` 1.4 (CV, stress), `PyPortfolioOpt` 1.6 (simple/BL), `cvxpy` 1.9 + `clarabel` | MVO, CVaR, risk parity, HRP, BL, custom regulatory constraints |
| Stress / scenarios | `skfolio` (Entropy Pooling, synthetic vine-copula stress) + own historical-scenario library (2008, 2013 taper, 2016 demonetisation, 2020 COVID, 2022 rate hikes) | Hypothetical and historical stress |
| Fixed income (v1.5) | `QuantLib` 1.43 | G-sec/corporate bond pricing, duration, rate shocks |
| Backtest (optional) | `bt` 1.2 (MIT) | Rebalance backtests of optimiser outputs |
| v2 credit models | `optbinning` 1.0 (binning, scorecard, PSI monitoring), `scorecardpy` (cross-check), `statsmodels`/`scikit-learn` (logit PD), `lifelines` 0.30 (lifetime PD) | PD scorecards, lifetime PD term structure |
| v2 ECL and staging | own ECL engine (12m vs lifetime, discounted PD×LGD×EAD, SICR rules: DPD > 30, RBI SMA buckets), `transitionMatrix` (migration matrices; pin or vendor) | Ind AS 109 three-stage ECL, probability-weighted macro scenarios |
| v2 concentration | `concentrationMetrics` (or vendor HHI/Gini) | Single-borrower, sector and geography concentration vs RBI limits |
| v2 credit stress / capital | own Vasicek/ASRF implementation (formulas, cf. open-risk/portfolioAnalytics) + `copulae` for correlated defaults | Stressed PD, unexpected loss, economic capital |
| Reference designs (don't depend on) | ShrishDhuria/IFRS9_ECL (MIT), naenumtou/ifrs9 (no licence: read only), openNPL schema (MIT), ORE (methodology) | Checklists for ECL page and loan-tape schema |

Pairings I recommend against:
- Running Riskfolio-Lib and skfolio as two competing optimisers. Use Riskfolio for production weights and skfolio for validation and stress.
- vectorbt in the commercial product (Commons Clause).
- Several Indian scrapers with no cache layer. NSE rate-limits and changes endpoints often.

---

## (c) License warnings

| Severity | Repo / package | License | Implication for Riskcore |
|---|---|---|---|
| **Do not use commercially** | attack68/rateslib | Source-available, non-commercial; paid commercial licence | Any paid or production use needs a licence |
| **Do not use** | hudson-and-thames/mlfinlab | Proprietary licence agreement (LICENSE.txt) | Paid product. Code is not open source |
| **Network copyleft** | ghostfolio (AGPL-3.0), QuantLib-Risks-Py (AGPL-3.0) | AGPL-3.0 | Using or modifying them in a hosted service forces source disclosure of the combined work. Use as UX/methodology reference only |
| **Strong copyleft** | FinancePy, backtrader, fortitudo.tech, nsepython (+ nsepythonserver), eiten, open-risk/portfolioAnalytics (GPL-2.0), PerformanceAnalytics (R, GPL; unverified) | GPL-2.0/3.0 | Importing them into Riskcore and *distributing* it (on-prem install, desktop app) requires GPL-licensing Riskcore. Pure SaaS is a grey area for GPL (not AGPL), but avoid it if you may ever ship on-prem to NBFCs. Prefer the permissive alternatives: QuantLib (for FinancePy), skfolio Entropy Pooling (for fortitudo), nselib/jugaad (for nsepython) |
| **Commercial-sale restriction** | vectorbt | Apache-2.0 + **Commons Clause** | Can't sell a product or service whose value derives substantially from vectorbt. OK for internal research |
| **Field-of-use restriction** | sdv-dev/Copulas | Business Source License 1.1 | Bars use in a "Synthetic Data Creation Service". Riskcore probably isn't one, but BSL is not OSI-approved; prefer copulae (MIT) |
| Weak copyleft (OK as a library) | nautilus_trader, nsepy | LGPL-3.0 | Fine if used unmodified as a dynamically imported library. Modifications to the library must be shared |
| No licence = all rights reserved | naenumtou/ifrs9, sebastian-gm/credit_risk_IFRS9_ECL_model, rkhuran/CECL-Modelling-Implementation, open-risk/openRiskScore, MBKraus VaR tool, awesome-quant (none detected) | none | Read for ideas. Don't copy code |
| Ambiguous | EigenLedger (GitHub Apache-2.0 vs PyPI "Other/Proprietary"), eiten PyPI package (homepage "test.com", authenticity unclear), universal-portfolios ("Feedback MIT", permissive) | mixed | Avoid EigenLedger and the PyPI eiten package |
| Permissive but note | jugaad-data ("YOLO" public domain), arch/linearmodels (NCSA), QuantLib/ORE (modified BSD), OpenBB (now Apache-2.0; older releases were AGPL, so pin the version) | permissive | OK. Keep the attribution notices |
| Data ToS (not code licence) | yfinance (Yahoo ToS), NSE scraping libs (jugaad, nselib, nsetools, nsepython, bsedata) | n/a | Scraping NSE/BSE/Yahoo may breach the sites' terms. For a commercial product, license data (NSE Data & Analytics, a broker API such as Kite Connect, or a vendor) |

---

## (d) Bibliography (pages and endpoints actually opened)

GitHub repository metadata came from the GitHub REST search API (through the MCP connector) on 2026-10-02. It covered every repo in the tables above: stars, pushed_at, SPDX licence, language, archived flag.

PyPI JSON endpoints (`https://pypi.org/pypi/<name>/json`, opened 2026-10-02): jugaad-data, nsepython, mftool, nselib, nsepy, nsetools, bsedata, kiteconnect, yfinance, pandas-datareader, exchange-calendars, pandas-market-calendars, openbb, riskfolio-lib, skfolio, pyportfolioopt, cvxpy, riskparityportfolio, fortitudo.tech, optimalportfolios, qis, finquant, deepdow, universal-portfolios, osqp, clarabel, quantstats, empyrical, empyrical-reloaded, pyfolio, pyfolio-reloaded, alphalens, alphalens-reloaded, ffn, fincore, financetoolkit, vectorbt, zipline, zipline-reloaded, backtrader, bt, lean, nautilus_trader, QuantLib, open-source-risk-engine, financepy, rateslib, tf-quant-finance, gs-quant, arch, statsmodels, linearmodels, scikit-learn, lifelines, pyextremes, copulae, copulas, mlfinlab (404), scorecardpy, optbinning, toad, scorecardpipeline, woe, transitionMatrix, concentrationMetrics, correlationMatrix, streamlit, dash, eiten, EigenLedger.

LICENSE files read (raw.githubusercontent.com):
- https://raw.githubusercontent.com/polakowo/vectorbt/master/LICENSE.md (Commons Clause)
- https://raw.githubusercontent.com/openbq-org/OpenBB/develop/LICENSE (Apache-2.0)
- https://raw.githubusercontent.com/lballabio/QuantLib/master/LICENSE.TXT
- https://raw.githubusercontent.com/bashtage/arch/main/LICENSE.md (NCSA-style)
- https://raw.githubusercontent.com/swapniljariwala/nsepy/master/LICENSE (LGPL-3.0)
- https://raw.githubusercontent.com/hudson-and-thames/mlfinlab/master/LICENSE.txt (proprietary)
- https://raw.githubusercontent.com/sdv-dev/Copulas/main/LICENSE (BSL 1.1)
- https://raw.githubusercontent.com/Marigold/universal-portfolios/master/LICENSE (Feedback MIT)
- https://raw.githubusercontent.com/pydata/pandas-datareader/main/LICENSE.md (BSD-3)
- https://raw.githubusercontent.com/auto-differentiation/QuantLib-Risks-Py/main/LICENSE.md (AGPL-3.0)
- https://raw.githubusercontent.com/jugaad-py/jugaad-data/master/LICENSE.YOLO.md (public domain)

READMEs read:
- https://github.com/wilsonfreitas/awesome-quant (full README.md downloaded; risk, factor, calendar and data sections read)
- https://github.com/OpenBB-finance/OpenBB (WebFetch; resolves to openbq-org/OpenBB)
- https://github.com/stefan-jansen/zipline-reloaded (WebFetch) and https://pypi.org/pypi/zipline-reloaded/json
- https://github.com/attack68/rateslib (WebFetch: dual/non-commercial licence)
- https://github.com/OpenSourceRisk/Engine (WebFetch: Modified BSD, XVA/SIMM)
- https://github.com/jugaad-py/jugaad-data (WebFetch + raw README)
- raw READMEs: open-risk/transitionMatrix, open-risk/concentrationMetrics, open-risk/correlationMatrix, open-risk/openLGD, open-risk/portfolioAnalytics, amphibian-dev/toad, aeron7/nsepython, RuchiTanmay/nselib, NayakwadiS/mftool, skfolio/skfolio (README.rst), swapniljariwala/nsepy (deprecation notice), guillermo-navas-palencia/optbinning (README.rst), naenumtou/ifrs9, ShrishDhuria/IFRS9_ECL, gerrymanoim/exchange_calendars (XBOM row), rsheftel/pandas_market_calendars, JerBouma/FinanceToolkit, goldmansachs/gs-quant, google/tf-quant-finance ("no longer maintained and has been archived")

Not verified, or blocked:
- api.github.com returned 403 through both curl and WebFetch.
- WebSearch was unavailable because the session budget (200) was exhausted before this agent started.
- I did not check the licences of braverock/PerformanceAnalytics and stefan-jansen/machine-learning-for-trading.
- MBKraus VaR tool: no LICENSE at master/LICENSE.
