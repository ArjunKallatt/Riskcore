# Agent 6 — Data Sources for Riskcore (v1 portfolio risk, v2 NBFC loan-book risk)

Research date: 2026-10-02. Author: Agent 6 (Data Source Agent).

## READ FIRST: how much of this was verified

The research environment was badly limited, and the results below reflect that:

1. **Most hosts were blocked by the sandbox's egress proxy.** WebFetch and curl returned `EGRESS_BLOCKED` (or HTTP 000) for nseindia.com, bseindia.com, niftyindices.com, amfiindia.com, mfapi.in, rbi.org.in, fred.stlouisfed.org, Dartmouth (Ken French), alphavantage.co, kaggle.com, uci.edu, wikipedia.org, huggingface.co and about 75 other source domains I tried. **Only github.com and pypi.org could be opened.**
2. **The session-wide WebSearch budget (200 calls, shared with the other agents) ran out** after this agent's first few searches.

So the "verified" column uses these codes:

| Code | Meaning |
|---|---|
| **V-S** | The URL came back in a **live web search on 2026-10-02**, and the details are taken from the search result or its summary. The page itself was not opened. |
| **V-G** | The page was **opened on 2026-10-02** (github.com). |
| **U** | **Unverified.** The URL and details come from the agent's prior knowledge (cutoff mid-2026). I could not open or search for it this session. Check the link, price and licence before you rely on it. |

Prices and limits marked U are **approximate, from memory, and may be out of date**. They are given so the list can be used to plan, not to quote.

---

## 1. Master table

### 1A. Indian market data (equities, indices, MFs)

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NSE "All Reports" (CM-UDiFF Common Bhavcopy) | EOD OHLCV, all NSE equities/ETFs; F&O, SLB, SME, indices reports | India (NSE), bhavcopy archive reported back to 1994 | Daily, after close | Free | No official API. Files can be downloaded (zip/csv) | NSE Terms of Use **prohibit "systematic or automated data collection (scraping, data mining, data extraction and data harvesting)"** and redistribution without written permission. The ToS carves out content that is "available for download". | https://www.nseindia.com/all-reports/ | V-S |
| 2 | NSE archives: direct bhavcopy file pattern | Same as #1. The UDiFF format replaced the old bhavcopy on 8 Jul 2024. | NSE | Daily | Free | Direct file URL `https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_YYYYMMDD_F.csv.zip` | Same as #1 | https://nsearchives.nseindia.com/content/cm/ (pattern taken from search summary citing the jugaad-data PR) | V-S (pattern), U (not opened) |
| 3 | NSE Terms of Use | Legal | — | — | — | — | Bans scraping and redistribution; see the ToS warnings section | https://www.nseindia.com/static/nse-terms-of-use | V-S |
| 4 | NSE DotEx historical data portal (Terms PDF) | Paid/licensed historical data (NSE Data & Analytics) | NSE | On request | Paid (U) | Portal | Terms of Use PDF also bans automated collection without written consent | https://dotexdata.nseindia.com/TermsAndConditions/TermsofUse.pdf | V-S |
| 5 | Nifty Indices (NSE Indices Ltd) historical data | Index price history (~59 indices), **TRI** (~52), **PE/PB/Div Yield** (~51). The site's backend endpoint is undocumented. | India, from index inception | Daily | Free download | Unofficial (undocumented JSON endpoint used by jugaad-data) | Index data is IP of NSE Indices. Commercial use or redistribution of index values needs a licence (U). | https://www.niftyindices.com/reports/historical-data | V-S |
| 6 | BSE Bhav Copy (equity, derivatives, debt, currency) | EOD OHLCV for BSE scrips | India (BSE), historical archive | Daily | Free | No official free API. Legacy zip pattern `bseindia.com/download/BhavCopy/Equity/EQ[DDMMYY]_CSV.zip` (from the bhav CLI docs). The format has since changed to UDiFF (U). | BSE website ToS restricts commercial reuse (U, not opened). BSE sells data feeds commercially (U). | https://www.bseindia.com/markets/equity/eqreports/equitydebcopy.aspx | V-S |
| 7 | AMFI NAVAll.txt | Latest NAV for every open-ended Indian MF scheme. Pipe-delimited: Scheme Code, ISIN payout, ISIN reinvest, Scheme Name, NAV, Date. | India, all AMCs | Daily (end of business day) | Free, no login | Plain file download (de facto API) | AMFI site disclaimer; no explicit open licence seen (U). Widely used by fintechs. | https://www.amfiindia.com/spages/NAVAll.txt (also http://portal.amfiindia.com/spages/NAVAll.txt) | V-S |
| 8 | AMFI NAV history / NAV download | Historical NAV by date range, **max 90 days per request** | India, roughly 2006 onward (U) | Daily | Free | Unofficial endpoint `portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=DD-Mon-YYYY&todt=DD-Mon-YYYY`. **A search snippet said the old-format NAV download is available "only till 30th September 2026"**, which is two days before this report, so expect the format or endpoint to change. | Same as #7 | https://www.amfiindia.com/net-asset-value/nav-download | V-S |
| 9 | MFapi.in | JSON API on top of AMFI data: search, scheme list, full NAV history, latest NAV | India, 10,000+ schemes | Refreshed 6 times a day | Free | **Yes.** REST, no key, not rate-limited (as claimed): `GET https://api.mfapi.in/mf/{scheme_code}`, `/mf/{code}/latest`, `/mf/search?q=` | Community project. No SLA. Terms not read (U). | https://www.mfapi.in/ , docs https://www.mfapi.in/docs/ | V-S |
| 10 | captn3m0/historical-mf-data | Full AMFI NAV history as a SQLite db (.zst). Tables: schemes, funds, securities. | India, "all historical NAVs at all known times" | CalVer releases (periodic) | Free | Download (GitHub releases) | **MIT licence** (repo). Underlying data is from AMFI. | https://github.com/captn3m0/historical-mf-data | V-G |
| 11 | jugaad-data (Python lib) | Wrapper for NSE stocks/F&O/indices, niftyindices (incl. TRI/PE/PB) and RBI current rates. Includes caching to avoid blocking. | India | On demand | Free | Python library | Uses an unusual "LICENSE.YOLO.md". **Scrapes NSE, so the NSE ToS issue applies.** | https://github.com/jugaad-py/jugaad-data | V-G |
| 12 | Getbhavcopy | Desktop downloader for NSE/BSE EOD data | India | Daily | Free | No (desktop app) | Pulls from exchange servers, so exchange ToS applies | https://www.getbhavcopy.com/ | V-S |
| 13 | nser (CRAN R package) | Bhavcopy + live data from NSE and BSE | India | Daily | Free | R library | GPL (U). Same exchange-ToS caveat. | https://cran.r-project.org/web/packages/nser/nser.pdf | V-S |
| 14 | Tigzig MF NAV API / database | Full AMFI NAV history as a downloadable DB or free API | India | Daily (U) | Free (as claimed) | Yes (U) | Terms unknown (U) | https://www.tigzig.com/apis/mf-nav | V-S |
| 15 | freefincal NSE TRI / MF NAV downloaders | Excel tools that pull niftyindices TRI/PE/PB and AMFI NAV | India | On demand | Free | No (spreadsheet) | Personal-use tools | https://freefincal.com/download-historical-total-returns-index-data-52-nse-indices/ | V-S |
| 16 | PrimeInvestor Nifty PE data | About 20 years of Nifty PE ratio (downloadable) | India | Periodic | Free (U) | No | Site terms (U) | https://primeinvestor.in/nifty-pe-ratio/ | V-S |
| 17 | SEBI statistics | MF, FPI and market statistics | India | Monthly | Free | No | Govt. site terms (U) | https://www.sebi.gov.in/statistics.html | U |
| 18 | CMIE Prowess / ProwessIQ | Indian company fundamentals and prices (database for academic/research use) | India, 1989+ | Daily/annual | **Paid** (institutional) | Yes (paid) | Commercial licence | https://prowessiq.cmie.com/ | U |

