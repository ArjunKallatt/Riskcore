# Agent 2 – Commercial Credit-Risk / Loan-Book Software Scan (for Riskcore v2)

Research date: 2026-10-02. Prepared for Riskcore v2, an NBFC/bank loan-book risk module covering concentration, PD/LGD/EAD, ECL under Ind AS 109 / IFRS 9, stress testing and early-warning signals (EWS).

## How the research was done, and how far to trust it

- **WebFetch was blocked for every domain I tried** ("EGRESS_BLOCKED" from the network egress proxy): moodys.com, ma.moodys.com, sas.com, spglobal.com, experian.com, crif.in and wikipedia.org. Because of this, **I could not open any page directly**, and following links two levels deep was not possible.
- **Everything below comes from WebSearch result titles, URLs and the snippets the search engine extracted.** The URLs appeared in real search results, so they are real. However, I did not open the pages to read them in full.
- **WebSearch ran out partway through.** The session's 200-call search limit was reached during the last batch, so some vendors were only lightly covered.
- Evidence labels used in the table:
  - **S** = backed by a search-result snippet from the vendor's own domain.
  - **S3** = backed by a third-party snippet only (reseller, news site, directory or blog).
  - **BK** = my background knowledge, not checked against any source. Treat it as a hint only.
  - **unverified** = I found nothing.
- Pricing: I did not see an official list price for any enterprise vendor. Every "not public" entry means no price appeared on the vendor's own pages in search. Third-party price estimates are shown with an S3 label.
- Source dates: anything more than 3 years old (before Oct 2023) is marked **[OLD]**.

---

## (a) Comparison table

ECL = handles expected credit loss (IFRS 9 / CECL / Ind AS 109). Stress = has portfolio stress testing / scenario analysis. Y? = likely, but backed only by weak evidence (BK or S3).

