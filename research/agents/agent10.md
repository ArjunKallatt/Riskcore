# Agent 10 — Gap Analysis & Critic (Riskcore)

Research date: 2026-10-02. Inputs: agent1.md–agent9.md (all read in full) and the existing repo (`riskcore/{data,metrics,stress,sample}.py`, `app.py`, `tests/test_riskcore.py`).
No web access was used. Every verdict below comes from comparing the agents with each other and from my own domain knowledge, which is labelled **[BK]**. Line references look like `a8:L97`, meaning agent8.md, line 97.

**Overall:** Agents 1–9 were all blocked by the proxy and most of their claims are search-snippet level. The open-source licence and maintenance data (Agent 4: GitHub API, PyPI JSON, LICENSE files read) and Agent 3's BlackRock API schemas are the only **primary-verified** evidence. Regulatory dates and thresholds (Agents 2, 5, 8) are mostly secondary sources. Use them for design, but do not hard-code them until checked against the primary PDFs.

---

## 1. Contradictions between agents

| # | Topic | Side A | Side B | Verdict |
|---|---|---|---|---|
| C1 | **Indian price data source** | a4:L132,L176 rates jugaad-data **H (core)**: "Primary free EOD price, index-TRI and RBI-rate source… fallback order jugaad → nselib → yfinance". | a6:L160,L179 says to use a **broker API** as primary and "avoid automated NSE scraping in anything you distribute… NSE ToS prohibit systematic or automated data collection". Agent 4 itself concedes this in its own ToS row (a4:L214). | **Agent 6 is right for anything published.** Agent 4 assessed the *code licence* (jugaad is public domain), not the *data licence*. Use jugaad/nselib only as an opt-in **local, user-run** adapter that is off by default in the hosted demo. The hosted demo should run on synthetic data, AMFI NAVs and user-uploaded CSVs. |
| C2 | **OpenBB licence** | a4:L144 and a7:L31: Apache-2.0. Agent 4 read the LICENSE file; Agent 7 marks it [P]. | a6:L62: "Free (AGPL, U)". | **Apache-2.0 for current releases** (two primary reads beat one memory). There is an open issue, though: a4:L144 says the API reports the owner as **`openbq-org/OpenBB`**, a name one letter off from the real org. That looks like a typo-squat or misread. Check the canonical org and PyPI publisher before installing. In any case OpenBB is not needed for the MVP. |
| C3 | **Architecture shape** | Agent 3 (a3:L188–241) is **domain-model-first**: security master by type/subtype, a positions table with `source ∈ {POSITION, ORDER, TRADE}`, ABOR lots, compliance rules with DRAFT→APPROVED lifecycle, a violations inbox, and an append-only event log. FastAPI is "optional". | Agent 7 (a7:L148–203) is **pipeline-first**: `providers/ → store/ (Parquet + DuckDB) → models/ → results/run_id → ui/`, with Prefect, Postgres, FastAPI and Evidence.dev at stage 2. | **They are compatible but both over-scoped for 6 weeks.** Take Agent 7's folder layout and its "models never do I/O; every number carries a run_id" rules. From Agent 3 take only the *security master with asset_class/type* and the *limit-rule shape* (filter, group_by, warning, breach) as a YAML file. **Drop** for now: rule lifecycle states, ORDER/TRADE positions, ABOR lots, FastAPI, Prefect, Postgres and Evidence.dev. Evidence.dev is also a Node/JS toolchain, which adds a second language for a Python-only developer. |
| C4 | **Per-client instances** | a3:L241: "What not to copy: per-client instances". | a7:L170: stage 3 is "on-prem k8s at an NBFC" for data residency. | Not really a conflict. For NBFCs, **local-first / self-hosted** is the right *distribution* model (borrower PII, DPDP Act). Build it as a pip-installable package plus `streamlit run`, not as multi-tenant SaaS. |
| C5 | **Aladdin language** | a3:L86: Java core (job ads), plus a multi-language messaging layer. | a9:L35: HN snippet from about 2017 says Aladdin is "being largely written/re-written in Julia". | **Java core.** The Julia claim is a stale, snippet-only HN comment. **[BK]** BlackRock used Julia for some analytics, not to rewrite Aladdin. This does not affect the build. |
| C6 | **Aladdin scale figure** | a3:L37: ~$25T on platform (marketing / third-party site). a3:L38: $21.6T (2020, FT, unverified). | a3:L289 (tmcnet): "orchestrates $11T". | These measure different things: assets on the platform versus BlackRock's own AUM. Do not quote any of them in Riskcore copy. |
| C7 | **Who must apply Ind AS 109 ECL** | a2:L107: "NBFCs already follow Ind AS 109". a8:L110 says the same. | a8:L86–89: Ind AS applies only to NBFCs with net worth ≥ ₹500 cr (FY19), or listed, or net worth ₹250–500 cr (FY20). | **This matters for the v2 thesis.** Most small unlisted NBFCs (net worth < ₹250 cr), which are the *target market* in a2:L92–107, are **not on Ind AS**. They follow Indian GAAP plus **RBI IRACP** provisioning (standard-asset % plus NPA ageing buckets). For them the must-have is a correct **DPD → SMA/NPA → IRACP provision** engine. ECL is nice-to-have, or for Ind AS NBFCs only. a8:L94 hints at 2026 IRACP amendments that touch ECL for NBFCs; this is unverified and should be checked first. |
| C8 | **RBI bank ECL dates** | a2:L105: final 27 Apr 2026, effective 1 Apr 2027, glide path to 31 Mar 2031, excludes SFBs/PBs/RRBs. | a8:L97–110: the same dates, plus draft 7 Oct 2025 and Discussion Paper 16 Jan 2023. a5:L135–136 gives "Jan 2023" and "Draft 2025" without dates (unverified). | **Agents 2 and 8 agree.** Agent 8's [S-official] RBI press-release URL is the best lead. The reference no. "RBI/DOR/2026-27/398" is unverified. The regulation **does not apply to NBFCs**, so it is only relevant if Riskcore later targets banks. Keep it as a configurable "floor table", not a v2 core feature. |
| C9 | **Gold-loan rules** | a2:L86,L229: "RBI final gold loan LTV norms April 2026" (IIFL blog). | a8:L119: final Directions issued **6 Jun 2025**, amended 29 Sep 2025, **comply by 1 Apr 2026**. Tiered LTV 85/80/75%. | Consistent: April 2026 is the compliance date, not the issue date. **[BK]** The 85/80/75 tiers by ticket size (₹2.5L / ₹5L) match my recollection. Agent 8 flags that it is unclear whether the tiers apply to income-generating loans; that needs the primary text. |
| C10 | **NBFC NPA norm** | a8:L77: the NBFC move to 90 DPD has "dates [UNVERIFIED]". | a8:L75: SMA/NPA at 90 DPD. | **[BK]** The SBR glide path for NBFC-BL was >150 DPD by Mar 2024, >120 DPD by Mar 2025 and >90 DPD by Mar 2026. As of Oct 2026, 90 DPD should apply to all layers. Still, make the NPA threshold a dated parameter so historical tapes can be reclassified. |
| C11 | **SMA day-count** | a8:L75: "SMA-0 1–30, SMA-1 31–60, SMA-2 61–90" **and**, in the same bullet, "SMA-1 at day-end once it has been continuously overdue for 30 days… NPA on the 90th day". | Same paragraph. | This is an **off-by-one ambiguity**, and it is the most likely bug in a v2 engine. **[BK]** The RBI 12 Nov 2021 circular includes a worked example (due 31 Mar → SMA-1 30 Apr → SMA-2 30 May → NPA 29 Jun). Encode that example as a golden test. |
| C12 | **Riskfolio-Lib risk-measure count** | a1:L48: "13+". | a4:L32: "about 24". a9:L87: "26+". | This is just documentation drift. It does not matter. |
| C13 | **IFRS 9 OSS maturity** | a4:L119: naenumtou/ifrs9 has **130 stars**. | a9:L67: the "GitHub `ifrs9` topic's top repo has only 21 stars". | Both can be true, because the topic page only lists repos tagged with it. The conclusion holds either way: **there is no maintained, licensed IFRS 9 library.** naenumtou has no licence, and ShrishDhuria/IFRS9_ECL is MIT but has only 2 stars and is a few months old. |
| C14 | **IIMA factor data** | a5:L49: verified "Yes"; working paper dated 2013. | a6:L97: "U"; cites the same authors as **2014**. a1:L143: BK. | The 2013 working paper and the 2014 date refer to the same work. Treat the **URL and the data's terms of use as unverified**. The data is academic, and redistribution rights are unknown. Fetch it at runtime with attribution and do not bundle it. |
| C15 | **PyPortfolioOpt home** | a4:L34: moved to `PyPortfolio/PyPortfolioOpt`. | a9:L88: `robertmartin8/PyPortfolioOpt`. | Probably a redirect. Install from PyPI, which avoids the question. |
| C16 | **MSCI's India scenarios** | a1:L83 reads as if RiskManager's library includes "India-specific: 2016 demonetisation, 2018 IL&FS". | The cited source is a search snippet of MSCI's generic page. | **This is a misattribution.** Those India events are Agent 1's *suggestions*. Do not claim MSCI has them. |
| C17 | **AMFI liquidity stress participation rate** | a8:L41: default 20% (user-editable). The AMFI rate itself is unverified. | — | **[BK, moderate confidence]** The AMFI methodology uses about **10% of the 3-month average traded volume** and excludes the bottom 20% of holdings by liquidity. Default to 10% and label it, because a 20% default would make liquidity look about twice as good. Verify before shipping. |
| C18 | **Repo size** | a7:L19: "about 280 lines". | Actual count: about 173 lines in `riskcore/`, about 70 in `app.py`, about 40 in tests. | Trivial. |

