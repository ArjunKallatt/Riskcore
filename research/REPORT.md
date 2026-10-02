# Riskcore research report: what exists, what's missing, and what to build

**Research date:** 2 October 2026
**Method:** ten specialist research agents. Agents 1–9 ran in parallel. Agent 10 then critiqued their findings, and this report compiles all ten.
**Companion files:**
- [`csv/`](csv/): all the tables, as CSV.
- [`agents/`](agents/): each agent's full findings, with line-level evidence.
- [`build_csv.py`](build_csv.py): regenerates the CSVs from the agent files.

---

## Read this first: how far to trust this report

The research environment had **severe network restrictions**, and that limits how much of this report is verified.

- The sandbox's egress proxy **blocked almost every source site**. That included NSE, BSE, AMFI, RBI, SEBI, BIS, IFRS, MSCI, BlackRock, Bloomberg, Moody's, SAS, Kaggle, FRED, Ken French, arXiv, Reddit, Hacker News, Medium and Wikipedia.
- Only **github.com, raw.githubusercontent.com and pypi.org** could be opened directly.
- The session's **web-search allowance (200 searches) ran out** partway through. Agents 4, 6, 7 and 9 got few or no searches.
- Most commercial, regulatory and community claims therefore rest on **search-result snippets**: the URL is real, but the page body was not read.

Every row in the CSVs and the agent files carries a verification tag. The common meanings across agents are:

| Tag family | Meaning | Trust |
|---|---|---|
| `V-page`, `[P]`, `V-G`, `LIC`, `README`, `PyPI`, `GH`, `[verified]` | The page, file or API response was opened and read | High |
| `S`, `V-S`, `[S-official]`, `V-search`, `Yes` (Agent 5) | The URL came back in a live search, and the claim comes from the snippet or summary | Medium. Click through before you quote it. |
| `S-3P`, `S3`, `[S-secondary]` | As above, but from a third party (news, blog, aggregator) | Medium–low |
| `BK`, `U`, `[unverified]`, `?` | Background knowledge, not checked in this session | Low. A planning hint only. |

**The strongest primary evidence** is:
- The open-source licence and maintenance data. Agent 4 read the PyPI JSON for 70 packages and 11 LICENSE files, and took repo stats from GitHub's search API through the GitHub connector.
- BlackRock's own public API schemas on GitHub (Agent 3).
- Platform documentation hosted on GitHub: Streamlit, DuckDB, Hugging Face (Agent 7).

**Regulatory thresholds** (gold LTV tiers, ECL floors, SMA day-counts, PCA bands) come from secondary sources. **Do not hard-code any of them until you have read the primary circular.** §6 and the verification list in §9 say which ones to check first.

---

## 1. Executive summary

**What exists.** Commercial portfolio-risk software splits into two worlds:
- **Enterprise platforms**: Aladdin, MSCI RiskManager/BarraOne, Bloomberg PORT, FactSet, SimCorp Axioma. They are powerful, priced privately and multi-month projects to implement.
- **Retail trackers**: Indian ones such as INDmoney, Kuvera, Value Research, Tickertape and Zerodha Console, and global ones such as Portfolio Visualizer, Sharesight and Kubera. They do XIRR, overlap and tax, but little tail or liquidity risk.

Credit risk follows the same split:
- **Global suites**: Moody's ImpairmentCalc, SAS ECL, Oracle OFSAA, OneSumX and Finastra. They do IFRS 9 ECL plus stress testing, for banks.
- **Indian NBFC options**: ICRA Analytics ECL 3.0 (Excel plus managed service), Acies Kepler, ECL Square, and EWS (early-warning) vendors such as Crediwatch.
- **Indian lending platforms**: Nucleus FinnOne Neo, Lentra, Perfios. They run origination and collections, but no confirmed ECL engine.
- **No vendor surfaced a lightweight tool** that combines provisioning, concentration, gold-price stress and EWS.

**Open source is rich for the maths but thin for India and for credit.**
- Permissively licensed libraries cover nearly all of v1's quantitative needs: Riskfolio-Lib, skfolio, PyPortfolioOpt, arch, statsmodels, QuantLib, quantstats/empyrical-reloaded, optbinning, lifelines.
- There is **no maintained, licensed open-source IFRS 9 / ECL library**. The best references are naenumtou/ifrs9 (no licence) and ShrishDhuria/IFRS9_ECL (MIT, 2 stars).
- Indian data libraries exist (jugaad-data, nselib, mftool, casparser). However, **NSE's terms of use prohibit automated collection**, and yfinance is "personal use only". Data supply, not maths, is the binding constraint.

**What's missing (the opportunity).**
1. **Indian retail:** a free, transparent tool that measures tail risk (VaR/ES) and liquidity risk across a *combined* MF + direct equity + US-stock portfolio in INR, built on correct Indian data plumbing. That means CAS statement import, AMFI NAVs, total-return benchmarks and FX conversion, with **backtested** risk numbers. Trackers don't do risk, and DIY dashboards rarely backtest or handle Indian data correctly.
2. **Small/mid NBFCs:** an auditable, local-first tool that does:
   - a correct **DPD → SMA/NPA → IRACP provisioning** engine;
   - optional Ind AS 109 ECL with the RBI-required IRACP comparison and Impairment Reserve;
   - **gold-loan LTV mark-to-market and price-shock stress** under RBI's 2025 gold-lending Directions;
   - concentration analysis (HHI, top-20 exposures);
   - an auditor-ready Excel pack.

**Two corrections to the original plan from the critique (Agent 10):**
- **Most small NBFCs are not on Ind AS 109.** Ind AS applies to listed NBFCs and those with net worth ≥ ₹250 cr. The rest use Indian GAAP plus RBI IRACP provisioning. So v2's first must-have is **IRACP provisioning**, not ECL.
- **Cut the optimiser.** Optimisation is a crowded space, and suggesting target weights edges toward regulated investment advice under SEBI's IA/RA rules. Keep user-driven what-if analysis only.

**Main risks.**
- Data licensing: NSE/BSE, Yahoo, index providers.
- SEBI adviser rules for any public v1.
- **Employer IP.** v2 must use no employer data, code or parameters. Check your employment contract.
- NBFC demand is unvalidated. The evidence is vendor and consultant snippets, not buyer interviews.

**Recommendation.** Spend 4 weeks making v1 India-correct and credible: data plumbing, VaR backtesting, an India scenario library, liquidity and limits. Spend 2 weeks on a thin v2 wedge: loan tape → DPD → IRACP, plus gold stress, ECL-lite, concentration and an auditor pack. Then show v2 to 3–5 NBFC practitioners before building further (§10).

---

## 2. Commercial landscape

Full table: [`csv/commercial_landscape.csv`](csv/commercial_landscape.csv) (69 platforms, with columns for ECL, stress testing, verification and source date). Details are in [`agents/agent1.md`](agents/agent1.md) (investment) and [`agents/agent2.md`](agents/agent2.md) (credit).
**No enterprise vendor publishes a price.** Retail prices come from vendor pricing pages or third-party reviews and are indicative only.

