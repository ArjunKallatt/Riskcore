# Agent 9 — Practitioner & Community Intelligence (Riskcore)

Research date: 2026-10-02. Researcher: Agent 9.

## 0. Read this first: how much evidence there is, and what was blocked

This agent could not reach most of the community sources it was asked to cover. Weigh every finding below with that in mind.

| Source | Status |
|---|---|
| Reddit (all subs incl. r/quant, r/IndiaInvestments, r/PersonalFinanceIndia) | **BLOCKED.** `old.reddit.com` fetch was refused, curl got a proxy 403 (policy denial), and WebSearch rejects `reddit.com` ("not accessible to our user agent"). General web searches returned **zero** Reddit threads. **There is no Reddit evidence in this report.** |
| Hacker News (news.ycombinator.com, hn.algolia.com) | **Fetch BLOCKED** by egress proxy. Thread titles and short summaries came only from search-engine results, so every HN item is marked **snippet-only**. I could not open or check the quotes. |
| Quant StackExchange | Fetch blocked. A domain-restricted search returned nothing. **No evidence.** |
| Medium, Substack, InfoQ, QuantInsti, PyQuantNews, Wikipedia, arXiv | Fetch **BLOCKED** by egress proxy. Search titles are listed as **snippet-only**. |
| BDO / RSM / KPMG / BCAJ / SKP / ifrstech (NBFC ECL) | Fetch **BLOCKED**. The content comes from search-result summaries only (**snippet-only**). |
| GitHub (github.com pages via WebFetch) | **Worked.** Most of the evidence I could check comes from here. |
| YouTube, LinkedIn, Wilmott/Nuclear Phynance | Not reached. The session's shared WebSearch budget (200) ran out partway through, and these domains are almost certainly blocked too. |

Treat everything marked "snippet-only" as a lead to re-check, not as a quotation. Quotes marked **[verified]** were read on the actual page.

---

## 1. Recurring themes (with evidence)

### Theme 1: Excel is still the real risk system, and its weakness is control (audit trail, versioning), not the maths
- HN thread: "Spreadsheets are widely used in financial institutions, and not just for little ..." — https://news.ycombinator.com/item?id=13906770 (snippet-only; ~2017, **>3 yrs old**). The search summary describes a bank where *thousands of equity-derivative trades were each an Excel sheet in source control*, run on a compute grid to produce the official desk risk numbers.
- HN: "We software guys complain about this all the time, but Excel completely permeate..." — https://news.ycombinator.com/item?id=5198376 (snippet-only; ~2013, **>3 yrs old**). Summary: spreadsheets lack version control, rollback, auditing and QA.
- HN: "Stop Using Excel, Finance Chiefs Tell Staffs" — https://news.ycombinator.com/item?id=15756062 and "Finance Pros Say You'll Have to Pry Excel Out of Their Cold, Dead Hands" — https://news.ycombinator.com/item?id=15819016 (snippet-only titles; ~2017, **>3 yrs old**).
- HN: "Claude for Excel" — https://news.ycombinator.com/item?id=45722639 (snippet-only; ~2025). This suggests Excel-native workflows are still the battleground in 2025.
- For NBFC ECL specifically, a search summary of ECL software vendor content says spreadsheets "are very prone to manual errors and lack a proper audit trail" — https://ifrstech.com/blog/ifrs-9-ecl-software-for-banks/ (snippet-only, vendor content, date unknown).
- **Implication for Riskcore:** compete on *auditability* (versioned runs, input snapshots, reproducible reports, Excel export), not on fancier models.

### Theme 2: Aladdin is admired as a "single data model / single source of truth", and distrusted for concentration and opacity
- HN comment: "...Aladdin isn't an AI, just a codename for the platform and data-model" (paraphrased by the search summary) — https://news.ycombinator.com/item?id=35432421 (snippet-only; ~2023).
- HN: "Interesting to note that BlackRock's Aladdin software platform ... is being largely written/re-written in Julia" — https://news.ycombinator.com/item?id=14019500 (snippet-only; ~2017, **>3 yrs old**).
- HN: "Holy moly. This lead me down a quick read..." (Aladdin acronym and scale) — https://news.ycombinator.com/item?id=43490345 (snippet-only; ~2025). The summary notes concern that one firm has this much indirect influence over world assets.
- HN: https://news.ycombinator.com/item?id=13403061 (snippet-only; ~2017, **>3 yrs old**).
- BlackRock's own 10-K flags Aladdin's growth as bringing "execution, operational and data management risks" — https://www.sec.gov/Archives/edgar/data/1364742/000095017023004343/blk-20221231.htm (snippet-only; FY2022).
- **Implication:** borrow the *idea* (one canonical position, security and risk data model that every view reads from). Make transparency the selling point against "black-box" perceptions.