| Platform | Category | Key features | Target users | ECL | Stress | Pricing | Link | Verified | Source date |
|---|---|---|---|---|---|---|---|---|---|
| **Moody's CreditLens** | Commercial-lending lifecycle platform | Origination, spreading, scoring/risk rating, workflow, portfolio monitoring; part of the Moody's Lending Suite | Commercial banks (snippet: "weighted toward regional and global banks") | N (ECL sits in ImpairmentCalc / Credit Loss & Impairment suite) | N (not in snippets) | Not public. Licensed per module ("optional modules ... additional fee") | https://www.moodysanalytics.com/microsites/the-creditlens-solution/resources/credit-management-articles | S + S3 (aloan.ai, AWS blog) | Launched 2017 (biia.com); AWS blog undated |
| **Moody's RiskCalc** | Private-firm PD model | Financial-statement PD for middle-market firms; 10 ratios from 17 inputs; built on the Credit Research Database; 20+ country models | Banks lending to private and SME corporates | Feeds ECL (supplies PD) | Y? (BK: has stressed-PD mode) | Not public | https://www.moodys.com/sites/products/ProductAttachments/MA_RiskCalc_FactSheet.pdf | S (snippet only) | Factsheet undated; North America fact sheet is v1.0 **[OLD]** |
| **Moody's CreditEdge (EDF)** | Market-implied PD / EWS | Daily EDF (PD) for 42k+ public firms, term structure up to 10 years; EDF Early Warning Toolkit; example: Carillion flagged 6 months before default | Banks, investors, corporates | Feeds ECL | Y? (BK) | Not public | https://www.moodys.com/web/en/us/insights/credit-risk/advances-in-default-detection-and-early-warning.html | S | Training decks 2019 **[OLD]**; AI features PR 2020 **[OLD]** |
| **Moody's ImpairmentCalc** (+ Credit Loss & Impairment Analysis Suite) | ECL engine | Takes user asset classes plus PD/LGD/EAD; converts through-the-cycle (TTC) PD or internal ratings to a point-in-time (PIT) PD term structure; probability-weighted multiple scenarios; Stage 1/2/3 staging; produces fair value, gross carrying amount and amortised cost; runs standalone or inside the suite | Banks under IFRS 9 / CECL | **Y** | Y (scenario-weighted macro) | Not public | http://ma.moodys.com/rs/961-KCJ-308/images/SP39812_MA_ImpairmentCalc.pdf | S (snippet only; PDF blocked) | Undated; Risk.net awards 2019 **[OLD]** and later "IFRS 9 solution of the year" (risk.net/awards/7954555, undated) |
| **S&P Global Credit Analytics** (PD Model Market Signals, PD Fundamentals, RiskGauge) | PD/scoring models + data | PDMS: 1–5 year PD for public corporates and financial institutions; enhanced Merton model with country and industry factors; 86k+ companies; RiskGauge blends fundamentals and market signals; covers rated and unrated, public and private firms | Banks, asset managers, corporates | Y (separate IFRS 9 impairment solutions page) | unverified | Not public | https://www.spglobal.com/market-intelligence/en/solutions/credit-risk-solutions ; https://www.spglobal.com/market-intelligence/en/solutions/ifrs-9-solutions | S | Research piece Mar 2026; brochure undated |
| **SAS Expected Credit Loss / Solution for IFRS 9 / Allowance for Credit Loss** | ECL platform | Modular calculation and reporting; model templates, workflows, rules and reporting packs; point-and-click interface; governed, automated workflow; in-memory engine; sits on an integrated risk-finance platform (stress, ALM, model risk management) | Banks and lenders under IFRS 9 / CECL; India page exists | **Y** | **Y** (integrated) | Not public | https://www.sas.com/en_in/solutions/risk-management/solution/expected-credit-loss.html ; https://www.sas.com/en_us/software/allowance-for-credit-loss.html | S | SAS Communities posts 2024 |
| **SAS Stress Testing** | Enterprise stress testing | Regulatory and business-as-usual stress tests; scenario repository; credit-portfolio stress models; auditable intermediate results; Basel III/IV reporting (Standard Chartered is a customer) | Large banks | Y (links to ECL) | **Y** | Not public | https://www.sas.com/en_us/solutions/risk-management/solution/stress-testing.html | S | SAS Communities 2024–25; climate stress press release Nov 2025 |
| **FICO Platform / FICO Scores (India)** | Decisioning + scores | Decision management, segmentation and scorecards, low-latency high-volume decisions; FICO Score for India (built on bureau data); FICO Score X Data India (alternative data, with Lenddo); India customers AU Bank (vehicle loans), Axis Bank (card over-limit) | Large banks, card issuers, auto lenders | N (not in snippets) | N (not in snippets) | Not public | https://www.fico.com/en/newsroom/global-fico-score-set-new-credit-risk-scoring-standard-india ; https://www.fico.com/en/industries/banking | S | Undated |
| **Experian PowerCurve** | Decisioning / strategy / collections | Strategy design studio, content gallery, analytical data mart, runtime; Strategy Management covers acquisition, portfolio and debt decisions; PowerCurve Collections with machine learning | Banks and lenders across the lifecycle | N | N (strategy simulation only, BK) | Not public | https://www.experian.co.uk/business/platforms/powercurve | S | Launch PR 2012 **[OLD]**; UK page undated |
| **CRIF / CRIF High Mark (India)** | Bureau + analytics/software | India bureau; EWS on retail borrowers (IDBI pilot, Dec 2018); CRIF group has an IFRS 9 solution page (UAE site) | Banks, NBFCs, MFIs | Y (CRIF group, UAE page); India unverified | unverified | Not public | https://www.crif.ae/solutions/ifrs9/ ; https://en.wikipedia.org/wiki/CRIF_High_Mark_Credit_Information_Services | S3 (Wikipedia) + S (title only) | EWS pilot 2018 **[OLD]** |
| **TransUnion CIBIL** | Bureau | Consumer and commercial reports, CIBIL Score, portfolio re-pulls for monitoring, Detect & Fraud Suite | Banks, NBFCs, HFCs, insurers | N | N | Not public | https://www.transunioncibil.com/product/cibil-commercial-report | S3 (rfp.wiki) + S (product page title) | Undated |
| **Equifax India** | Bureau + portfolio reviews | Retail and MFI Portfolio Review (early warning of delinquency); Microfinance Pulse reports (with SIDBI); serves 7,000+ banks and NBFCs | Banks, NBFCs, MFIs | N | N | Not public | https://www.equifax.co.in/business/all-products/ | S | MFI Pulse Vol XXVI, Mar 2026 |
| **Oracle OFSAA – LLFP / IFRS 9 Solution Cloud Service** | ECL + finance/risk data platform | Loan Loss Forecasting & Provisioning upgraded for IFRS 9; cloud service covering classification & measurement, impairment and hedge accounting; SICR-based 12-month vs lifetime ECL; ECL overview and detail reports; regional templates | Large banks | **Y** | **Y** (Enterprise Stress Testing & Capital Planning; Stress Testing & Scenario Analytics) | Not public | https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/ifrs9-solution-cloud/25d/ifrsr/expected-credit-loss-overview-reports.html | S | Docs 24c/25d (2024–25); LLFP 8.0.x guides **[OLD]** |
| **Oracle OFS Credit Risk Management** | Credit risk analytics | 300+ prebuilt reports (credit quality, reserves, delinquency, migration, capital, **concentration**); counterparty risk; delinquency management | Large banks | Y (integrates) | **Y** | Not public | https://www.oracle.com/a/ocom/docs/industries/financial-services/ofs-credit-risk-management-ds.pdf | S | Undated datasheet |
| **Finastra Fusion Risk (ARC)** | Balance-sheet risk + regulatory reporting | IFRS 9 module (classification, measurement, impairment, hedge accounting); Basel II/III/IV credit RWA; dashboards; customers include FINCA Impact Finance (microfinance) | Banks, MFIs, emerging markets (e.g. Indonesia) | **Y** | Y? (BK; ALM/stress likely) | Not public | https://www.finastra.com/solutions/arc | S | ARC PDF Dec 2022 **[OLD]** |
| **Wolters Kluwer OneSumX IFRS 9 / Credit Risk** | Finance-risk-regulatory platform | Contract-level IFRS subledger; ECL accounting schemes; ECL by individual or collective segments; multi-scenario ECL; uses internal ratings and TTC PD; scenario and stress testing across credit/counterparty parameters (deterministic or stochastic) | Banks | **Y** | **Y** | Not public | https://www.wolterskluwer.com/en-sg/solutions/onesumx-for-finance-risk-and-regulatory-reporting/onesumx-ifrs-9 | S | Undated |
| **Quantifi** | Trading/derivatives risk | XVA, counterparty exposure (EE, PFE), RWA, limits, market risk; commodity counterparty risk management system (CCRMS) | Banks' trading desks, energy and commodity firms | N (not a loan-book ECL tool) | Y (market/counterparty) | Not public | https://www.quantifisolutions.com/counterparty-risk/ | S | Energy Risk award 2026 |
| **Nucleus Software FinnOne Neo** | Lending system (origination, servicing, collections) | Customer acquisition, loan management, collections; credit scoring; analytics; 540+ APIs; "Lending-in-a-Box" cloud; NBFC brochure; customers Saarathi Finance, Esskay Fincorp | Banks and NBFCs (retail, MSME, housing, microfinance) | unverified (not a risk/ECL product per snippets) | N | Not public | https://www.nucleussoftware.com/finnone-neo/ | S | NBFC PDF Dec 2023; Saarathi news Aug 2025 |
| **Perfios** | Data/underwriting SaaS | Bank-statement analysis, automated Credit Assessment Memo, monitoring; acquired Clari5 (fraud) Feb 2025; 500+ financial institutions | Banks, NBFCs, fintechs | N | N | Not public | https://perfios.com/credit-monitoring-platform | S | 2025 |
| **Crediwatch** | EWS / portfolio monitoring | AI/ML continuous monitoring; 200+ configurable alerts; distress signals "up to 12 months in advance"; listed on Microsoft Marketplace | Banks, NBFCs (incl. housing-finance books needing EWS) | N | N | Not public (Marketplace listing exists) | https://about.crediwatch.com/about/product/early-warning-systems | S | Undated |
| **Lentra** | Cloud lending platform | GoNoGo origination, MultiBureau, BREx rule engine; Growth Alliance Program for NBFCs targeting ₹1,000 cr+ AUM; pay-as-you-go | Banks, NBFCs, HFCs | N | N | "Pay-as-you-go" (S3); amounts not public | https://lentra.ai/ | S + S3 | Undated |
| **CredAble** | Working-capital / supply-chain-finance platform | Invoice discounting, receivables/payables finance, configurable underwriting; 35+ banks and NBFCs | Banks, NBFCs, corporates | N | N | Not public | https://credable.in/ | S | Undated |
| **Kaleidofin (ki score / ki view)** | Alternative-data scoring + portfolio view | ML score (1–100, lower is better); ki view for portfolio monitoring; 35M-customer database; claims ~3% lower 90+ DPD on accepted books; Federal Bank is a partner | Banks and NBFCs with microfinance / informal-sector books | N | N | Not public | https://www.kaleidofin.com/lending-as-a-service | S + S3 | Undated |
| **ICRA Analytics ECL 3.0** | **India ECL tool + managed service** | Segmentation and staging policy; 12-month and lifetime PD; macro forward-looking adjustments with multiple scenarios; LGD; EAD; probability-weighted ECL; **Excel-based data input**; reporting for management and auditors; quarterly ECL as a service for housing, LAP, vehicle, infrastructure and lease-rental-discounting (LRD) books | **NBFCs** (snippet: "trusted by top private and public sector NBFCs") | **Y (Ind AS 109)** | Y (macro scenarios) | Not public | https://www.icraanalytics.com/risk-management-offerings-solutions/solutions-and-tools/expected-credit-loss | S | Undated |
| **CRISIL Risk Solutions** (now part of the CRISIL/S&P group) | Consulting + models | Ind AS 109 provisioning analysis (webinar); IFRS 9 model upgrade for a global bank | Banks, NBFCs | Y (services) | unverified | Not public | https://www.crisil.com/en/home/events/crisil-webinar/risk-solutions/ind-as-109-provision-pain-ahead-for-lenders.html | S | Webinar undated (likely 2017–18, **[OLD]** BK) |
| **Acies TechWorks – Kepler** | **India-built IFRS 9 / ECL suite** | Risk models, effective interest rate (EIR), ECL, automated model validation, out-of-the-box disclosures, scenario simulation with "virtually unlimited" stress scenarios; clients in 20+ countries; Risk.net IFRS 9 Solution of the Year 2025 | Banks, NBFCs, insurers, corporates (Kepler for Corporates) | **Y** | **Y** | Not public | https://www.acies.consulting/keplerifrs9.html | S | Award Jun 2025 |
| **ECL Square** | **Cloud ECL SaaS for India** | Ind AS 109 / IFRS 9 ECL for loan books and trade receivables; SaaS; dedicated NBFC page | NBFCs, corporates | **Y** | unverified | Not public (not in snippet) | https://eclsquare.com/solutions/for-nbfcs | S (snippet only) | Undated |
| **Roopya** | NBFC lending SaaS (LOS, LMS, EWS, collections) | EWS module with behavioural risk scores; ECL explainer page; claims 5–7 day go-live; 300+ APIs | Small and mid NBFCs, fintechs | unverified (blog page only; no confirmed ECL module) | N | Not public ("free demo") | https://roopya.money/early-warning-signal/ | S | Undated |
| **TCS BaNCS** | Core banking | Only found a TCS whitepaper on ECL provisioning systems; no BaNCS ECL module confirmed | Banks | unverified | unverified | Not public | https://www.tcs.com/content/dam/global-tcs/en/pdfs/insights/whitepapers/deploying-efficient-expected-credit-loss-provisioning-system.pdf | S (whitepaper title) | Undated |
| **Mphasis** | IT services | Builds credit and counterparty risk applications for clients; no product found | Banks | unverified | unverified | n/a | https://www.mphasis.com/home/industries/banking-capitalmarkets/corporate-banking.html | S | Undated |
| **Aryaa / Aptus** | — | Nothing found. "Aptus" is likely Aptus Value Housing Finance, which is a lender rather than a vendor (BK) | — | unverified | unverified | — | — | unverified | — |

