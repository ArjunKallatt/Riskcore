# Agent 1 – Commercial Platform Scout (Investment Risk)

Project: **Riskcore**, a free, Aladdin-inspired risk analytics tool (Python + Streamlit). v1 covers investment portfolio risk; v2 covers NBFC loan-book risk.
Research date: 2026-10-02.

---

## 0. How this was researched (read this first)

- **Page fetching was blocked.** Every `WebFetch` call (blackrock.com, msci.com, bloomberg.com, factset.com, simcorp.com) and every direct `curl` (portfoliovisualizer.com, wikipedia.org, smallcase.com, sharesight.com, kubera.com) failed. The egress proxy refused them with `EGRESS_BLOCKED` / `CONNECT 403`. The GitHub API was also refused for this session.
- **Only `WebSearch` worked.** It returns result titles, URLs and an AI-written summary of the matching pages. I could **not open and read any page in full**, so the "2 levels deep" rule could not be met.
- **The search budget ran out partway through.** The session-wide limit (200) was hit, so these were never searched: Aladdin Wealth detail, Bloomberg Terminal price, MProfit, PortfolioPilot, Morningstar Direct, Empower, Groww, Tijori.
- **Verification legend used below:**
  - **S** = the URL came back in a live search result on 2026-10-02 and the claim comes from the search engine's summary of it. The page itself was not opened. This is moderate confidence. The URL exists in the search index, but treat the exact wording and numbers as needing a click-through.
  - **S-3P** = same as S, but the claim comes from a third-party review or aggregator, not the vendor. Treat third-party prices as indicative only.
  - **BK** = from my background knowledge. Not verified this session.
  - **N** = not verified.
- **Source dates:** most search results showed no date. A date is given only when the URL or title shows one ("n/v" = not visible). ⚠ marks sources more than 3 years old (before Oct 2023).

---

## (a) Summary table