---

## 2. Claims that most need manual verification (ranked by impact on the build)

| Rank | Claim | Where | Why it is suspicious or important | How to verify |
|---|---|---|---|---|
| 1 | Small NBFCs need Ind AS 109 ECL (implied market gap) | a2:L92–107 | Contradicted by the Ind AS roadmap (C7). If wrong, v2's headline feature targets the wrong customers. | Read the MCA Ind AS roadmap and the latest RBI NBFC IRACP directions (2025/26 consolidation). Ask two NBFC CFOs or CAs. |
| 2 | AMFI old NAV-history format "available only till 30 Sep 2026" | a6:L37,L159 | A single snippet, two days before the research date. **It directly breaks MF history ingestion**, which is v1's most important data feed. | Open amfiindia.com NAV download. Also test mfapi.in and captn3m0/historical-mf-data, which avoid the endpoint. |
| 3 | NSE ToS bans automated collection, with a carve-out for "available for download" | a6:L30,L179 | Decides whether a bhavcopy downloader can ship. The carve-out wording is snippet-level. | Read the ToS in full. Assume the conservative reading until a lawyer says otherwise. |
| 4 | SEBI IA/RA amendments (16 Dec 2024, guidelines 8 Jan 2025) and finfluencer rules | a8:L52–54, L271–279 | Defines what v1 may display (for example, whether an optimiser's "target weights" count as advice). The circular numbers are unverified. | Read the SEBI IA Regulations as amended and the Jan 2025 guidelines. Get a one-hour legal opinion before a public launch. |
| 5 | SMA/NPA day-count and borrower-level contagion | a8:L73–82 | Core v2 logic. An off-by-one error makes every number wrong (C11). | Read the RBI 12 Nov 2021 circular example and turn it into a test. |
| 6 | Gold LTV tiers, bullet-loan LTV on the maturity amount, valuation basis (30-day average vs previous close, 22 ct) | a8:L119–126 | v2's distinctive feature. The valuation basis is explicitly unverified. | Read RBI Notification Id=12859 and the 29 Sep 2025 amendment. |
| 7 | IRACP provisioning % for standard / substandard / doubtful / loss assets for NBFCs | a8:L82 (unverified) | Needed for the dual-book engine. | RBI NBFC prudential norms (consolidated directions). |
| 8 | Ind AS shortfall → Impairment Reserve (13 Mar 2020) | a8:L90–93 | A strong differentiator, but secondary-sourced (FIDC copy). | The RBI circular via the RBI index. |
| 9 | yfinance "personal use only" | a6:L53, a4:L140 | The existing MVP relies on yfinance. | Read the yfinance README (Agent 6 opened it) and Yahoo's terms. Confirmed enough to act on: keep yfinance as a prototype provider only. |
| 10 | jugaad-data "YOLO" licence = public domain | a4:L132 | Fine for code, but it bundles NSE endpoints (C1). | The LICENSE was read. The ToS question remains separate. |
| 11 | OpenBB owner `openbq-org` | a4:L144 | Possible supply-chain red flag (C2). | Check `pip show openbb` and the PyPI maintainers, or simply don't install it. |
| 12 | ShrishDhuria/IFRS9_ECL "41 tests, Excel mirrors cell-for-cell" | a4:L120, a9:L84 | A 2-star, months-old repo; the same author also appears in a7:L34. Plausible, but it is a hobby project. | Clone it and run its tests. Use it as a checklist, not a dependency. |
| 13 | AMFI liquidity stress parameters | a8:L39 vs my recollection (C17) | Sets the default for a v1 headline feature. | Read the AMFI stress-test format (Feb 2024 letter and any 2025–26 revisions). |
| 14 | Riskometer score bands and PRC CRV thresholds | a8:L24, L33 | Needed only for the "shadow riskometer". Risky if the result is presented as official. | SEBI MF Master Circular 27 Jun 2024, annex. |
| 15 | Streamlit Community Cloud limits (690 MB–2.7 GB, sleeps after 12 h) and "external PRs paused" | a7:L89, L104 | The docs say "as of February 2024", which may be stale. This affects the Monte Carlo path budget for the demo. | Deploy and observe. |
| 16 | HF Spaces Docker/Streamlit now paid | a7:L105 | Contradicts many blogs. Low impact. | Check the hub-docs pricing page. |
| 17 | Kaggle Home Credit / Give Me Some Credit = non-commercial | a6:L130–131, L173 | Affects bundling demo data. **[BK]** Competition data is generally limited to the competition and non-commercial or academic use. | Read each competition's rules tab. Default: don't redistribute it; use synthetic data. |
| 18 | Third-party price estimates (Moody's $17k–$4.8M, Addepar $65k–$400k, "28% of institutions use Excel for IFRS 9") | a2:L94, L103; a1:L40 | Vendor-SEO and aggregator figures. Fine for colour, not for a pitch deck. | Ignore for the build. |
| 19 | "Crediwatch EWS flags distress up to 12 months ahead" and "Kaleidofin ~3% lower 90+ DPD" | a2:L45, L48 | Vendor marketing claims. | Don't benchmark against them. |
| 20 | Polygon rebranded "Massive"; Twelve Data / EODHD NSE coverage and prices | a6:L55–59 | All unverified (U). Only matters if you buy a feed. | Check when budgeting a paid feed. |

**Implausible or overreaching items:**
- a3:L37 "$25T", which comes from businesstats.com, is low reliability.
- a1:L32 Bloomberg AIM "15,000 users / 900+ firms" and a9:L72 PORT "47,000 users" are vendor press figures.
- a5:L62 (arXiv 2205.10535) has an unconfirmed title.
- a5:L80–81 are 2024/2026 arXiv items whose authors are guessed.
- a8:L135 (liquilens RFA timelines) is flagged by Agent 8 itself as low quality.

None of these should be quoted.

---

## 3. Market gaps (with evidence)

### Indian retail investors (v1)

| Gap | Evidence | Strength | Comment |
|---|---|---|---|
| **Tail and liquidity risk for a combined MF + direct equity + US stock portfolio, in INR, free and transparent** | Indian tools do XIRR, overlap and "health scores" (a1:L50–58). Portfolio Visualizer caps the free tier at 15 assets (a1:L45). Trackers like Ghostfolio and Wealthfolio have no VaR or factor risk (a9:L49–51). | Moderate | The most defensible v1 positioning: "risk, not tracking". |
| **Robust CAS import** (CAMS/KFin/NSDL/CDSL) | casparser issue churn in 2025–26 (a9:L54). The GitHub topic `mutual-funds-india` is empty (a9:L57). | Strong | casparser is MIT. Wrap it, pin PyMuPDF, and add golden fixtures. |
| **MF look-through** (stock/sector exposure across funds) | Morningstar India free X-Ray status is uncertain (a1:L54, L175). The freefincal tool is a Google Sheet (a9:L56). | Moderate | **The data is the hard part:** each AMC publishes monthly portfolios in its own Excel format, with no clean free API **[BK]**. Defer to v1.5, or start with the top 10 AMCs. |
| **Liquidity stress (days-to-liquidate) for retail small-cap portfolios** | SEBI/AMFI mandates it for MFs (a8:L38–41). No DIY tool models liquidity (a9:L119). | Moderate | Cheap to build once ADV data is available (bhavcopy volumes). Clearly India-specific. |
| **Backtested VaR shown to users** | Almost no DIY dashboards backtest (a9:L104, L112). | Moderate | It is a credibility signal more than a user demand. |
| **Debt/bond risk for retail** (duration, credit buckets, PRC-like view) | PRC matrix (a8:L29–35). Proposed SEBI Credit Risk-o-Meter (a8:L26). | Weak–moderate | Most retail bond exposure is through debt MFs. Use factsheet YTM, modified duration and rating mix rather than bond pricing. |

### Small and mid NBFCs (v2)

| Gap | Evidence | Strength | Comment |
|---|---|---|---|
| **One lightweight tool for DPD/SMA/NPA + IRACP provisioning + (optional) Ind AS ECL + concentration + gold stress + EWS** | Enterprise suites only (a2:L94). Indian LOS/LMS vendors show no confirmed ECL engine (a2:L96). ICRA ECL 3.0 is Excel plus managed service (a2:L49). | Moderate (snippet-level) | The gap is in **integration and auditability**, not in models. |
| **Dual-book IRACP vs Ind AS with Impairment Reserve** | RBI 13 Mar 2020 (a8:L90–95). | Moderate | Only for Ind AS NBFCs (C7). Still a sharp differentiator, because no vendor in a2 mentions it. |
| **Gold-loan MTM LTV monitor and price-shock stress under the 2025 Directions** | "No vendor surfaced a dedicated product" (a2:L86). New tiered LTV rules (a8:L119–130). Gold-price risk commentary (CRISIL Jun 2026, Fitch; a2:L86). | Moderate | Small, well-defined and topical. **The best v2 wedge.** |
| **Loan-tape data-quality validator** (DPD/aging errors, broken customer IDs) | Audit focus in SKP/RSM/BDO material (a9:L63–64). | Moderate | Cheap with pandera. Auditors care about it. |
| **Co-lending / DLG partner tracker** | DLG cap of 5% (a8:L154–158). | Weak | Niche. Later. |

**Caveat on the NBFC gap:** demand evidence is all vendor or consultant snippets. There is **no buyer testimony**; forums were blocked (a9:L73, L106). NBFCs buy through auditors and consultants and are wary of open-source tools that touch borrower PII. Validate the gap with 3–5 conversations before building past week 6.

---

## 4. Open-source composition (licence-safe) and what to write in-house

### Compose (all permissive; confirmed by Agent 4 via GitHub/PyPI/LICENSE)

| Layer | Use | Licence | Note |
|---|---|---|---|
| Core | numpy, pandas, scipy, statsmodels, scikit-learn (LedoitWolf, PCA, logit) | BSD | Already in use or trivial to add. |
| UI | streamlit, plotly | Apache / MIT | Keep. |
| Storage | pyarrow (Parquet), duckdb | Apache / MIT | DuckDB is single-writer (a7:L47): the pipeline writes Parquet and the UI reads it. |
| Vol / VaR | **arch** (GARCH, FHS) | NCSA | One dependency covers EWMA/GARCH/FHS. |
| KPIs (test oracle) | empyrical-reloaded (tests only) | Apache | Cross-check your own metrics. Don't add quantstats as well: overlapping libraries mean more breakage. |
| Calendars | exchange_calendars (XBOM) | Apache | Close enough to NSE. Verify holiday parity. |
| MF data | mftool, or plain AMFI NAVAll.txt + captn3m0/historical-mf-data (MIT) | MIT | Prefer the raw AMFI file plus the SQLite backfill: fewer moving parts. |
| CAS import | casparser | MIT | Pin PyMuPDF (a9:L54). |
| Fixed income (v1.5) | QuantLib | BSD | Only once actual bonds are held. Use a duration proxy before then. |
| Validation | pandera, hypothesis | MIT / MPL-2.0 | pandera for loan-tape and holdings schemas. **[BK]** Hypothesis is MPL-2.0 (file-level copyleft). Fine as a test-only dependency. |
| v2 scoring (later) | optbinning | Apache | Only when a PD scorecard is needed. Not in the 6-week plan. |
| Optimiser (optional, later) | **one** of skfolio or Riskfolio-Lib | BSD | Don't ship three optimisers (a4:L183). See §7 on advice risk. |

**Avoid:** FinancePy, nsepython, backtrader, fortitudo.tech and open-risk/portfolioAnalytics (GPL); ghostfolio and QuantLib-Risks-Py (AGPL); rateslib (non-commercial); vectorbt (Commons Clause); ArcticDB and sdv Copulas (BSL); mlfinlab (proprietary); naenumtou/ifrs9 (no licence: read it, don't copy it). Source: a4:L200–214, a7:L30.

**Vendor rather than depend:** open-risk transitionMatrix (cohort estimator) and concentrationMetrics (HHI/Gini). Both stopped releasing on PyPI in 2022 (a4:L17, L112–113). The formulas are about 50 lines and their licences are Apache/MIT. Keep the attribution.

### Write in-house (this is the product)

1. **`providers/`**: AMFI, CSV/CAS upload, yfinance (prototype), synthetic, and an opt-in local NSE bhavcopy adapter, with a disk cache and data-health flags (stale, missing, unmapped).
2. **Security master + FX layer**: `asset_id`, class, currency, sector, ISIN/AMFI code; INR conversion of USD holdings. **This is currently missing**: `data.py` mixes USD-priced US tickers with INR without conversion.
3. **Total-return correctness**: TRI benchmarks; LIQUIDBEES-style dividend-in-units ETFs (price return ≈ 0); IDCW plans.
4. **VaR/ES engine + backtests**: historical, EWMA-parametric and FHS; Kupiec, Christoffersen and Basel traffic light (about 150 lines; a5:L149).
5. **India scenario library (YAML)** and conditional stress propagation (Kupiec 1998, a5:L73).
6. **Liquidity engine**: days-to-liquidate at X% participation.
7. **Limit rules (YAML)**: single-name, sector and asset-class caps, with breaches.
8. **v2: loan-tape schema + validator; DPD → SMA/NPA engine; IRACP provisioning; staging; simple ECL; gold LTV MTM and stress; concentration (HHI, top-20).**
9. **Run store + Excel/PDF report export** with an inputs hash and parameter-table version.

---

## 5. What is genuinely hard, and how to de-risk it

| Hard thing | Why | De-risk |
|---|---|---|
| **Legal data supply for Indian prices** | NSE/BSE ToS, index IP, Yahoo terms (a6:L179–189). | Hosted demo = synthetic + AMFI + uploads. Price fetching runs **on the user's machine** with the user's own source: broker API, bhavcopy they downloaded, or yfinance. Budget for a licensed feed only if this becomes commercial. |
| **Total returns, corporate actions, survivorship** | yfinance adjusted close is not TRI. LIQUIDBEES pays returns as units. Merged MF schemes disappear (a9:L117–118). | Use TRI benchmarks. Add a per-asset `return_basis` flag. Keep closed schemes. Add a "data health" page. |
| **Mixed-calendar / mixed-currency portfolios** | US and India close at different times. Asynchronous closes understate correlation. FX is missing. | Convert to INR using a daily FX series. Offer weekly-return covariance for cross-market portfolios. Align on exchange_calendars. |
| **Bond pricing in India** | Most corporate bonds don't trade. Valuation curves (CRISIL/ICRA, FIMMDA spread matrix) are paid or members-only (a6:L82–84, a1:L196). | v1: model debt via **debt-MF NAV + factsheet modified duration/YTM + rating buckets**. Direct bonds via "G-sec curve (NSS fit to RBI DBIE yields) + rating spread bucket" matrix pricing, labelled as an estimate. QuantLib only for G-secs/SDLs. |
| **MF look-through holdings** | AMC monthly portfolio files differ by AMC; there is no free API. | Defer. Start with a manual upload template, then build parsers for the top AMCs. |
| **VaR model validation** | Short Indian histories, regime shifts (a9:L116). | Rolling backtest with lagged VaR (a9:L113). Show the traffic light in the UI. Use property tests (a7:L116). |
| **Regulatory interpretation (v2)** | Day-count, contagion, restructured accounts, upgrade rules, NPA thresholds over time, and consolidation of directions (a8:L13, L292–296). | Put every threshold in a **dated, cited parameter table**. Turn RBI worked examples into golden tests. Get a practising CA to review the IRACP outputs before claiming "compliance". Market it as "decision support". |
| **ECL without default history** | Small NBFCs have sparse data. PD curves cross (a9:L66). | Use roll-rate (DPD-bucket Markov) PDs with pooling and floors. Add a management-overlay register. **Don't build survival or ML PD in v2.** |
| **Model validation on synthetic data** | Synthetic tapes validate code, not models. | State this honestly on the page. Calibrate synthetic aggregates to RBI FSR / CRIF PAR figures (a6:L171–172). |
| **Trust and PII** | NBFCs won't upload borrower data to a hobby SaaS. DPDP Act (a8:L288). | Local-first: pip install plus a local Streamlit app, with no telemetry. |
| **Solo maintainer bandwidth** | Scrapers break, regulations change. | Few dependencies, adapters behind one interface, CI with recorded fixtures. Not scraping at all removes most of the breakage. |

---

## 6. Differentiation (ranked)

1. **India-correct data plumbing**: CAS import, AMFI NAV history, TRI benchmarks, INR-converted global holdings, an explicit return basis, and a data-health page. Every DIY dashboard gets this wrong (a9 Themes 3 and 5).
2. **Backtested, explained risk**: VaR/ES with Kupiec, Christoffersen and traffic light visible in the UI, plus a methodology page per metric. Almost no competitor shows whether its numbers are any good (a9:L104).
3. **India scenario library with conditional propagation**: demonetisation (Nov 2016), IL&FS (Sep 2018), taper tantrum (2013; also INR −20%), COVID (Mar 2020), Franklin Templeton debt wind-up (Apr 2020), the 2022 rate cycle and Adani (Jan 2023). Each is stored as data with narrative and source.
4. **Liquidity risk for retail portfolios** (SEBI-style days-to-liquidate) alongside VaR.
5. **v2 wedge: gold-loan LTV MTM and price-shock stress plus IRACP (and Ind AS dual-book) provisioning in one auditable run.** Narrow, topical, and no vendor surfaced it (a2:L86).
6. **Auditability**: `run_id`, inputs hash, parameter-table version with citations, and an Excel export that ties out to the screen (a9 Theme 1; a9:L84 "Excel mirrors").
7. **Local-first / self-hosted, permissive licence (Apache-2.0)**: suits privacy-minded retail users (a9:L50) and PII-constrained NBFCs.
8. **"Shadow" regulatory views** (portfolio riskometer, PRC position), always labelled "Riskcore estimate". These are useful, but carry impersonation risk (a8:L281–283), so they rank last.

---

## 7. Scope critique and legal/ToS risks

### Cut or defer from the original plan

| Cut / defer | Reason |
|---|---|
| **Optimisation** (PyPortfolioOpt / Riskfolio / BL / HRP), currently in the README roadmap | Crowded (a9 Theme 3). Overfits (a9:L115). **Target weights move toward "investment advice"** under the SEBI IA rules (a8:L272). Keep only user-driven what-if (already built). |
| FastAPI, Prefect/Dagster, Postgres, Docker, `st.login`, Evidence.dev | Stage-2 infrastructure for users who don't exist yet (a7 §5). Cron plus Parquet plus DuckDB is enough. |
| Aladdin-style compliance lifecycle, ORDER/TRADE positions, ABOR lots, LLM copilot | Enterprise patterns (a3 §7). Use YAML limits only. |
| Barra-style fundamental factor model | Months of work. Use an IIMA four-factor time-series regression if anything (v1.5). |
| EVT, copulas, Monte Carlo with vine copulas, Entropy Pooling | Adds marginal value over FHS plus a scenario library. |
| v2: survival/ML PD, scorecards, IRB capital, CECL toggle, PCA dashboard, ICAAP-lite, DLG tracker, RFA queue, Vasicek economic capital | Each is a project in itself (a8 §2.7–2.10, a5). The 6-week v2 slice is: DPD/IRACP + simple roll-rate ECL + gold stress + concentration. |
| Bank ECL floors (RBI 2026) | Not applicable to NBFCs (C8). Add later as a parameter table. |
| Tax-harvesting, options Greeks, broker OAuth sync | Off-mission. Tax features add their own liability. |
| Global equities beyond "US stocks held by Indians" | Converting USD holdings to INR is enough. |

### Legal / ToS risks

| Risk | Severity | Action |
|---|---|---|
| **Using employer data, code or know-how** (the user works on lending products) | **High** | Never use employer loan tapes, parameters, PD curves, vendor documents or code, even "anonymised". Check the employment contract for IP-assignment, moonlighting and conflict-of-interest clauses before publishing v2. **[BK]** In India, in-employment restrictions and IP assignment are generally enforceable; post-employment non-competes generally are not (s.27 Contract Act). Build v2 only on public regulation, public papers and synthetic data. Make commits on personal time and personal hardware. Consider written employer clearance. |
| **SEBI IA/RA rules** | High for a public v1 | Descriptive analytics only. No buy/sell/hold, no "best fund", no model portfolios, no AMC or distributor referral income. A disclaimer on every page. A legal opinion before any monetisation (a8:L271–279). |
| **NSE/BSE scraping and redistribution** | High if hosted | No scraping in the hosted app. Make the local adapter opt-in with a ToS notice. Never redistribute bhavcopy or index values (a6:L179–180). |
| **Yahoo/yfinance** | Medium | Prototype only. Keep the synthetic fallback (already in the code). |
| **Kaggle / Freddie / Fannie datasets** | Medium | Methods research only. Don't commit them to the repo or bundle them. Ship synthetic tapes (a6:L173, L186–187). |
| **Index / benchmark IP** (Nifty TRI, FBIL, LBMA) | Medium | Fetch at runtime on the user's machine and don't redistribute (a6:L184). |
| **Trademark** ("mini-Aladdin" in README.md) | Low–medium | Don't use BlackRock's mark in the name or tagline. Say "inspired by institutional risk platforms". |
| **Impersonating official labels** (riskometer, PRC, APMI) | Medium | Always use the "Riskcore estimate" label (a8:L281–283). |
| **DPDP Act / borrower PII** (v2) | Medium | Local-first, sample data only in demos, no telemetry. |
| **Dependency licences** | Low (if §4 is followed) | Add a CI licence check (`pip-licenses --fail-on GPL;AGPL`). |

### Bugs and gaps in the existing code (worth fixing first)

- `data.py`: USD-priced US tickers are mixed with INR with no FX conversion. `ffill()` across holiday-misaligned calendars creates artificial zero returns, which bias vol and correlation downward.
- `app.py`: tickers with no data are **silently dropped** (`holdings.loc[asset_rets.columns]`) (a9:L120). The benchmark falls back to the cross-sectional mean with only a warning.
- `metrics.sharpe` uses rf=0. With Indian T-bills at about 6–7%, that overstates Sharpe materially. Use a configurable rf, defaulting to the 91-day T-bill.
- VaR is 1-day only, with no horizon option and no backtest. ES at 97.5% is missing.
- `stress.py`: `fx_exposure` is added on top of a historically estimated beta that already contains some FX sensitivity (for example TCS/INFY), so FX is partly double-counted. Shocks are linear with no conditional propagation, and gold has no shock factor (GOLDBEES' beta to Nifty is about 0, so a "2008" scenario misses gold's rally or fall).
- `sample.py`: LIQUIDBEES has price return ≈ 0 because it pays returns as units, so it looks riskless and returnless. This is a concrete total-return bug example.

---

## 8. Proposed MVP and 6-week roadmap

Assumed capacity: about 10–12 h/week (3 evenings plus weekend), about 65 h in total. Weeks 1–4 are v1; weeks 5–6 are a thin v2 slice. Each week ends with green tests and a deployable demo.

### v1 (portfolio risk)

| Must-have | Nice-to-have |
|---|---|
| Refactor into `providers/ models/ store/ ui/pages` (Agent 7 layout, minus the API) | Shadow riskometer / PRC view (labelled estimate) |
| Holdings upload (CSV template) + **CAS import (casparser)** | IIMA 4-factor regression exposures |
| AMFI NAV provider (daily file + historical backfill) + yfinance (prototype) + synthetic; disk cache; data-health page | MF look-through (manual holdings upload) |
| INR conversion for USD assets; `return_basis` flag; TRI benchmark where available | GARCH/FHS VaR via `arch` |
| VaR/ES: historical + EWMA-parametric at 95/99/97.5%, 1–10 day horizon | Weekly-return covariance option for cross-market portfolios |
| **VaR backtest page**: Kupiec, Christoffersen, traffic light | Debt view: factsheet duration/YTM/rating buckets |
| Risk contributions (exists), correlation, drawdown, rolling vol; configurable rf | PDF report |
| **India scenario library (YAML)** + conditional propagation + gold and rates factors | Optional local NSE bhavcopy adapter (opt-in, ToS notice) |
| **Liquidity: days-to-liquidate X% (ADV, participation default 10%)** | — |
| YAML limit rules (single-name, sector, asset class) with breach table | — |
| Run store (Parquet + run_id + inputs hash) + Excel export | — |
| Disclaimers; methodology page; Apache-2.0 licence; README without "Aladdin" branding | — |

### v2 (NBFC loan book), first slice only

| Must-have | Nice-to-have |
|---|---|
| Loan-tape schema (borrowing openNPL entity ideas) + **pandera validator** (missing DPD, duplicate IDs, negative balances, date logic) | Ind AS 109 dual-book + Impairment Reserve table |
| **Synthetic NBFC tape generator** (gold, MSME, vehicle, personal), seeded | Roll-rate Markov lifetime PD + 3-scenario weighting |
| **DPD → SMA-0/1/2 → NPA engine** with borrower-level contagion and the "all arrears cleared" upgrade rule; golden tests from RBI examples | EWS rule library (about 10 rules) → watchlist |
| **IRACP provisioning** (dated parameter table) | Vintage curves, roll-rate matrix chart |
| Simple ECL: stage = f(DPD 30/90 + flags); ECL = PD₁₂ₘ/lifetime × LGD × EAD by segment, with user-supplied PD/LGD | Granularity adjustment |
| **Gold LTV engine**: ticket-size tier caps, bullet maturity-LTV, gold-price shock slider (−10/−20/−30%) → breaches, shortfall ₹ | Rate-shock NII impact |
| Concentration: HHI and top-20 by borrower / sector / geography / product | — |
| Excel "auditor pack": stage/bucket movement, provision by bucket, parameter-table version | — |

### 6-week plan (builds on the existing code)

| Week | Goal | Deliverables (concrete) | Exit test |
|---|---|---|---|
| **1** | Foundations + fix existing bugs | Package restructure (`providers/base.py` Protocol; move `data.py` → `providers/yfinance.py`, `providers/synthetic.py`); `pyproject.toml`; config rf; FX conversion; explicit dropped-ticker warning; licence file; README de-branding; CI (ruff, pytest, licence check) | Existing 5 tests pass; new tests for FX conversion and dropped tickers |
| **2** | India data + holdings import | AMFI NAV provider (NAVAll + captn3m0 SQLite backfill, defensive parser for the format change); CSV and CAS upload (casparser, pinned PyMuPDF, 2–3 anonymised fixtures you create yourself); security master table; disk cache; data-health page; `return_basis` handling (fixes the LIQUIDBEES case) | MF + equity + US portfolio loads offline from fixtures |
| **3** | Credible risk numbers | `models/market/var.py` (historical, EWMA, horizons, ES 97.5%); `models/validation/var_backtest.py` (Kupiec, Christoffersen, traffic light, lagged VaR); Hypothesis properties (CVaR ≥ VaR, monotone in confidence, contributions sum to 1); backtest page | Backtest on seeded synthetic series reproduces the expected exception counts |
| **4** | Stress + liquidity + limits + run store | Scenario YAML (6–8 India events, cited); conditional propagation (Kupiec 1998); add gold and rates factors; liquidity engine; YAML limits + breach table; `store/` Parquet run_id + Excel export; methodology and disclaimer pages; **deploy v1 demo (synthetic + AMFI)** | v1 demo live; Excel export ties out to the screen |
| **5** | v2 core: loan tape → DPD → IRACP | Loan schema + pandera validator; synthetic tape generator; DPD/SMA/NPA engine with contagion and upgrade rule; IRACP parameter table (dated, cited, marked "verify"); golden tests from the RBI 12 Nov 2021 examples | Golden RBI example passes; 100k-loan tape runs in < 10 s |
| **6** | v2 wedge: gold + ECL-lite + concentration + pack | Gold LTV engine + shock slider; simple staging + ECL by segment; HHI/top-20; auditor Excel pack; Loan Book page; **user-validation step: show it to 3–5 NBFC risk or finance people (not your employer's colleagues) before going further** | Synthetic gold book under −20% shock shows breach count and ₹ shortfall; feedback notes captured |

**After week 6, prioritise by feedback:**
- If NBFC interest is real: dual-book Ind AS + Impairment Reserve, roll-rate lifetime PD, EWS rules.
- If not: v1.5 work (FHS/GARCH, factor regression, MF look-through, debt view).

**Keep doing throughout:** re-verify the top-10 items in §2 against primary sources, in order, before each dependent feature ships.