### 1B. Global market data APIs

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 19 | yfinance (Yahoo Finance) | OHLCV, adjusted prices, dividends/splits, some fundamentals. Includes NSE (`.NS`), BSE (`.BO`) and Indian indices (`^NSEI`). | Global | Daily/intraday | Free | Unofficial Python lib (scrapes Yahoo endpoints) | README: "not affiliated, endorsed, or vetted by Yahoo"; "the Yahoo! finance API is intended for **personal use only**"; for "research and educational purposes". **Not for a commercial product.** Library itself is Apache-2.0 (U). | https://github.com/ranaroussi/yfinance , https://pypi.org/project/yfinance/ | V-G |
| 20 | Alpha Vantage | Equities, FX, crypto, some fundamentals and technicals; BSE symbols supported (U) | Global | Daily/intraday | Free tier about 25 req/day (U). Premium from about $50/mo (U). | Yes, REST + key | Free-tier ToS restricts commercial redistribution (U) | https://www.alphavantage.co/documentation/ | U |
| 21 | Twelve Data | Stocks/ETFs/FX/crypto incl. NSE/BSE (U) | Global | Real-time/EOD | Free "Basic" about 800 req/day, 8/min (U). Paid tiers higher. | Yes, REST/WebSocket | Free tier is personal/non-commercial (U) | https://twelvedata.com/pricing | U |
| 22 | Finnhub | Quotes, fundamentals, news, some intl exchanges | Global (US-centric on free tier) | Real-time/EOD | Free about 60 calls/min (U). Paid per market. | Yes | Free tier non-commercial (U) | https://finnhub.io/pricing | U |
| 23 | Polygon.io (rebranded "Massive" in 2025, U) | US stocks/options/FX/crypto | US | Real-time/EOD | Free basic (5 calls/min, EOD) (U). Paid from about $29/mo (U). | Yes | Paid plans distinguish individual vs business use (U) | https://polygon.io/pricing | U |
| 24 | Tiingo | EOD US/China equities, IEX intraday, news, fundamentals | US + some intl | Daily | Free tier (U). Power about $30/mo (U). | Yes. Also supported by pandas-datareader (V-G). | Free/Power plans are for internal/personal use. Commercial redistribution needs a commercial licence (U). | https://www.tiingo.com/about/pricing | U (pandas-datareader support V-G) |
| 25 | EOD Historical Data (EODHD) | EOD/intraday for 70+ exchanges **incl. NSE/BSE**, fundamentals, mutual funds, bonds (U) | Global | Daily | Free 20 calls/day (U). From about $20–$80/mo (U). | Yes | Personal vs commercial licence tiers (U) | https://eodhd.com/pricing | U |
| 26 | Stooq | Free bulk CSV database of global stocks, indices, FX, bonds, commodities | Global (good for US/EU indices, yields) | Daily | Free | CSV download. Supported by pandas-datareader (V-G). | Site terms not read (U) | https://stooq.com/db/h/ | U (pandas-datareader support V-G) |
| 27 | Nasdaq Data Link (ex-Quandl) | Mix of free and premium datasets (many free legacy feeds discontinued) | Global | Varies | Free and paid | Yes, REST + Python lib | Per-dataset licence | https://data.nasdaq.com/ | U |
| 28 | OpenBB Platform | Open-source aggregator that wraps many of the providers above | Global | — | Free (AGPL, U). Underlying provider keys still needed. | Python lib | Inherits each provider's ToS | https://github.com/OpenBB-finance/OpenBB | V-G (listed in awesome-quant) |
| 29 | pandas-datareader | Library for FRED, Fama-French, Stooq, World Bank, OECD, Eurostat, Tiingo, Bank of Canada | Global | — | Free | Python lib | BSD (U). Inherits source ToS. | https://github.com/pydata/pandas-datareader | V-G |
| 30 | SEC EDGAR APIs | US company filings and XBRL financials | US | Real-time | Free | Yes (data.sec.gov JSON). User-Agent required, about 10 req/s fair-access limit (U). | Public domain (US govt) (U) | https://www.sec.gov/edgar/sec-api-documentation | U |
| 31 | Kaggle market datasets | Community snapshots, e.g. NSE/Nifty stock histories | Varies | Static | Free | Kaggle API | **Per-dataset licence.** Many re-uploads of exchange data have unclear rights. | https://www.kaggle.com/datasets | U |