### Theme 3: The DIY "portfolio risk dashboard" is a very crowded genre, and most projects are student or portfolio pieces with the same blind spots
- GitHub has many Streamlit + yfinance + Plotly VaR/CVaR dashboards, most with 0 stars (see table in section 2). They repeat the same pattern: three VaR methods, an efficient frontier, and Monte Carlo with normal returns.
- One project's README admits **[verified]**: the optimized portfolio "uses the same data for both estimation and evaluation, inflating performance metrics", and the Monte Carlo "assumes normally distributed returns" — https://github.com/ParidhiBhardwajj/portfolio-risk-optimizer (2026).
- The better ones add **VaR backtesting** (Kupiec POF + Christoffersen) and Student-t Monte Carlo **[verified]** — https://github.com/zongmaow/portfolio-risk-dashboard (2026, 0 stars).
- Show HN posts in the same space (all snippet-only): "A system that monitors portfolio risk and warns when it gets dangerous" https://news.ycombinator.com/item?id=46896523 (~2026); CashGraphs, an optimizer using non-normal returns and tail behaviour, https://news.ycombinator.com/item?id=32118796 (~2022, **>3 yrs**); Eiten https://news.ycombinator.com/item?id=24428206 (~2020, **>3 yrs**); Finarky (IRR-based personal return) https://news.ycombinator.com/item?id=36284990 (~2023); Wealthfolio https://news.ycombinator.com/item?id=41465735 (~2024) and 2.0 https://news.ycombinator.com/item?id=46006016 (~2025).
- **Implication:** a generic "VaR dashboard" will not stand out. What does: backtested risk numbers, India-specific data plumbing, and a credible audit and report layer.

### Theme 4: Open-source trackers win on privacy and self-hosting, but they are *trackers*, not *risk systems*
- Ghostfolio **[verified]**: 9.4k stars, AGPLv3, NestJS/Angular/Postgres. Its only risk feature is "static analysis to identify potential risks in your portfolio" — https://github.com/ghostfolio/ghostfolio. A search of its issues for "india" returned 1 unrelated issue, which suggests little India-specific coverage (accessed 2026-10-02).
- Wealthfolio **[verified]**: 9.1k stars. "Local-first: your data lives on your device." Rust/Tauri/SQLite, with time-weighted returns but no VaR or factor risk — https://github.com/afadil/wealthfolio.
- **Implication:** there is a gap between trackers (performance, net worth) and institutional risk tools (factor and tail risk, stress tests). Riskcore v1 sits in that gap. Local-first and privacy should be treated as features users expect.

### Theme 5: Indian retail tooling is held back by data plumbing (CAS PDFs, AMFI NAVs), not by analytics
- casparser **[verified]** (MIT, 231 stars) parses CAMS, KFintech, NSDL and CDSL CAS PDFs and produces capital gains in Schedule 112A format — https://github.com/codereverser/casparser. Its issue tracker shows how fragile this is **[verified issue titles]**: #150 "not well-formed (invalid token)" (Sep 2026); #132 "CDSL stock parsing fails with unusual text wrapping" (Jun 2026); #130 "CDSL ignores mutual fund entries spanning multiple pages" (May 2026); #106 "CAMS parsing fails for PyMuPDF >= 1.25.0" (Feb 2025); #113 "Unable to parse mutual fund folios in NSDL" (Sep 2025) — https://github.com/codereverser/casparser/issues.
- mftool **[verified]** (MIT, 257 stars) pulls AMFI NAVs and scheme lists — https://github.com/NayakwadiS/mftool.
- The commercial and blog space covers XIRR, stock-level overlap and portfolio health scores: FundSageAI blog (2026, vendor, snippet-only) https://www.fundsageai.com/blog/best-mutual-fund-portfolio-analyzer-india-2026. The freefincal overlap tool is Google-Sheets based, with SEBI sector classification (snippet-only, mirrored blog posts) https://www.goodreads.com/author_blog_posts/25179967-update-mutual-fund-portfolio-overlap-tool-with-sebi-classified-stock-se?tab=book. Business Standard on overlapping MFs (Apr 2025, snippet-only) https://www.business-standard.com/finance/personal-finance/overlapping-mutual-funds-reduce-your-returns-here-is-how-to-fix-risk-125041500475_1.html.
- The GitHub topic `mutual-funds-india` has **zero** repos **[verified]** — https://github.com/topics/mutual-funds-india.
- **Implication:** robust CAS import (pin PyMuPDF, add regression fixtures), AMFI NAV ingestion and MF look-through to stock holdings would be differentiators in their own right.

