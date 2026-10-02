# Mini-Aladdin Risk Analytics Platform — Research Director Report

**Research date:** 2 October 2026  
**Scope:** investment portfolio risk (v1) + lending/loan-book risk (v2)  
**Approach:** ten specialist research tracks, followed by de-duplication, source cross-checking, and product/architecture synthesis.

> **Verification note.** This report is deliberately conservative. Claims are linked to primary/first-party sources where a current page was retrievable. Where a vendor/repository was not sufficiently verified during this pass, it is explicitly marked **Follow-up verification** rather than filled with guessed metadata. Fast-moving regulatory and software facts are dated. Pricing is reported only when public; otherwise “not publicly disclosed / contact sales” is used.

## 1. Executive summary

The market already has highly mature “Aladdin-like” capabilities, but the important lesson is architectural rather than numerical. BlackRock describes Aladdin as a platform built around a common data language, common risk/return views, portfolio-wide public/private asset coverage, APIs, and a shared workflow layer. Its public materials also show an API-first cloud platform, a governed data cloud, scenario/stress workflows, and a broad ecosystem rather than one monolithic risk formula. SimCorp Axioma and Murex describe a similar pattern: common portfolio/instrument data, multi-asset risk engines, stress/what-if analysis, portfolio construction, limits, reporting, and scalable workflow/integration. Sources: [BlackRock Aladdin](https://www.blackrock.com/aladdin), [Aladdin Studio](https://www.blackrock.com/aladdin/products/aladdin-studio), [Axioma Risk](https://www.simcorp.com/products/axioma/axioma-risk), [Murex Investment Management](https://www.murex.com/en/investment-management).

For a solo/open-source-style build, reproducing the whole enterprise surface area would be the wrong target. The practical opportunity is a transparent **risk operating system for smaller portfolios and smaller financial institutions**: one normalized data model; pluggable data adapters; a versioned risk engine; explainable calculations; a scenario registry; model/data lineage; and a Streamlit cockpit. The differentiation is not “we calculate VaR,” because that is commodity. It is **how quickly a user can ingest messy real-world Indian portfolio or loan data, understand where risk comes from, run controlled what-if scenarios, and reproduce every number later**.

For v1, the strongest open-source building blocks are QuantLib for instrument/fixed-income analytics, Riskfolio-Lib and PyPortfolioOpt for portfolio construction/risk optimization, skfolio for modern portfolio modelling, OpenBB as a research/data-integration layer, and DuckDB/Parquet/PostgreSQL as the storage foundation. A key licensing caveat is vectorbt: its repository contains a Commons Clause restriction, so its license needs careful review before making it a core dependency in something intended for commercial distribution. Sources: [QuantLib](https://github.com/lballabio/QuantLib), [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib), [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt), [skfolio](https://github.com/skfolio/skfolio), [OpenBB](https://github.com/OpenBB-finance/OpenBB), [vectorbt license](https://github.com/polakowo/vectorbt/blob/main/LICENSE.txt).

For v2, the larger gap is not another generic PD model. Commercial lending risk platforms already cover credit analytics, portfolio monitoring, stress testing, and IFRS 9-style expected-loss workflows. Oracle’s public documentation, for example, shows multi-scenario economic assumptions plus PD/LGD/CCF term structures and rule-driven provision workflows. The opportunity is a **transparent, deployable loan-book risk lab for small/mid NBFCs and banks**, especially around messy loan-tape ingestion, concentration views, collateral-aware stress, model monitoring, ECL explainability, and audit/reconciliation. Sources: [Oracle IFRS 9 ECL rules](https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/ifrs9-acct-guide/), [S&P Credit Analytics](https://www.spglobal.com/market-intelligence/en/solutions/credit-analytics), [Experian credit risk modelling](https://www.experian.com/decision-analytics/credit-risk-modelling.html), [Finastra Loan IQ](https://www.finastra.com/lending/loan-iq).

Current regulation reinforces the need for versioned rules rather than hard-coded assumptions. In 2026 RBI published amendments to concentration-risk directions, provisioning/income-recognition directions, and other NBFC rules; SEBI’s March 2026 mutual-fund master circular includes stress-testing requirements for many debt funds. The product therefore needs a **regulatory/rule registry** with effective dates, entity applicability, source citation, and calculation version. Sources: [RBI notifications](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=), [SEBI Master Circular for Mutual Funds](https://www.sebi.gov.in/legal/master-circulars/mar-2026/master-circular-for-mutual-funds_100208.html).

### Bottom-line product thesis

Build **“Aladdin for the analyst, not Aladdin for the enterprise”**:

1. **Common data model** first: instrument → portfolio → position → exposure → scenario → result.
2. **Deterministic risk engine** second: every metric has methodology, inputs, timestamp, and version.
3. **Scenario engine** third: shocked curves, equity moves, FX moves, spreads, sector shocks, collateral haircuts, macro paths.
4. **Explainability** everywhere: contribution, marginal risk, top drivers, reason codes, before/after.
5. **Lineage and reproducibility** as a first-class feature: source → transform → model → result.
6. **Streamlit first, service architecture later**: keep calculation logic independent of the UI so the same engines can move behind FastAPI and other front ends.

---

## 2. Commercial landscape

### 2.1 Investment / portfolio risk

| Platform | Category | Key capabilities verified | Target users | Pricing | Link |
|---|---|---|---|---|---|
| BlackRock Aladdin | Enterprise investment/risk platform | Common data language; whole-portfolio public/private views; risk/return analytics; scenarios/stress; portfolio management; APIs; Data Cloud; wealth; climate | Asset managers, asset owners, insurers, wealth firms, banks | Not publicly disclosed; enterprise sales | https://www.blackrock.com/aladdin |
| MSCI Barra / PortfolioManager | Portfolio risk / attribution / optimization | Risk and return attribution, what-if analysis, portfolio construction, optimization, backtesting, peer analytics, data/reporting | Asset managers, asset owners, risk teams | Not publicly disclosed | https://www.msci.com/our-solutions/analytics/barra-portfolio-manager |
| SimCorp Axioma Risk | Multi-asset risk | Top-down and full revaluation, stress tests, what-if, factor-linked risk/performance, cloud/SaaS, batch + interactive scale | Asset managers, banks, institutional investors | Not publicly disclosed | https://www.simcorp.com/products/axioma/axioma-risk |
| SimCorp Axioma Portfolio Analytics | Portfolio analytics | Risk analytics, factor/Brinson attribution, point-in-time and time-series analysis, reporting | Buy-side / institutional | Not publicly disclosed | https://www.simcorp.com/products/axioma/portfolio-analytics |
| SimCorp Axioma Portfolio Optimizer | Construction/rebalancing | Constraints, efficient frontier, optimization, batch rebalancing, backtesting | Portfolio managers, quants | Not publicly disclosed | https://www.simcorp.com/products/axioma/portfolio-optimizer |
| Murex MX.3 Investment Management | Front-to-back investment platform | Portfolio management, trading, compliance, risk, performance, accounting; multi-asset market/credit/liquidity risk; VaR/ES/stress; APIs; cloud/on-prem | Banks, buy-side, institutional | Not publicly disclosed | https://www.murex.com/en/investment-management |
| Clearwater Analytics | Cloud investment operations + analytics | Portfolio management, accounting, reconciliation, reporting, performance, compliance, risk | Asset owners/managers, insurers, wealth/institutional | Not publicly disclosed | https://clearwateranalytics.com/ |
| Charles River IMS | Cloud investment/wealth platform | Front-office investment management, compliance, portfolio/workflow support | Asset managers, asset owners, insurers, wealth firms | Not publicly disclosed | https://www.crd.com/ |
| FactSet Portfolio Analytics | Portfolio/market analytics | Whole-portfolio analysis, public/private coverage, performance/risk workflows and data | Buy-side, wealth, private capital, corporates | Not publicly disclosed | https://www.factset.com/ |
| Bloomberg PORT | Portfolio analytics/risk | Portfolio analytics, risk, attribution, scenario/portfolio workflows | Institutional investors / investment professionals | Not publicly disclosed | https://www.bloomberg.com/professional/product/portfolio-and-risk-analytics/ |
| Addepar | Wealth / multi-asset portfolio platform | Portfolio reporting, aggregation, analytics and client workflows | Wealth managers, family offices, institutions | Not publicly disclosed | https://addepar.com/ |
| smallcase | Indian retail/model portfolio platform | Equity/ETF/MF baskets, portfolio construction and rebalancing; retail-oriented portfolio views | Indian retail investors / advisors | Mixed; platform-specific / broker economics | https://www.smallcase.com/ |

### What is worth copying from commercial investment platforms

**Copy the product mechanics, not the enterprise scale:**

- Unified instrument/position taxonomy.
- One risk view across asset classes instead of separate calculators.
- Scenario library + user-defined what-if scenarios.
- Risk decomposition: portfolio → sleeve → asset → factor → scenario driver.
- Batch processing plus interactive single-portfolio drill-down.
- Rebalancing linked to risk/constraint objectives.
- Reproducible historical snapshots (“what did we know on that date?”).
- API-first calculation services so a dashboard is only one client.

### 2.2 Lending / credit-risk software

| Platform | Category | Key capabilities verified / benchmarked | ECL / stress relevance | Pricing | Link |
|---|---|---|---|---|---|
| Finastra Loan IQ | Loan servicing / lending platform | Commercial loan front-to-back, centralized loan/portfolio servicing, bilateral/syndicated, specialized credit workflows, integration | Portfolio data foundation for credit risk; risk integration depends on deployment | Not publicly disclosed | https://www.finastra.com/lending/loan-iq |
| Oracle Financial Services / OFSAA | Banking risk analytics | Risk-adjusted performance, compliance, portfolio risk analytics | Oracle public IFRS 9 docs show scenario-driven PD/LGD/CCF and provision-rule workflows | Not publicly disclosed | https://www.oracle.com/financial-services/financial-services-analytical-applications/ |
| S&P Global Credit Analytics / RiskGauge | Credit portfolio analytics | Company/country/industry stratification, comparative scores, monitoring and early-warning style analytics | Portfolio credit monitoring / stress use cases | Not publicly disclosed | https://www.spglobal.com/market-intelligence/en/solutions/credit-analytics |
| Experian credit risk modelling / analytics | Credit risk analytics | Predictive models, data, ML, explainability and model-governance themes | Portfolio loss controls and decisioning; ECL depends on implementation | Not publicly disclosed | https://www.experian.com/decision-analytics/credit-risk-modelling.html |
| Moody’s Analytics | Credit risk / ECL benchmark | Credit risk modelling, PD / portfolio analytics and IFRS 9-related solutions are major market capabilities | Yes; validate product/module-specific scope | Not publicly disclosed | https://www.moodys.com/ |
| FICO | Credit decisioning / risk | Credit scoring, decisioning, portfolio risk and analytic tooling | ECL is solution/configuration dependent | Not publicly disclosed | https://www.fico.com/ |
| SAS | Enterprise credit risk / modelling | Credit risk modelling, stress testing, model risk/governance ecosystem | IFRS 9 / CECL / stress use cases exist; verify module-specific current scope | Not publicly disclosed | https://www.sas.com/ |
| CRIF | Credit bureau / analytics | Credit data, decisioning, portfolio analytics | Regulatory and bureau analytics; module-specific ECL should be validated | Not publicly disclosed | https://www.crif.com/ |
| Indian credit-bureau ecosystem | Data / underwriting input | Bureau histories and related credit information feed lending/risk models | Input layer, not a replacement for internal PD/LGD/ECL engine | Commercial / contract | https://www.transunioncibil.com/ |

**Important:** the table distinguishes “market benchmark” from “independently deep-verified module scope.” For Moody’s, FICO, SAS and CRIF, use the official homepages above as follow-up starting points rather than treating every product-level claim as source-verified in this pass.

---

## 3. Open-source repository library

| Repository | Stars (as surfaced) | Last updated | License | Purpose | Reuse potential | Link |
|---|---:|---|---|---|---|---|
| QuantLib | ~7.6k | Current repository crawl; exact commit date not surfaced | Modified BSD-3 | Quantitative finance, pricing, fixed income, risk | **High** | https://github.com/lballabio/QuantLib |
| Riskfolio-Lib | ~4.5k | 2026 crawl; exact commit date not surfaced | BSD-3 | Portfolio optimization, CVaR, drawdown, factor/risk-parity methods | **High** | https://github.com/dcajasn/Riskfolio-Lib |
| PyPortfolioOpt | ~6.1k | 2026-07-07 surfaced | MIT | Mean-variance, Black-Litterman, HRP, shrinkage, optimizers | **High** | https://github.com/robertmartin8/PyPortfolioOpt |
| skfolio | ~2.4k | 2026-09-26 surfaced | BSD-3 | Modern portfolio modelling / optimization / selection | **High** | https://github.com/skfolio/skfolio |
| cvxportfolio | ~1.3k | 2026-04-27 surfaced | GPL-3.0 | Portfolio optimization and backtesting | **Medium** (license matters) | https://github.com/cvxgrp/cvxportfolio |
| QuantConnect Lean | ~21.8k | Current crawl; exact commit date not surfaced | Apache-2.0 | Algorithmic trading/backtesting engine | **Medium** | https://github.com/QuantConnect/Lean |
| Backtrader | ~23.4k | Exact current commit date not surfaced | GPL-3.0 | Backtesting/trading framework | **Medium** (license matters) | https://github.com/mementum/backtrader |
| pyfolio | ~6.4k | Legacy project; exact last commit not surfaced | Apache-2.0 | Portfolio performance/risk tear sheets and statistics | **Medium** (legacy) | https://github.com/quantopian/pyfolio |
| empyrical | — | Legacy project; exact date not surfaced | Apache-2.0 | Performance/risk metric primitives | **Medium** (use concepts carefully) | https://github.com/quantopian/empyrical |
| FinRL | ~16.4k | Current crawl; exact commit date not surfaced | MIT | Reinforcement learning for trading | **Low-Medium** for core risk; useful research | https://github.com/AI4Finance-Foundation/FinRL |
| OpenBB | Thousands of stars; current 2026 repository activity | 2026-09-19 surfaced | Verify current repository license before embedding | Research/data aggregation platform | **High** as integration/reference layer | https://github.com/OpenBB-finance/OpenBB |
| vectorbt | Large active community | Current repository crawl | Apache-2.0 + Commons Clause | Vectorized backtesting/portfolio analytics | **Conditional**; commercial distribution requires license review | https://github.com/polakowo/vectorbt |
| awesome-quant | Curated list | Frequently updated | Repository-specific / list | Discovery index for quant resources | **High for research discovery** | https://github.com/wilsonfreitas/awesome-quant |

### Open-source conclusions

**Best core combination for v1:**

`QuantLib + Riskfolio-Lib + skfolio/PyPortfolioOpt + SciPy/statsmodels + DuckDB/Parquet + PostgreSQL + Streamlit`

**Use pyfolio/empyrical as references, not architectural foundations.** They are useful for metric definitions and historical conventions but are much less compelling as the centre of a new 2026 platform.

**Treat licensing as architecture.** The presence of GPL or Commons Clause terms can affect whether a proprietary or hosted commercial version can safely embed a library. This needs legal review before distribution.

---

## 4. Academic research library

### 4.1 Portfolio theory, factors and optimization

| Must-read | Paper | Authors | Year | What it gives you | Build implication | Link |
|---|---|---|---:|---|---|---|
| **★ MUST-READ** | Portfolio Selection | Harry Markowitz | 1952 | Mean-variance portfolio selection and efficient portfolios | Baseline optimizer and sanity check | https://doi.org/10.2307/2975974 |
| **★ MUST-READ** | Common risk factors in the returns on stocks and bonds | Eugene F. Fama; Kenneth R. French | 1993 | Three equity factors plus two bond factors; factor-based explanation of returns | Factor exposure and attribution foundation | https://doi.org/10.1016/0304-405X(93)90023-5 |
| Risk Parity / Risk Budgeting | The Benefits of Equity-Leverage / risk-parity literature; practical anchor: “On the Properties of Equally-Weighted Risk Contributions Portfolios” | Maillard, Roncalli, Teïletche | 2010 | Equal risk contribution and portfolio construction | Add risk-budgeted allocation rather than pure return optimization | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1271972 |
| **★ MUST-READ** | Optimization of Conditional Value-at-Risk | R. Tyrrell Rockafellar; Stanislav Uryasev | 2000 | CVaR / Expected Shortfall optimization as a coherent optimization problem | Formal ES engine and constrained optimization | https://www.jstor.org/stable/2699986 |

### 4.2 VaR / validation / Expected Shortfall

| Paper | Authors | Year | What it gives you | Build implication | Link |
|---|---|---:|---|---|---|
| Techniques for Verifying the Accuracy of Risk Measurement Models | Philippe Jorion / Kupiec literature anchor; primary technical paper: “Techniques for Verifying the Accuracy of Risk Measurement Models” | Paul H. Kupiec | 1995 | VaR exception-rate testing | Add formal VaR backtesting rather than eyeballing charts | https://www.ssrn.com/abstract=702397 |
| Evaluating Interval Forecasts | Peter F. Christoffersen | 1998 | Conditional-coverage framework for interval/VaR forecasts | Detect clustering and dependence of VaR breaches | https://doi.org/10.1016/S0304-4076(97)00064-7 |
| Conditional Value-at-Risk for General Loss Distributions | Rockafellar; Uryasev | 2002 | General CVaR formulation and optimization | Extend beyond one loss distribution assumption | https://doi.org/10.21314/JOR.2002.024 |

### 4.3 Credit risk

| Must-read | Paper | Authors | Year | What it gives you | Build implication | Link |
|---|---|---:|---|---|---|
| **★ MUST-READ** | On the Pricing of Corporate Debt: The Risk Structure of Interest Rates | Robert C. Merton | 1974 | Structural credit-risk model linking firm value, debt and default | Conceptual foundation for structural PD | https://doi.org/10.2307/2326104 |
| Basel credit-risk framework | Basel Committee | Current Basel framework | PD/LGD/EAD, default definition, capital treatment | Regulatory mapping for bank-credit engine | https://www.bis.org/basel_framework/standard/CRE.htm |

### Five papers/frameworks to read first

1. **Markowitz (1952)** — portfolio construction baseline.
2. **Fama-French (1993)** — factor attribution and exposures.
3. **Rockafellar & Uryasev (2000)** — CVaR / Expected Shortfall.
4. **Kupiec (1995) + Christoffersen (1998)** — VaR validation.
5. **Merton (1974)** — structural credit risk, then Basel/IFRS 9 for production translation.

**Research gap:** this pass deliberately prioritised canonical, retrievable sources. It did not exhaustively enumerate 2023–2026 ML-credit papers because many current papers require journal/SSRN discovery and clause-level review. Do not interpret the paper table as a complete literature review.

---

## 5. Data-source catalogue

| Source | Data type | Coverage | Frequency | Cost | API? | License / use caution | Link |
|---|---|---|---|---|---|---|---|
| AMFI India | Mutual-fund NAVs | Indian mutual funds; latest NAV + history | Daily / history downloads | Public web access; no fee stated on page | Download/web | Check AMC/data redistribution terms; AMFI page limits some downloads to 90 days and notes an old format cutoff on 30-Sep-2026 | https://www.amfiindia.com/net-asset-value/nav-history |
| NSE / NSE Data & Analytics | Equities, derivatives, market data | Indian markets | Intraday/daily depending product | Access varies | Yes / licensed products | **Commercial/data-use policy matters; do not redistribute by default** | https://www.nseindia.com/market-data/real-time-data-subscription |
| RBI DBIE / Data Releases | Banking, macro, rates, credit | India | Daily / weekly / monthly series | Public | Web/download; programmatic options vary | Check series-specific RBI terms | https://data.rbi.org.in/ |
| FRED | Macro/market series | US + global series sourced from many institutions | Varies | API access generally available | Yes | Third-party series can have their own copyright/terms; attribution and commercial-use conditions vary | https://fred.stlouisfed.org/docs/api/fred/ |
| Nasdaq Data Link | Market / macro / alternative datasets | Multiple datasets | Varies | Free + paid datasets | Yes | **Terms/license vary by dataset; 2026 terms emphasize limited licenses** | https://data.nasdaq.com/ |
| Yahoo Finance ecosystem | Equities/FX/funds reference data | Broad global market universe | Daily/intraday depends endpoint | Access method varies | Unofficial/community wrappers | **Treat data as subject to Yahoo terms; do not assume redistribution rights** | https://finance.yahoo.com/ |
| Kaggle Lending Club datasets | Loan-level credit | Historical Lending Club-style loan data | Static snapshots | Public download subject to Kaggle terms | Download/API | Competition/dataset rules apply; verify before redistribution | https://www.kaggle.com/datasets/wordsforthewise/lending-club |
| Kaggle Home Credit | Credit application/behavior | Multi-table retail credit dataset | Static competition data | Public download subject to Kaggle terms | Download/API | Competition/data rules apply | https://www.kaggle.com/competitions/home-credit-default-risk/data |
| Ken French Data Library | Equity/bond factor datasets | Global/US factor portfolios and research data | Monthly/daily depending dataset | Public | Web download | Review the library's terms and attribution requirements | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html |
| BSE India | Indian securities/market reference | India | Varies | Access varies | Product-dependent | Confirm current data policy before automated redistribution | https://www.bseindia.com/ |
| Alpha Vantage | Market/FX/crypto/API data | Global | Endpoint-dependent | Free + paid plans | Yes | Rate limits and redistribution terms need current plan review | https://www.alphavantage.co/ |

### Data architecture recommendation

Use **source adapters** so no downstream calculator knows whether data came from AMFI, RBI, NSE, FRED, or a CSV.

Suggested canonical flow:

`External Source → Raw Landing → Normalization → Instrument/Entity Master → Point-in-Time Snapshot → Risk Engine → Results Store → Dashboard/API`

For every row, retain:

- `source_id`
- `source_url`
- `retrieved_at`
- `effective_at`
- `as_of_date`
- `license_tag`
- `transform_version`
- `quality_status`

This becomes essential when a risk number has to be reproduced six months later.

---

## 6. Regulatory and standards map → feature requirements

| Framework / source | What matters for product | Feature that should exist | Verification / link |
|---|---|---|---|
| SEBI Master Circular for Mutual Funds, Mar-2026 | Stress-testing requirements apply to specified debt schemes; governance and periodic testing matter | Stress-test scheduler, scenario registry, run history, board/report export, versioned assumptions | https://www.sebi.gov.in/legal/master-circulars/mar-2026/master-circular-for-mutual-funds_100208.html |
| RBI NBFC Concentration Risk Management Directions + 2026 amendment | Concentration limits / exposure framework can change through amendments | Concentration dashboards, configurable exposure buckets, rule-effective dates, entity applicability, breach alerts | https://www.rbi.org.in/Scripts/NotificationUser.aspx |
| RBI 2026 NBFC income-recognition / provisioning amendment | Accounting/provisioning rules can change and may have future effective dates | Regulatory rule engine with effective-date versioning; reconciliation to accounting output | https://www.rbi.org.in/Scripts/NotificationUser.aspx |
| RBI gold-loan framework / 2025 handbook material | Gold-loan LTV and related lending constraints are regulatory inputs; exact current applicability must be tied to entity/product | Collateral valuation, LTV monitor, price shock, purity/weight/valuation controls, auction/exception workflow | https://www.rbi.org.in/ ; handbook/reference surfaced in RBI material |
| Basel stress-testing principles | Governance, objectives, scenarios, methods, resources, documentation | Scenario library, scenario ownership, methodology version, result archive, validation evidence | https://www.bis.org/publ/bcbs155.htm |
| Basel credit-risk framework | PD/LGD/EAD, default definition, risk-weight/capital concepts | PD/LGD/EAD fields, default-state transitions, segmentation, capital/risk metrics | https://www.bis.org/basel_framework/standard/CRE.htm |
| Basel market-risk framework | Expected Shortfall and market-risk modelling concepts | ES/CVaR engine, liquidity horizon awareness, model governance | https://www.bis.org/basel_framework/standard/MAR.htm |
| IFRS 9 Financial Instruments | ECL is forward-looking and scenario-driven; staging, PD/LGD/EAD and discounting need accounting-consistent design | Stage 1/2/3, 12-month/lifetime ECL, scenario weights, forward-looking variables, EIR discounting, overlays, reconciliation | https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/ |
| Ind AS 109 | Indian accounting implementation of financial instruments / expected-credit-loss framework | Same core ECL engine with Indian accounting configuration and disclosures; maintain current notified text separately | https://www.mca.gov.in/ |

### Regulatory product principle

Do **not** hard-code regulatory constants into business logic. Model them as data:

```text
Rule
 ├─ jurisdiction
 ├─ regulator
 ├─ entity_type
 ├─ product_type
 ├─ effective_from
 ├─ effective_to
 ├─ threshold / formula
 ├─ source_document
 └─ rule_version
```

Then a 2026 amendment becomes a new rule version rather than a code fork.

---

## 7. Aladdin architecture breakdown

### 7.1 What is publicly known

BlackRock’s public material consistently points to these architectural characteristics:

1. **Common data language / common data layer** — the objective is to connect investment, risk and operational information instead of maintaining isolated application silos.
2. **Whole-portfolio view** — public and private assets can be analysed together.
3. **Common analytics** — risk, performance, scenarios, exposures and reporting are built on the shared information model.
4. **API-first access** — Aladdin Studio exposes programmatic operations and analytics; BlackRock describes Python/Jupyter access and APIs.
5. **Governed data cloud** — Aladdin Data Cloud is positioned as normalized/mapped data delivered into a cloud environment, including Snowflake integrations.
6. **Scenario lifecycle** — scenarios are treated as reusable objects with drivers, cross-asset relationships and governance, not one-off chart sliders.
7. **Automation and controls** — alerts, thresholds, remediation, permissions and auditability are part of the workflow.
8. **Distributed enterprise architecture** — public engineering/job materials reference Java/Python, SQL/NoSQL, Kafka, Kubernetes, Docker, Snowflake, Redis and cloud architectures.

Primary sources: [Aladdin overview](https://www.blackrock.com/aladdin), [Aladdin Studio](https://www.blackrock.com/aladdin/products/aladdin-studio), [Aladdin Data Cloud](https://www.blackrock.com/aladdin/products/aladdin-data-cloud), [Aladdin Risk](https://www.blackrock.com/aladdin/products/aladdin-risk), [BlackRock engineering/SDK material](https://medium.com/blackrock-engineering), [BlackRock careers – technology roles](https://careers.blackrock.com/).

### 7.2 Simplified architecture you can actually build

```text
                       ┌─────────────────────────┐
                       │       Streamlit UI      │
                       │ portfolio / loan / risk │
                       └────────────┬────────────┘
                                    │
                             API / Python calls
                                    │
        ┌───────────────────────────▼───────────────────────────┐
        │                    RISK ORCHESTRATOR                  │
        │ portfolio snapshot → scenario → model → result       │
        └──────────────┬──────────────┬──────────────┬──────────┘
                       │              │              │
                ┌──────▼─────┐ ┌────▼───────┐ ┌────▼────────┐
                │ Market Risk│ │ Portfolio  │ │ Credit Risk │
                │ VaR / ES   │ │ factors/opt│ │ PD LGD EAD  │
                └──────┬─────┘ └────┬───────┘ └────┬────────┘
                       │             │              │
                       └─────────────┼──────────────┘
                                     │
                           ┌─────────▼─────────┐
                           │ Scenario Engine   │
                           │ shocks / paths /  │
                           │ correlations      │
                           └─────────┬─────────┘
                                     │
                       ┌─────────────▼────────────┐
                       │ Canonical Data Model     │
                       │ positions / loans /      │
                       │ instruments / customers  │
                       └─────────────┬────────────┘
                                     │
                 ┌───────────────────▼───────────────────┐
                 │ Data + Lineage Layer                  │
                 │ Raw files → normalized → snapshots   │
                 │ source / timestamp / license / v     │
                 └───────────────────┬───────────────────┘
                                     │
               ┌─────────────────────▼─────────────────────┐
               │ DuckDB/Parquet + PostgreSQL               │
               │ research history + operational metadata   │
               └───────────────────────────────────────────┘
```

### 7.3 The key Aladdin-inspired object model

The most useful design is to make a **Scenario** a first-class object:

```text
Scenario
  id
  name
  effective_date
  parent_scenario
  shocks[]
  correlations_override
  pricing_policy
  valuation_policy
  macro_path
  collateral_haircuts
  created_by
  approved_by
  model_version
```

The risk result then stores:

```text
Result
  portfolio_id / loan_book_id
  as_of
  scenario_id
  model_version
  data_snapshot_id
  metric
  value
  contribution
  confidence / validation status
```

This single idea makes v1 and v2 compatible: the same scenario engine can shock an equity portfolio, an interest-rate book, or a gold-loan collateral pool.

---

## 8. Recommended tech stack

### 8.1 Solo-developer v1 stack

| Layer | Recommendation | Why |
|---|---|---|
| Language | Python | Strong quant ecosystem; one language from data to UI |
| UI | Streamlit | Fastest path to a useful analyst cockpit |
| Dataframes | Polars + pandas | Polars for scalable transforms; pandas for broad compatibility |
| Numerical | NumPy + SciPy | Core math / optimization primitives |
| Statistics | statsmodels + scikit-learn | Regression, factor models, validation, baseline ML |
| Finance | QuantLib | Fixed income, pricing and instruments |
| Portfolio optimization | Riskfolio-Lib + PyPortfolioOpt / skfolio | Ready-made optimization and risk measures |
| Solver | CVXPY | Custom constrained optimization / research prototypes |
| Storage | Parquet + DuckDB | Cheap analytical storage, fast local research queries |
| Operational DB | PostgreSQL | Users, portfolios, instruments, configs, run metadata |
| Cache | Streamlit cache initially; Redis later | Keep v1 simple; add shared cache only when needed |
| Scheduling | cron/OS initially; Prefect/Dagster later | Avoid premature orchestration complexity |
| API upgrade | FastAPI | Decouple engines from UI for v2+ |
| Testing | pytest + property-based tests | Risk models need deterministic and edge-case checks |
| Quality / lint | Ruff + mypy | Keep analytics code disciplined |
| Packaging | pyproject.toml + uv/Poetry | Reproducible dependencies |

### 8.2 Upgrade path

**Stage 1:** Streamlit + local Parquet/DuckDB.  
**Stage 2:** PostgreSQL + FastAPI while keeping Streamlit as a client.  
**Stage 3:** Background workers / queue, Redis, object storage, scheduled pipelines.  
**Stage 4:** React or another dedicated front end only if user/tenant scale justifies it.

### 8.3 Architecture rules

Keep these boundaries from day one:

- `domain/` — instruments, portfolios, loans, scenarios.
- `data/` — source adapters and normalization.
- `risk/` — metrics and model implementations.
- `scenarios/` — shock definitions and scenario execution.
- `validation/` — backtests and model validation.
- `storage/` — persistence.
- `ui/` — Streamlit only.

Do **not** bury risk formulas inside Streamlit callbacks.

---

## 9. Gap analysis and product opportunity

### 9.1 What already exists

- Enterprise investment platforms can already do multi-asset risk, portfolio construction, stress testing, attribution and workflow.
- Enterprise lending platforms can already do loan servicing, credit analytics, portfolio monitoring and ECL-related modelling.
- Open source already has strong individual building blocks for portfolio optimization, pricing, backtesting and quant research.

### 9.2 What remains fragmented

The strongest gap is the **connective tissue**:

1. **Data ingestion → normalized exposure → risk → explanation** in one small, deployable product.
2. **Indian data and products** as first-class citizens rather than a US/European afterthought.
3. **Portfolio + lending concepts under one scenario abstraction**.
4. **Model transparency** rather than opaque “risk score” outputs.
5. **Regulatory/version lineage** so a number can be defended months later.
6. **Small/mid-market deployment** where an enterprise Aladdin/Murex/Oracle implementation is too heavy.
7. **Open-source extensibility** around formulas and adapters rather than an inaccessible black box.

### 9.3 Practical whitespace for India

Potential user groups:

- Independent wealth managers and RIAs.
- Family offices and small asset managers.
- Treasury / investment teams of mid-sized firms.
- Small/mid NBFC risk teams.
- Fintech lenders that need an explainable internal risk lab.
- Students/researchers who want professional-style risk infrastructure without enterprise licenses.

### 9.4 Hard problems you should expect

**1. Data rights and redistribution.** A technically excellent dashboard can still be unusable commercially if its market-data license does not permit the intended delivery model.

**2. Instrument master.** Tickers are not enough. You need stable instrument IDs, share classes, corporate actions, currencies, sector mappings, bond identifiers, maturity/coupon structures and fund look-through relationships.

**3. Fixed-income realism.** Bonds require curves, pricing conventions, accrued interest, duration/DV01, credit spreads and sometimes full revaluation.

**4. Look-through data.** Mutual-fund/ETF exposure may lag and have incomplete holdings; “factor exposure” can therefore be stale or approximate.

**5. VaR model risk.** Historical VaR can fail in regime change; parametric VaR can be mis-specified; Monte Carlo is only as good as its factor dynamics and pricing.

**6. Credit model governance.** A high-AUC default model is not automatically a good regulatory/accounting model.

**7. ECL.** ECL is an accounting process as well as a statistical model. Staging, discounting, scenario weights, overlays, recoveries and reconciliation matter.

**8. Rule churn.** RBI/SEBI frameworks change. Effective-dated configuration is mandatory.

---

## 10. Proposed MVP

### 10.1 v1 — Investment portfolio risk

**P0 / release-blocking**

- CSV/manual portfolio ingestion.
- Canonical instrument + position model.
- Daily price/NAV ingestion adapters.
- Returns, annualized volatility, beta, drawdown.
- Historical VaR and Expected Shortfall/CVaR.
- Correlation matrix and hierarchical clustering.
- Factor exposure: at minimum market + sector; add Fama-French-style factors where data rights permit.
- Fixed-income basics: yield, duration, DV01 and parallel curve shocks.
- Scenario engine: equity shock, rate shock, FX shock, spread shock.
- What-if rebalance with constraint checks.
- Risk contribution / marginal contribution.
- Exportable report with methodology + data timestamp.

**P1**

- Monte Carlo VaR.
- Non-parallel yield-curve scenarios.
- Fund look-through when holdings are available.
- Historical crisis scenarios.
- VaR backtesting (Kupiec / Christoffersen-style).
- Saved scenario sets.
- Portfolio comparison and benchmark-relative risk.

### 10.2 v2 — Lending / loan-book risk

**P0**

- Standard loan-tape schema.
- Portfolio concentration by product, geography, branch, industry, borrower, channel, vintage and collateral.
- DPD / delinquency migration.
- Baseline PD model (logistic/scorecard first).
- LGD model with collateral / recovery assumptions.
- EAD/CCF framework.
- Expected loss.
- ECL staging engine: Stage 1 / 2 / 3.
- 12-month vs lifetime ECL.
- Multi-scenario macro assumptions and weights.
- Rate-shock and gold-price-shock scenarios.
- Early-warning rules.
- Model version + audit trail.

**P1**

- Survival / hazard PD.
- Vintage curves.
- Roll-rate ECL.
- Segment-level challenger models.
- SHAP / local explainability.
- Management overlays.
- Reconciliation to finance/provisioning outputs.
- Collateral haircut / auction-recovery scenarios for gold loans.

---

## 11. Six-week build roadmap

### Week 1 — Data foundation

- Define canonical schemas for instrument, price, position, portfolio, loan, customer, collateral, scenario.
- Build source-adapter interface.
- Land raw data in Parquet.
- Create DuckDB research database.
- Create Streamlit shell and portfolio selector.

**Definition of done:** a portfolio can be loaded reproducibly from a saved snapshot.

### Week 2 — Core portfolio risk

- Returns.
- Volatility.
- Beta.
- Drawdowns.
- Correlation.
- Historical VaR.
- Expected Shortfall.
- Top-risk-contributor views.

**Definition of done:** every metric can be recomputed from one stored portfolio snapshot.

### Week 3 — Fixed income + factors + validation

- QuantLib bond analytics.
- Duration / DV01.
- Parallel and non-parallel rate shocks.
- Factor regression.
- VaR backtesting.
- Model/version metadata.

**Definition of done:** the risk engine produces both a number and its methodology/data lineage.

### Week 4 — What-if + dashboard productization

- Rebalance constraints.
- Marginal risk and contribution.
- Scenario editor.
- Portfolio comparison.
- Downloadable risk report.
- Saved scenarios.
- UI polish.

**Definition of done:** an analyst can answer “what changed, why, and what happens if I rebalance?” without touching code.

### Week 5 — Hardening

- Unit tests + property tests.
- Golden test portfolios.
- Cross-check metrics against independent calculations.
- Data-quality checks.
- Cache strategy.
- Instrument-master edge cases.
- License/ToS review for every external data source.

**Definition of done:** a repeat run from the same snapshot returns the same results.

### Week 6 — Release v1 + v2 credit foundation

- Package v1.
- Documentation and architecture diagrams.
- Public sample dataset.
- Loan-tape canonical schema.
- Concentration engine prototype.
- Baseline PD/LGD/EAD notebook/service.
- First ECL staging model.
- Gold-price shock prototype.

**Definition of done:** v1 is usable and v2 has a real data/risk foundation rather than a slide-deck design.

---

## 12. Implementation blueprint

### Core tables

```text
instrument_master
position_snapshot
price_observation
curve_observation
factor_observation
portfolio
portfolio_target
scenario
scenario_shock
risk_run
risk_metric
risk_contribution
model_version
source_snapshot
regulatory_rule
```

### Credit tables

```text
customer
loan_account
loan_snapshot
payment_observation
collateral
collateral_valuation
segment_definition
pd_model_score
lgd_model_score
ead_assumption
ecl_result
macro_scenario
ews_signal
model_validation_run
```

### API-oriented calculation signature

```python
def run_risk(
    portfolio_snapshot_id: str,
    scenario_id: str,
    model_version: str,
) -> RiskRun:
    ...
```

That same pattern can be reused for:

```python
def run_credit_risk(
    loan_book_snapshot_id: str,
    scenario_id: str,
    model_version: str,
) -> CreditRiskRun:
    ...
```

### UI pages

**v1**

- Overview
- Holdings
- Risk
- Factors
- Scenarios
- Rebalance
- Validation
- Data lineage

**v2**

- Loan Book
- Concentration
- Delinquency
- PD/LGD/EAD
- ECL
- Stress Testing
- Early Warning
- Model Validation
- Regulatory Rules
- Audit Trail

---

## 13. Practitioner/community signals

The strongest recurring practical themes found in the accessible practitioner discussion are:

- Users care about **scenario and stress analysis**, not just a single headline VaR number.
- Risk engines become materially more useful when they support **factor decomposition** and **why-did-risk-change** analysis.
- Illiquid/new instruments create data problems that often push practitioners toward proxy/factor models.
- Open-source quant projects generate interest, but community feedback is skeptical of shallow “AI wrapper” products; the durable value is in the underlying data/model transparency.

Examples: [r/quant — open-source multi-factor risk model discussion](https://www.reddit.com/r/quant/), [Quant StackExchange — CVaR / scenario questions](https://quant.stackexchange.com/), [Quant StackExchange — covariance/data issues](https://quant.stackexchange.com/).

**Coverage limitation:** Reddit and Quant StackExchange were the strongest retrievable community sources in this pass. Hacker News, LinkedIn and YouTube were not independently deep-read enough to be presented as a representative survey.

---

## 14. Risks / anti-patterns to avoid

1. **Do not start with ML.** First make deterministic risk metrics and data lineage excellent.
2. **Do not start with a giant microservice architecture.** Modular Python packages + one database are enough for v1.
3. **Do not make Streamlit the domain layer.** It is only the presentation layer.
4. **Do not let every data source have its own schema.** Normalize once.
5. **Do not mix market-data timestamps with portfolio-as-of dates.** Point-in-time correctness matters.
6. **Do not present factor exposure without describing the factor dataset and look-through assumptions.**
7. **Do not call a generic PD model “IFRS 9 compliant.”** Accounting compliance requires much more than predictive performance.
8. **Do not bake RBI/SEBI numbers into code.** Store effective-dated regulatory rules.
9. **Do not build an undocumented stress slider.** Every scenario should be a reproducible object.
10. **Do not ignore licenses.** “Publicly accessible” is not the same as “redistributable.”

---

## 15. Research conclusions by specialist track

### Agent 1 — Commercial Investment Scout
The enterprise market is mature. A differentiating small platform should compete on transparency, deployment simplicity, India-specific data and workflow—not on matching every enterprise feature.

### Agent 2 — Commercial Lending/Credit Scout
Credit risk is also mature commercially. The most defensible open-source wedge is a transparent internal risk lab with loan-tape ingestion, concentration, collateral stress and ECL lineage, not another black-box score.

### Agent 3 — Aladdin Deep-Dive
The strongest public architecture signals are the common data language, shared risk models, scenario lifecycle, Data Cloud, API-first design, and distributed/cloud architecture.

### Agent 4 — Open-Source Hunter
The building blocks exist, but they are fragmented. QuantLib + risk/optimization libraries + data/storage + dashboard can form a credible base. Licensing requires attention.

### Agent 5 — Academic Research
Classical methods remain essential. Build the deterministic baseline first; add advanced ML only after model validation, data quality and explainability are in place.

### Agent 6 — Data Source Scout
India-first data is feasible, but the major constraint is not discovery; it is rights, redistribution and point-in-time quality.

### Agent 7 — Tech Architecture
A modular monolith is the right solo-developer starting point. Design clean service boundaries now, but only split into FastAPI/workers/event systems once scale demands it.

### Agent 8 — Regulatory/Standards
Regulatory configuration and effective dates should be data-driven. Stress testing, concentration, provisioning and gold-loan constraints all point to the same rule/scenario architecture.

### Agent 9 — Practitioner Intelligence
The practical demand is for explainability, scenarios, data realism and useful workflows. Community interest is strong around open factor/risk tools, but shallow presentation layers are not enough.

### Agent 10 — Gap/Critic
The project is most compelling as a **transparent, India-aware, modular risk operating system** combining investment and lending risk primitives under one scenario/data lineage architecture.

---

## 16. Full bibliography / source index

### BlackRock / Aladdin

- BlackRock Aladdin overview — https://www.blackrock.com/aladdin
- Aladdin Studio — https://www.blackrock.com/aladdin/products/aladdin-studio
- Aladdin Data Cloud — https://www.blackrock.com/aladdin/products/aladdin-data-cloud
- Aladdin Risk — https://www.blackrock.com/aladdin/products/aladdin-risk
- Aladdin Wealth — https://www.blackrock.com/aladdin/products/aladdin-wealth
- BlackRock Engineering — https://medium.com/blackrock-engineering
- BlackRock Careers — https://careers.blackrock.com/

### Investment platforms

- MSCI Barra Portfolio Manager — https://www.msci.com/our-solutions/analytics/barra-portfolio-manager
- SimCorp Axioma Risk — https://www.simcorp.com/products/axioma/axioma-risk
- SimCorp Portfolio Analytics — https://www.simcorp.com/products/axioma/portfolio-analytics
- SimCorp Portfolio Optimizer — https://www.simcorp.com/products/axioma/portfolio-optimizer
- Murex Investment Management — https://www.murex.com/en/investment-management
- Clearwater Analytics — https://clearwateranalytics.com/
- Charles River Development — https://www.crd.com/
- FactSet — https://www.factset.com/
- Bloomberg Portfolio & Risk Analytics — https://www.bloomberg.com/professional/product/portfolio-and-risk-analytics/
- Addepar — https://addepar.com/
- smallcase — https://www.smallcase.com/

### Credit / lending

- Finastra Loan IQ — https://www.finastra.com/lending/loan-iq
- Oracle Financial Services — https://www.oracle.com/financial-services/financial-services-analytical-applications/
- Oracle IFRS 9 documentation — https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/ifrs9-acct-guide/
- S&P Credit Analytics — https://www.spglobal.com/market-intelligence/en/solutions/credit-analytics
- Experian credit risk modelling — https://www.experian.com/decision-analytics/credit-risk-modelling.html
- Moody’s — https://www.moodys.com/
- FICO — https://www.fico.com/
- SAS — https://www.sas.com/
- CRIF — https://www.crif.com/
- TransUnion CIBIL — https://www.transunioncibil.com/

### Open source

- QuantLib — https://github.com/lballabio/QuantLib
- Riskfolio-Lib — https://github.com/dcajasn/Riskfolio-Lib
- PyPortfolioOpt — https://github.com/robertmartin8/PyPortfolioOpt
- skfolio — https://github.com/skfolio/skfolio
- cvxportfolio — https://github.com/cvxgrp/cvxportfolio
- Lean — https://github.com/QuantConnect/Lean
- Backtrader — https://github.com/mementum/backtrader
- pyfolio — https://github.com/quantopian/pyfolio
- empyrical — https://github.com/quantopian/empyrical
- FinRL — https://github.com/AI4Finance-Foundation/FinRL
- OpenBB — https://github.com/OpenBB-finance/OpenBB
- vectorbt — https://github.com/polakowo/vectorbt
- vectorbt license — https://github.com/polakowo/vectorbt/blob/main/LICENSE.txt
- awesome-quant — https://github.com/wilsonfreitas/awesome-quant

### Data

- AMFI NAV history — https://www.amfiindia.com/net-asset-value/nav-history
- NSE market-data subscriptions/policies — https://www.nseindia.com/market-data/real-time-data-subscription
- RBI DBIE — https://data.rbi.org.in/
- RBI Data Releases — https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx
- FRED API — https://fred.stlouisfed.org/docs/api/fred/
- FRED terms — https://fred.stlouisfed.org/docs/terms.html
- Nasdaq Data Link — https://data.nasdaq.com/
- Yahoo Finance — https://finance.yahoo.com/
- Lending Club dataset — https://www.kaggle.com/datasets/wordsforthewise/lending-club
- Home Credit dataset — https://www.kaggle.com/competitions/home-credit-default-risk/data
- Ken French Data Library — https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- BSE India — https://www.bseindia.com/
- Alpha Vantage — https://www.alphavantage.co/

### Regulation / standards

- SEBI Master Circular for Mutual Funds, March 2026 — https://www.sebi.gov.in/legal/master-circulars/mar-2026/master-circular-for-mutual-funds_100208.html
- RBI notifications — https://www.rbi.org.in/Scripts/NotificationUser.aspx
- RBI main site — https://www.rbi.org.in/
- Basel Stress Testing Principles — https://www.bis.org/publ/bcbs155.htm
- Basel Credit Risk standard — https://www.bis.org/basel_framework/standard/CRE.htm
- Basel Market Risk standard — https://www.bis.org/basel_framework/standard/MAR.htm
- IFRS 9 — https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/
- Ministry of Corporate Affairs (Ind AS source portal) — https://www.mca.gov.in/

### Academic

- Markowitz 1952 — https://doi.org/10.2307/2975974
- Fama & French 1993 — https://doi.org/10.1016/0304-405X(93)90023-5
- Maillard, Roncalli & Teïletche — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1271972
- Rockafellar & Uryasev 2000 — https://www.jstor.org/stable/2699986
- Rockafellar & Uryasev 2002 — https://doi.org/10.21314/JOR.2002.024
- Kupiec 1995 — https://www.ssrn.com/abstract=702397
- Christoffersen 1998 — https://doi.org/10.1016/S0304-4076(97)00064-7
- Merton 1974 — https://doi.org/10.2307/2326104

### Practitioner / community

- Reddit r/quant — https://www.reddit.com/r/quant/
- Quant StackExchange — https://quant.stackexchange.com/

---

## 17. Final recommendation

Build **v1 as a risk engine with a Streamlit front end, not as a Streamlit project**.

The product’s central abstraction should be:

> **Snapshot + Scenario + Model Version → Explainable Risk Result**

That abstraction is broad enough to cover:

- equity portfolio VaR,
- bond duration/curve stress,
- factor exposures,
- what-if rebalancing,
- loan concentration,
- PD/LGD/EAD,
- ECL,
- gold-loan collateral stress,
- and early-warning signals.

Once that engine is clean, the “Mini-Aladdin” label becomes justified by architecture rather than by the number of dashboards.