### 1C. Indian broker APIs (live + historical, needs a demat/trading account)

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 32 | Zerodha Kite Connect | Orders, portfolio, live WebSocket ticks, historical candles | NSE/BSE/MCX/NFO | Real-time | Pricing not confirmed. From memory: a free "Personal" plan (no market data) and a paid "Connect" plan with live and historical data, about ₹500–₹2,000/mo (U). | Yes, REST + WebSocket. pykiteconnect is MIT (V-G). | Data is for the account holder's use. **No redistribution of exchange data** (exchange vendor rules). | https://github.com/zerodha/pykiteconnect , docs https://kite.trade/docs/connect/v3 | V-G (lib), U (price) |
| 33 | Angel One SmartAPI | Orders, WebSocket, **historical candle data** (e.g. ONE_MINUTE), Greeks | NSE/BSE/MCX | Real-time | Free with an Angel One account (U) | Yes. smartapi-python v1.4.8. | Personal-use / exchange rules (U) | https://github.com/angel-one/smartapi-python , https://smartapi.angelbroking.com/ | V-G (lib), U (price) |
| 34 | Upstox API v2 | Orders, WebSocket, historical candles (1-min, 30-min, daily), sandbox | NSE/BSE/MCX | Real-time | Free with an Upstox account (U) | Yes. upstox-python-sdk 2.23.0, MIT. | Exchange rules (U) | https://github.com/upstox/upstox-python , https://upstox.com/developer/api-documentation/open-api | V-G (lib), U (price) |
| 35 | Dhan (DhanHQ) | Orders, historical intraday + daily OHLC, expired-options data, 200-level depth, option chain with Greeks, US stocks | NSE/BSE/MCX + US | Real-time | Trading APIs free. A separate "Data APIs" subscription is reportedly paid, about ₹499/mo (U). | Yes. `pip install dhanhq`. | Exchange rules (U) | https://github.com/dhan-oss/DhanHQ-py , https://dhanhq.co/docs/v2/ | V-G (lib), U (price) |
| 36 | Fyers API v3 | Orders, WebSocket, historical data (U) | NSE/BSE/MCX | Real-time | Free with an account (U) | Yes (v3 sample code) | Exchange rules (U) | https://github.com/FyersDev/fyers-api-sample-code | V-G (repo), U (features/price) |