### Theme 6: NBFC ECL is judgement-heavy and data-starved, and small NBFCs depend on Excel and consultants
(All snippet-only. The primary pages were blocked. Re-check before citing.)
- "Ind AS 109 does not prescribe the methods... prone to a lot of subjectivity, judgement and complexity for NBFCs". It is "an enormous challenge ... especially for small and medium sized as well as closely held entities" (search summary of BCAJ article) — https://bcajonline.org/journal/implementation-of-expected-credit-loss-model-for-non-banking-financial-companies/ (date unknown).
- Data quality and availability, plus the lack of a "single customer level identifier", are named as key challenges (BDO India, Standard Stance Vol 13) — https://www.bdo.in/getmedia/f9e47607-d6da-49ae-b778-25df3a8ec4ad/The-Standard-Stance_BDO-India_Vol-13.pdf.
- Audit focus: whether ECL data is "complete, accurate, and derived from reliable source systems", and "errors in aging, days-past-due computation, or incorrect linkage of source data to ECL models" (search summary) — SKP: https://suditkparekh.com/pdf/ind-as-109-ecl-modelling-key-judgements-and-practical-challenges-skpcollp.pdf ; RSM India NBFC whitepaper (~Oct 2025): https://www.rsm.global/india/sites/default/files/media/thumbnails/1-0CT-25/RSM%20India%20Whitepaper%20-%20NBFCs%20-%20Financial%20Reporting%20-%20Key%20Considerations%207.pdf
- Older Big-4 primers (2017, **>3 yrs old**): KPMG "Demystifying ECL" https://assets.kpmg.com/content/dam/kpmg/in/pdf/2017/07/Demystifying-Expected-Credit-Loss.pdf ; BDO "ECL Simplified" https://www.bdo.in/getmedia/00bdaa48-d483-4c18-b2df-288434bedd26/Expected-Credit-Losses-Simplified-A-BDO-India-Publication-2017.pdf.aspx?ext=.pdf&disposition=attachment ; Wipro comparison of 3 banks https://www.wipro.com/applications/ind-as-109-expected-credit-loss-ecl-computation/.
- Small portfolios with sparse migration data produce "zero counts and high count volatility" and "intersecting forward PDs" (arXiv 1708.00062, search summary) — https://arxiv.org/pdf/1708.00062.
- Open-source ECL is thin. The GitHub `ifrs9` topic's top repo has only 21 stars **[verified]** — https://github.com/topics/ifrs9. The best reference I found is ShrishDhuria/IFRS9_ECL **[verified]**, described below.
- **Implication for v2:** the unmet need is less "a better PD model" and more a *DPD/staging engine that cannot be wrong* plus a data-quality checker, a documented overlay register and an auditor-ready output pack.