---

## (b) Notes

### Which platforms do what (summary)

- **ECL (IFRS 9 / Ind AS 109), with snippet evidence:**
  - Global: Moody's ImpairmentCalc, SAS (ECL / IFRS 9 / ACL), Oracle OFSAA (LLFP / IFRS 9 Cloud), Finastra Fusion Risk, Wolters Kluwer OneSumX, S&P (IFRS 9 solutions page).
  - India: ICRA Analytics ECL 3.0, Acies Kepler, ECL Square, CRISIL (services).
- **Portfolio stress testing, with snippet evidence:** SAS Stress Testing, Oracle Enterprise Stress Testing & Capital Planning / Stress Testing & Scenario Analytics, OneSumX, Acies Kepler, and macro scenarios inside Moody's ImpairmentCalc and ICRA ECL 3.0.
- **Small and mid NBFCs explicitly targeted:**
  - ICRA ECL 3.0 (Excel input plus a quarterly managed service).
  - ECL Square (NBFC page).
  - Roopya (lending SaaS with EWS).
  - Lentra G.A.P. (₹1,000 cr+ AUM; origination, not risk).
  - Crediwatch (EWS for NBFCs).
  - Kaleidofin (microfinance).
  - Nucleus FinnOne Neo NBFC brochure (lending core, not risk).