### 2a. Investment portfolio and risk platforms

| Platform | Category | Key features worth noting | Target users | Pricing | Link |
|---|---|---|---|---|---|
| BlackRock Aladdin | Enterprise investment OS + risk | One data model across PM, trading, compliance, ops and risk; scenario library; APIs | Asset managers, insurers, pensions | Not public | https://www.blackrock.com/aladdin/platforms/products/aladdin-risk |
| MSCI RiskMetrics RiskManager | Market-risk system | Parametric, historical and MC VaR side by side; historical and hypothetical stress; predictive stress that propagates factor shocks | Hedge funds, asset managers, banks | Not public | https://www.msci.com/data-and-analytics/risk-management-solutions/riskmetrics-riskmanager |
| MSCI BarraOne | Multi-asset factor risk | Factor vs specific risk decomposition; attribution in the same factor language | Institutional | Not public | https://www.msci.com/data-and-analytics/portfolio-management/barra-one |
| Bloomberg PORT / AIM | Terminal analytics; OMS | Benchmark-relative risk, attribution by any grouping, AI commentary; AIM what-if rebalancing with compliance rules | Terminal users, buy-side | Not public | https://data.bloomberglp.com/professional/sites/4/Portfolio_and_Risk_Analytics_Brochure4.pdf |
| FactSet Portfolio Analytics | Analytics + multi-asset risk | Pluggable risk models (Barra, Axioma, Northfield, client custom) | Asset managers | Not public | https://www.factset.com/solutions/portfolio-analytics/risk-analytics |
| SimCorp Axioma | Factor models + optimiser | Short, medium and trading-horizon models; fund-allocation (look-through) risk models | Quants, asset managers | Not public | https://www.simcorp.com/solutions/strategic-solutions/axioma-solutions/axioma-portfolio-optimizer/axioma-portfolio-analytics |
| SimCorp Dimension, Charles River, SS&C Advent, Clearwater/Enfusion, Arcesium | Front-to-back ops / IBOR / accounting | IBOR single source of truth, pre/post-trade compliance, data-quality lineage | Large managers | Not public | see CSV |
| Addepar | Wealth aggregation | Multi-custodian aggregation, drift monitoring, household grouping | Family offices, RIAs | Not public (third-party est. ~$65k–$400k/yr) | https://www.capterra.com/p/275617/Addepar/ |
| Murex MX.3 | Sell-side trading + risk | Regulatory and internal risk in one engine | Banks | Not public | https://www.murex.com/en/solutions/business-solutions/enterprise-risk-management |
| Portfolio Visualizer | Retail web analytics | Backtest, Monte Carlo, Fama-French regression, efficient frontier | DIY investors | Free ≤15 assets; ~$30–55/mo (3P) | https://www.findmymoat.com/tools/portfolio-visualizer |
| Kubera / Sharesight | Net-worth / dividend tracker | FX-aware dividend-inclusive returns, tax reports | Retail/HNW | ~$249/yr; free–~$23/mo (3P) | see CSV |
| **India:** Tickertape | Screener + portfolio health | Diversification score, red flags, MF overlap | Retail | ₹2,999/yr Pro | https://www.tickertape.in/pricing |
| **India:** Value Research | MF research + tracker | Risk grade relative to category; free portfolio manager | Retail | ₹4,900/yr Fund Advisor | https://www.valueresearchonline.com/premium/subscribe/ |
| **India:** Kuvera / INDmoney | Direct MF / super-app | CAS import, INR+USD XIRR, LTCG tax harvesting | Retail | Free | see CSV |
| **India:** Morningstar India X-Ray | MF look-through | Overlap, style box, sector vs benchmark (free status uncertain) | MF investors | Free (?) | https://www.morningstar.in/posts/64689/get-instant-x-ray-fund-holdings.aspx |
| **India:** Zerodha Console / Sensibull | Broker analytics | P&L calendar heatmap, tax P&L; option payoff and Greeks | Broker clients | Free / ~₹800/mo | https://zerodha.com/products/console |
| **India:** Investwell, REDVision | MFD/RIA back office | Risk profiling → model allocation → rebalance | Distributors | From ₹25k/yr (Investwell) | https://investwellonline.com/pricing/ |
| **India:** CRISIL, ICRA Analytics, ACE Equity, Capitaline | Institutional data/risk services | Bond valuation, MF database, NBFC/bank financial templates | Institutions | Not public | see CSV |

### 2b. Lending and credit-risk platforms

| Platform | Category | ECL | Stress | Small/mid NBFC fit | Link |
|---|---|---|---|---|---|
| Moody's ImpairmentCalc (+ CreditLens, RiskCalc, CreditEdge) | ECL engine; PD models; EWS | Y | Y | Low (enterprise; third-party spend est. $17k–$4.8M/yr) | http://ma.moodys.com/rs/961-KCJ-308/images/SP39812_MA_ImpairmentCalc.pdf |
| SAS ECL / IFRS 9 / Stress Testing | ECL + enterprise stress | Y | Y | Low | https://www.sas.com/en_in/solutions/risk-management/solution/expected-credit-loss.html |
| Oracle OFSAA (LLFP, IFRS 9 Cloud, Credit Risk Mgmt) | ECL + 300+ credit reports incl. concentration | Y | Y | Low | https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/ifrs9-solution-cloud/25d/ifrsr/expected-credit-loss-overview-reports.html |
| Wolters Kluwer OneSumX | Finance-risk-regulatory | Y | Y | Low | https://www.wolterskluwer.com/en-sg/solutions/onesumx-for-finance-risk-and-regulatory-reporting/onesumx-ifrs-9 |
| Finastra Fusion Risk (ARC) | Balance-sheet risk + IFRS 9 | Y | Y? | Medium (MFI clients) | https://www.finastra.com/solutions/arc |
| S&P Credit Analytics | PD models + data | Y (separate page) | ? | Low | https://www.spglobal.com/market-intelligence/en/solutions/credit-risk-solutions |
| FICO, Experian PowerCurve | Decisioning / scores | N | N | — | see CSV |
| **India:** ICRA Analytics ECL 3.0 | Ind AS ECL tool + quarterly managed service; Excel input | Y | Y (macro) | **High** | https://www.icraanalytics.com/risk-management-offerings-solutions/solutions-and-tools/expected-credit-loss |
| **India:** Acies Kepler | IFRS 9 suite (Risk.net award 2025) | Y | Y | Medium | https://www.acies.consulting/keplerifrs9.html |
| **India:** ECL Square | Cloud ECL SaaS, NBFC page | Y | ? | High | https://eclsquare.com/solutions/for-nbfcs |
| **India:** Crediwatch, Roopya | EWS / NBFC SaaS | N / ? | N | High | https://about.crediwatch.com/about/product/early-warning-systems |
| **India:** CIBIL, Equifax, CRIF High Mark | Bureaus + portfolio reviews | N (CRIF group has an IFRS 9 page, UAE) | N | — | see CSV |
| **India:** Nucleus FinnOne Neo, Lentra, Perfios, CredAble, Kaleidofin | LOS/LMS, underwriting, alt-data | N | N | — | see CSV |

