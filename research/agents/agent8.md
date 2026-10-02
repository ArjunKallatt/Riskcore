# Agent 8 — Regulatory & Standards: frameworks mapped to Riskcore features

Research date: 2026-10-02. Prepared for Riskcore (v1: Indian retail/MF/PMS portfolio risk; v2: NBFC/bank loan-book risk).

## 0. Method, tool limits, and how to read the evidence labels

- **Tool limits (important):** WebFetch returned `EGRESS_BLOCKED` for every regulator and standard-setter domain I tried: rbi.org.in, www.rbi.org.in, rbidocs.rbi.org.in, www.sebi.gov.in, www.bis.org, www.ifrs.org, and also ey.com and kpmg.com. `curl` through the proxy also failed for mca.gov.in, icai.org and amfiindia.com (HTTP 000). Partway through, the session's shared WebSearch budget (200 calls) ran out. Because of this, **I could not open the full text of any official document.**
- **Evidence labels used below:**
  - **[S-official]**: the official URL showed up in WebSearch results, and the summary/snippet supports the claim. The URL is real, but I did not read the document body.
  - **[S-secondary]**: the claim comes from a secondary source (law firm, rating agency, news, AMC, taxguru, etc.) that appeared in WebSearch results.
  - **[UNVERIFIED]**: I did not see the claim in this session. It comes from background knowledge and is listed only so the feature design is complete. **Check it against the primary text before building or citing it.**