- **Indian EWS players:** Crediwatch, Roopya, CRIF High Mark (2018 pilot), Equifax Portfolio Review, CIBIL portfolio re-pulls. Accumn (hello.accumn.ai) also appeared in results but was not researched.

### Features worth copying into Riskcore v2

1. **TTC to PIT PD conversion and PD term structure** (Moody's ImpairmentCalc). Let users upload an internal rating or TTC PD and get a PIT lifetime PD curve, using a Vasicek / Z-factor shift driven by a macro scenario.
2. **Probability-weighted multi-scenario ECL** (Moody's, ICRA, OneSumX). Use three scenarios (base, upside, downside) with editable weights and show the ECL from each scenario next to the weighted total.
3. **Explicit staging-policy engine** (ICRA, OneSumX, Oracle). Make the SICR rules configurable: DPD > 30 goes to Stage 2, DPD > 90 or NPA goes to Stage 3, plus rating downgrade and restructured flags. Ind AS 109 does not prescribe a method, so a transparent and editable policy is a selling point.
4. **Excel-in, auditor-ready report out** (ICRA ECL 3.0). Mid-size NBFCs live in Excel. Accept an Excel/CSV loan tape and export an auditor pack showing stage movements, ECL roll-forward (opening, new, repaid, stage transfers, write-off, closing) and assumptions used.
5. **Individual vs collective ECL** with segment-level aggregation (OneSumX).
6. **Configurable alert library** (Crediwatch has 200+ alerts). Start with about 15–20 rule-based EWS alerts on the loan tape: DPD roll-forward, bounce counts, LTV breach, bureau score drop, sector concentration breach, and repeated restructuring.
7. **Gold-loan mark-to-market LTV monitor.** No vendor surfaced a dedicated product for this. RBI tells lenders to monitor gold portfolios closely (Business Standard, May 2025). CRISIL Ratings (Jun 2026) stress-tested 25 years of gold prices, and Fitch says another 15% price fall is a risk. Build a gold-price shock slider (-10/-15/-20/-30%) that shows LTV breaches, the count of loans needing margin calls or auctions, and shortfall in rupees.
8. **Prebuilt concentration and migration reports** (Oracle's 300+ reports include concentration and risk migration). Ship HHI and top-20 borrower, sector and geography concentration, plus a DPD-bucket transition matrix.
9. **Regulatory vs business-as-usual stress modes** (SAS). Keep RBI-style prescribed shocks (rate +200 bps, PD multipliers, gold -20%) separate from user-defined scenarios.
10. **Contract-level audit trail** (OneSumX subledger). Persist per-loan ECL inputs and outputs for every run so results can be reproduced.
11. **Daily market-implied PD for listed borrowers** (CreditEdge, S&P PDMS). This can be an optional add-on for corporate books, using a Merton-style PD from NSE equity prices.

### The gap for small and mid NBFCs

The global ECL and stress-testing platforms (Moody's, SAS, Oracle OFSAA, OneSumX, Finastra) are enterprise suites. They are priced per module and not publicly. Third-party estimates (S3, vendr.com / investables.ai) put Moody's spending anywhere from about $17k to $4.8M a year, with a median of about $72.5k, and implementations described as "multi-month to over a year". In practice these are bought by large banks.

Indian lending platforms (Nucleus FinnOne Neo, Lentra, Roopya, Perfios, CredAble) cover origination, servicing and collections, but none of them showed a confirmed ECL or stress-testing engine in the snippets. The bureaus (CIBIL, Equifax, CRIF High Mark) sell data and portfolio reviews, not provisioning engines.

The mid-market ECL options that do target NBFCs are:
- ICRA Analytics ECL 3.0: Excel-based, often delivered as a quarterly consulting service.
- Acies Kepler: award-winning, enterprise-leaning.
- ECL Square: SaaS.

None of them publishes a price. None was seen combining **ECL + concentration + stress testing (including gold-price shocks) + EWS** in one lightweight tool. Many small NBFCs therefore run Ind AS 109 ECL in spreadsheets maintained by auditors or consultants, and run EWS separately, if at all. (This is background knowledge, consistent with ICRA offering ECL as a service. One snippet citing research found that 28% of institutions used Excel for IFRS 9.)

The regulatory push is growing. RBI's final ECL framework for scheduled commercial banks was issued on 27 Apr 2026 and takes effect 1 Apr 2027, with a glide path to 31 Mar 2031 (S3: jmfinancialservices.in, bankingfinance.in). RBI also expects EWS for some NBFC books (S3: Crediwatch / Elets) and closer gold-loan monitoring.

A Python/Streamlit tool that takes a loan-tape CSV, applies a transparent staging policy, computes probability-weighted lifetime ECL, runs rate and gold shocks, flags concentration and EWS breaches, and exports an auditor-ready pack would fill this gap credibly. One caveat: the RBI bank framework excludes SFBs, payment banks and RRBs, and NBFCs already follow Ind AS 109. Riskcore's ECL defaults should therefore follow Ind AS 109 first and RBI prudential floors second.

### What to verify next (needs WebFetch access or more search budget)

- Open the Acies Kepler, ICRA ECL 3.0 and ECL Square pages to confirm feature lists and any pricing tiers.
- Confirm whether CRIF High Mark India sells an Ind AS 109 product. The crif.in pages were blocked.
- Check TCS BaNCS, Mphasis, Aryaa and Accumn.
- Check the dates of Moody's product pages.

---

## (c) Bibliography

Every URL below appeared in a WebSearch result. I did **not** open any page, because WebFetch was blocked. Dates are taken from the URL or snippet where one was available.

**Moody's**
- https://www.moodysanalytics.com/microsites/the-creditlens-solution/resources/credit-management-articles
- https://aws.amazon.com/blogs/migration-and-modernization/moodys-transforms-creditlens-change-management-platform-with-innovative-serverless-architecture/
- https://www.biia.com/moodys-analytics-launches-the-creditlens-platform/ (2017 launch) [OLD]
- https://aloan.ai/compare/aloan-vs-moodys (third-party, 2026)
- https://www.moodys.com/web/en/us/about-us/innovation-technology/saas.html
- https://www.moodys.com/sites/products/ProductAttachments/MA_RiskCalc_FactSheet.pdf
- https://www.moodys.com/sites/products/ProductAttachments/RiskCalc%20Version%201.0%20North%20America.pdf [OLD]
- https://www.moodys.com/web/en/us/insights/credit-risk/advances-in-default-detection-and-early-warning.html
- https://www.moodys.com/sites/products/ProductAttachments/CreditEdge_brochure.pdf
- https://ma.moodys.com/rs/961-KCJ-308/images/CreditEdge%20Training%20-%20September%2011%202019.pdf [OLD, 2019]
- https://www.businesswire.com/news/home/20200824005363/en/Moodys-Analytics-Strengthens-CreditEdge-and-RiskCalc-Platforms-with-AI-Powered-Features [OLD, 2020]
- http://ma.moodys.com/rs/961-KCJ-308/images/SP39812_MA_ImpairmentCalc.pdf
- http://ma.moodys.com/rs/961-KCJ-308/images/Credit-Loss-Impairment-Analysis-Suite.pdf
- https://www.moodys.com/web/en/us/insights/banking/ifrs-9-impairment-regulations.html
- https://www.risk.net/awards/6756371/risk-technology-awards-2019-moodys-analytics [OLD]
- https://www.risk.net/awards/7954555/ifrs-9-solution-of-the-year-moodys-analytics
- https://investables.ai/blog/how-much-does-moodys-analytics-cost (third-party pricing estimate)
- https://www.vendr.com/marketplace/moodys (third-party pricing estimate)
- https://ma.moodys.com/rs/961-KCJ-308/images/5.24.11%20-%20CreditLens%20Release%20Notes.pdf?version=0

**S&P Global**
- https://www.spglobal.com/market-intelligence/en/solutions/credit-risk-solutions
- https://www.spglobal.com/content/dam/spglobal/mi/en/documents/general/ineeddata-Credit-Analytics-Product-Brochure.pdf
- https://pages.marketintelligence.spglobal.com/Credit-Analytics-RiskGauge-Demo.html
- https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/03/pricing-risk-in-unrated-companies (Mar 2026)
- https://www.spglobal.com/market-intelligence/en/solutions/ifrs-9-solutions
- https://pages.marketintelligence.spglobal.com/IFRS-9-Website.html

**SAS**
- https://www.sas.com/en_us/solutions/risk-management/solution/expected-credit-loss.html
- https://www.sas.com/en_in/solutions/risk-management/solution/expected-credit-loss.html
- https://www.sas.com/en_ae/software/solution-for-ifrs-9.html
- https://www.sas.com/content/dam/SAS/documents/product-collateral/product-brief/en/sas-solution-for-ifrs9-108636.pdf
- https://www.sas.com/en_us/software/allowance-for-credit-loss.html
- https://www.sas.com/en_us/solutions/risk-management/solution/stress-testing.html
- https://www.sas.com/en_us/software/solution-for-stress-testing.html
- https://www.sas.com/en_in/customers/standard-chartered-bank.html
- https://www.sas.com/en_us/news/press-releases/2025/november/climate-stress-testing-report.html (Nov 2025)
- https://communities.sas.com/t5/SAS-Communities-Library/Resilient-Finance-SAS-Stress-Testing-Calculation-Process/ta-p/953332
- https://communities.sas.com/t5/SAS-Communities-Library/What-is-SAS-Allowance-for-Credit-Loss/ta-p/918407

**FICO / Experian**
- https://www.fico.com/en/newsroom/global-fico-score-set-new-credit-risk-scoring-standard-india
- https://investors.fico.com/news-releases/news-release-details/new-fico-credit-scores-provide-lenders-opportunity-expand-access
- https://www.fico.com/en/industries/banking
- https://www.experian.co.uk/business/platforms/powercurve
- https://www.experian.co.uk/business/platforms/powercurve/collections
- https://www.experianplc.com/newsroom/press-releases/2012/08-05-2012 [OLD, 2012]

**Bureaus (India)**
- https://www.crif.ae/solutions/ifrs9/
- https://en.wikipedia.org/wiki/CRIF_High_Mark_Credit_Information_Services
- https://www.transunioncibil.com/product/cibil-commercial-report
- https://www.transunioncibil.com/product/cibil-score
- https://www.rfp.wiki/financial-services-banking-fintech/consumer-credit-reporting-agencies-credit-bureaus/transunion-cibil (third-party)
- https://www.equifax.co.in/business/all-products/
- https://assets.equifax.com/marketing/india/assets/mfi-pulse-vol-xxvi-mar-2026.pdf (Mar 2026)

**Oracle / Finastra / Wolters Kluwer / Quantifi**
- https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/ifrs9-solution-cloud/25d/ifrsr/expected-credit-loss-overview-reports.html
- https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/ifrs9-solution-cloud/24c/ifbug/getting-started-ifrs9-solution.html
- https://www.oracle.com/a/ocom/docs/industries/financial-services/ofs-loan-loss-forecasting-ds.pdf
- https://www.oracle.com/a/ocom/docs/industries/financial-services/ofs-credit-risk-management-ds.pdf
- https://www.oracle.com/a/ocom/docs/industries/financial-services/fs-stress-testing-scenario-analysis-ds.pdf
- https://docs.oracle.com/en/industries/financial-services/ofs-analytical-applications/stress-testing-analytics/8.1.2.5.0/stsuh/introduction-ofsstsa.html
- https://www.finastra.com/solutions/arc
- https://www.finastra.com/sites/default/files/file/2022-12/resource-finastra-arc-comprehensive-and-open-banking-book-risk-and-regulatory-compliance.pdf [OLD, Dec 2022]
- https://www.finastra.com/news-events/press-releases/finca-impact-finance-goes-live-finastra-meet-regulatory-standards
- https://www.wolterskluwer.com/en-sg/solutions/onesumx-for-finance-risk-and-regulatory-reporting/onesumx-ifrs-9
- https://assets.contenthub.wolterskluwer.com/api/public/content/ifrs9-ecl-product-sheet?v=d276c815
- https://www.wolterskluwer.com/en-gb/solutions/onesumx-for-finance-risk-and-regulatory-reporting/onesumx-credit-risk
- https://www.quantifisolutions.com/counterparty-risk/
- https://www.quantifisolutions.com/xva/

**Indian vendors**
- https://www.nucleussoftware.com/finnone-neo/
- https://www.nucleussoftware.com/wp-content/uploads/2023/12/FinnOne_Neo_for_-NBFC.pdf (Dec 2023)
- https://www.nucleussoftware.com/finnone-neo/collections/
- https://www.business-standard.com/markets/capital-market-news/saarathi-finance-selects-nucleus-software-s-finnone-neo-for-transforming-its-lending-platform-125081900209_1.html (Aug 2025)
- https://perfios.com/credit-monitoring-platform
- https://about.crediwatch.com/about/product/early-warning-systems
- https://marketplace.microsoft.com/en-us/product/saas/tchinformationanalyticsprivatelimited1654155358283.crediwatch_1?tab=overview
- https://bfsi.eletsonline.com/navigating-challenges-and-innovations-in-indias-nbfc-sector-the-role-of-credit-watch/
- https://lentra.ai/
- https://bfsi.eletsonline.com/lentra-launches-growth-alliance-program-to-help-emerging-nbfcs-scale-amid-rapid-industry-growth/
- https://credable.in/
- https://www.kaleidofin.com/lending-as-a-service
- https://ibsintelligence.com/ibsi-news/federal-bank-taps-kaleidofin-to-optimise-microfinance-loan-portfolio/
- https://www.icraanalytics.com/risk-management-offerings-solutions/solutions-and-tools/expected-credit-loss
- https://www.crisil.com/en/home/events/crisil-webinar/risk-solutions/ind-as-109-provision-pain-ahead-for-lenders.html
- https://www.crisil.com/content/crisilcom/en/home/our-businesses/global-research-and-risk-solutions/our-offerings/quantitative-services/current-expected-credit-loss/case-studies/credit-risk-model-upgrades-for-IFRS-9-compliance.html
- https://www.acies.consulting/keplerifrs9.html
- https://www.tribuneindia.com/news/business/acies-techworks-kepler-wins-the-2025-ifrs-9-solution-of-the-year (Jun 2025)
- https://eclsquare.com/solutions/for-nbfcs
- https://roopya.money/early-warning-signal/
- https://roopya.money/expected-credit-loss-or-ecl-calculation/
- https://www.tcs.com/content/dam/global-tcs/en/pdfs/insights/whitepapers/deploying-efficient-expected-credit-loss-provisioning-system.pdf
- https://www.mphasis.com/home/industries/banking-capitalmarkets/corporate-banking.html

**Regulatory / market context**
- https://www.jmfinancialservices.in/blogs-and-articles/rbi-unveils-final-ecl-framework-for-banks (RBI final ECL, 27 Apr 2026)
- https://www.bankingfinance.in/rbi-finalises-expected-credit-loss-norms-rollout-set-for-april-2027.html
- https://www.icra.in/Rating/DownloadResearchSpecialCommentReport?id=6908
- https://www.business-standard.com/amp/industry/banking/rbi-asks-lenders-to-tighten-monitoring-of-gold-loan-portfolios-125052901875_1.html (May 2025)
- https://www.crisilratings.com/en/home/newsroom/press-releases/2026/06/gold-loan-lenders-ringfenced-well-from-price-correction-risk.html (Jun 2026)
- https://www.kotakneo.com/news/market-news/gold-loan-nbfcs-risk-fitch-15-percent-price-drop/
- https://www.iifl.com/blogs/gold-loan/rbi-final-gold-loan-ltv-norms-april-2026-impact
- https://www.idfy.com/blog/credit-risk-management-for-nbfcs-and-digital-lenders-in-india--a-complete-guide-2026/
- https://www.aryza.com/news/advancing-ifrs9/ (source of the "28% used Excel" statistic)