| Platform | Category | Key features (relevant to Riskcore) | Target users | Pricing | Link | Verified | Source date |
|---|---|---|---|---|---|---|---|
| BlackRock Aladdin (Aladdin Risk) | Enterprise investment OS + risk engine | Multi-asset risk and return view; positions and exposures; performance and attribution; scenario analysis ("thousands of scenarios daily", e.g. inflation, oil, EU recession); hundreds of risk metrics; customizable reports; compliance; public + private markets; APIs | Asset managers, asset owners, insurers, banks | Not public | https://www.blackrock.com/aladdin/platforms/products/aladdin-risk | S (page fetch blocked) | n/v |
| Aladdin Climate | Climate-risk analytics module | Climate scenarios and risk analytics | Institutional | Not public | https://www.blackrock.com/aladdin/platforms/products/aladdin-climate | S (title only) | n/v |
| MSCI RiskMetrics RiskManager | Enterprise market-risk system | VaR (parametric, historical, Monte Carlo); factor risk; stress tests (historical + hypothetical library, user-defined, predictive stress that propagates core-factor shocks); liquidity; counterparty risk | Hedge funds, asset managers, banks, asset owners | Not public | https://www.msci.com/data-and-analytics/risk-management-solutions/riskmetrics-riskmanager | S | n/v |
| MSCI BarraOne | Multi-asset factor risk + attribution | Barra Integrated Model (59 equity / 48 fixed-income markets per summary); long-horizon factor model; VaR; full-revaluation stress tests; public + private + derivatives; MAC performance attribution | Institutional risk managers and PMs | Not public | https://www.msci.com/data-and-analytics/portfolio-management/barra-one | S | n/v |
| MSCI Barra PortfolioManager | Equity factor analytics + optimization | Factor-based portfolio construction (title only) | Equity PMs | Not public | https://www.msci.com/data-and-analytics/portfolio-management/barra-portfolio-manager | S (title only) | n/v |
| Bloomberg PORT / PORT Enterprise | Terminal-based portfolio + risk analytics | Historical performance vs benchmark; attribution by sector, region or custom classification; factor risk models; tracking error; VaR; stress tests; intraday monitoring + portfolio news; ESG screen; AI commentary on return drivers (PORT Enterprise) | Terminal users: PMs, risk, analysts | Not public (needs Terminal) | https://data.bloomberglp.com/professional/sites/4/Portfolio_and_Risk_Analytics_Brochure4.pdf | S | n/v (brochure); AI launch press n/v |
| Bloomberg AIM | Buy-side OMS / front-to-back | IBOR; intraday positions; risk/P&L; **what-if analysis and rebalancing**; OEMS (30+ venues); coded compliance rules; ~15,000 users / 900+ firms (per summary) | Buy-side PMs, traders, compliance | Not public | https://professional.bloomberg.com/solutions/buy-side/trade-execution/ | S | WatersTech ranking 2025 |
| FactSet Portfolio Analytics / MAC Risk | Analytics + multi-asset risk | Multi-asset risk models; absolute and relative vol; VaR; tail loss; stress tests; factor exposures; risk decomposition; hosts third-party models (Axioma, Barra, Northfield) and **custom user models** | Asset managers, asset owners | Not public | https://www.factset.com/solutions/portfolio-analytics/risk-analytics | S | n/v |
| SimCorp Axioma (formerly Qontigo's Axioma) | Factor risk models + optimizer + analytics | Fundamental, statistical and macro factor models; short, medium and "Trading Horizon" (Jan 2026) versions; Worldwide Equity model with ML "non-linear residual factor" (May 2025); fund-allocation risk models (2024); Portfolio Optimizer; Portfolio Analytics | Quants, hedge funds, asset managers, asset owners | Not public | https://www.simcorp.com/solutions/strategic-solutions/axioma-solutions/axioma-portfolio-optimizer/axioma-portfolio-analytics | S | 2024, 2025, 2026 news URLs |
| SimCorp Dimension / SimCorp One | Front-to-back IMS | IBOR; PMS/OMS; risk; performance; compliance; accounting; client reporting; multi-asset; Azure cloud | Large asset managers, pensions, SWFs, insurers | Not public (Capterra listing) | https://www.simcorp.com/solutions/simcorp-one/risk-and-performance | S / S-3P | n/v |
| Charles River IMS (State Street Alpha) | Front-office IMS / OMS | PM, risk analytics, trading, post-trade; centralized compliance (what-if, pre-trade, intra-trade, post-trade, batch); "As-of" compliance; plug-ins for MSCI, FactSet and Axioma risk | Asset managers, wealth, insurers | Not public | https://www.crd.com/wp-content/uploads/2026/01/CRD_Charles-River-IMS.pdf | S | Jan 2026 (PDF path); MSCI datasheet Sep 2024; FactSet datasheet Mar 2023 ⚠ |
| SS&C Advent (APX, Geneva) | Portfolio accounting / PMS | APX: multi-asset, multi-currency accounting, dashboards, performance, composites, GIPS; Geneva: complex fund structures, derivatives and credit accounting; rebalancing / OMS integrations | RIAs and wealth managers (APX); hedge funds and fund admins (Geneva) | Not public | https://www.advent.com/resources/all-resources/brief-advent-portfolio-exchange/ | S | n/v; product update 1H2023 ⚠ (borderline) |
| Clearwater Analytics (+ Enfusion) | Cloud investment accounting, reporting, risk | Single-instance multi-tenant SaaS; accounting; reconciliation; regulatory reporting; performance; compliance; risk; Fund Analytics for private markets (Jun 2026); bought Enfusion for $1.5B (closed Apr 2025, per summary) | Insurers, asset managers, corporates, governments | Subscription (from 10-K summary); amount not public | https://www.sec.gov/Archives/edgar/data/1866368/000162828025021130/cwan-20241231x10k.pdf | S | FY2024 10-K; Jun 2026 press |
| Enfusion (now part of Clearwater) | Cloud PMS / OEMS / accounting | Real-time positions and P&L; embedded risk reporting; stress tests and scenarios; OEMS with 200+ brokers | Hedge funds, alternatives managers | Not public | https://www.enfusion.com/for-hedge-funds/ | S | n/v |
| Addepar | Wealth aggregation + reporting | Multi-custodian aggregation and reconciliation; alternatives analytics; custom reports; client portals; API; trading, drift monitoring and rebalancing; scenario modeling; $9T+ on platform, 1,400+ firms (Q1 2026, per summary) | Family offices, RIAs, private banks | Not public. Third-party estimates: ~$65k/yr (~$220M AUM) to ~$400k/yr (~$4.6B AUM) | https://www.capterra.com/p/275617/Addepar/ (3P) | S-3P | 2026 (review titles) |
| Murex MX.3 | Sell-side trading + enterprise risk | All VaR methods; stress; FRTB SA + IMA; XVA; SA-CCR; credit risk; initial margin; GPU compute; 150+ customers (per summary) | Banks, treasuries | Not public | https://www.murex.com/en/solutions/business-solutions/enterprise-risk-management | S | n/v; award pages 2019 ⚠ |
| Arcesium (Aquata) | Investment data platform / ops | Thousands of pre-built data models and connectors; ingestion, normalization, data quality, lineage, catalog; GenAI extraction from PDFs and emails (Dec 2025) | Hedge funds, private markets, asset managers, admins | Not public | https://www.arcesium.com/press-release/arcesium-launches-aquata-an-advanced-data-platform-purpose-built-for-the-investments-industry | S | 2023 launch (PRN); Dec 2025 AI |
| Qontigo (historical) | Index + analytics (now dissolved) | Axioma merged into SimCorp; STOXX/DAX moved to ISS STOXX (Deutsche Börse) | n/a | n/a | https://www.waterstechnology.com/trading-tech/7951439/deutsche-borse-to-merge-simcorp-and-axioma-excluding-qontigo | S | 2023 deal ⚠ (borderline) |
| Ortec Finance OPAL | Scenario-based wealth planning / Private ALM | Economic Scenario Generator (thousands of scenarios; 700+ asset classes; monthly updates); goal-based planning; risk profiling; monitoring; climate scenarios | Banks, wealth managers, pension providers | Not public | https://www.ortecfinance.com/en/insights/product/opal-wealth | S | n/v |
| Portfolio Visualizer | Retail/advisor web analytics | Backtesting; Monte Carlo; Fama-French / Carhart factor regression; efficient frontier / optimization; timing models | DIY investors, advisors | Free (≤15 assets, limited history); Basic ~$30/mo; Pro ~$55/mo, billed annually (3P) | https://www.findmymoat.com/tools/portfolio-visualizer (3P) | S-3P | 2026 (review title) |
| Kubera | Net-worth tracker | 20,000+ bank connections; crypto/DeFi; IRR; "Fast Forward" projections; document vault; estate "Life Beat"; nested portfolios | HNW individuals, family offices | ~$249/yr Essentials; ~$2,499/yr Black; white-label from ~$299/mo (3P) | https://thecfoclub.com/tools/kubera-software-review/ (3P) | S-3P | 2026 (review titles) |
| Sharesight | Portfolio + dividend + tax tracker | Dividend tracking; performance incl. dividends and FX; tax reports; alerts; sharing | Retail investors, accountants | Free (1 portfolio, 10 holdings); paid ~$7–$23.25/mo (3P, USD) | https://www.saasworthy.com/product/sharesight/pricing (3P) | S-3P | Sep 2026 (aggregator) |
| Riskfolio-Lib (OSS reference) | Open-source Python optimization library | CVXPY-based; 13+ risk measures (CVaR, EVaR, CDaR, Tail Gini, …); risk parity / risk budgeting incl. factor risk parity; HRP | Students, quants (Riskcore can build on it) | Free / open source | https://github.com/dcajasn/Riskfolio-Lib | S (GitHub API blocked) | docs v7.3 |
| **India** | | | | | | | |
| smallcase | Model-portfolio (basket) platform | Thematic baskets of stocks/ETFs; one-click buy through linked broker; rebalance alerts; free and fee-based baskets; Publisher for RAs/RIAs | Indian retail; SEBI RAs/RIAs as managers | Manager fee (flat or AUM-based) + transaction/SIP fees; details on smallcase pages | https://www.smallcase.com/learn/smallcase-fees-and-charges/ | S | 2026 (title) |
| INDmoney | Super-app: invest + track | Multi-broker sync; MF "portfolio scan"; US stocks analytics (XIRR, S&P 500 benchmark, INR/USD P&L, sector and market-cap split) | Indian retail | App free (revenue from broking/products; not detailed) | https://www.indmoney.com/blog/us-stocks/tracking-us-stocks-from-india-just-got-smarter-with-indmoney-analytics | S | n/v |
| Kuvera | Direct-MF platform + tracker | Commission-free direct MFs; import external holdings; family accounts; XIRR and allocation; **LTCG tax-harvesting** (₹1.25 lakh exemption); goals | Indian retail | Free direct-MF investing | https://kuvera.in/blog/tax-harvesting-in-mutual-funds-how-it-works-and-why-it-matters/ | S | n/v |
| Value Research | MF/stock research + tracker | Free Portfolio Manager; fund ratings (Return Score − Risk Score → stars); Fund Advisor; Stock Advisor | Indian retail, advisors | Fund Advisor from ₹490/mo or ₹4,900/yr; Stock Advisor ₹9,990+GST/yr | https://www.valueresearchonline.com/premium/subscribe/ | S | n/v |
| Morningstar India – Instant X-Ray | MF portfolio X-ray | ≤10 funds; asset allocation; geography; sector vs benchmark; style box; top-10 underlying holdings; **holding overlap**; PDF export | Indian MF investors | Free (but a Bogleheads thread says the US free Instant X-Ray was withdrawn; India status unverified) | https://www.morningstar.in/posts/64689/get-instant-x-ray-fund-holdings.aspx | S | n/v (old article, likely ⚠) |
| Tickertape (Smallcase group) | Screener + portfolio analysis | Stock/MF screeners (60+ filters); linking for 16+ brokers; diversification score; red-flag assets; overlap; forecasts | Indian retail | Pro ₹399/1 mo, ₹899/3 mo, ₹2,999/12 mo | https://www.tickertape.in/pricing | S | n/v |
| Screener.in | Fundamental screener | Custom query language; **custom ratios** usable in screens, columns and peers; ~10 yrs of fundamentals; result alerts; Excel export | Indian fundamental investors | Free; Premium ~₹4,999/yr (3P) | https://www.screener.in/features/ | S / S-3P | n/v |
| Zerodha Console | Broker back-office analytics | Free; P&L tracked through corporate actions; P&L calendar heatmap; sector breakdown; trade tagging (journal); tax P&L (STCG/LTCG, grandfathering, pre/post 23-Jul-2024 split); tax-loss harvesting report | Zerodha clients | Free | https://zerodha.com/products/console | S | ≥Jul 2024 (from content) |
| Sensibull | Options analytics | Strategy builder; payoff charts; max profit/loss; breakevens; probability of profit; net Greeks; P&L vs time; margin; virtual trading | Indian F&O traders | Free tier; Pro ~₹800/mo (3P); Pro free for Zerodha users (3P) | https://sensibull.com/ | S / S-3P | 2026 (reviews) |
| Investwell Mint | MFD/RIA back-office SaaS | Portfolio review; capital gains; transactions via BSE/NSE/MFU; brokerage reconciliation; CRM; SIP mining; **rebalancing**; **risk profiling** | MF distributors, RIAs | AUM-based, from ₹25,000/yr (≤₹25 Cr AUM); all features in one plan | https://investwellonline.com/pricing/ | S | n/v |
| REDVision Wealth Elite | White-label MFD SaaS | Client onboarding (Video KYC); multi-asset reports; rebalancing; Goal GPS; risk profiling; calculators; P&L and capital-gain reports | MF distributors / IFAs | Not public | https://www.redvisiontechnologies.com/wealth-elite.php | S | 2026 blog |
| CRISIL (Intelligence / GR&RS) | Ratings-group data + risk services | Fund Analyser (6,500+ schemes); Bond Valuer (AMC standard); PF Analytics; outsourced portfolio-risk services (attribution, multi-factor risk, VaR, sensitivities) | AMCs, insurers, pension funds, global AMs | Not public | https://www.crisil.com/en/home/our-businesses/global-research-and-risk-solutions/our-offerings/quantitative-services/portfolio-risk-management.html | S | n/v |
| ICRA Analytics (MFI Explorer / MFI360) | MF research database | MFI Explorer (desktop, since 2000; 9 of top 10 AMCs per summary); MFI360 cloud; MF Portfolio Tracker for distributors | AMCs, treasuries, distributors | Not public | https://www.icraanalytics.com/mutual-fund-solutions | S | n/v |
| ACE Equity Nxt (Accord Fintech) | Indian corporate financial database | 40,000+ companies; ~1,750 fields; 10 industry formats (incl. banking, NBFC); Excel add-in; query builder; ACE Reports portfolio app | Institutions, researchers, academia | Not public | https://www.accordfintech.com/ace-equity-nxt | S | n/v |
| Capitaline (Capital Market Publishers) | Indian corporate financial database | 35,000–55,000+ listed and unlisted companies (figures differ by source); ~740 fields; 9 formats; NAV/MF, TP, commodity, news modules | Institutions, academia | Not public (CFA Society India member-offer PDF exists, 2021 ⚠) | http://software.capitaline.com/aboutus.asp | S | n/v |

---

## (b) Notes per platform and "features worth copying"

### Global enterprise

**BlackRock Aladdin (Aladdin Risk)**
- What it is: BlackRock's analytics engine. It gives one consistent view of risk and return across asset classes, covering positions, exposures, performance attribution, risk, scenarios and compliance. It is embedded in a wider front-to-back OS.
- Worth copying:
  1. **A named scenario library written as plain-English questions** ("What if oil +30%?", "EU recession", "inflation shock"). Each one maps to factor shocks.
  2. **One "whole-portfolio" view** where every metric reads from the same positions and data model. This is how Riskcore's Streamlit pages should share state.
  3. **Many metrics with a user-picked report builder.** Let users pin metrics to a custom dashboard.
  4. **API-first.** Expose the Python core as a library and keep the UI separate.

**MSCI RiskMetrics RiskManager**
- Worth copying:
  1. **All three VaR methods side by side** (parametric, historical, Monte Carlo), with CVaR, so users can see how much the model choice matters.
  2. **A stress-test library with historical events** (2008 GFC, 2020 COVID, 2013 taper tantrum; India-specific: 2016 demonetisation, 2018 IL&FS, 2020 March crash) **plus user-defined shocks**.
  3. **"Predictive" stress:** shock one core factor (e.g. Nifty −20%) and spread it to every holding through betas or factor regressions. This is cheap to build and very useful.
  4. **A liquidity view:** days-to-liquidate from ADV. This also matters for Indian small-caps.

**MSCI BarraOne / Barra PortfolioManager**
- Worth copying:
  1. **Risk decomposition into factor and specific risk**, with marginal and percentage contribution to risk by holding and by factor.
  2. **Performance attribution in the same factor framework as risk**, so the language stays consistent.
  3. **Full-revaluation stress for bonds** (use duration and convexity as a simple proxy in v1).
- Note: the Barra USE4 methodology PDF found (top1000funds.com, Aug 2011 ⚠) is old but still a good public reference for factor-model design.

**Bloomberg PORT / AIM**
- Worth copying:
  1. **Benchmark-relative analytics everywhere**: tracking error, active weights, active risk.
  2. **Attribution by any grouping** (sector, region, market cap, custom tags).
  3. **AI commentary on return drivers.** Riskcore could produce a template-based or LLM "what moved my portfolio this week" summary.
  4. From AIM: **what-if trade simulation before rebalancing**, showing the pre/post change in risk, plus **rule-based compliance checks** (e.g. "no single stock > 10%", "sector cap 25%"). These map directly to Riskcore's what-if rebalancing feature.

**FactSet Portfolio Analytics / MAC Risk**
- Worth copying:
  1. **Model-agnostic design.** FactSet hosts Barra, Axioma, Northfield and *client custom* models. Riskcore should use a pluggable `RiskModel` interface: historical covariance, EWMA, statistical PCA, and a Fama-French-style fundamental model.
  2. **Show the standard metric set together**: absolute and relative volatility, VaR, tail loss (CVaR), stress results and factor exposures.

**SimCorp Axioma (ex-Qontigo)**
- Worth copying:
  1. **Several horizons of the same model** (short, medium, trading). In Riskcore this is just an EWMA half-life selector.
  2. **Statistical (PCA) and macro factor models alongside fundamental ones.**
  3. **An optimizer tied to the risk model** (min-variance, risk-parity and max-Sharpe with constraints). Riskfolio-Lib can supply this.
  4. **Fund-allocation risk models.** These treat MFs or ETFs as exposures to look through, which is very relevant for Indian MF investors.

**SimCorp Dimension / One; Charles River IMS (State Street Alpha); SS&C Advent; Clearwater; Enfusion; Arcesium**
- These are mainly front-to-back operations and accounting platforms (IBOR, OMS, accounting, compliance, data). They matter less to a solo-dev risk tool.
- Worth copying:
  1. **An IBOR-style single source of truth.** Keep one canonical holdings and transactions table, then derive positions as of any date.
  2. **Pre-trade and post-trade compliance rules engine** (CRD): a small YAML rules file checked on what-if trades.
  3. **GIPS-style performance**: TWR vs MWR/XIRR, as in APX.
  4. **Data-quality checks and lineage** (Arcesium Aquata): flag stale prices, missing NAVs and unmapped tickers on a "data health" page.
  5. **Private-markets / fund analytics** (Clearwater, Jun 2026): later.

**Addepar**
- Worth copying:
  1. **Multi-custodian aggregation**: import CAS (CAMS/KFintech), broker CSVs and manual assets into one view.
  2. **Drift monitoring against a target allocation**, with rebalancing suggestions.
  3. **Household / entity grouping**: family members as sub-portfolios.

**Murex MX.3**
- Sell-side. Not relevant to v1.
- For v2 (NBFC): look at its **credit-risk and regulatory-suite approach** of running regulatory calculations (FRTB/SA-CCR) next to internal risk in one engine. The Riskcore equivalent is Ind AS 109 ECL alongside internal PD/LGD stress.

**Ortec Finance OPAL**
- Worth copying:
  1. **An economic scenario generator** that drives forward Monte Carlo, linked to **goals** ("probability of reaching ₹X by 2040").
  2. **A risk-profiling questionnaire mapped to a risk budget** (vol/VaR limit). This is also what Indian MFD tools do.

### Retail / prosumer global

**Portfolio Visualizer** — the closest thing to a feature benchmark for a free Riskcore.
- Worth copying:
  1. Backtesting with benchmark.
  2. Monte Carlo (historical bootstrap + parametric), with survival / withdrawal analysis.
  3. **Factor regression** (Fama-French / Carhart). For India, use IIM-A's Indian Fama-French factor data (BK, verify licence and availability).
  4. Efficient frontier.
  5. Rolling returns and rolling correlations.
- Its free tier caps at 15 assets. **Riskcore being free with no asset cap is a clear differentiator.**

**Kubera / Sharesight**
- Worth copying:
  1. **Dividend-inclusive, FX-aware returns** (Sharesight). This matters for Indian investors with US stocks.
  2. **Tax reports.**
  3. **"Fast Forward" projections** (Kubera).
  4. **Shareable read-only portfolio links.**

**Riskfolio-Lib**
- Not a competitor. It is a **build-on dependency**: CVaR, CDaR, risk-parity and HRP optimizers are ready-made.
- Licence: BSD-3 per background knowledge; unverified this session.

### India

**smallcase / Tickertape**
- Worth copying:
  1. **Diversification score** and **red-flag assets** (Tickertape).
  2. **Holding overlap across MFs.**
  3. **Basket / model-portfolio rebalancing to target weights** (smallcase).
- A free Riskcore could add an "overlap + concentration + red-flags" health check.

**INDmoney / Kuvera / Value Research / Morningstar India X-Ray**
- Worth copying:
  1. **CAS / multi-broker import.**
  2. **XIRR in both INR and USD.**
  3. **LTCG tax-harvesting helper** (₹1.25 lakh exemption, per Kuvera's page).
  4. **MF look-through X-Ray**: asset allocation, sector vs benchmark, style box, top underlying holdings, overlap.
  5. **Risk grade relative to category** (Value Research's return score minus risk score).
- The availability of Morningstar's free Instant X-Ray is uncertain (a Bogleheads thread says the US one was withdrawn). A free look-through X-Ray could fill that gap in India.

**Zerodha Console / Sensibull**
- Worth copying:
  1. **P&L calendar heatmap.**
  2. **Trade tagging / journal.**
  3. **Tax-loss harvesting report.**
  4. Correct corporate-action handling.
  5. **Payoff and Greeks visualization for option positions** (Sensibull). Useful if Riskcore later adds F&O hedging what-ifs: net delta, vega and theta of the portfolio.

**Investwell / REDVision Wealth Elite**
- These are back-office tools for MF distributors.
- Worth copying:
  1. **Risk-profiling questionnaire → model allocation → rebalancing suggestion.**
  2. **Goal mapping** (Goal GPS).
  3. **Client-ready PDF reports.**
- Distributors are a possible future user segment for a free risk add-on.

**CRISIL / ICRA Analytics / ACE Equity / Capitaline**
- These are institutional Indian data vendors with no public pricing.
- Useful to Riskcore as:
  1. **A conceptual reference for Indian fixed-income valuation** (CRISIL Bond Valuer is the AMC standard).
  2. **Standardized NBFC and bank financial formats** (ACE and Capitaline both have banking and NBFC templates). These are relevant to v2 counterparty / early-warning features.
- CRISIL's outsourced portfolio-risk menu (attribution, multi-factor risk, sensitivities, VaR, alpha/beta) is a good **checklist of what "institutional-grade" means**.

### Cross-cutting "copy list" for Riskcore v1 (prioritized)
1. Pluggable risk models (sample cov / EWMA / PCA / factor regression) — FactSet, Axioma
2. VaR/CVaR via three methods side by side — RiskManager
3. Historical + hypothetical stress library with India events, plus factor-propagated shocks — RiskManager, Aladdin
4. Risk decomposition (MCTR, % contribution by holding and factor) — Barra
5. What-if rebalance with pre/post risk diff and rule-based limit checks — Bloomberg AIM, CRD
6. MF look-through X-Ray + overlap + diversification score — Morningstar, Tickertape
7. Benchmark-relative metrics (TE, active weights, beta to Nifty/S&P) — PORT
8. Backtest + Monte Carlo + factor regression — Portfolio Visualizer
9. Data-health page — Arcesium
10. INR/USD XIRR, dividend-inclusive returns, tax-harvest helper — INDmoney, Sharesight, Kuvera, Console

---

## (c) Bibliography (every URL used; all came back in live WebSearch results on 2026-10-02; none could be opened directly)

**Aladdin**
- https://www.blackrock.com/aladdin/platforms/products/aladdin-risk
- https://www.blackrock.com/aladdin/discover/blog/automate-risk-management-workflows
- https://www.blackrock.com/aladdin/platforms/products/aladdin-climate
- https://www.blackrock.com/aladdin/benefits/risk-managers
- https://www.centralbanking.com/awards/7941401/risk-management-technology-blackrocks-aladdin-risk
- https://www.limina.com/blackrock-aladdin

**MSCI**
- https://www.msci.com/data-and-analytics/risk-management-solutions/riskmetrics-riskmanager
- https://www.msci.com/downloads/web/msci-com/our-solutions-/analytics/managed-solutions/RiskMetrics_RiskManager.pdf
- https://www.msci.com/resources/research/technical_documentation/RMGuide.pdf (⚠ old RiskMetrics technical guide)
- https://www.msci.com/documents/10199/248121/RiskMetrics_Risk_Reporting_for_Individual_Investor_Portfolios.pdf (⚠ 2012)
- https://www.msci.com/data-and-analytics/portfolio-management/barra-one
- https://www.msci.com/data-and-analytics/portfolio-management/barra-portfolio-manager
- https://www.msci.com/documents/1296102/8335426/MSCI+MAC+Performance+Attribution+Factsheet.pdf
- https://www.top1000funds.com/wp-content/uploads/2011/09/USE4_Methodology_Notes_August_2011.pdf (⚠ 2011)

**Bloomberg**
- https://data.bloomberglp.com/professional/sites/4/Portfolio_and_Risk_Analytics_Brochure4.pdf
- https://www.bloomberg.com/company/press/bloomberg-advances-portfolio-analytics-with-launch-of-ai-portfolio-commentary-in-port-enterprise
- https://www.waterstechnology.com/trading-tech/7952749/bloomberg-integrates-ai-summaries-into-port
- https://professional.bloomberg.com/solutions/buy-side/trade-execution/
- https://www.waterstechnology.com/awards-rankings/7952605/waters-rankings-2025-best-buy-side-order-management-system-oms-provider%E2%80%94bloomberg

**FactSet**
- https://www.factset.com/solutions/portfolio-analytics/risk-analytics
- https://www.factset.com/solutions/portfolio-analytics
- https://investor.factset.com/news-releases/news-release-details/factset-expands-multi-asset-class-analytics-performance-and-risk

**SimCorp / Axioma / Qontigo**
- https://www.simcorp.com/solutions/strategic-solutions/axioma-solutions/axioma-portfolio-optimizer/axioma-portfolio-analytics
- https://www.simcorp.com/solutions/simcorp-one/risk-and-performance
- https://www.simcorp.com/about-us/news/2025/simcorp-launches-improved-axioma-worldwide-equity-factor-risk-model
- https://www.simcorp.com/about-us/news/2024/SimCorp-launches-Axioma-fund-allocation-risk-models
- https://www.simcorp.com/about-us/news/2026/simcorp-launches-risk-model-to-support-short-horizon-trading
- https://www.capterra.com/p/13760/SimCorp-Dimension/
- https://www.waterstechnology.com/trading-tech/7951439/deutsche-borse-to-merge-simcorp-and-axioma-excluding-qontigo
- https://www.deutsche-boerse.com/dbg-en/media/news-stories/press-releases/DEUTSCHE-B-RSE-AG-ANNOUNCES-RECOMMENDED-ALL-CASH-TAKEOVER-OFFER-FOR-SIMCORP-A-S-INTENDS-TO-COMBINE-QONTIGO-AND-ISS-AND-CREATE-NEW-INVESTMENT-MANAGEMENT-SOLUTIONS-SEGMENT-3516210 (2023)

**Charles River / State Street**
- https://www.crd.com/wp-content/uploads/2026/01/CRD_Charles-River-IMS.pdf
- https://www.crd.com/wp-content/uploads/2025/12/CRD_Charles-River-PM.pdf
- https://www.crd.com/wp-content/uploads/2024/09/CRD-MSCI_Datasheet.pdf
- https://www.crd.com/wp-content/uploads/2023/03/FactSet-CRD-Integration-Datasheet.pdf (⚠ Mar 2023)
- https://www.crd.com/wp-content/uploads/2023/04/CRD_As-Of-Compliance.pdf

**SS&C Advent**
- https://www.advent.com/resources/all-resources/brief-advent-portfolio-exchange/
- https://www.prnewswire.com/news-releases/ssc-announces-1h2023-ssc-advent-product-updates-301831875.html (2023)
- https://www.limina.com/advent

**Clearwater / Enfusion**
- https://www.sec.gov/Archives/edgar/data/1866368/000162828025021130/cwan-20241231x10k.pdf
- https://www.businesswire.com/news/home/20260617631534/en/Clearwater-Analytics-Launches-Fund-Analytics-Bringing-Verified-Intelligence-to-Private-Markets
- https://en.wikipedia.org/wiki/Clearwater_Analytics
- https://www.enfusion.com/for-hedge-funds/
- https://www.limina.com/enfusion
- https://hedgenordic.com/2023/12/enfusion-platform-an-integrated-front-middle-and-back-office-experience/

**Addepar**
- https://www.capterra.com/p/275617/Addepar/
- https://thecfoclub.com/tools/addepar-review/
- https://andsimple.co/companies/addepar/

**Murex**
- https://www.murex.com/en/solutions/business-solutions/enterprise-risk-management
- https://www.murex.com/en/insights/brochure/mx3-enterprise-risk-and-regulatory-suite
- https://www.murex.com/en/insights/article/banorte-completes-strategic-frtb-project-murex-mx3-platform

**Arcesium**
- https://www.arcesium.com/press-release/arcesium-launches-aquata-an-advanced-data-platform-purpose-built-for-the-investments-industry
- https://www.alternativeswatch.com/2025/12/15/arcesium-aquata-launch-new-ai-features/

**Ortec Finance**
- https://www.ortecfinance.com/en/insights/product/opal-wealth
- https://www.thewealthmosaic.com/vendors/ortec-finance/opal/
- https://www.risk.net/awards/7962575/buy-side-alm-product-of-the-year-ortec-finance

**Retail global**
- https://www.findmymoat.com/tools/portfolio-visualizer
- https://robberger.com/tools/portfolio-visualizer/
- https://thecfoclub.com/tools/kubera-software-review/
- https://jeangalea.com/kubera-review/
- https://www.saasworthy.com/product/sharesight/pricing
- https://github.com/dcajasn/Riskfolio-Lib
- https://riskfolio-lib.readthedocs.io/en/latest/index.html

**India**
- https://www.smallcase.com/learn/smallcase-fees-and-charges/
- https://www.smallcase.com/learn/how-does-smallcase-subscription-work/
- https://publisher.smallcase.com/
- https://www.indmoney.com/blog/us-stocks/tracking-us-stocks-from-india-just-got-smarter-with-indmoney-analytics
- https://www.indmoney.com/features/mutual-fund-portfolio-scan
- https://kuvera.in/blog/tax-harvesting-in-mutual-funds-how-it-works-and-why-it-matters/
- https://en.wikipedia.org/wiki/Kuvera.in
- https://www.valueresearchonline.com/premium/subscribe/
- https://www.valueresearchonline.com/methodologies/
- https://www.morningstar.in/posts/64689/get-instant-x-ray-fund-holdings.aspx
- https://www.bogleheads.org/forum/viewtopic.php?t=469099
- https://www.tickertape.in/pricing
- https://www.screener.in/features/
- https://www.strike.money/reviews/screener-in
- https://zerodha.com/products/console
- https://zerodha.com/z-connect/updates/tax-filing-simplified-with-zerodha-consoles-tax-reports
- https://sensibull.com/
- https://www.strike.money/reviews/sensibull
- https://investwellonline.com/pricing/
- https://investwellonline.com/investwell-mint/
- https://www.redvisiontechnologies.com/wealth-elite.php
- https://www.crisil.com/en/home/our-businesses/global-research-and-risk-solutions/our-offerings/quantitative-services/portfolio-risk-management.html
- https://www.crisil.com/en/home/our-businesses/crisil-intelligence/india-research/capital-market/mutual-fund-research.html
- https://www.icraanalytics.com/mutual-fund-solutions
- https://www.accordfintech.com/ace-equity-nxt
- https://mdi.ac.in/elibrary/User_Guide/Ace_Equity_User_Guide.pdf
- http://software.capitaline.com/aboutus.asp
- https://cfasocietyindia.org/wp-content/uploads/2021/07/Capitaline_offer-doc.pdf (⚠ 2021)

**Not covered (search budget exhausted):** MProfit, PortfolioPilot, Empower, Morningstar Direct pricing, Bloomberg Terminal price, Aladdin Wealth detail, Groww, Tijori, StockEdge. Recommend a follow-up pass with page fetching enabled.