**Features worth copying** (merged from Agents 1 and 2):
- Three VaR methods side by side.
- A named, plain-English scenario library with factor propagation.
- Factor/specific risk decomposition with per-holding contribution.
- What-if trades with before/after risk and rule-based limit checks.
- MF look-through and overlap.
- A data-health page.
- A transparent, configurable staging policy.
- Probability-weighted three-scenario ECL.
- Excel loan tape in, auditor pack out.
- A configurable EWS alert library.
- Prebuilt concentration and DPD-migration reports.
- Separate regulatory and BAU stress modes.
- A per-loan, per-run audit trail.

---

## 3. Open-source repositories

Full table: [`csv/open_source_repos.csv`](csv/open_source_repos.csv) (92 repos). Stars are a snapshot from GitHub's search API on 2026-10-02. Release dates and licences were checked on PyPI where marked. Details: [`agents/agent4.md`](agents/agent4.md).

### 3a. High-reuse core (permissive licences)

| Repo | Stars | Last updated | License | Purpose | Reuse | Link |
|---|---|---|---|---|---|---|
| dcajasn/Riskfolio-Lib | 4.5k | PyPI 7.3.0, May 2026 | BSD-3 | ~24 risk measures, risk parity, HRP, BL | H (if optimiser kept) | https://github.com/dcajasn/Riskfolio-Lib |
| skfolio/skfolio | 2.5k | PyPI 1.4.10, Sep 2026 | BSD-3 | sklearn-style optimisation, stress tests, Entropy Pooling | H | https://github.com/skfolio/skfolio |
| PyPortfolio/PyPortfolioOpt | 6.1k | PyPI 1.6.0, Feb 2026 | MIT | MVO, BL, HRP, Ledoit-Wolf | H | https://github.com/PyPortfolio/PyPortfolioOpt |
| bashtage/arch | 1.6k | PyPI 8.0.0, Oct 2025 | NCSA | GARCH, filtered historical simulation, bootstrap | **H** | https://github.com/bashtage/arch |
| statsmodels/statsmodels | 11.7k | PyPI 0.15.0, Aug 2026 | BSD-3 | Factor regressions, logit PD, macro satellites | **H** | https://github.com/statsmodels/statsmodels |
| scikit-learn | 67k | PyPI 1.9.1, Sep 2026 | BSD-3 | Ledoit-Wolf, PCA, classifiers | **H** | https://github.com/scikit-learn/scikit-learn |
| ranaroussi/quantstats | 7.7k | PyPI 0.0.86, Sep 2026 | Apache-2.0 | KPIs, tear sheets | H | https://github.com/ranaroussi/quantstats |
| stefan-jansen/empyrical-reloaded | 124 | PyPI 0.5.12, Jun 2025 | Apache-2.0 | Metric functions (use as test oracle) | M/H | https://github.com/stefan-jansen/empyrical-reloaded |
| lballabio/QuantLib | 7.6k | PyPI 1.43, Jul 2026 | BSD | Bond, curve and day-count pricing | M/H | https://github.com/lballabio/QuantLib |
| guillermo-navas-palencia/optbinning | 532 | PyPI 1.0.0, Sep 2026 | Apache-2.0 | Binning, scorecards, PSI monitoring (v2) | H (v2) | https://github.com/guillermo-navas-palencia/optbinning |
| CamDavidsonPilon/lifelines | 2.6k | PyPI 0.30.3, Mar 2026 | MIT | Survival curves → lifetime PD | H (v2, later) | https://github.com/CamDavidsonPilon/lifelines |
| open-risk/transitionMatrix | 88 | PyPI 0.5.1, **2022** | Apache-2.0 | DPD/stage migration matrices | H (vendor the code) | https://github.com/open-risk/transitionMatrix |
| open-risk/concentrationMetrics | 44 | PyPI 0.6.0, **2022** | MIT | HHI, Gini, etc. | H (vendor the code) | https://github.com/open-risk/concentrationMetrics |
| NayakwadiS/mftool | 257 | PyPI 3.4, Sep 2026 | MIT | AMFI NAVs | H | https://github.com/NayakwadiS/mftool |
| codereverser/casparser | 231 | active 2026 | MIT | CAMS/KFin/NSDL/CDSL CAS parsing | H | https://github.com/codereverser/casparser |
| captn3m0/historical-mf-data | — | periodic | MIT | Full AMFI NAV history as SQLite | H | https://github.com/captn3m0/historical-mf-data |
| gerrymanoim/exchange_calendars | 670 | PyPI 4.13.2, Mar 2026 | Apache-2.0 | XBOM trading calendar | H | https://github.com/gerrymanoim/exchange_calendars |
| jugaad-py/jugaad-data, RuchiTanmay/nselib | 583 / 179 | Sep / May 2026 | Public domain / Apache | NSE data, TRI, VIX | **M**: code is fine, but NSE's ToS restricts the *data* (§5) | https://github.com/jugaad-py/jugaad-data |
| streamlit/streamlit | 46k | PyPI 1.64.0, Sep 2026 | Apache-2.0 | UI | H | https://github.com/streamlit/streamlit |

### 3b. Reference only, or avoid