### Theme 7: Practitioner skill demand is Excel/VBA + Python + SQL for automating risk reporting
- Job postings repeatedly ask for automating "risk reporting and reconciliation tools using Python and SQL" alongside Excel/VBA, and for knowing "Greeks, PVBP, VaR, and Stress Testing" (snippet-only) — https://builtin.com/job/market-risk-analyst/7034996 ; https://corporatefinanceinstitute.com/resources/career-map/sell-side/risk-management/market-risk-analyst.
- Bloomberg PORT's claimed reach is "93 of the top 100 asset managers", "47,000 active users" (vendor press, snippet-only) — https://www.bloomberg.com/company/?p=10829. This places PORT, rather than Aladdin, as the everyday analytics tool for many PMs.
- **Caveat:** I have **no direct practitioner testimony** (Reddit, QSE or forums were all blocked) on what people use daily. This theme rests on job ads and vendor claims only.

---

## 2. "Built-my-own" projects and tutorials

| Name | Author | Date | Stack | What's good | Link |
|---|---|---|---|---|---|
| portfolio-risk-dashboard | zongmaow | 2026 (4 commits, 0 stars) | Python, Streamlit, yfinance, Plotly | 3 VaR methods + ES. Student-t Monte Carlo. **Kupiec POF + Christoffersen** backtests on lagged VaR (avoids look-ahead). Regime-aware violations, stress scenarios, sector exposure [verified] | https://github.com/zongmaow/portfolio-risk-dashboard |
| Portfolio_Value-at-Risk_Engine_and_Dashboard | apiwit1604 | 2026 (114 commits, MIT) | Streamlit, NumPy/SciPy, SLSQP, yfinance + **FRED yield curves** | Multi-asset: bonds, FX, European options, forwards. Kupiec backtest. Usable as a package or as a dashboard [verified] | https://github.com/apiwit1604/Portfolio_Value-at-Risk_Engine_and_Dashboard |
| portfolio-risk-optimizer | ParidhiBhardwajj | 2026 | Streamlit, yfinance, scipy, Plotly | MPT frontier, VaR/CVaR, MC vs SPY & 60/40. **Openly admits in-sample bias** [verified] | https://github.com/ParidhiBhardwajj/portfolio-risk-optimizer |
| IFRS9_ECL | ShrishDhuria | Jun 2026 (2 stars) | NumPy, Matplotlib, Streamlit, Excel mirrors, PPT | 4-trigger SICR waterfall (relative PD, absolute PD, qualitative, 30-DPD). Vasicek macro→PIT PD. 3-scenario weighting. **Excel workbooks mirror Python cell-for-cell for auditability**. 41 tests in CI [verified] | https://github.com/ShrishDhuria/IFRS9_ECL |
| casparser | codereverser | active 2024–2026 (231 stars, MIT) | Python, PyMuPDF, Pydantic | Parses CAMS/KFintech/NSDL/CDSL CAS → JSON/CSV + Schedule 112A gains [verified] | https://github.com/codereverser/casparser |
| mftool | NayakwadiS | active (257 stars, MIT) | Python | AMFI NAVs (live + historical), scheme lists, an MCP server [verified] | https://github.com/NayakwadiS/mftool |
| Riskfolio-Lib | Dany Cajas | v7.3, 2026 (4.5k stars, BSD-3) | Python, CVXPY | 26+ convex risk measures (CVaR, EVaR, CDaR, Ulcer…), HRP/HERC/NCO, Black-Litterman [verified] | https://github.com/dcajasn/Riskfolio-Lib |
| PyPortfolioOpt | Robert Martin | active (6.1k stars, MIT) | Python | Shrinkage covariance. README warns clearly about estimation error [verified] | https://github.com/robertmartin8/PyPortfolioOpt |
| QuantStats | Ran Aroussi | active (7.7k stars, Apache-2.0) | Python | Tear sheets, HTML reports, drawdowns, MC [verified] | https://github.com/ranaroussi/quantstats |
| Ghostfolio | ghostfolio | active (9.4k stars, AGPLv3) | NestJS, Angular, Postgres, Redis | Self-hosted multi-account tracker with basic "static analysis" risk rules [verified] | https://github.com/ghostfolio/ghostfolio |
| Wealthfolio | afadil | active (9.1k stars) | Rust/Tauri, React, SQLite | Local-first and private, TWR, addon SDK [verified] | https://github.com/afadil/wealthfolio |
| open-risk (transitionMatrix, portfolioAnalytics, openNPL) | Open Risk | various | Python | Credit transition matrices, loss-distribution tests, NPL data platform [verified listing] | https://github.com/open-risk |
| Show HN: portfolio risk monitor w/ alerts | unknown | ~2026 | unknown | Broker OAuth sync, risk thresholds, weekly summaries (snippet-only) | https://news.ycombinator.com/item?id=46896523 |
| Show HN: CashGraphs | unknown | ~2022 (>3y) | unknown | Optimizer with non-normal returns and tail specs (snippet-only) | https://news.ycombinator.com/item?id=32118796 |
| VaR tutorials (Medium ×3, QuantInsti, PyQuantNews, Ryan O'Connell, DataCamp, Data Intellect) | various | various | Python/Excel | Standard 3-method VaR walkthroughs (all snippet-only; fetch blocked) | https://medium.com/@nabil.nouali/mastering-value-at-risk-var-in-python-a-complete-guide-to-the-three-essential-methods-5d1552202a76 ; https://blog.quantinsti.com/calculating-value-at-risk-in-excel-python/ ; https://www.pyquantnews.com/free-python-resources/calculate-value-risk-python-three-methods ; https://ryanoconnellfinance.com/monte-carlo-method-value-at-risk/ ; https://dataintellect.com/blog/calculating-var-using-monte-carlo-simulation/ |

---

## 3. Unmet needs (inferred; strength of evidence noted)

1. **India-native data plumbing:** reliable CAS import (CAMS/KFin/NSDL/CDSL), AMFI NAV history, NSE/BSE prices, total-return series. *Evidence: strong* (casparser issue churn; empty `mutual-funds-india` topic; Ghostfolio has little India-specific coverage).
2. **MF look-through risk:** stock- and sector-level overlap, concentration and factor exposure *across* funds, not just fund-level XIRR. *Evidence: moderate* (freefincal, FundSageAI, Business Standard; snippet-only).
3. **A bridge between trackers and risk systems:** trackers (Ghostfolio, Wealthfolio) do performance; institutional tools (PORT, Aladdin, Barra) do risk. Nothing lightweight, transparent and self-hostable does both for India. *Evidence: moderate.*
4. **Backtested, explainable risk numbers:** almost no DIY dashboards backtest their VaR. The ones that do stand out. *Evidence: moderate* (GitHub sample).
5. **Auditability as a feature:** versioned runs, input snapshots, Excel export that matches Python. *Evidence: strong* for spreadsheet pain (HN, old) and the ECL audit focus (snippet-only). The IFRS9_ECL repo shows the "Excel mirror" pattern.
6. **Small-NBFC ECL toolkit:** DPD/staging engine, data-quality validator (missing DPD, broken customer IDs, aging errors), PD from sparse data (pooling, vintage/roll-rate), documented management-overlay register, and auditor/RBI disclosure pack. *Evidence: moderate* (Big-4/CA literature, snippet-only). Practitioner first-hand voice is **missing** because forums were blocked.
7. **Transparency vs black-box vendors:** the Aladdin "single data model" is admired, but concentration and opacity are criticised. *Evidence: weak to moderate* (HN snippets).

## 4. Common mistakes to avoid (with evidence)

1. **Normal-distribution VaR at 99%** understates tail loss, and fat tails matter more at higher confidence levels. *Evidence:* search summaries of arXiv VaR literature (https://arxiv.org/pdf/2101.08559 ; https://arxiv.org/pdf/1310.4538; snippet-only). DIY repos still default to parametric-normal [verified: ParidhiBhardwajj, apiwit1604 README notes normality "understat[es]" tails]. **Do:** historical / filtered-HS + Student-t, plus ES alongside VaR.
2. **No VaR backtesting.** **Do:** Kupiec + Christoffersen, as in zongmaow [verified].
3. **Look-ahead bias:** using same-day data to estimate the VaR you test against. **Do:** lag the estimate by one day (zongmaow explicitly lags [verified]).
4. **In-sample optimisation shown as performance:** ParidhiBhardwajj README admits this inflates metrics [verified].
5. **Overfitting mean-variance optimisers:** PyPortfolioOpt README says sample covariance has "high estimation error, which is particularly dangerous in mean-variance optimization" and MV "portfolios ... underperform out-of-sample" [verified]. **Do:** shrinkage (Ledoit-Wolf), weight caps, HRP, robust or risk-parity options.
6. **Historical VaR assumes stationarity:** "volatility and correlations change over time" (search summary of arXiv/QSE-type content; snippet-only). **Do:** EWMA/GARCH vol scaling and regime views.
7. **Mixing price returns with total returns** (dividends, MF IDCW, splits). yfinance-based dashboards are prone to this. *Evidence: inferred.* Every sampled dashboard relied on yfinance and none documented its total-return handling. **Do:** use adjusted close or TRI, and label which one is used.
8. **Survivorship bias** from using today's index constituents or live MF schemes only. *Evidence: inferred, not found in a source I could open.* **Do:** keep merged and closed schemes in AMFI history.
9. **Ignoring liquidity / small-cap impact:** no sampled DIY tool models liquidity horizon. *Evidence: inferred.* **Do:** liquidity-adjusted VaR or days-to-liquidate using ADV.
10. **"Unknown" sector / bad mappings silently dropped:** zongmaow notes exotic tickers fall to "Unknown" [verified]. **Do:** surface unmapped exposure as its own bucket.
11. **ECL-specific:** DPD/aging errors, broken customer IDs, sparse-data PD term structures that cross over, undocumented overlays, and no reconciliation to the GL. *Evidence:* snippet-only Big-4/CA sources and arXiv 1708.00062.
12. **Fragile PDF parsing dependencies:** CAMS parsing broke with PyMuPDF ≥1.25.0 [verified issue #106]. **Do:** pin versions and keep golden-file tests.

## 5. Bibliography (accessed 2026-10-02)

**Verified (page opened):**
- https://github.com/zongmaow/portfolio-risk-dashboard
- https://github.com/apiwit1604/Portfolio_Value-at-Risk_Engine_and_Dashboard
- https://github.com/ParidhiBhardwajj/portfolio-risk-optimizer
- https://github.com/ShrishDhuria/IFRS9_ECL
- https://github.com/codereverser/casparser and /issues
- https://github.com/NayakwadiS/mftool
- https://github.com/dcajasn/Riskfolio-Lib
- https://github.com/robertmartin8/PyPortfolioOpt
- https://github.com/ranaroussi/quantstats
- https://github.com/ghostfolio/ghostfolio (and /issues?q=india)
- https://github.com/afadil/wealthfolio
- https://github.com/open-risk
- https://github.com/topics/ifrs9 ; https://github.com/topics/portfolio-risk ; https://github.com/topics/xirr ; https://github.com/topics/mutual-funds-india

**Snippet-only (search result seen, page not opened; re-verify):**
- HN: 13906770, 5198376, 5198416, 15756062, 15819016, 45722639, 43330206, 35432421, 14019500, 43490345, 13403061, 46896523, 32118796, 24428206, 36284990, 41465735, 46006016, 45833816, 46265459, 44491686 (all at https://news.ycombinator.com/item?id=<id>)
- BlackRock 10-K FY2022: https://www.sec.gov/Archives/edgar/data/1364742/000095017023004343/blk-20221231.htm
- Bloomberg PORT press: https://www.bloomberg.com/company/?p=10829
- NBFC ECL: BDO (2 PDFs), RSM India whitepaper, SKP PDF, BCAJ article, KPMG 2017, Wipro, ifrstech blog (URLs in Theme 6)
- arXiv: 1708.00062, 2101.08559, 1310.4538
- India retail: FundSageAI blog, freefincal overlap (goodreads mirror), Business Standard Apr 2025
- VaR tutorials: Medium (quaintitative, nabil.nouali, serdarilarslan), QuantInsti, PyQuantNews, Ryan O'Connell, Data Intellect, DataCamp
- Aladdin alternatives: https://www.limina.com/blackrock-aladdin-vs-simcorp ; https://www.globaltrading.net/deutsche-borse-to-offer-alternative-to-blackrocks-aladdin/ ; https://www.infoq.com/presentations/portfolio-analysis-scale/ ; https://wallstreetfintech.substack.com/p/jody-kochansky-building-the-operating

**Not reached:** Reddit (all subs), Quant StackExchange, YouTube, LinkedIn, Wilmott, Nuclear Phynance.