- **Before any feature ships, re-verify every threshold against the primary PDF.** That matters most for gold-loan LTV, the ECL floors and the PCA thresholds.
- **Structural change to note:** RBI has been consolidating its instructions into entity-wise "Directions, 2025/2026" (for example, "RBI (Commercial Banks – Asset Classification, Provisioning and Income Recognition) Directions, 2026" and "RBI (NBFCs – Prudential Norms – Capital Adequacy) Third Amendment Directions, 2026" [S-secondary: taxguru](https://taxguru.in/rbi/rbi-non-banking-financial-companies-prudential-norms-capital-adequacy-third-amendment-directions-2026.html)). Older circulars cited below may now sit inside these consolidated directions. Always cite the **current** consolidated direction in product copy.

---

## 1. SEBI (v1: portfolio risk)

### 1.1 Mutual fund Risk-o-meter (product labelling)
- **Circular:** SEBI/HO/IMD/DF3/CIR/P/2020/197, dated **5 Oct 2020**, "Product Labeling in Mutual Fund schemes – Risk-o-meter" [S-secondary: [taxguru](https://taxguru.in/sebi/product-labeling-mutual-fund-schemes-risk-o-meter.html), [taxguru methodology](https://taxguru.in/sebi/evaluation-methodology-risk-level-mutual-fund-scheme.html)]. These provisions are now consolidated in the SEBI Master Circular for Mutual Funds, SEBI/HO/IMD/IMD-PoD-1/P/CIR/2024/90, dated 27 Jun 2024. That circular number and date appear in SEBI-hosted scheme documents that came up in search ([example SID on sebi.gov.in](https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1763372767700.pdf)), but I did not open the master circular itself.
- **Levels:** there are six: Low, Low to Moderate, Moderate, Moderately High, High, Very High [S-secondary: [Value Research](https://www.valueresearchonline.com/stories/48907/decoding-the-new-riskometer/), [stableinvestor](https://stableinvestor.com/2020/10/new-riskometer-mutual-fund-sebi.html)].
- **Equity parameters:** market cap, volatility and impact cost (liquidity). Large-cap scores 5, mid-cap 7, small-cap 9 [S-secondary: [Value Research](https://www.valueresearchonline.com/stories/48592/sebi-rejigs-the-risk-o-meter/), [Business Standard](https://www.business-standard.com/article/markets/decoding-risk-o-meter-3-0-and-its-use-as-an-investment-tool-in-the-mf-space-120100601112_1.html)].
- **Debt parameters:** credit risk, interest-rate risk and liquidity risk. G-secs score 1 and below-investment-grade paper scores 12 [S-secondary: same].
- **Aggregation:** a simple average of the parameter risk values gives a score from 1 to 12, which maps to the six levels. The exact band cut-offs are **[UNVERIFIED]**; take them from the master circular annex.
- **Frequency and disclosure:** AMCs update the risk-o-meter monthly on their own and the AMFI websites (from 1 Jan 2021). They also publish an annual (31 March) disclosure of each scheme's risk level and how many times it changed [S-secondary: taxguru above].
- **Newer (Aug 2026):** SEBI consulted on a colour-coded **Credit Risk-o-Meter for individual debt securities**, mapping ratings from AAA to D into six categories. **Status: proposal / consultation only** [S-secondary: [Business Standard 15 Aug 2026](https://www.business-standard.com/markets/capital-market-news/sebi-proposes-credit-risk-o-meter-for-debt-securities-to-make-credit-risk-easier-to-assess-126081500533_1.html), [corplawupdates](https://www.corplawupdates.in/updates/sebi-credit-risk-o-meter-debt-securities-2026)].
- **Riskcore features:** (a) a **holdings-based "shadow riskometer"** that rebuilds a fund's score from its portfolio disclosure and compares it with the AMC's published label (a drift alert); (b) a **portfolio-level riskometer** using the AUM-weighted score across a user's funds; (c) a debt-holding credit-bucket view that is ready for the proposed rating-to-six-level map. Label all of these as "Riskcore estimate, not the official AMC riskometer".

### 1.2 Potential Risk Class (PRC) matrix for debt schemes
- **Circular dated 7 Jun 2021**, "Potential Risk Class Matrix for debt schemes based on Interest Rate Risk and Credit Risk", effective 1 Dec 2021 [S-secondary: [freefincal](https://freefincal.com/sebis-maximum-risk-matrix-for-debt-mutual-funds/), [TeamLease RegTech](https://www.teamleaseregtech.com/updates/article/13716/sebi-has-issued-a-circular-for-the-potential-risk-class-matrix-for-deb/), [Business Standard](https://www.business-standard.com/amp/article/markets/sebi-asks-debt-mfs-to-do-a-second-risk-assessment-label-for-investors-121060701135_1.html)]. I could not see the circular number. **[UNVERIFIED]**
- **What it is:** a 3x3 matrix showing the *maximum* risk a scheme may take.
  - **Interest-rate risk** is measured by Macaulay duration: Class I is MD ≤ 1 year; Class II is MD ≤ 3 years [S-secondary: freefincal]; Class III is any MD **[UNVERIFIED in this session]**.
  - **Credit risk** is measured by Credit Risk Value (CRV) with classes A, B and C. The CRV thresholds (for example A ≥ 12, B ≥ 10) are **[UNVERIFIED]**.
  - The matrix must appear in the SID, the KIM and the NFO application form. AMC example: [Invesco MF PRC doc](https://www.invescomutualfund.com/docs/default-source/default-document-library/classification-of-debt-schemes-in-terms-of-potential-risk-class-matrix).
- **Riskcore features:** a **PRC compliance checker** that computes the actual Macaulay duration and weighted CRV of the current portfolio and flags when the portfolio is near or beyond the scheme's declared PRC cell. Also a **duration and credit heat-map** for a user's debt-fund basket.

### 1.3 Stress test of small and mid-cap MF schemes (2024)
- SEBI asked AMCs (via AMFI) in **Feb 2024** to stress test small-cap and mid-cap schemes. **AMFI's letter is dated 28 Feb 2024.** The first disclosures came out on 15 Mar 2024, and they are now published monthly by the 15th using the previous month's data [S-secondary: [Business Standard 29 Feb 2024](https://www.business-standard.com/amp/markets/mutual-fund/mfs-told-to-disclose-stress-test-reports-of-midcap-smallcap-schemes-124022901229_1.html), [Business Standard 10 Mar 2024](https://www.business-standard.com/amp/markets/news/stress-disclosures-on-small-mid-cap-funds-by-amcs-from-march-report-124031000372_1.html), [BusinessToday](https://www.businesstoday.in/personal-finance/news/story/mutual-funds-market-regulator-sebi-to-release-stress-test-findings-on-small-cap-funds-442849-2024-08-24)].
- **Metric:** the number of days needed to liquidate 25% and 50% of the portfolio pro-rata. The common methodology assumes participation of up to a set share of daily traded volume, but that participation % is **[UNVERIFIED]**. The disclosure also includes portfolio concentration, beta, volatility, P/E and turnover, all **[UNVERIFIED]** (AMFI format not opened).
- One secondary source mentions 2026 tightening of small-cap stress-test rules [S-secondary: [oquilia](https://www.oquilia.com/news/sebi-small-cap-mutual-fund-stress-testing-2026)]. Treat this as **unverified**.
- **Riskcore features:** a **liquidity stress engine** that computes days-to-liquidate X% for any equity portfolio (MF or PMS) using ADV and a participation-rate parameter (default 20%, user-editable), shown next to the AMC-published figure. It can also be applied to the user's direct-equity portfolio.

### 1.4 PMS reporting
- **Circular SEBI/HO/IMD/IMD-PoD-2/P/CIR/2022/172, dated 16 Dec 2022:** performance benchmarking and reporting by Portfolio Managers [S-secondary: [APMI-hosted PDF of the circular](https://www.apmiindia.org/storagebox/images/Circulars/Performance-Benchmarking-16th-Dec'22.pdf), [Business Standard](https://www.business-standard.com/article/markets/sebi-issues-performance-benchmarking-guidelines-for-portfolio-managers-122121600879_1.html)].
  - It defines four strategies (equity, debt, hybrid, multi-asset), and APMI prescribes up to 3 benchmarks per strategy.
  - Monthly reports go to SEBI and APMI within 7 working days of month-end. APMI publishes comparisons.
  - Effective 1 Apr 2023.
- A SEBI Master Circular for Portfolio Managers exists ([lexibox index](https://www.lexibox.in/pms/master-circular/)). Its latest date and number are **[UNVERIFIED]**.
- **Riskcore features:** a **PMS analytics pack** with TWRR versus the APMI-prescribed benchmark for the strategy, a rolling-return / drawdown / tracking-error report, and an exportable monthly client risk statement. Do not label it as the "official APMI report".

### 1.5 Investment Adviser (IA) / Research Analyst (RA) regulations: the **biggest legal risk for a public app**
- The SEBI (Investment Advisers) Regulations, 2013 and the SEBI (Research Analysts) Regulations, 2014 were amended on **16 Dec 2024**. Implementing circulars "Guidelines for Investment Advisers" and "Guidelines for Research Analysts" followed on **8 Jan 2025**. Both came out of SEBI's consultation paper of 6 Aug 2024 [S-secondary: [AZB](https://www.azbpartners.com/bank/overhaul-of-the-regulatory-framework-for-investment-advisers-and-research-analysts/), [Lexology](https://www.lexology.com/library/detail.aspx?g=666c5c80-23cb-4217-a261-ac19257cd5b2)].
- Official sources: the [SEBI board memo, Oct 2024](https://www.sebi.gov.in/sebi_data/meetingfiles/oct-2024/1728550911419_1.pdf) and the [FAQs on IA Regulations](https://www.sebi.gov.in/sebi_data/attachdocs/1424862077270.pdf) [S-official, not opened].
- **Finfluencer / unregistered-entity restrictions:** SEBI-regulated entities and their agents may not have financial, referral or technological links with unregistered persons who give securities advice or make return claims [S-secondary: Lexology / AZB]. The underlying SEBI circular number and date are **[UNVERIFIED]**. My understanding is that it was an Aug 2024 board decision followed by a circular, but I could not confirm this.
- **See section 6 for the cautions.**

---

## 2. RBI (v2: NBFC and bank loan-book risk)

### 2.1 Scale-Based Regulation (SBR) for NBFCs
- **SBR: A Revised Regulatory Framework for NBFCs**, dated **22 Oct 2021**, effective **1 Oct 2022**. It creates four layers: Base, Middle, Upper (identified by a parametric scoring methodology) and Top. Once identified, an NBFC-UL stays under enhanced regulation for at least 5 years [S-official: [RBI notification Id=12179](https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12179&Mode=0); [RBI Master Directions page](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12179); [RBI FAQs on NBFCs (Apr 2025)](https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/ALLNBFC23042025.pdf); [Master Direction – NBFC SBR, 19 Oct 2023 PDF](https://rbidocs.rbi.org.in/rdocs/notification/PDFs/106MDNBFCS1910202343073E3EF57A4916AA5042911CD8D562.PDF)].
- **Riskcore feature:** an **entity profile / layer selector** (BL/ML/UL) that switches which limits and disclosures apply: concentration limits, ICAAP and so on. This is a configuration, not a computation.

### 2.2 Large exposures and concentration (NBFC)
- **Large Exposures Framework for NBFC-UL**, dated **19 Apr 2022**, applicable from 1 Oct 2022 [S-secondary: [taxguru](https://taxguru.in/rbi/large-exposures-framework-upper-layer-nbfc-ul.html), [Business Standard](https://www.business-standard.com/article/finance/rbi-caps-lending-limits-of-nbfcs-to-bring-them-on-a-par-with-those-of-banks-122041901223_1.html)].
  - The single-counterparty limit is 20% of the eligible capital base. The Board can add 5% (to 25%), and up to 5% more is allowed for infrastructure.
  - The group limit is 25% (+10% infrastructure) **[UNVERIFIED]**.
- Under SBR, NBFC-ML and NBFC-BL (which are not UL) follow the older concentration-of-credit/investment norms, which are tied to Tier 1 capital **[UNVERIFIED percentages]**.
- **Riskcore features:** a **single-name and group exposure monitor** that computes exposure as a % of Tier 1 / eligible capital, uses an editable limit table pre-filled per layer, and gives breach and near-breach alerts. Add **sector / geography / product HHI** as a Pillar-2 style concentration view (see Basel, §3.2).

### 2.3 IRACP: SMA / NPA classification and the Nov 2021 clarification
- **RBI circular of 12 Nov 2021**, clarifications on the prudential norms on IRACP [S-secondary: [Vinod Kothari](https://vinodkothari.com/2021/11/npa-classification-norms-2/), [Argus Partners](https://www.argus-p.com/updates/updates/rbi-issues-clarifications-on-prudential-norms-on-income-recognition-asset-classification-and-provisioning-pertaining-to-advances/), bank consumer-education docs, e.g. [Axis Bank](https://www.axis.bank.in/docs/default-source/default-document-library/rbi-instructions-on-prudential-norms-on-income-recognition-asset-classification-and-provisioning.pdf?sfvrsn=4f3762fe_1)]. Its key points:
  - Classification is done **as part of the day-end process** for the relevant date.
  - SMA-0 is 1–30 days overdue, SMA-1 is 31–60, SMA-2 is 61–90, and NPA is more than 90 days. For example, an account becomes SMA-1 at day-end once it has been continuously overdue for 30 days, SMA-2 on the 60th day, and NPA on the 90th day.
  - An NPA is **upgraded to standard only when all arrears of interest and principal are paid**. For borrowers with several facilities, the arrears on all of them must be cleared.
- For NBFCs, the NPA norm moved to 90 DPD through a glide path, but the dates of that glide path are **[UNVERIFIED]** in this session.
- **Riskcore features:**
  - A **day-end DPD engine**, deterministic and as-of-date, that assigns SMA-0, SMA-1, SMA-2 or NPA.
  - **Borrower-level contagion**: if any facility is NPA, every facility of that borrower is NPA.
  - A **"full arrears cleared" upgrade rule**.
  - NPA ageing into **Substandard / Doubtful-1/2/3 / Loss**, using the standard IRACP vintage buckets and provisioning % **[UNVERIFIED]**; keep these configurable.
  - Roll-rate / flow-rate matrices across buckets.

### 2.4 Ind AS 109 for NBFCs and the RBI Ind AS guidance (13 Mar 2020)
- **MCA roadmap:**
  - Phase 1, from 1 Apr 2018: NBFCs with net worth of ₹500 cr or more, plus their holding, subsidiary, JV and associate companies.
  - Phase 2, from 1 Apr 2019: listed NBFCs with net worth below ₹500 cr, and unlisted NBFCs with net worth of ₹250–500 cr.
  - Sources: [S-secondary: [PwC roadmap PDF](https://www.pwc.in/assets/pdfs/services/ifrs/ind-as-roadmap-bank-and-insurance-2016.pdf), [taxguru](https://taxguru.in/chartered-accountant/impact-ind-non-banking-financial-companies-nbfcs.html)]. The MCA's Companies (Indian Accounting Standards) Amendment Rules notification number and date are **[UNVERIFIED]**: mca.gov.in was unreachable.
- **RBI, 13 Mar 2020**, "Implementation of Indian Accounting Standards" for NBFCs and ARCs [S-secondary: [FIDC-hosted copy of the RBI circular](https://fidcindia.org.in/wp-content/uploads/2020/03/RBI-IND-AS-13-03-20.pdf), [Vinod Kothari](https://vinodkothari.com/2020/03/guidance-on-implementation-of-ind-as-by-nbfcs/), [RBI circular index](https://m.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=11818) (S-official)]:
  - NBFCs keep running IRACP classification and provisioning **in parallel** with Ind AS 109.
  - They disclose an IRACP-versus-Ind AS comparison.
  - If the Ind AS 109 allowance is lower than the IRACP provision, the shortfall is moved from profit after tax to an **Impairment Reserve**. That reserve does not count as regulatory capital and cannot be withdrawn without RBI approval.
- **2026:** a secondary source reports amendments to the NBFC IRACP directions in 2026 touching ECL and DLG [S-secondary: [KNM India](https://knmindia.com/navigating-the-2026-rbi-iracp-amendment-ecl-provisions-and-default-loss-guarantee-dlg-arrangements-for-nbfcs/)]. **Unverified**; check the primary text.
- **Riskcore features:** a **dual-book provisioning engine** that runs ECL (Ind AS 109) and IRACP side by side, computes the shortfall, posts it to the **Impairment Reserve**, and produces the comparison-disclosure table automatically. This is a strong differentiator for small NBFCs.

### 2.5 RBI ECL framework for banks: draft (Oct 2025) to final (Apr 2026)
- **Background:** RBI Discussion Paper on ECL, 16 Jan 2023 [S-official: [RBI PDF](https://rbidocs.rbi.org.in/rdocs/Publications/PDFs/DPECL160012023AE79B7B546C94715AA8468B0811096F5.PDF)].
- **Draft:** RBI (Scheduled/Commercial Banks – Asset Classification, Provisioning and Income Recognition) Directions, 2025, issued **7 Oct 2025** [S-secondary: [Business Standard](https://www.business-standard.com/amp/finance/news/rbi-announces-draft-norms-for-transition-to-expected-credit-loss-framework-125100701326_1.html), [Uniqus](https://uniqus.com/rbi-draft-ecl-directions-2025/), [ICRA Oct 2025](https://www.icra.in/Research/ViewResearchReport/impact-of-rbi-s-proposed-ecl-framework-on-banks-capitalisation-profile-likely-to-be-moderate/6587)].
- **Final:** RBI (Commercial Banks – Asset Classification, Provisioning and Income Recognition) Directions, 2026, issued **27 Apr 2026** [S-official: [RBI press release PDF 27 Apr 2026](https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR150994739A099E843668A75A7F92C9E9BD1.PDF); S-secondary: [taxguru](https://taxguru.in/rbi/rbi-commercial-banks-asset-classification-provisioning-income-recognition-directions-2026.html), [AZB](https://www.azbpartners.com/bank/rbi-commercial-banks-asset-classification-provisioning-and-income-recognition-directions-2026-5/), [KPMG May 2026](https://assets.kpmg.com/content/dam/kpmgsites/in/pdf/2026/05/expected-credit-loss.pdf), [JM Financial](https://www.jmfinancialservices.in/blogs-and-articles/rbi-unveils-final-ecl-framework-for-banks)]. One secondary result cites the reference number "RBI/DOR/2026-27/398"; that number is **[UNVERIFIED]**.
  - **Applicability:** scheduled commercial banks, **excluding RRBs, SFBs and payments banks** (per JM Financial). From **1 Apr 2027**.
  - **Transition:** the one-time impact on the existing book can be spread to **31 Mar 2031**.
  - **Approach:**
    - Three stages: 12-month ECL in Stage 1, lifetime ECL in Stages 2 and 3.
    - SICR assessment.
    - Effective interest rate (EIR) method.
    - The extant NPA norms are **kept alongside** the staging.
    - Prudential floors act as backstops. Secondary sources give Stage 1 floors of about 0.25% (SME/agri) to 1.25% (CRE under construction) and Stage 2 floors of 1.5%–5% by portfolio. Stage 3 floors depend on NPA vintage and on whether the exposure is secured or unsecured [S-secondary: Uniqus "Implementation reality check", BankExamsToday]. The exact floor table is **[UNVERIFIED]** and must be taken from the directions annex.
  - **Draft to final:** the floors were reportedly retained broadly, and bank requests for lower Stage-2 floors were not accepted [S-secondary: [Uniqus](https://uniqus.com/the-implementation-reality-check/), [Business Standard Nov 2025](https://www.business-standard.com/amp/finance/news/draft-ecl-framework-banks-plan-to-move-rbi-for-lower-stage-ii-floor-125111101999_1.html)].
  - **NBFCs:** Ind AS NBFCs are already on Ind AS 109 ECL (see §2.4). These bank directions do not themselves cover NBFCs, per the secondary sources.
- **Riskcore features:**
  - A **floor-aware ECL engine**: final provision = max(model ECL, regulatory floor by stage × segment), with configurable floor tables for "RBI-bank-2026", "Ind AS NBFC (IRACP floor)" and "Pure IFRS 9".
  - A **transition glide-path calculator** for the FY27 to FY31 add-back.
  - **EIR amortisation** for fees.

### 2.6 Gold loans
- **Earlier circulars:** RBI's Sep 2024 circular on irregular practices in gold loans is **[UNVERIFIED]** in this session. The "Oct 2023" circular the brief mentions could not be verified.
- **Draft:** Draft RBI (Lending Against Gold Collateral) Directions, 2025, issued **9 Apr 2025** [S-official: [RBI draft page](https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4633), [website.rbi.org.in](https://website.rbi.org.in/web/rbi/-/notifications/draft-reserve-bank-of-india-lending-against-gold-collateral-directions-2025); S-secondary: [Business Standard](https://www.business-standard.com/markets/capital-market-news/rbi-releases-draft-directions-on-lending-against-gold-collateral-125040901089_1.html)].
- **Final:** **RBI (Lending Against Gold and Silver Collateral) Directions, 2025**, issued **6 Jun 2025** and updated to **29 Sep 2025** (1st Amendment). Reference **RBI/2025-26/47 DOR.CRE.REC.26/21.01.023/2025-26**. Comply as early as possible and **no later than 1 Apr 2026** [S-official: [RBI notification Id=12859](https://rbi.org.in/scripts/NotificationUser.aspx?Mode=0&Id=12859); S-secondary: [EY impact assessment](https://www.ey.com/en_in/insights/strategy-transactions/rbi-gold-loan-guidelines-2025-impact-assessment-and-key-changes), [Business Standard 6 Jun 2025](https://www.business-standard.com/economy/news/rbi-to-raise-gold-lending-ltv-to-85-for-loans-under-rs-2-5-lakh-malhotra-125060600690_1.html), [IIFL](https://www.iifl.com/blogs/gold-loan/rbi-gold-and-silver-lending-directions)].
  - **Scope:** all commercial banks (including SFBs), UCBs, NBFCs and HFCs, for consumption and income-generating loans (including farm credit) against gold or silver.
  - **Tiered LTV for consumption loans:** up to **85%** for loans up to ₹2.5 lakh; **80%** for ₹2.5–5 lakh; **75%** above ₹5 lakh. These figures come from secondary sources; confirm in the primary text which loan types the tiers apply to.
  - **For bullet-repayment loans, LTV is computed on the total amount repayable at maturity**, meaning principal plus interest.
  - **The tenor of bullet consumption loans is capped at 12 months**, renewable under para 11.
  - **No loans may be given to purchase gold** (including gold ETFs and gold MF units).
  - Collateral may be handled and stored only in the lender's own staffed branches with vaults.
  - Valuation basis (the lower of the 30-day average and the previous-day close, at 22 carat), quantity caps, auction reserve price and return timelines are all **[UNVERIFIED]**; I could not open the PDF.
- **Riskcore features:**
  - A **gold-loan LTV engine** that applies the ticket-size tier LTV cap; projects bullet LTV at maturity as (P + accrued interest to maturity) / collateral value; runs a daily mark-to-market with a gold price feed; and gives **LTV-breach and margin-call alerts**.
  - A **tenor check**: bullet consumption loans over 12 months are flagged.
  - **Gold price shock stress** at −10%, −20% and −30%, showing the share of the book that breaches LTV or goes underwater, the expected auction shortfall, and the LGD.
  - An **"end-use" flag check** that rejects loans whose purpose is buying gold.

### 2.7 Early warning signals and fraud
- **RBI Master Directions on Fraud Risk Management**, revised **15 Jul 2024**: three separate MDs for commercial banks, cooperative banks and NBFCs (including HFCs). They extend the **EWS and Red-Flagged Account (RFA)** framework to NBFCs and require natural-justice process before an account is declared fraud [S-secondary: [AZB](https://www.azbpartners.com/bank/master-directions-on-fraud-risk-management-in-banks-and-nbfcs/), [SCC Online](https://www.scconline.com/blog/post/2024/07/17/rbi-revises-master-directions-on-fraud-risk-management-in-regulated-entities-legal-news/), [Vinod Kothari PDF](https://vinodkothari.com/wp-content/uploads/2024/07/FRM.pdf)].
  - A secondary source says RFA reporting is due within 7 days for exposures of ₹3 cr or more and the fraud decision within 180 days [S-secondary: [liquilens](https://liquilens.in/guides/rbi-nbfc-early-warning-system/)]. This is a low-quality source; treat it as **unverified**.
- **Riskcore features:** an **EWS rules engine** with a configurable signal library that runs daily and produces a watchlist with a reason code. Example signals:
  - DPD-bucket deterioration and repeated SMA-1 entries
  - bounce / NACH-return frequency
  - utilisation above 90%
  - bureau score drop
  - GST / turnover decline
  - delays in financial statements
  - collateral-value drops (for gold, LTV drift)
  - payments to related parties
  
  An **RFA-candidate queue** with an audit trail (a decision-support tool only; it never classifies fraud). Feed EWS into **SICR** (see §4).

### 2.8 Prompt Corrective Action (PCA) for NBFCs
- **PCA Framework for NBFCs**, issued **14 Dec 2021**, effective **1 Oct 2022** based on financials from 31 Mar 2022. Indicators are CRAR, Tier 1 ratio and NNPA ratio, with three risk thresholds for NBFC-D and NBFC-ND in the Middle and Upper layers. Government NBFCs were added later **[UNVERIFIED]** [S-official: [RBI notification Id=12208](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12208&Mode=0); S-secondary: [Business Standard](https://www.business-standard.com/article/finance/rbi-issues-prompt-corrective-action-framework-for-nbfcs-121121400825_1.html), [Dvara note](https://dvararesearch.com/wp-content/uploads/2024/01/Note-on-RBIs-PCA-Framework-for-NBFCs.pdf)].
  - Thresholds from secondary sources: CRAR breaches up to 300, 300–600 and over 600 bps below 15%; NNPA bands of over 6%, over 9% and over 12%. **Verify these against the RBI text.**
- **Riskcore feature:** a **PCA proximity dashboard** that projects CRAR, Tier 1 and NNPA under base and stress scenarios and shows the distance to each threshold.

### 2.9 Digital lending and Default Loss Guarantee (DLG)
- **Digital lending guidelines**, 2 Sep 2022. **DLG guidelines**, 8 Jun 2023: DLG cover is capped at **5% of the loan portfolio** (or the equivalent for implicit arrangements). Both were later consolidated into the **RBI (Digital Lending) Directions, 2025** [S-secondary: [Mondaq](https://www.mondaq.com/india/fin-tech/1347832/guidelines-on-default-loss-guarantee-in-digital-lending), [Vinod Kothari FAQs](https://vinodkothari.com/2023/06/faqs-on-default-loss-guarantee-in-digital-lending/), [Zee Biz](https://www.zeebiz.com/personal-finance/banking/news-rbi-faqs-on-default-loss-guarantee-in-digital-lending-frequently-asked-questions-on-dlg-issued-in-june-2023-286835)]. The date of the 2025 consolidation is **[UNVERIFIED]**.
  - DLG accounting: the RE recognises the asset as NPA and provides without netting off the DLG **[UNVERIFIED]**.
- **Riskcore features:**
  - A **DLG-pool tracker** per Lending Service Provider / partner: DLG % of the portfolio (alert above 5%), DLG invocation versus remaining cover, and ECL computed **gross of DLG**, with DLG shown separately.
  - **Partner-level vintage / roll-rate analytics.**

### 2.10 NBFC risk management, ICAAP and stress testing
- Under SBR, NBFC-ULs must run an **ICAAP**. The other SBR governance requirements are a Risk Management Committee and a Chief Risk Officer for larger NBFCs, and **liquidity risk management including LCR**, which applies to deposit-taking NBFCs and NBFCs above a size threshold. Sources: the SBR notification above [S-official, not opened]. The detailed clauses are **[UNVERIFIED]**.
- RBI stress-testing guidance for banks (originally 2007, revised Dec 2013) is **[UNVERIFIED]**: I could not reach rbi.org.in.
- **Riskcore features:**
  - An **ICAAP-lite workbook** combining Pillar-1 CRAR, Pillar-2 add-ons (concentration, IRRBB, liquidity), and a capital plan under stress.
  - A **scenario library**: PD multipliers, LGD haircuts, gold price shocks, sector shocks, rate shocks.
  - A **liquidity gap report** (structural liquidity buckets).

---

## 3. Basel II/III (v2, and v1 for market risk)

All bis.org pages were blocked. **Every item in this section is [UNVERIFIED] in this session.** The canonical URLs are listed so the developer can open them.

### 3.1 IRB risk-weight function (CRE31)
- **Source:** Basel Framework CRE31, https://www.bis.org/basel_framework/chapter/CRE/31.htm. Basel III final reforms in BCBS d424 (Dec 2017), https://www.bis.org/bcbs/publ/d424.htm.
- **The function:** the Vasicek single-factor model at **99.9%** confidence.
  - K = [LGD·N((N⁻¹(PD) + √R·N⁻¹(0.999)) / √(1−R)) − PD·LGD] · (1 − 1.5b)⁻¹ · (1 + (M − 2.5)·b)
  - The maturity adjustment is b = (0.11852 − 0.05478·ln PD)².
  - RWA = K · 12.5 · EAD.
  - Corporate correlation R runs from 0.12 to 0.24 depending on PD. Retail correlations: residential mortgage 0.15, QRRE 0.04, other retail 0.03–0.16.
  - The d424 PD floor is 0.05% (corporate).
- **Riskcore features:**
  - An **IRB capital calculator** (analytical, for education and benchmarking) that gives unexpected loss and capital per loan and segment.
  - The **economic capital vs ECL** split: EL = PD·LGD·EAD, and UL comes from the IRB function.
  - Note: Indian banks and NBFCs report regulatory capital on the **Standardised approach**; RBI has not approved IRB. Label the IRB calculator as "economic-capital proxy".

### 3.2 Concentration risk (Pillar 2) and large exposures (BCBS 283)
- **Large exposures:** BCBS 283, "Supervisory framework for measuring and controlling large exposures" (Apr 2014), https://www.bis.org/publ/bcbs283.htm.
  - The limit is 25% of Tier 1 (15% between G-SIBs).
  - Reporting starts at 10% of Tier 1.
  - Connected counterparties are aggregated.
- **Pillar 2 (Basel II Pillar 2, BCBS 128, 2006)** expects banks to assess **name and sector concentration**. Common measures are HHI and the Granularity Adjustment (Gordy-Lütkebohmert).
- **Riskcore features:** single-name HHI; the **granularity adjustment add-on**; sector HHI using an RBI sector code mapping; and a top-20 exposures report as % of Tier 1.

### 3.3 Market risk: FRTB expected shortfall
- **FRTB**, BCBS d457 (Jan 2019), https://www.bis.org/bcbs/publ/d457.htm, and Basel Framework MAR33.
  - The internal-models approach replaces 99% VaR with **97.5% Expected Shortfall**, with liquidity horizons from 10 to 120 days and a stressed calibration.
- **Riskcore features (v1):** portfolio **ES at 97.5%** (historical and filtered-historical) next to VaR 99%; a stressed-ES window (for example the 2008 or Mar 2020 Indian market); and liquidity-horizon scaling per asset class (simplified).

### 3.4 Stress testing principles (BCBS 2018)
- **BCBS "Stress testing principles"**, d450, Oct 2018, https://www.bis.org/bcbs/publ/d450.htm. It sets out 9 principles: governance, objectives, scenario severity, data and models, challenge, and documentation.
- **Riskcore features:** a **scenario manager** with versioned scenarios, documented assumptions, owners and approval state; reverse stress testing (the shock needed to breach CRAR or PCA thresholds); and an audit log.

---

## 4. IFRS 9 / Ind AS 109 (v2), and CECL for contrast

ifrs.org and icai.org could not be reached. Sections 5.5.x of IFRS 9 below are **[UNVERIFIED]** in this session, but they are long-standing and the canonical sources are listed. The Indian secondary source [IFRS 9 ECL guide (quintedge)](https://quintedge.com/blog/ifrs-9-ecl-model-guide) and the RBI Ind AS circular (§2.4) back up the general three-stage description.

- **Source:** IFRS 9 Financial Instruments, https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/. Ind AS 109 is notified by the MCA under the Companies (Indian Accounting Standards) Rules, 2015, and ICAI publishes the text at https://www.icai.org (both unverified this session).
- **Requirements:**
  1. **Three stages.** Stage 1 takes 12-month ECL. Stage 2 (significant increase in credit risk since initial recognition) takes lifetime ECL. Stage 3 (credit-impaired) takes lifetime ECL, with interest on the net carrying amount.
  2. **SICR** compares the lifetime PD at the reporting date with the PD at origination. It uses reasonable and supportable forward-looking information.
  3. **Rebuttable presumption: more than 30 DPD means SICR** (IFRS 9 para 5.5.11).
  4. **Rebuttable presumption: default no later than 90 DPD** (B5.5.37).
  5. ECL is **unbiased and probability-weighted** over multiple scenarios, includes the time value of money, and uses forward-looking macro information.
  6. **POCI assets** (purchased or originated credit-impaired) use a credit-adjusted EIR. Only cumulative changes in lifetime ECL since recognition are booked.
  7. There is a simplified approach for trade receivables (lifetime ECL).
- **US CECL (ASC 326, FASB ASU 2016-13)** for contrast: there are **no stages**. Lifetime ECL is booked from day 1 for all assets at amortised cost, using a reasonable and supportable forecast and then reverting to history. Canonical source: https://www.fasb.org (unverified this session).
- **Riskcore features:**
  - A **stage classification engine** with the following rules:
    - Stage 3 if more than 90 DPD, NPA, restructured-impaired, or written-off/POCI.
    - Stage 2 if more than 30 DPD, **or** SICR by relative PD change (configurable, for example lifetime PD × 2 and a +x bps absolute floor), **or** an EWS watchlist flag, **or** restructuring.
    - Otherwise Stage 1.
    - Optional cure / probation periods.
  - **PD term structures:** 12-month and lifetime, built from roll-rate Markov chains or vintage curves, with a macro overlay using scenario weights (base/up/down).
  - **LGD**: workout, or collateral-based for gold (haircut + auction cost).
  - **EAD**: amortising schedule plus a CCF for undrawn amounts.
  - **ECL** = Σₜ PDₜ · LGDₜ · EADₜ · DFₜ, discounted at EIR.
  - **POCI** handling.
  - A **CECL toggle** that books lifetime ECL for every asset, for comparison.
  - **Disclosure outputs:** stage migration matrix, ECL movement reconciliation, and the IRACP comparison table (§2.4).

---

## 5. Master mapping table

| # | Requirement | Source doc | Date / status | Riskcore feature | v1/v2 | Link (evidence) |
|---|---|---|---|---|---|---|
| 1 | Six-level MF risk-o-meter based on holdings (equity: mcap/vol/impact cost; debt: credit/IR/liquidity), updated monthly | SEBI circ. SEBI/HO/IMD/DF3/CIR/P/2020/197, now in MF Master Circular 2024 | 5 Oct 2020; in force (from 1 Jan 2021) | Shadow riskometer per fund + portfolio-weighted riskometer + label-drift alert | v1 | [taxguru](https://taxguru.in/sebi/product-labeling-mutual-fund-schemes-risk-o-meter.html) (S-secondary) |
| 2 | Credit Risk-o-Meter for individual debt securities (AAA→D into 6 levels) | SEBI consultation | Aug 2026; **proposal** | Rating-to-risk-level mapper for bond holdings | v1 | [Business Standard](https://www.business-standard.com/markets/capital-market-news/sebi-proposes-credit-risk-o-meter-for-debt-securities-to-make-credit-risk-easier-to-assess-126081500533_1.html) |
| 3 | PRC matrix (max Macaulay duration class I/II/III × CRV class A/B/C) | SEBI circular | 7 Jun 2021; effective 1 Dec 2021; in force | PRC compliance checker (actual MD and CRV vs declared cell) | v1 | [freefincal](https://freefincal.com/sebis-maximum-risk-matrix-for-debt-mutual-funds/) (S-secondary) |
| 4 | Days to liquidate 25%/50% of small/mid-cap scheme | SEBI direction via AMFI letter | 28 Feb 2024; monthly since 15 Mar 2024 | Liquidity stress engine (ADV × participation) for any equity portfolio | v1 | [Business Standard](https://www.business-standard.com/amp/markets/mutual-fund/mfs-told-to-disclose-stress-test-reports-of-midcap-smallcap-schemes-124022901229_1.html) |
| 5 | PMS performance vs APMI strategy benchmarks; monthly reporting | SEBI/HO/IMD/IMD-PoD-2/P/CIR/2022/172 | 16 Dec 2022; effective 1 Apr 2023 | PMS benchmark-relative risk & return report | v1 | [APMI-hosted circular](https://www.apmiindia.org/storagebox/images/Circulars/Performance-Benchmarking-16th-Dec'22.pdf) |
| 6 | Securities advice / research needs IA or RA registration; regulated entities may not link with unregistered advisers / finfluencers | IA Regs 2013 & RA Regs 2014 (amended 16 Dec 2024); guidelines 8 Jan 2025 | In force | "Analytics-only" product mode, no buy/sell recommendations, disclaimers, legal review (§6) | v1 | [AZB](https://www.azbpartners.com/bank/overhaul-of-the-regulatory-framework-for-investment-advisers-and-research-analysts/); [SEBI board memo](https://www.sebi.gov.in/sebi_data/meetingfiles/oct-2024/1728550911419_1.pdf) |
| 7 | NBFC layers BL/ML/UL/TL; proportional regulation | RBI SBR framework | 22 Oct 2021; effective 1 Oct 2022 | Entity-layer configuration driving limits and reports | v2 | [RBI](https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12179&Mode=0) (S-official) |
| 8 | Single counterparty ≤20% of eligible capital (+5% Board, +5% infra) for NBFC-UL | RBI Large Exposures Framework NBFC-UL | 19 Apr 2022; effective 1 Oct 2022 | Single-name / group exposure monitor with breach alerts | v2 | [taxguru](https://taxguru.in/rbi/large-exposures-framework-upper-layer-nbfc-ul.html) |
| 9 | SMA-0/1/2 and NPA at 90 DPD, flagged at day-end; NPA upgrade only once all arrears are cleared | RBI IRACP clarification | 12 Nov 2021; in force | Day-end DPD & SMA/NPA engine, borrower-level contagion, upgrade rule | v2 | [Vinod Kothari](https://vinodkothari.com/2021/11/npa-classification-norms-2/) |
| 10 | Ind AS adoption by NBFCs (₹500 cr+ from FY19; listed / ₹250 cr+ from FY20) | MCA Ind AS roadmap | 2018–2019; in force | Ind AS 109 ECL mode as default for NBFC tenants | v2 | [PwC](https://www.pwc.in/assets/pdfs/services/ifrs/ind-as-roadmap-bank-and-insurance-2016.pdf) |
| 11 | Parallel IRACP; when Ind AS ECL < IRACP, the gap goes to Impairment Reserve; comparison disclosure | RBI Ind AS implementation guidance | 13 Mar 2020; in force | Dual-book provisioning + Impairment Reserve calc + disclosure table | v2 | [FIDC copy of RBI circular](https://fidcindia.org.in/wp-content/uploads/2020/03/RBI-IND-AS-13-03-20.pdf) |
| 12 | ECL (3 stages, SICR, EIR) with prudential floors for SCBs | RBI CB–Asset Classification, Provisioning & IR Directions | Draft 7 Oct 2025 → **final 27 Apr 2026**; effective **1 Apr 2027**; transition to 31 Mar 2031 | Floor-aware ECL engine, bank floor tables, glide-path calculator | v2 | [RBI press release](https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR150994739A099E843668A75A7F92C9E9BD1.PDF) (S-official) |
| 13 | Tiered gold LTV 85/80/75% by ticket size (≤₹2.5L / ₹2.5–5L / >₹5L) | RBI Lending Against Gold & Silver Collateral Directions | 6 Jun 2025, amended 29 Sep 2025; comply by **1 Apr 2026** | Gold LTV engine + daily MTM + breach alerts | v2 | [RBI](https://rbi.org.in/scripts/NotificationUser.aspx?Mode=0&Id=12859) (S-official) |
| 14 | Bullet loans: LTV on total repayable at maturity; tenor ≤12 months | Same | Same | Maturity-LTV projection and tenor validator | v2 | Same |
| 15 | No lending to buy gold / gold ETFs / gold MFs | Same | Same | End-use validation rule | v2 | Same |
| 16 | EWS / Red-Flagged Accounts framework extended to NBFCs | RBI MDs on Fraud Risk Management (banks, UCBs, NBFCs) | 15 Jul 2024; in force | EWS rules engine + watchlist + RFA-candidate queue with audit trail | v2 | [AZB](https://www.azbpartners.com/bank/master-directions-on-fraud-risk-management-in-banks-and-nbfcs/) |
| 17 | PCA triggers on CRAR, Tier 1, NNPA (3 thresholds) | RBI PCA framework for NBFCs | 14 Dec 2021; effective 1 Oct 2022 | PCA proximity dashboard under stress | v2 | [RBI](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12208&Mode=0) (S-official) |
| 18 | DLG cap 5% of portfolio | RBI DLG guidelines → Digital Lending Directions 2025 | 8 Jun 2023; consolidated 2025 | DLG pool tracker; ECL gross of DLG | v2 | [Mondaq](https://www.mondaq.com/india/fin-tech/1347832/guidelines-on-default-loss-guarantee-in-digital-lending) |
| 19 | ICAAP for NBFC-UL; RMC / CRO governance | RBI SBR | 22 Oct 2021 | ICAAP-lite workbook, scenario library | v2 | [RBI SBR MD 2023 PDF](https://rbidocs.rbi.org.in/rdocs/notification/PDFs/106MDNBFCS1910202343073E3EF57A4916AA5042911CD8D562.PDF) (S-official, clause detail unverified) |
| 20 | IRB ASRF risk-weight function at 99.9% | BCBS CRE31 / d424 | Dec 2017; Basel III final | Economic-capital (UL) calculator | v2 | https://www.bis.org/basel_framework/chapter/CRE/31.htm **[UNVERIFIED: blocked]** |
| 21 | Large exposures 25% of Tier 1; reporting at 10% | BCBS 283 | Apr 2014 | Top-N exposures vs Tier 1; connected-group aggregation | v2 | https://www.bis.org/publ/bcbs283.htm **[UNVERIFIED]** |
| 22 | Pillar 2 name/sector concentration | Basel II Pillar 2 | 2006 | HHI + granularity adjustment | v2 | https://www.bis.org/publ/bcbs128.htm **[UNVERIFIED]** |
| 23 | ES 97.5% replaces VaR 99% | BCBS d457 (FRTB) | Jan 2019 | ES 97.5% + stressed ES for portfolios | v1 | https://www.bis.org/bcbs/publ/d457.htm **[UNVERIFIED]** |
| 24 | Stress-testing governance principles | BCBS d450 | Oct 2018 | Versioned scenario manager, reverse stress test | v1/v2 | https://www.bis.org/bcbs/publ/d450.htm **[UNVERIFIED]** |
| 25 | 3-stage ECL; SICR; >30 DPD and 90 DPD rebuttable presumptions; POCI; forward-looking multi-scenario | IFRS 9 §5.5 / Ind AS 109 | IFRS 9 effective 2018 | Stage engine, PD term structures, scenario-weighted ECL, POCI | v2 | https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/ **[UNVERIFIED: blocked]** |
| 26 | CECL lifetime-from-day-1 | FASB ASC 326 | US, 2020+ | CECL comparison toggle | v2 | https://www.fasb.org **[UNVERIFIED]** |

---

## 6. Compliance and legal cautions for publishing Riskcore

1. **IA / RA regulations (the highest risk for v1).**
   - If the public app tells a named user to buy, sell or hold a specific security, recommends a fund switch, or produces "model portfolios", that is close to **investment advice** (IA Regs 2013) or **research** (RA Regs 2014). Both need SEBI registration, and the Dec 2024 / Jan 2025 amendments tighten the rules further.
   - Return claims and "performance promises" draw scrutiny under the finfluencer restrictions. SEBI-regulated partners (AMCs, brokers, distributors) cannot have referral or technology links with unregistered persons who give advice [S-secondary: Lexology/AZB, see §1.5].
   - **Mitigations:**
     - Ship v1 as **descriptive analytics only**: risk metrics, stress outcomes, regulatory-label reconstruction.
     - No recommendations, no ranked "best funds", no target allocations.
     - Put clear disclaimers on every page ("not investment advice; not SEBI-registered").
     - Do not monetise through AMC or distributor referral fees.
     - Get an Indian securities-law opinion before launch.
     - If advice features are ever wanted, partner with a registered IA or RIA, or register yourself.
2. **Do not impersonate official labels.**
   - Call the computed riskometer and PRC "Riskcore-estimated". Show the AMC-published label next to it.
   - Never present Riskcore output as the official SEBI/AMFI riskometer or the official APMI report.
3. **Data licensing.**
   - Exchange prices and indices (NSE/BSE, NSE Indices), AMFI NAV/portfolio files, rating agency data and bureau data carry licence terms. Redistributing them in a public app may need a licence.
   - Check that each source's terms allow commercial redistribution. This was not researched here; see the data-sources agents.
4. **v2 (loan-book) deployments.**
   - The tool processes borrower personal data. The **Digital Personal Data Protection Act, 2023** applies; its rules and status were not verified this session.
   - RBI's outsourcing and IT-governance expectations would apply to an NBFC that uses Riskcore as a vendor; those directions are not verified here.
   - **Market Riskcore as a decision-support tool.** Regulatory classification (NPA, fraud/RFA, PCA) stays the lender's own responsibility.
   - Do not publish real borrower data in demos.
5. **Regulatory drift.**
   - Thresholds change and get consolidated (RBI's 2025–26 consolidation; gold directions amended within 4 months; ECL floors).
   - Keep every threshold in **versioned, dated parameter tables** with source citations.
   - Show an "as-of regulation version" stamp on every report.
   - Mark draft-based logic clearly. For example, bank ECL is now final, but the SEBI Credit Risk-o-Meter is still a proposal.
6. **Model risk.**
   - IRB, ES and ECL outputs are model estimates. Ship model documentation, back-testing and limitation notices. This follows the spirit of the BCBS stress-testing principles and supervisory model-risk expectations (Indian model-risk guidance not verified).

---

## 7. Gaps to close (needs primary-text verification)

- Exact riskometer score bands, and the PRC CRV / Class III definitions (from the SEBI MF Master Circular 2024).
- AMFI stress-test methodology: participation %, the extra metrics, and any 2025–26 revision.
- Gold directions: valuation basis, quantity caps, auction rules, whether the LTV tiers apply to income-generating loans, and the content of the 29 Sep 2025 amendment.
- The RBI ECL 2026 floor table, SICR backstops, and whether any NBFC-specific ECL directions exist or are proposed.
- PCA threshold exact text; NBFC concentration norms for the ML/BL layers; IRACP glide-path dates for NBFCs.
- SEBI finfluencer circular number and date; Digital Lending Directions 2025 date.
- All BIS and IFRS items in §3–4. All bis.org and ifrs.org pages were blocked.

---

## 8. Bibliography (URLs seen in search results this session unless marked)

**Official (RBI):**
- RBI Lending Against Gold and Silver Collateral Directions, 2025: https://rbi.org.in/scripts/NotificationUser.aspx?Mode=0&Id=12859
- RBI Draft Lending Against Gold Collateral Directions, 2025: https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4633 ; https://website.rbi.org.in/web/rbi/-/notifications/draft-reserve-bank-of-india-lending-against-gold-collateral-directions-2025
- RBI press release on ECL final directions, 27 Apr 2026: https://rbidocs.rbi.org.in/rdocs/PressRelease/PDFs/PR150994739A099E843668A75A7F92C9E9BD1.PDF
- RBI Discussion Paper on ECL, 16 Jan 2023: https://rbidocs.rbi.org.in/rdocs/Publications/PDFs/DPECL160012023AE79B7B546C94715AA8468B0811096F5.PDF
- RBI SBR notification: https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12179&Mode=0
- RBI Master Direction – NBFC SBR, 19 Oct 2023: https://rbidocs.rbi.org.in/rdocs/notification/PDFs/106MDNBFCS1910202343073E3EF57A4916AA5042911CD8D562.PDF
- RBI PCA framework for NBFCs: https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12208&Mode=0
- RBI FAQs on NBFCs (Apr 2025): https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/ALLNBFC23042025.pdf
- RBI circular index (Ind AS 2020): https://m.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=11818

**Official (SEBI):**
- SEBI board memo on IA/RA review (Oct 2024): https://www.sebi.gov.in/sebi_data/meetingfiles/oct-2024/1728550911419_1.pdf
- SEBI FAQs on IA Regulations: https://www.sebi.gov.in/sebi_data/attachdocs/1424862077270.pdf

**Hosted copies of official circulars:**
- SEBI PMS circular, 16 Dec 2022: https://www.apmiindia.org/storagebox/images/Circulars/Performance-Benchmarking-16th-Dec'22.pdf
- RBI Ind AS circular, 13 Mar 2020: https://fidcindia.org.in/wp-content/uploads/2020/03/RBI-IND-AS-13-03-20.pdf

**Secondary:**
- Riskometer: https://taxguru.in/sebi/product-labeling-mutual-fund-schemes-risk-o-meter.html ; https://taxguru.in/sebi/evaluation-methodology-risk-level-mutual-fund-scheme.html ; https://www.valueresearchonline.com/stories/48907/decoding-the-new-riskometer/ ; https://www.valueresearchonline.com/stories/48592/sebi-rejigs-the-risk-o-meter/
- PRC matrix: https://freefincal.com/sebis-maximum-risk-matrix-for-debt-mutual-funds/ ; https://www.teamleaseregtech.com/updates/article/13716/sebi-has-issued-a-circular-for-the-potential-risk-class-matrix-for-deb/
- MF stress tests: https://www.business-standard.com/amp/markets/mutual-fund/mfs-told-to-disclose-stress-test-reports-of-midcap-smallcap-schemes-124022901229_1.html
- SEBI Credit Risk-o-Meter proposal: https://www.business-standard.com/markets/capital-market-news/sebi-proposes-credit-risk-o-meter-for-debt-securities-to-make-credit-risk-easier-to-assess-126081500533_1.html
- IA/RA amendments: https://www.azbpartners.com/bank/overhaul-of-the-regulatory-framework-for-investment-advisers-and-research-analysts/ ; https://www.lexology.com/library/detail.aspx?g=666c5c80-23cb-4217-a261-ac19257cd5b2
- Gold directions: https://www.ey.com/en_in/insights/strategy-transactions/rbi-gold-loan-guidelines-2025-impact-assessment-and-key-changes ; https://www.business-standard.com/economy/news/rbi-to-raise-gold-lending-ltv-to-85-for-loans-under-rs-2-5-lakh-malhotra-125060600690_1.html
- ECL: https://uniqus.com/rbi-draft-ecl-directions-2025/ ; https://uniqus.com/the-implementation-reality-check/ ; https://assets.kpmg.com/content/dam/kpmgsites/in/pdf/2026/05/expected-credit-loss.pdf ; https://taxguru.in/rbi/rbi-commercial-banks-asset-classification-provisioning-income-recognition-directions-2026.html ; https://www.jmfinancialservices.in/blogs-and-articles/rbi-unveils-final-ecl-framework-for-banks
- IRACP clarification: https://vinodkothari.com/2021/11/npa-classification-norms-2/
- Ind AS for NBFCs: https://vinodkothari.com/2020/03/guidance-on-implementation-of-ind-as-by-nbfcs/ ; https://www.pwc.in/assets/pdfs/services/ifrs/ind-as-roadmap-bank-and-insurance-2016.pdf
- Large exposures (NBFC-UL): https://taxguru.in/rbi/large-exposures-framework-upper-layer-nbfc-ul.html
- PCA: https://dvararesearch.com/wp-content/uploads/2024/01/Note-on-RBIs-PCA-Framework-for-NBFCs.pdf
- Fraud risk management: https://www.azbpartners.com/bank/master-directions-on-fraud-risk-management-in-banks-and-nbfcs/
- DLG: https://www.mondaq.com/india/fin-tech/1347832/guidelines-on-default-loss-guarantee-in-digital-lending ; https://vinodkothari.com/2023/06/faqs-on-default-loss-guarantee-in-digital-lending/

**Canonical but NOT seen this session (blocked / out of search budget), so treat as unverified links:**
- BIS: https://www.bis.org/basel_framework/chapter/CRE/31.htm ; https://www.bis.org/bcbs/publ/d424.htm ; https://www.bis.org/publ/bcbs283.htm ; https://www.bis.org/publ/bcbs128.htm ; https://www.bis.org/bcbs/publ/d457.htm ; https://www.bis.org/bcbs/publ/d450.htm
- IFRS: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/
- Others: https://www.mca.gov.in ; https://www.icai.org ; https://www.fasb.org