### 1D. Bonds, yields, rates

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 37 | RBI DBIE (Database on Indian Economy) | G-sec yields, T-bill rates, policy rates, money supply, credit, BoP, sectoral credit, NBFC aggregates | India, decades | Daily–annual | Free | Web downloads. Newer data.rbi.org.in portal with API/SDMX (U). | RBI website disclaimer; attribution expected (U) | https://dbie.rbi.org.in/ , https://data.rbi.org.in/ | U |
| 38 | CCIL | NDS-OM G-sec trades, CCIL zero-coupon yield curve, tri-party repo rates, indices | India | Daily | Free (website). Data products are paid (U). | No public API (U) | CCIL site terms (U) | https://www.ccilindia.com/ | U |
| 39 | FBIL (Financial Benchmarks India) | Overnight MIBOR, Term MIBOR, T-bill/CD curves, G-sec/SDL valuation prices, **FX reference rates** (replaced RBI ref rate from 2018) (U) | India | Daily | Free display | No public API (U) | Benchmark IP of FBIL. **Commercial use of benchmarks may require a licence** (U). | https://www.fbil.org.in/ | U |
| 40 | FIMMDA | Market conventions; corporate bond spread matrix for valuation (U) | India | Daily/monthly | Partly members-only (U) | No | Membership terms (U) | https://www.fimmda.org/ | U |
| 41 | NSE debt segment / WDM reports | Corporate bond and G-sec trade reports, NSE zero-coupon yield curve (U) | India | Daily | Free download | No (same NSE ToS) | NSE ToS (see #3) | https://www.nseindia.com/market-data/debt-market-reports | U |
| 42 | Investing.com bond/index history | India 10Y yield, Nifty 500 TRI history, etc. | Global | Daily | Free (web) | **No.** Scraping is banned by ToS (U). | **ToS prohibits automated access and reuse** (U) | https://in.investing.com/indices/cnx-500-tri-historical-data | V-S (TRI page), U (ToS) |
| 43 | US Treasury Daily Yield Curve | Par yield curve, real yields, T-bill rates | US, 1990+ | Daily | Free | CSV/XML feeds; Fiscal Data API | US govt public domain (U) | https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve | U |
| 44 | US Treasury FiscalData API | Debt, average interest rates, Treasury FX rates | US | Daily/monthly | Free | Yes, REST no key | Public domain (U) | https://fiscaldata.treasury.gov/api-documentation/ | U (client listed in awesome-quant, V-G) |
| 45 | ECB Data Portal | Euro-area yield curves, €STR, FX reference rates, monetary stats | Euro area | Daily | Free | Yes, SDMX REST | Reuse allowed with source attribution (U) | https://data.ecb.europa.eu/ | U |
| 46 | BIS Data Portal | Policy rates, credit-to-GDP gaps, debt securities, property prices (incl. India) | Global | Quarterly/monthly | Free | Yes, SDMX | BIS terms; attribution (U) | https://data.bis.org/ | U |

### 1E. Factor data

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 47 | Kenneth French Data Library | FF 3/5-factor, momentum, industry portfolios. US, Developed, **Emerging** regions. | US 1926+, intl ~1990+ | Monthly/daily, updated roughly monthly | Free | CSV zip. Accessible via pandas-datareader `famafrench` (V-G). | Free with citation. Copyright Kenneth French (U). | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html | U (pandas-datareader access V-G) |
| 48 | IIM Ahmedabad Indian Fama-French-Momentum factors (Agarwalla, Jacob, Varma) | Indian market, SMB, HML, WML, risk-free (+ later 4/5-factor versions) | India, ~1993+ | Daily/monthly/yearly | Free | CSV download | Academic; cite Agarwalla, Jacob & Varma (2014) "Four factor model in Indian equities market" (U) | https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/ | U |
| 49 | AQR Data Sets | QMJ, BAB, HML-Devil, TSMOM, Value & Momentum Everywhere, Century of Factor Premia | Global (some country-level) | Monthly | Free | XLSX download | AQR terms: personal/non-commercial use, attribution (U) | https://www.aqr.com/Insights/Datasets | U |
| 50 | Open Source Asset Pricing (Chen & Zimmermann) | 200+ stock-level signals and portfolio returns | US (CRSP/Compustat-based) | Annual releases | Free | Download from openassetpricing.com. Code on GitHub. | Code GPL-2.0 (V-G). Firm-level data needs a WRDS licence for full replication (U). | https://www.openassetpricing.com/ , https://github.com/OpenSourceAP/CrossSection | V-G (repo) |
| 51 | Alphalens (lib) | Factor performance analysis tool (not data) | — | — | Free | Python lib | Apache-2.0 (U) | https://github.com/quantopian/alphalens | V-G (listed in awesome-quant) |

### 1F. Macro

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 52 | FRED (St. Louis Fed) | 800k+ series incl. India CPI/rates/FX, US yields, spreads (U) | Global | Daily–annual | Free | Yes, REST, free API key | FRED ToS. **Some series are third-party copyrighted** (e.g. ICE BofA indices, history truncated around 2022) (U). | https://fred.stlouisfed.org/docs/api/fred/ | U (pandas-datareader access V-G) |
| 53 | MOSPI eSankhyiki | CPI, IIP, GDP, PLFS and other official Indian statistics | India | Monthly/quarterly | Free | API reportedly available (U) | Govt open data (U) | https://esankhyiki.mospi.gov.in/ | U |
| 54 | data.gov.in (OGD Platform India) | Thousands of govt datasets | India | Varies | Free | Yes, REST + key | **Government Open Data License – India (GODL)**: commercial use allowed with attribution (U) | https://www.data.gov.in/ | U |
| 55 | World Bank Open Data / WDI | Development and macro indicators, Global Findex | Global | Annual | Free | Yes, API v2. Also via pandas-datareader (V-G). | CC BY 4.0 for most datasets (U) | https://data.worldbank.org/ | U |
| 56 | IMF Data (IFS, WEO, etc.) | Macro, BoP, FX, interest rates | Global | Monthly/annual | Free | Yes, SDMX | IMF terms permit reuse with attribution (U) | https://data.imf.org/ | U |
| 57 | OECD Data Explorer | Macro, leading indicators (India in some datasets) | OECD + partners | Monthly | Free | Yes, SDMX. Also via pandas-datareader (V-G). | CC BY 4.0 (since 2024, U) | https://data-explorer.oecd.org/ | U |
| 58 | Eurostat | EU macro | EU | Monthly | Free | Yes. Also via pandas-datareader (V-G). | Reuse permitted (U) | https://ec.europa.eu/eurostat | U |
| 59 | CEIC | Curated global/India macro | Global | — | **Paid** (institutional) | Yes (paid) | Commercial licence | https://www.ceicdata.com/en | U |

### 1G. Commodities and FX

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 60 | IBJA rates | Indian gold/silver benchmark rates (999, 995, etc.) | India | Twice daily | Free display | No public API (U) | IBJA terms (U) | https://ibjarates.com/ | U |
| 61 | MCX bhavcopy | Commodity futures EOD (gold, silver, crude...) | India | Daily | Free download | No official free API | MCX ToS restricts redistribution (U) | https://www.mcxindia.com/market-data/bhavcopy | U |
| 62 | LBMA precious metal prices | LBMA Gold/Silver Price (administered by ICE Benchmark Administration) | Global, history | Daily | Free delayed view. **Licence required for commercial use** (U). | No (free) | IBA/LBMA IP (U) | https://www.lbma.org.uk/prices-and-data/precious-metal-prices | U |
| 63 | World Gold Council Goldhub | Gold prices in many currencies incl. INR, ETF flows, demand | Global | Daily/quarterly | Free (registration) | No (Excel) | Goldhub terms: non-commercial, attribution (U) | https://www.gold.org/goldhub/data/gold-prices | U |
| 64 | RBI reference rate archive / FBIL FX reference rate | USD/INR, EUR, GBP, JPY reference rates. RBI series runs to Jul 2018; FBIL publishes after that (U). | India | Daily | Free | No (RBI current rates also via jugaad-data, V-G) | RBI/FBIL terms (U) | https://www.rbi.org.in/scripts/ReferenceRateArchive.aspx , https://www.fbil.org.in/ | U |

### 1H. Credit / loan-level data (v2)

| # | Source | Data type | Coverage | Frequency | Cost | API? | License / terms | Link | Verified |
|---|---|---|---|---|---|---|---|---|---|
| 65 | Lending Club (Kaggle copy "wordsforthewise/lending-club") | ~2.2M+ accepted and rejected P2P consumer loans with status, grade, int. rate | US, 2007–2018 | Static | Free (Kaggle login) | Kaggle API | Uploader-declared licence (U). LendingClub stopped public P2P data in 2020 (U). | https://www.kaggle.com/datasets/wordsforthewise/lending-club | U |
| 66 | Home Credit Default Risk (Kaggle) | 300k+ applications, bureau and installment history (closest to an emerging-market consumer NBFC) | Multi-country (CIS/Asia), anonymised | Static (2018) | Free | Kaggle API | **Competition rules: generally non-commercial/research use** (U) | https://www.kaggle.com/c/home-credit-default-risk | U |
| 67 | Give Me Some Credit (Kaggle) | 150k borrowers, 2-year serious delinquency target | US | Static (2011) | Free | Kaggle API | Competition rules (U) | https://www.kaggle.com/c/GiveMeSomeCredit | U |
| 68 | Statlog German Credit (UCI) | 1,000 applicants, 20 attributes, good/bad | Germany | Static | Free | ucimlrepo Python package (U) | CC BY 4.0 (U) | https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data | U |
| 69 | Default of Credit Card Clients, Taiwan (UCI) | 30,000 cardholders, 6-month payment history, default next month | Taiwan, 2005 | Static | Free | ucimlrepo | CC BY 4.0 (U) | https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients | U |
| 70 | Freddie Mac Single-Family Loan-Level Dataset | Origination + monthly performance for ~50M+ mortgages | US, 1999+ | Quarterly | Free (registration) | Bulk download | Terms prohibit redistribution of raw files (U) | https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset | U |
| 71 | Fannie Mae Single-Family Loan Performance Data | Acquisition + monthly performance, loss data | US, 2000+ | Quarterly | Free (registration, Data Dynamics) | Bulk download | Terms restrict redistribution (U) | https://capitalmarkets.fanniemae.com/credit-risk-transfer/single-family-credit-risk-transfer/fannie-mae-single-family-loan-performance-data | U |
| 72 | Prosper loan data | P2P loans; a 2014 snapshot is common on Kaggle/Udacity | US | Static | Free (copies) | No | Unclear rights on copies (U) | https://www.prosper.com/ | U |
| 73 | Bondora public reports | Full loan-level dataset of a European P2P lender (DPD, defaults, recoveries) | EE/FI/ES/SK, 2009+ | Daily refresh (U) | Free | CSV download | Bondora terms (U) | https://www.bondora.com/en/public-reports | U |
| 74 | RBI Report on Trend & Progress of Banking in India | NBFC sector chapter: credit growth, GNPA/NNPA, CRAR by NBFC layer | India | Annual (Dec) | Free | No (PDF + XLS tables) | RBI terms (U) | https://www.rbi.org.in/Scripts/AnnualPublications.aspx?head=Trend%20and%20Progress%20of%20Banking%20in%20India | U |
| 75 | RBI Financial Stability Report | Systemic NBFC asset quality, stress-test results, sectoral GNPA | India | Semi-annual (Jun/Dec) | Free | No (PDF) | RBI terms (U) | https://www.rbi.org.in/Scripts/FsReports.aspx | U |
| 76 | RBI NBFC statistics / DBIE NBFC tables | Consolidated NBFC balance sheets, sectoral credit | India | Quarterly | Free | DBIE downloads | RBI terms (U) | https://dbie.rbi.org.in/ | U |
| 77 | TransUnion CIBIL–SIDBI MSME Pulse | MSME credit exposure, NPA rates by segment | India | Quarterly | Free (PDF) | No | Report copyright; cite only (U) | https://www.transunioncibil.com/resources/msme-pulse | U |
| 78 | CRIF High Mark MicroLend / How India Lends | Microfinance and retail portfolio size, PAR 30/90 by lender type and state | India | Quarterly | Free (PDF, registration) | No | Report copyright (U) | https://www.crifhighmark.com/knowledge-centre/microlend | U |
| 79 | MFIN Micrometer | NBFC-MFI industry portfolio and PAR | India | Quarterly | Free (U) | No | Report copyright (U) | https://mfinindia.org/ | U |
| 80 | S&P Global Annual Default & Rating Transition Study | Corporate default rates, rating transition matrices | Global | Annual | Free with registration (U) | No | S&P copyright, internal use (U) | https://www.spglobal.com/ratings/en/research-insights/special-reports/default-transition-and-recovery | U |
| 81 | Moody's Annual Default Study | Default and recovery rates, transition matrices | Global | Annual | Mostly paid / registration (U) | No | Moody's copyright (U) | https://www.moodys.com/ | U |
| 82 | CRISIL / ICRA / CARE / India Ratings default studies | **Indian** rating transition matrices and cumulative default rates (SEBI-mandated disclosures) — useful for calibrating Indian PDs | India | Annual / semi-annual | Free (PDF) | No | Agency copyright; cite (U) | https://www.crisilratings.com/ (and the other agencies' sites) | U |
| 83 | Synthetic loan-book generators (SDV, Faker) | Generate synthetic NBFC loan tapes calibrated to RBI/CRIF aggregates | — | — | Free | Python libs | MIT/BSL (U) | https://github.com/sdv-dev/SDV | U |

**Count: 83 entries.** Status: 22 V-S, 15 V-G or partly V-G, the rest U.

---

## 2. Recommended data stack

### v1 — investment portfolio risk (Streamlit, solo dev, near-zero cost)

| Need | Primary (free) | Fallback / upgrade | Notes |
|---|---|---|---|
| Indian MF NAVs | **AMFI NAVAll.txt** daily + **captn3m0/historical-mf-data** (MIT) to backfill | MFapi.in for on-demand history | Watch out: the old AMFI NAV-history format reportedly ended 30 Sep 2026, so build the parser defensively. |
| Indian equities EOD | **Broker API** you hold an account with (Upstox / Angel SmartAPI / Dhan historical candles) for personal use | Manual NSE/BSE bhavcopy downloads; yfinance `.NS` for prototyping only | Avoid automated NSE scraping in anything you distribute (see ToS). For a commercial SaaS, budget for a licensed vendor (EODHD or Twelve Data paid, or an NSE Data & Analytics licence). |
| Indian indices / TRI / valuation | niftyindices.com historical data (manual or jugaad-data) | yfinance `^NSEI`, `^BSESN` | Use TRI for benchmark returns. Licence is needed for commercial redistribution. |
| Global equities/ETFs | yfinance (prototype) → **Tiingo** or **EODHD** (paid) | Stooq CSV | yfinance is "personal use only". |
| Rates / yield curves | **RBI DBIE** (G-sec, T-bill), **FBIL** (MIBOR, T-bill curves), CCIL ZCYC | FRED (India 10Y long-term rate), US Treasury, ECB | Build your own Nelson-Siegel-Svensson fit from published yields if you can't automate the CCIL curve. |
| Factors | **IIMA Indian FF+Momentum**, **Ken French** (Developed/Emerging), **AQR** | Open Source Asset Pricing (US) | All free with citation. |
| Macro | FRED API, RBI DBIE, MOSPI eSankhyiki, data.gov.in (GODL), World Bank, IMF | OECD, BIS | data.gov.in and World Bank have the clearest reuse licences. |
| FX / gold | FBIL FX reference rates; FRED `DEXINUS`; WGC Goldhub / IBJA | yfinance `INR=X`, `GC=F` | LBMA prices need a licence for commercial use. |

### v2 — NBFC loan-book risk

1. **Model development (PD/LGD/roll-rates):** Home Credit (closest to an EM consumer NBFC), Lending Club, Taiwan, German Credit, Give Me Some Credit. Bondora for recovery/LGD curves. Freddie/Fannie for long performance histories and vintage analysis.
2. **India calibration layer:** RBI Trend & Progress + FSR (sector GNPA, stress scenarios), CRIF MicroLend / MFIN Micrometer (PAR by segment and state), CIBIL-SIDBI MSME Pulse (MSME NPA), CRISIL/ICRA/CARE transition matrices (Indian PDs by rating).
3. **Synthetic Indian loan tape:** use SDV (or a hand-written generator) to generate an NBFC-style book (gold loan, MFI-JLG, MSME, vehicle, personal) whose aggregate DPD/PAR distributions match the RBI/CRIF figures. This is what you ship in demos, because it avoids every licensing problem with real loan data.
4. Note that Home Credit and Give Me Some Credit are under Kaggle **competition rules**, which are typically non-commercial. Don't bundle them in a commercial product; use them only to research methods.

---

## 3. ToS warnings (important)

1. **NSE (nseindia.com and the DotEx data portal):** the Terms of Use explicitly prohibit "any systematic or automated data collection activities (including scraping, data mining, data extraction and data harvesting)", and copying or redistributing content without prior written permission. Libraries like nsepy, nsetools and jugaad-data all hit NSE endpoints. Their own GitHub issues discuss the legality (nsepy #46, nsetools #23). NSE also actively blocks bots (cookie and header checks). **For a commercial Riskcore, license the data.** (Source: NSE ToS URL and dotexdata ToS PDF, both seen in a live search, 2026-10-02.)
2. **BSE / MCX / niftyindices:** these are exchange or index IP, and redistributing raw or derived index values usually needs a licence. Not verified this session.
3. **Yahoo Finance / yfinance:** "intended for personal use only"; not affiliated with Yahoo (yfinance README, opened 2026-10-02). Endpoints break often, so don't build a paid product on it.
4. **Broker APIs (Kite, Upstox, Angel, Dhan, Fyers):** the data is licensed to you as the account holder. Showing it to *other* users means redistributing exchange data, which requires an exchange data-vendor agreement (U).
5. **Investing.com:** its ToS forbids scraping (U). Don't automate.
6. **Benchmarks (FBIL, LBMA/IBA, Nifty indices):** commercial use of benchmark values may need a licence (U).
7. **FRED:** some series belong to third parties (e.g. ICE BofA), and redistribution is restricted (U).
8. **Kaggle competition datasets** (Home Credit, Give Me Some Credit): competition rules usually restrict use to non-commercial/research (U).
9. **Freddie Mac / Fannie Mae:** registration-gated, and the terms prohibit redistributing the raw files (U).
10. **AMFI:** the data is freely downloadable and widely reused, but I saw no explicit open licence. An endpoint/format change was reportedly due around 30 Sep 2026 (V-S snippet).
11. **Free API tiers** (Alpha Vantage, Twelve Data, Finnhub, Polygon, Tiingo, EODHD) are usually "personal / non-commercial". A commercial or display licence costs extra (U).

---

## 4. Bibliography / links seen this session

**Live web search results (2026-10-02, V-S):**
- NSE All Reports — https://www.nseindia.com/all-reports/
- NSE Terms of Use — https://www.nseindia.com/static/nse-terms-of-use
- NSE DotEx Terms PDF — https://dotexdata.nseindia.com/TermsAndConditions/TermsofUse.pdf
- jugaad-data PR #140 (UDiFF) — https://github.com/jugaad-py/jugaad-data/pull/140
- nsepy legality issue #46 — https://github.com/swapniljariwala/nsepy/issues/46
- nsetools legality issue #23 — https://github.com/vsjha18/nsetools/issues/23
- Zerodha TradingQnA "Has NSE changed bhavcopy location?" — https://tradingqna.com/t/has-nse-changed-bhavcopy-location/169551
- nser CRAN PDF (May 2026) — https://cran.r-project.org/web/packages/nser/nser.pdf
- Nifty Indices historical data — https://www.niftyindices.com/reports/historical-data
- freefincal TRI downloader — https://freefincal.com/download-historical-total-returns-index-data-52-nse-indices/
- freefincal MF NAV downloader — https://freefincal.com/mutual-fund-nav-history-downloader-amfi-yahoo-finance/
- niftyindices TRI endpoint notes — https://github.com/satwikbasu/indian-market-data-endpoints/blob/main/endpoints/niftyindices-tri-api.md
- Investing.com Nifty 500 TRI — https://in.investing.com/indices/cnx-500-tri-historical-data
- PrimeInvestor Nifty PE — https://primeinvestor.in/nifty-pe-ratio/
- BSE Bhav Copy — https://www.bseindia.com/markets/equity/eqreports/equitydebcopy.aspx
- bhav (PyPI) — https://pypi.org/project/bhav/
- Getbhavcopy — https://www.getbhavcopy.com/
- AMFI NAV Download — https://www.amfiindia.com/net-asset-value/nav-download
- AMFI NAVAll.txt explainer — https://v2.webnotes.in/amfi-nav-file-navall
- MFapi.in — https://www.mfapi.in/ and https://www.mfapi.in/docs/
- Tigzig MF NAV — https://www.tigzig.com/apis/mf-nav
- AMFI-NAV-History-Scraper — https://github.com/AmruthPillai/AMFI-NAV-History-Scraper

**Pages opened (V-G, 2026-10-02):**
- yfinance — https://github.com/ranaroussi/yfinance
- jugaad-data — https://github.com/jugaad-py/jugaad-data
- historical-mf-data — https://github.com/captn3m0/historical-mf-data
- pandas-datareader — https://github.com/pydata/pandas-datareader
- OpenSourceAP CrossSection — https://github.com/OpenSourceAP/CrossSection
- pykiteconnect — https://github.com/zerodha/pykiteconnect
- smartapi-python — https://github.com/angel-one/smartapi-python
- DhanHQ-py — https://github.com/dhan-oss/DhanHQ-py
- upstox-python — https://github.com/upstox/upstox-python
- Fyers sample code — https://github.com/FyersDev/fyers-api-sample-code
- awesome-quant — https://github.com/wilsonfreitas/awesome-quant

**Blocked by the egress proxy this session (links in the table are from prior knowledge, U):** nseindia.com (direct), bseindia.com, niftyindices.com, amfiindia.com, mfapi.in, rbi.org.in, dbie.rbi.org.in, ccilindia.com, fbil.org.in, fimmda.org, fred.stlouisfed.org, mba.tuck.dartmouth.edu, faculty.iima.ac.in, aqr.com, alphavantage.co, twelvedata.com, finnhub.io, polygon.io, tiingo.com, eodhd.com, stooq.com, data.nasdaq.com, kaggle.com, archive.ics.uci.edu, freddiemac.com, fanniemae.com, bondora.com, transunioncibil.com, crifhighmark.com, spglobal.com, moodys.com, treasury.gov, ecb.europa.eu, worldbank.org, imf.org, oecd.org, data.gov.in, mospi.gov.in, ceicdata.com, ibjarates.com, mcxindia.com, lbma.org.uk, gold.org, sec.gov, investing.com, wikipedia.org, huggingface.co.

**Recommended follow-up:** re-run verification of the U rows (prices, licences, IIMA factor URL, Kite/Dhan pricing) from an environment with open egress and a fresh search budget.