| Repo | Why | Link |
|---|---|---|
| OpenSourceRisk/Engine (ORE) | Closest open "Aladdin-like" engine (XVA, VaR, SIMM). Too heavy; use as a methodology reference | https://github.com/OpenSourceRisk/Engine |
| ShrishDhuria/IFRS9_ECL | MIT Streamlit ECL engine with a SICR waterfall and Excel mirrors. Only 2 stars, so use it as a design checklist | https://github.com/ShrishDhuria/IFRS9_ECL |
| naenumtou/ifrs9 | Full IFRS 9 notebooks, **no licence**. Read only | https://github.com/naenumtou/ifrs9 |
| open-risk/openNPL | Borrow the loan-tape schema ideas (MIT) | https://github.com/open-risk/openNPL |
| FinancePy, backtrader, nsepython, fortitudo.tech, open-risk/portfolioAnalytics | **GPL**. Avoid if you might ever distribute Riskcore | see CSV |
| ghostfolio, QuantLib-Risks-Py | **AGPL** (network copyleft). UX reference only | https://github.com/ghostfolio/ghostfolio |
| vectorbt | Apache + **Commons Clause**: no selling a product built on it | https://github.com/polakowo/vectorbt |
| rateslib, mlfinlab | Non-commercial or proprietary | see CSV |
| ArcticDB, sdv Copulas | **BSL 1.1**: no free production or commercial use (ArcticDB) or field-of-use limits (Copulas) | https://github.com/man-group/ArcticDB |
| tf-quant-finance, quantopian/* originals, nsepy | Archived, stale or deprecated. Use the `-reloaded` forks or jugaad | see CSV |
| OpenBB | Now Apache-2.0 (LICENSE read). Agent 4 saw the repo owner reported as `openbq-org`, so **check the canonical org and PyPI publisher before installing**. Not needed for the MVP | https://github.com/OpenBB-finance/OpenBB |

---

## 4. Research paper library

Full table: [`csv/research_papers.csv`](csv/research_papers.csv) (90 entries: about 66 verified, 13 partially verified, 11 unverified). Summaries and how each applies to Riskcore are in [`agents/agent5.md`](agents/agent5.md).

### ★ Top 5 must-reads

1. ★ **Vasicek (2002), "The Distribution of Loan Portfolio Value"** with **Gordy (2003), "A Risk-Factor Model Foundation for Ratings-Based Bank Capital Rules"**. One closed-form formula gives the portfolio loss distribution, economic capital and stress (by shifting the systematic factor). It is also the Basel IRB function. https://www.bankofgreece.gr/MediaAttachments/Vasicek.pdf · https://doi.org/10.1016/S1042-9573(03)00040-8
2. ★ **Acerbi & Tasche (2002), "On the Coherence of Expected Shortfall"**, with **Artzner et al. (1999)**. The correct ES estimator for discrete historical scenarios, and why ES rather than VaR should be the headline metric. https://doi.org/10.1016/S0378-4266(02)00283-2 · https://doi.org/10.1111/1467-9965.00068
3. ★ **Christoffersen (1998), "Evaluating Interval Forecasts"**, with **Kupiec (1995)**. The standard VaR backtests (conditional and unconditional coverage). About 50 lines of Python. https://doi.org/10.2307/2527341 · https://doi.org/10.3905/jod.1995.407942
4. ★ **Gordy & Lütkebohmert (2013), "Granularity Adjustment for Regulatory Capital Assessment"**, with BCBS WP15. A data-light add-on for name concentration on lumpy NBFC books. https://www.researchgate.net/publication/275031591 · https://www.bis.org/publ/bcbs_wp15.pdf
5. ★ **Bellotti & Crook (2009), "Credit Scoring with Macroeconomic Variables Using Survival Analysis"**. Lifetime, forward-looking PD for ECL and credit stress. https://www.researchgate.net/publication/233706892

Runner-up for v1: López de Prado (2016) HRP plus Ledoit-Wolf (2004) shrinkage.

### Grouped reading list (key items)

| Topic | Papers (year) | Riskcore use |
|---|---|---|
| **VaR / ES / backtesting** | RiskMetrics Technical Document (1996); Mina & Xiao, Return to RiskMetrics (2001); Rockafellar & Uryasev (2000, 2002); Barone-Adesi et al. FHS (1999); Pritsker, Hidden Dangers of HS (2006); McNeil & Frey EVT-GARCH (2000); **Karmakar (2013), EVT on Indian indices**; Acerbi & Székely (2014); Du & Escanciano (2017); Fissler, Ziegel & Gneiting (2016); BCBS FRTB d457 (2019) | VaR engine (HS, EWMA, FHS), ES at 97.5%, backtest page, rationale for not using normal VaR |
| **Factor models** | Fama & French (1993, 2015); Carhart (1997); Rosenberg (1974); Barra USE4 Methodology Notes (2011); **Agarwalla, Jacob & Varma: Indian 4-factor data (IIMA, 2013) and Vikalpa (2017)** | Factor exposures from free IIMA Indian factor data (v1.5) |
| **Portfolio construction** | Markowitz (1952); Michaud (1989); Black & Litterman (1992); He & Litterman (1999); Idzorek (2004); Maillard, Roncalli & Teïletche (2010); López de Prado HRP (2016); Ledoit & Wolf (2004, 2020); DeMiguel et al. 1/N (2009) | Covariance shrinkage; risk contributions (Euler); why the optimiser is deferred |
| **Stress testing** | **Kupiec (1998), conditional stress**; Breuer et al. (2009), plausible worst case; Rebonato (2010); Glasserman, Kang & Kang (2015), reverse stress; Grundke & Pliszka (2018); BCBS d450 (2018); IMF (2012) | Scenario propagation: "Nifty −20%" moves every holding; reverse stress |
| **Credit risk / PD / LGD / EAD** | Merton (1974); CreditMetrics (1997); CreditRisk+ (1997); Gordy (2000); Altman Z (1968); Stepanova & Thomas (2002); Dirick et al. (2017); Lessmann et al. (2015); Loterman et al. (2012); Tong et al. LGD (2013) and EAD (2016); BCBS IRB note (2005) | v2 PD/LGD/EAD choices and realistic accuracy expectations |
| **Concentration** | BCBS WP15 (2006); Martin & Wilde (2002); Pykhtin (2004); Düllmann & Masschelein (2006); Cespedes et al. (2006); Bandyopadhyay, Indian cases (2010) | HHI, granularity adjustment, sector diversification factor |
| **IFRS 9 / ECL** (mostly *unverified* — the search allowance ran out) | Bellini, *IFRS 9 and CECL Credit Risk Modelling and Validation* (2019); BCBS d350 (2015); RBI ECL Discussion Paper (Jan 2023); Cohen & Edwards, BIS QR (2017); Abad & Suarez on procyclicality; Belkin et al. Z-factor (1998); Jarrow-Lando-Turnbull (1997) | Roll-rate Markov lifetime PD plus Z-factor macro overlay: the most practical NBFC approach |

---

## 5. Data source catalogue

Full table: [`csv/data_sources.csv`](csv/data_sources.csv) (83 sources). Only about 37 were confirmed live; **prices and licences marked `U` are unverified**. Details and the full ToS list are in [`agents/agent6.md`](agents/agent6.md).

| Source | Data type | Coverage | Cost | API? | License / terms | Link |
|---|---|---|---|---|---|---|
| **AMFI NAVAll.txt** | Latest NAV, all Indian MF schemes | India, daily | Free | File (de facto API) | No explicit open licence; widely reused | https://www.amfiindia.com/spages/NAVAll.txt |
| AMFI NAV history | Historical NAV (90-day windows) | India | Free | Unofficial endpoint | ⚠ A snippet says the old format ran "only till 30 Sep 2026", so expect breakage | https://www.amfiindia.com/net-asset-value/nav-download |
| **MFapi.in** | JSON NAV history, 10k+ schemes | India | Free | Yes, no key | Community project, no SLA | https://www.mfapi.in/ |
| **captn3m0/historical-mf-data** | Full AMFI NAV history (SQLite) | India | Free | Download | MIT (repo) | https://github.com/captn3m0/historical-mf-data |
| NSE bhavcopy (UDiFF) / All Reports | EOD equities, F&O, indices | India, 1994+ | Free | No official API | **ToS bans automated collection and redistribution** | https://www.nseindia.com/all-reports/ |
| Nifty Indices | Index price, **TRI**, PE/PB | India | Free download | Unofficial | Index IP; licence needed to redistribute | https://www.niftyindices.com/reports/historical-data |
| BSE bhavcopy | EOD equities | India | Free | No | Restricts commercial reuse (U) | https://www.bseindia.com/markets/equity/eqreports/equitydebcopy.aspx |
| Broker APIs: Kite Connect, Upstox, Angel SmartAPI, Dhan, Fyers | Live + historical candles, holdings | India | Free to ~₹2k/mo (U) | Yes | For the account holder only; **no redistribution of exchange data** | https://github.com/zerodha/pykiteconnect |
| yfinance | Global prices incl. `.NS`, FX | Global | Free | Unofficial | **"Personal use only"** (README) | https://github.com/ranaroussi/yfinance |
| EODHD, Tiingo, Twelve Data, Alpha Vantage, Finnhub, Polygon | Licensed market data | Global (EODHD/Twelve Data incl. NSE, U) | ~$20–80/mo (U) | Yes | Personal vs commercial tiers | see CSV |
| RBI DBIE / data.rbi.org.in | G-sec yields, T-bills, policy rates, NBFC aggregates | India | Free | Downloads / SDMX (U) | Attribution (U) | https://dbie.rbi.org.in/ |
| CCIL, FBIL, FIMMDA | Yield curves, MIBOR, G-sec valuations, FX reference rates | India | Free display / paid products | No | Benchmark IP (U) | https://www.fbil.org.in/ |
| **IIMA Indian Fama-French-Momentum** | Indian factor returns | India, ~1993+ | Free | CSV | Academic; cite, don't bundle | https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/ |
| Ken French Data Library, AQR datasets | Global factors | US/Dev/EM | Free | CSV (pandas-datareader) | Citation; AQR non-commercial (U) | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html |
| FRED, World Bank, IMF, OECD, data.gov.in, MOSPI | Macro | Global/India | Free | Yes | data.gov.in GODL and World Bank CC BY are the clearest (U) | https://fred.stlouisfed.org/docs/api/fred/ |
| IBJA, MCX, LBMA, World Gold Council | Gold prices (INR and USD) | India/global | Free display | No | LBMA needs a licence for commercial use (U) | https://ibjarates.com/ |
| Home Credit, Lending Club, Give Me Some Credit (Kaggle); German & Taiwan (UCI); Freddie/Fannie; Bondora | Loan-level credit data | US/EU/EM | Free | Download | Kaggle competition rules are often non-commercial; Freddie/Fannie forbid redistribution | see CSV |
| RBI Trend & Progress, FSR; CRIF MicroLend; CIBIL-SIDBI MSME Pulse; Indian rating-agency default studies | Indian sector NPA/PAR, transition matrices | India | Free PDFs | No | Cite only | see CSV |
| SDV / hand-written generator | **Synthetic NBFC loan tape** calibrated to the aggregates above | — | Free | Python | MIT (SDV core; Copulas is BSL) | https://github.com/sdv-dev/SDV |

**Recommended data posture.** Agents 4, 6 and 10 agree on this:
- **Hosted demo:** synthetic data + AMFI NAVs + user uploads (CSV/CAS) only.
- **Price fetching** (yfinance, broker API, or bhavcopy files the user downloaded) runs **locally on the user's machine** as opt-in adapters.
- **v2 demos:** synthetic loan tapes only.
- **Commercial version:** budget for a licensed feed.

---

## 6. Regulatory requirements → feature mapping

Full table: [`csv/regulatory_feature_map.csv`](csv/regulatory_feature_map.csv) (26 rows). Details and cautions are in [`agents/agent8.md`](agents/agent8.md).
**No regulator page could be opened.** Dates and thresholds come from search results and secondary sources (law firms, taxguru, Business Standard), so verify each before relying on it.

| Requirement | Source / date / status | Riskcore feature | Ver. |
|---|---|---|---|
| Six-level MF riskometer from holdings, monthly | SEBI circular 2020/197, 5 Oct 2020 → MF Master Circular 2024 | "Shadow" riskometer per fund + portfolio-weighted, **labelled as an estimate** | v1 |
| PRC matrix (duration class × credit-risk class) for debt funds | SEBI, 7 Jun 2021, effective 1 Dec 2021 | PRC position checker; duration/credit heat-map | v1 |
| Days to liquidate 25%/50% of small/mid-cap schemes | AMFI letter 28 Feb 2024; monthly disclosures | Liquidity stress engine. Default participation **10% of ADV** per Agent 10 (Agent 8 suggested 20%); verify | v1 |
| PMS performance vs APMI benchmarks | SEBI 2022/172, 16 Dec 2022 | Benchmark-relative risk/return report | v1 |
| Investment advice / research needs SEBI registration; finfluencer links restricted | IA Regs 2013 / RA Regs 2014, amended 16 Dec 2024; guidelines 8 Jan 2025 | **Analytics-only mode**: no buy/sell, no model portfolios, disclaimers, legal review | v1 |
| SMA-0/1/2 and NPA at 90 DPD, classified at day-end; upgrade only when all arrears are paid | RBI IRACP clarification, 12 Nov 2021 | Day-end DPD → SMA/NPA engine, borrower contagion, upgrade rule, **golden tests from RBI's worked example** | v2 |
| IRACP provisioning % by asset class and vintage | RBI NBFC prudential norms (consolidated 2025/26 directions) — **% unverified** | IRACP provisioning engine with a dated parameter table | v2 |
| Ind AS 109 for NBFCs with net worth ≥ ₹500 cr (FY19), listed or ₹250 cr+ (FY20) | MCA roadmap | Ind AS mode for qualifying NBFCs only; **others use IRACP** | v2 |
| Parallel IRACP; if Ind AS ECL < IRACP, the gap goes to an Impairment Reserve; comparison disclosure | RBI, 13 Mar 2020 | **Dual-book engine + Impairment Reserve + disclosure table** | v2 |
| Gold loans: LTV caps 85% / 80% / 75% for ≤₹2.5L / ₹2.5–5L / >₹5L; bullet loans measured on maturity amount, ≤12 months; no lending to buy gold | RBI Lending Against Gold & Silver Collateral Directions, 6 Jun 2025, amended 29 Sep 2025, comply by 1 Apr 2026 | **Gold LTV engine**: tier caps, maturity-LTV projection, daily MTM, price-shock slider, tenor and end-use checks | v2 |
| Large exposures for NBFC-UL: 20% of eligible capital (+5% Board, +5% infrastructure) | RBI, 19 Apr 2022 | Single-name / group exposure monitor | v2 |
| EWS / red-flagged accounts extended to NBFCs | RBI Fraud Risk Management MDs, 15 Jul 2024 | EWS rule library → watchlist (decision support only) | v2 (later) |
| PCA on CRAR, Tier 1, NNPA | RBI PCA for NBFCs, 14 Dec 2021 | PCA proximity dashboard | v2 (later) |
| DLG cap 5% | RBI DLG guidelines, 8 Jun 2023 → Digital Lending Directions 2025 | DLG pool tracker | v2 (later) |
| Bank ECL: 3 stages, floors, effective 1 Apr 2027, transition to 31 Mar 2031 | RBI Directions final 27 Apr 2026 (draft 7 Oct 2025) — **banks only, not NBFCs** | Optional floor-table preset | later |
| IFRS 9: SICR, >30 DPD and 90 DPD rebuttable presumptions, probability-weighted scenarios, POCI | IFRS 9 §5.5 / Ind AS 109 | Stage engine, scenario-weighted ECL | v2 |
| IRB ASRF at 99.9%; Pillar 2 concentration; large exposures 25% of Tier 1 | BCBS CRE31/d424, BCBS 128, BCBS 283 | Economic-capital proxy, HHI + granularity adjustment | later |
| ES at 97.5% replaces VaR 99% | BCBS FRTB d457 | ES 97.5% next to VaR | v1 |
| Stress-testing governance | BCBS d450 (2018) | Versioned scenario library with sources and owners | v1/v2 |

**Engineering rule from Agents 8 and 10:**
- Every threshold lives in a **versioned, dated, cited parameter table**.
- Every report carries an "as-of regulation version" stamp.
- RBI's own worked examples become unit tests.
- Agent 10 flags a **likely off-by-one ambiguity in SMA day-counting**. Use RBI's 12 Nov 2021 worked example as the golden test. Agent 10 recalls it as: due 31 Mar → SMA-1 on 30 Apr → SMA-2 on 30 May → NPA on 29 Jun. That is background knowledge, so verify it.

---

## 7. Aladdin: what's publicly known, and a version you could build

Details and evidence levels: [`agents/agent3.md`](agents/agent3.md).

### What's known
- **Origins:**
  - 1988, on a single Sun workstation.
  - Charles Hallac was the first architect, and Bennett Golub co-built the early CMO models.
  - Sold externally through BlackRock Solutions, which was in heavy demand during 2007–09.
  - The historical "Green Package" was a standalone bundle of risk reports.
- **Scale:**
  - About $11T on the platform in 2013 (The Economist, "The monolith and the markets"). Recent marketing says about $25T, from a low-reliability third-party source.
  - BlackRock's FY2025 10-K reports **$2.0B "technology services and subscription" revenue (+24%)**, of which Aladdin is the majority. Contract value grew 31% including Preqin, 16% without (search-level).
- **Milestones:**
  - eFront acquired for $1.3B (2019).
  - Azure partnership (Apr 2020).
  - Aladdin Data Cloud on Snowflake (Feb 2021, part of Aladdin Studio).
  - Aladdin Copilot (2024).
  - Preqin acquired for about $3.2B (closed Mar 2025).
- **Tech stack:**
  - Java back end, microservices, Kafka (from job ads, search-level).
  - An in-house BlackRock Messaging System with clients in Java, C++, Python, JS, Perl, C# and Julia.
  - Per-client instances on Azure.
  - Protobuf/AIP-style APIs (inferred).
  - Copilot runs on isolated Azure OpenAI with LangChain/LangGraph and a **federated plugin registry used by 50+ teams** (LangChain Interrupt 2025 talk).
- **Primary evidence: BlackRock's public GitHub (`aladdinsdk`, `aladdinsdk-plugin-builder`).**
  - A REST "Graph API" of about 60 domain APIs at `/api/{domain}/{subdomain}/{entity}/v1/`.
  - A **type-specific security master** under one `assetId`.
  - A **polymorphic compliance-rule model** (prohibition, concentration, VaR, scripted, trade, counterparty) with filter, group-by, warning threshold, severity and a DRAFT→APPROVED lifecycle.
  - **Violations computed against ORDER, TRADE and POSITION sources**, i.e. pre- and post-trade on the same rules.
  - Governed risk rules with overrides, approvals and portfolio subscriptions.
  - Separate ABOR/OBOR lots.
- **Design principles:**
  - One common data model.
  - Risk built in from the start, not added later.
  - Governed, auditable objects.
  - Uniform versioned APIs.
  - Open at the edges (Snowflake, Python SDK).
  - A "whole portfolio" view across public and private assets.
- **Criticisms:**
  - Systemic concentration and herding from shared models (The Economist, 2013).
  - Platform-power critique (Geoforum).
  - Azure migration cost.
  - Conflict of interest (unverified).

### A simplified version you could build (merged from Agents 3, 7 and 10)

```
 providers/  (plugins: synthetic | AMFI | CSV/CAS upload | yfinance* | broker API* | NSE bhavcopy*  — *local, opt-in)
     │  ingest + validate (pandera)  → data-health flags (stale / missing / unmapped)
     ▼
 data/raw/*.parquet ──► data/curated/*.parquet ◄──► riskcore.duckdb (SQL views)
     │                     one common schema: security_master(asset_id, class, type, ccy, sector, ISIN/AMFI code),
     │                     prices/fx/curves, holdings(as_of), scenarios.yaml, limits.yaml, params/*.yaml (dated, cited)
     ▼
 models/  (pure functions, no I/O)
   market: returns · VaR/ES (HS, EWMA, FHS) · risk contributions · liquidity (days-to-liquidate)
   stress: scenario library + conditional propagation (Kupiec 1998)
   limits: Aladdin-shaped rules (filter, group_by, warning, breach) evaluated on current AND what-if holdings
   credit (v2): DPD→SMA/NPA · IRACP · staging · ECL-lite · gold LTV · concentration
   validation: Kupiec / Christoffersen / traffic light · RBI golden examples
     ▼
 data/results/run_id=…/*.parquet  + runs table (inputs hash, git sha, parameter-table version)
     ▼
 ui/ Streamlit multipage  ·  Excel/PDF export that ties out to the screen  ·  (later) FastAPI + SDK
```

**Copy from Aladdin:**
- One schema that every view reads.
- A type-specific security master.
- One rule shape for limits, evaluated against both what-if and actual holdings.
- Governed, dated parameters.
- A `run_id` on every number.

**Don't copy:**
- Per-client instances, Kafka/messaging, microservices.
- The rule-approval workflow and ABOR lots.
- The LLM copilot.

All of these are enterprise patterns for problems a solo build doesn't have yet.

---

## 8. Recommended tech stack

Details, comparison tables and sources: [`agents/agent7.md`](agents/agent7.md). The table is adjusted for Agent 10's scope critique.

| Component | Stage 1 (now, $0) | Stage 2 (hosted pilot, ~$5–30/mo) | Stage 3 (serious) | Why |
|---|---|---|---|---|
| Core | Python 3.11+ package `riskcore`, pure functions | same | same + SDK | Your strength; JPMorgan's Athena shows Python scales as a risk language |
| DataFrames | pandas in models; Polars/DuckDB for loan-book roll-ups | same | same | Lowest switching cost |
| Storage | **Parquet** (raw / curated / results by run_id) + **DuckDB** file | + **PostgreSQL** (users, portfolios, runs, audit) | Lakehouse table format (DuckLake/Iceberg) | DuckDB is MIT and zero-ops, but **single-writer**, so the pipeline writes Parquet and the UI reads it. ArcticDB is BSL, so avoid it |
| Providers | Plugin interface (OpenBB-style) | + licensed feed | + more | Isolates fragile sources; enables "local-only" adapters |
| Scheduling | cron / GitHub Actions | Prefect | Dagster (asset lineage for audit) | Airflow is too heavy for one person. GitHub Actions cron is **silently disabled after 60 days of repo inactivity** |
| Caching | `st.cache_data` + persisted results (+ diskcache) | same | Redis/Valkey (Redis 8 is RSAL/SSPL/AGPL) | Streamlit's cache is per process and in memory |
| Compute | numpy | + numba for loan-level loops | JAX/Ray if needed | Data is megabytes, not terabytes |
| UI | **Streamlit** multipage + plotly | + `st.login()` (native OIDC) | Dash or React + FastAPI | Already built; auth is now native |
| Reports | Excel export (openpyxl) | + Evidence.dev (adds a Node toolchain) | same | Auditors live in Excel |
| API | — | FastAPI | FastAPI + SDK (Aladdin SDK pattern) | Only when a second consumer exists |
| Hosting | Streamlit Community Cloud (≤2.7 GB RAM, sleeps after 12 h idle) | Docker on Railway/Render/Fly | Containers / **on-prem at an NBFC** | Hugging Face Docker Spaces now need a paid plan; Fly.io has no free tier for new orgs since Oct 2024 |
| Testing | pytest + **Hypothesis** invariants (CVaR ≥ VaR; contributions sum to 1; ECL ≥ 0) + VaR backtests + RBI golden tests | + CI licence check (`pip-licenses`) | model inventory and change control | Credibility comes from validation |

**Distribution model for v2: local-first.** Offer a pip install plus a local Streamlit app with no telemetry. NBFCs will not upload borrower PII (DPDP Act) to a hobby SaaS.

---

## 9. Gap analysis: where Riskcore can be different or better

From Agent 10 ([`agents/agent10.md`](agents/agent10.md)), which cross-checked agents 1–9.

### Ranked differentiators
1. **India-correct data plumbing.** CAS import (casparser), AMFI NAV history, TRI benchmarks, INR conversion of US holdings, an explicit `return_basis` per asset, and a data-health page. Every DIY dashboard sampled gets this wrong.
2. **Backtested, explained risk.** VaR/ES with Kupiec, Christoffersen and a traffic light visible in the UI, plus a methodology page per metric. Almost no competitor shows whether its numbers hold up.
3. **An India scenario library with conditional propagation:**
   - 2013 taper tantrum (INR −20%)
   - 2016 demonetisation
   - 2018 IL&FS
   - March 2020 COVID
   - April 2020 Franklin Templeton debt wind-up
   - 2022 rate cycle
   - January 2023 Adani

   Each is stored as data with a narrative and a source.
4. **Liquidity risk for retail portfolios.** SEBI/AMFI-style days-to-liquidate next to VaR.
5. **The v2 wedge: gold-loan LTV MTM and price-shock stress, plus IRACP provisioning (and the Ind AS dual-book with Impairment Reserve) in one auditable run.** No vendor surfaced this.
6. **Auditability.** `run_id`, inputs hash, cited parameter-table version, and an Excel export that ties out to the screen.
7. **Local-first, permissive licence (Apache-2.0).** Suits privacy-minded retail users and PII-constrained NBFCs.
8. **"Shadow" regulatory views** (portfolio riskometer, PRC position), always labelled as estimates.

### Contradictions resolved

| Issue | Verdict |
|---|---|
| jugaad-data as the core price source (Agent 4) vs NSE ToS (Agent 6) | Agent 6 wins for anything published. Use jugaad only as an opt-in local adapter |
| "NBFCs already follow Ind AS 109" (Agents 2, 8) vs the MCA roadmap (Agent 8) | Most small NBFCs are **not** on Ind AS. v2 must start with IRACP |
| Domain-model-first architecture (Agent 3) vs pipeline-first (Agent 7) | Compatible. Take Agent 7's folders and run-ID rule plus Agent 3's security master and limit-rule shape. Defer the rest |
| OpenBB licence: AGPL (Agent 6) vs Apache-2.0 (Agents 4, 7) | Apache-2.0 now (LICENSE file read). Check the `openbq-org` owner anomaly |
| MSCI "India scenarios" (Agent 1) | Misattribution. Those events were Agent 1's suggestions |
| Liquidity participation rate: 20% (Agent 8) vs ~10% (Agent 10, from memory) | Default to 10%, label it, and verify against AMFI's format |

### Verify these first (ranked by impact)
1. Ind AS applicability for small NBFCs, and any 2026 IRACP amendment that touches ECL.
2. AMFI NAV-history format change (reportedly 30 Sep 2026). This is v1's main feed.
3. NSE terms-of-use wording and its "available for download" carve-out.
4. SEBI IA/RA amended rules and guidelines: what an analytics app may show.
5. SMA/NPA day-count and borrower contagion (RBI 12 Nov 2021).
6. Gold LTV tiers, maturity-LTV, valuation basis (RBI notification Id=12859 and its 29 Sep 2025 amendment).
7. IRACP provisioning percentages for NBFCs.
8. The 13 Mar 2020 Impairment Reserve circular, against the primary text.
9. AMFI liquidity-stress parameters.
10. Riskometer bands and PRC credit-risk thresholds (MF Master Circular, 27 Jun 2024).

### Bugs found in the current code (fix in week 1)
- **No FX conversion.** US holdings priced in USD are mixed with INR.
- **Fake zero returns.** `ffill()` across mismatched exchange holidays understates vol and correlation.
- **Silent drops.** Tickers with no data disappear without a warning.
- **Sharpe overstated.** It uses rf = 0 even though Indian T-bills yield about 6–7%.
- **VaR is basic.** 1-day only, no backtest, no ES at 97.5%.
- **Stress double-counts FX.** FX exposure is added on top of a beta that already contains FX, and there is no gold factor.
- **LIQUIDBEES shows ~0 price return.** It pays returns as units, a concrete total-return bug.

### Legal and ToS risks
| Risk | Severity | Action |
|---|---|---|
| **Employer IP / data** (you work on lending products) | **High** | Use no employer loan tapes, parameters, curves, vendor documents or code, even anonymised. Check your contract's IP-assignment and moonlighting clauses. Build on personal time and hardware, from public regulation, public papers and synthetic data. Consider written clearance |
| SEBI IA/RA rules | High for a public v1 | Descriptive analytics only. No recommendations, model portfolios or referral income. Legal opinion before monetising |
| NSE/BSE scraping and redistribution | High if hosted | No scraping in the hosted app. Opt-in local adapter with a ToS notice |
| Yahoo/yfinance | Medium | Prototype only. Keep the synthetic fallback |
| Kaggle / Freddie / Fannie datasets | Medium | Methods research only. Don't bundle them |
| Index / benchmark IP (Nifty TRI, FBIL, LBMA) | Medium | Fetch at runtime locally; don't redistribute |
| BlackRock trademark ("mini-Aladdin") | Low–medium | Say "inspired by institutional risk platforms" |
| Impersonating official labels | Medium | Always "Riskcore estimate" |
| DPDP Act / borrower PII | Medium | Local-first; synthetic data in demos |

### Scope cuts from the original plan
Defer:
- **The optimiser.** Crowded, prone to overfitting, and close to investment advice.
- Barra-style factor models, EVT/copulas.
- FastAPI, Prefect, Postgres, Docker, Evidence.dev.
- Aladdin-style rule lifecycles and lots.
- Survival/ML PD, scorecards, IRB, CECL, PCA, ICAAP, DLG and RFA queues.
- Bank ECL floors.
- Tax harvesting and option Greeks.

---

## 10. Proposed MVP and 6-week roadmap

This assumes about 10–12 hours a week (three evenings plus a weekend), about 65 hours in total. Weeks 1–4 build v1 and weeks 5–6 a thin v2 slice. Each week ends with green tests and a deployable demo.

### v1 — portfolio risk

| Must-have | Nice-to-have |
|---|---|
| Refactor into `providers/ models/ store/ ui/pages` | Shadow riskometer / PRC view (labelled estimate) |
| Holdings CSV template + **CAS import** (casparser, pinned PyMuPDF) | IIMA four-factor regression exposures |
| AMFI NAV provider (daily file + SQLite backfill) + yfinance (prototype) + synthetic; disk cache; data-health page | MF look-through (manual holdings upload) |
| INR conversion; `return_basis` flag; TRI benchmark | GARCH/FHS VaR (`arch`) |
| VaR/ES: historical + EWMA at 95/97.5/99%, 1–10 day horizon | Weekly-return covariance for cross-market portfolios |
| **VaR backtest page** (Kupiec, Christoffersen, traffic light, lagged VaR) | Debt view: factsheet duration/YTM/rating buckets |
| Risk contributions, correlation, drawdown, rolling vol; configurable risk-free rate | PDF report |
| **India scenario library (YAML)** + conditional propagation + gold and rates factors | Opt-in local NSE bhavcopy adapter |
| **Liquidity: days-to-liquidate X%** (ADV, default 10%) | — |
| YAML limit rules (single-name, sector, asset class) with breach table, applied to what-if too | — |
| Run store (Parquet + run_id + inputs hash) + Excel export | — |
| Disclaimers, methodology page, Apache-2.0 licence, README without "Aladdin" branding | — |

### v2 — NBFC loan book (first slice)

| Must-have | Nice-to-have |
|---|---|
| Loan-tape schema (openNPL ideas) + **pandera validator** (missing DPD, duplicate IDs, negative balances, date logic) | Ind AS 109 dual-book + Impairment Reserve |
| **Synthetic NBFC tape generator** (gold, MSME, vehicle, personal), seeded and calibrated to RBI/CRIF aggregates | Roll-rate Markov lifetime PD + three-scenario weighting |
| **DPD → SMA-0/1/2 → NPA engine**: borrower contagion, "all arrears cleared" upgrade, RBI golden tests | EWS rule library (~10 rules) → watchlist |
| **IRACP provisioning** (dated, cited parameter table) | Vintage curves, roll-rate matrix chart |
| ECL-lite: stage = f(DPD 30/90 + flags); ECL = PD × LGD × EAD by segment (user-supplied PD/LGD) | Granularity adjustment |
| **Gold LTV engine**: tier caps, bullet maturity-LTV, shock slider (−10/−20/−30%) → breach count, shortfall in ₹ | Rate-shock NII impact |
| Concentration: HHI and top-20 by borrower / sector / geography / product | — |
| Excel **auditor pack**: bucket and stage movement, provisions, parameter version | — |

### Six-week plan, starting from the current repo

| Week | Goal | Deliverables | Exit test |
|---|---|---|---|
| **1** | Foundations + bug fixes | Package restructure (`providers/base.py` Protocol; `data.py` → `providers/yfinance.py`, `providers/synthetic.py`); `pyproject.toml`; configurable risk-free rate; FX conversion; dropped-ticker warning; LICENSE; README de-branding; CI (ruff, pytest, licence check) | The 5 existing tests pass, plus new FX and dropped-ticker tests |
| **2** | India data + holdings import | AMFI provider (NAVAll + historical-mf-data backfill, defensive parser); CSV + CAS upload with self-made fixtures; security master; disk cache; data-health page; `return_basis` (fixes LIQUIDBEES) | MF + equity + US portfolio loads offline from fixtures |
| **3** | Credible risk numbers | `models/market/var.py` (HS, EWMA, horizons, ES 97.5%); `models/validation/var_backtest.py` (Kupiec, Christoffersen, traffic light); Hypothesis invariants; backtest page | Seeded synthetic backtest reproduces the expected exception counts |
| **4** | Stress + liquidity + limits + run store | Scenario YAML (6–8 cited India events) + conditional propagation; gold and rates factors; liquidity engine; limits YAML + breach table; Parquet run store + Excel export; methodology and disclaimer pages; **deploy v1 demo (synthetic + AMFI)** | Live demo; Excel ties out to the screen |
| **5** | v2 core: loan tape → DPD → IRACP | Loan schema + pandera; synthetic tape generator; DPD/SMA/NPA engine with contagion and upgrade rule; IRACP parameter table (marked "verify"); RBI golden tests | Golden RBI example passes; 100k-loan tape runs in under 10 s |
| **6** | v2 wedge | Gold LTV engine + shock slider; staging + ECL-lite; HHI/top-20; auditor Excel pack; Loan Book page; **show it to 3–5 NBFC risk or finance people (not colleagues at your employer)** | A −20% gold shock on the synthetic book shows breach count and ₹ shortfall; feedback captured |

**After week 6:**
- If NBFC interest is real: build the Ind AS dual-book + Impairment Reserve, roll-rate lifetime PD and EWS next.
- If not: go to v1.5 (FHS/GARCH, factor regression, MF look-through, debt view).
- In either case, keep working down the "verify first" list in §9 before each dependent feature ships.

---

## 11. Bibliography

- **Every URL from every agent is in [`csv/bibliography.csv`](csv/bibliography.csv).** It has 715 unique URLs, each with its domain and the agents that cited it.
- **Each agent file ends with its own bibliography** that separates pages actually opened from search-result-only links and unverified links, with dates and ⚠ flags on sources more than 3 years old:
  - [Agent 1 — commercial (investment)](agents/agent1.md)
  - [Agent 2 — commercial (credit)](agents/agent2.md)
  - [Agent 3 — Aladdin](agents/agent3.md)
  - [Agent 4 — open source](agents/agent4.md)
  - [Agent 5 — papers](agents/agent5.md)
  - [Agent 6 — data](agents/agent6.md)
  - [Agent 7 — tech stack](agents/agent7.md)
  - [Agent 8 — regulation](agents/agent8.md)
  - [Agent 9 — community](agents/agent9.md)
  - [Agent 10 — critique](agents/agent10.md)
- **Not covered at all** (blocked, or the search allowance ran out):
  - Reddit, Quant StackExchange, YouTube, LinkedIn and Wilmott.
  - MProfit, PortfolioPilot, Empower, Groww, Tijori and StockEdge.
  - Full text of every RBI, SEBI, BIS and IFRS document.

  A second research pass from an environment with open network access should start with these and with the §9 verification list.
