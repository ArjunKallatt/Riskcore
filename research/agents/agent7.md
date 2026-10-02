# Agent 7: Tech stack and architecture for Riskcore

*Research date: 2026-10-02. Author: Agent 7 (Tech Stack & Architecture).*

## 0. Method, tool limits and how to read the citations

- **Web access was only partly available.** The egress proxy blocked direct WebFetch for most vendor documentation sites: docs.streamlit.io, duckdb.org, arcticdb.io, man.com, huggingface.co, render.com, fly.io, docs.railway.com, docs.github.com, bis.org, mathworks.com, wikipedia.org, pydata.org, calpaterson.com, news.ycombinator.com and engineering.blackrock.com. **github.com and raw.githubusercontent.com were reachable.** Because many vendors keep their docs in GitHub repositories, I read primary docs that way where I could: Streamlit docs, Hugging Face hub-docs, DuckDB docs, and the ArcticDB README.
- WebSearch worked for about 20 queries, then hit the session's shared search budget (200/200). After that I used only GitHub-hosted sources.
- **Citation tags:**
  - **[P]**: I opened the primary source page or file myself.
  - **[S]**: the claim comes from a WebSearch result summary or snippet for the linked page. I saw the link in the results but could not open the page because of the proxy. Treat these as lower confidence.
  - **[unverified]**: background knowledge I could not confirm in this session.
- **Age flags:** ⚠ >3y marks a source more than 3 years old (before October 2023).

---

## 1. What Riskcore is today (from the repo)

`riskcore/{data,metrics,stress,sample}.py`, a single-page Streamlit `app.py`, and `tests/test_riskcore.py`, about 280 lines in total. The dependencies are numpy, pandas, scipy, streamlit, plotly, yfinance and pytest. Data comes from Yahoo `.NS` tickers, with a synthetic fallback. The scale is tiny (tens of tickers, about 3 years of daily data), so **every recommendation below is sized for megabytes, not terabytes.** v2 (an NBFC loan book) adds tabular, loan-level data (maybe 10^4 to 10^6 loans), monthly snapshots, and IFRS 9 / Ind AS 109 ECL runs. Those runs are batch and auditable, and that need for auditability drives the data-layer choice.

---

## 2. How practitioners build these systems (reference architectures)

| System | What is publicly known | Lesson for Riskcore | Source |
|---|---|---|---|
| **JPMorgan Athena** | Python-based pricing, trading and risk platform, started in 2006. About 35M lines of Python 2.7. The Python 3 migration started in 2018. C++ underneath for speed-critical parts. | Python as the "glue + model" language with a compiled core is a proven pattern at the very top end. A huge monolith is a migration liability, so keep Riskcore modular and dependency-light. | [S] [TechRepublic](https://www.techrepublic.com/article/jpmorgans-athena-has-35-million-lines-of-python-code-and-wont-be-updated-to-python-3-in-time/) (c. 2019, ⚠ >3y); [S] [eFinancialCareers 2021](https://www.efinancialcareers.com/news/2021/02/jpmorgan-still-has-its-python-2-issue) ⚠ >3y; [S] [Python Bytes #152](https://pythonbytes.fm/episodes/show/152/you-have-35-million-lines-of-python-2-now-what) ⚠ >3y |
| **Goldman SecDB → Athena → BofA Quartz** | Kirat Singh built SecDB at Goldman, then led Athena and Quartz. Quartz's object database is called "Sandra". These are lineage "Bank Python" platforms built on a global object store, a dependency graph and a job runner. | The core idea is **a dependency graph of computations over versioned data**. A solo developer can get roughly 80% of that with pure functions, Parquet snapshots and an orchestrator that tracks assets (Dagster) or flows (Prefect). | [S] [eFinancialCareers 2017](https://www.efinancialcareers.com/news/2017/03/secdb-quartz-athena-analytics) ⚠ >3y; [S] [HN "An oral history of Bank Python"](https://news.ycombinator.com/item?id=29104047) (2021, ⚠ >3y). The essay itself (calpaterson.com) was **blocked**, so its details (Barbara/Dagger/Walpole) are **[unverified]** in this session. |
| **BlackRock Aladdin** | Built with Java, Python, SQL/NoSQL, Kafka, Kubernetes, Docker, Angular/React. Has an internal messaging system with clients in many languages. BlackRock open-sourced a Python **Aladdin SDK** that wraps auth, retries and data transforms. | Real enterprise risk platforms are **API-first services** with thin SDKs and UIs on top. The stage-3 target is "FastAPI service + SDK + UI", not "a bigger Streamlit". | [S] [BlackRock Eng blog index](https://blackrock-eng.medium.com/); [S] [Aladdin SDK post](https://engineering.blackrock.com/open-sourcing-the-aladdinsdk-empower-python-developers-with-a-quantitative-edge-7f63376061e6) (blocked; date unverified); [S] [BlackRock Messaging System](https://medium.com/blackrock-engineering/the-blackrock-messaging-system-aeae461e4211) |
| **Man Group Arctic / ArcticDB** | Arctic (LGPL, MongoDB-backed) has been in maintenance mode, and development moved to ArcticDB. ArcticDB is a C++-accelerated, Python-native DataFrame database on S3, Azure or LMDB, with versioning and snapshots. **License: BSL 1.1. Production or commercial use requires a paid licence.** Each version converts to Apache 2.0 after about 3 to 4 years (e.g. v1.0 on 2025-03-16, v6.21 on 2028-08-04). Bloomberg partnership announced 2023-02-27. | A strong fit for "versioned DataFrames", but **the licence rules it out** for a commercial Riskcore unless you pay. The idea (versioned, snapshotted frames) can be copied with Parquet plus run IDs, or with DuckLake or Iceberg later. | [P] [ArcticDB GitHub](https://github.com/man-group/ArcticDB), [P] [README (raw)](https://raw.githubusercontent.com/man-group/ArcticDB/master/README.md), [P] [Arctic (legacy)](https://github.com/man-group/arctic); [S] [Bloomberg/Man press](https://www.man.com/news-centre/man-group-brings-powerful-dataframe-database-product-arcticdb-to-market-with-bloomberg) (2023-02, ⚠ >3y) |
| **OpenBB Platform** | `openbb-core` is a runtime that "ships no data and no commands". It discovers **extensions via entry points**: routers (command namespaces), providers (data sources) and OBBject extensions (result accessors). The same core is exposed as a Python package, a FastAPI REST API and an MCP server. Apache 2.0. | **This is the best template for Riskcore's data layer:** a `providers/` plugin interface (yfinance, synthetic, NSE file, later a paid feed). The core stays data-agnostic, and one core serves Python, the API and the UI. | [P] [OpenBB repo](https://github.com/OpenBB-finance/OpenBB), [P] [openbb_platform tree](https://github.com/OpenBB-finance/OpenBB/tree/develop/openbb_platform) |
| **Quantopian / zipline** | Event-driven backtester, pandas in and out, "data bundles" ingested via `zipline ingest`. Quantopian closed in late 2020. Stefan Jansen maintains the `zipline-reloaded` fork (pandas ≥ 2, NumPy 2 support). | **Ingest → bundle → compute** separation: the ingest step writes a local, versioned store, and compute reads only from that store. Also a warning: a platform tied to one company's survival dies with it, so prefer standard formats (Parquet). | [P] [quantopian/zipline](https://github.com/quantopian/zipline); [P] [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded) |
| **PyData talk: "Creating a contemporary risk management system" (C2FO)** | A risk suite for underwriting and portfolio management on the PyData stack, with pandas for data prep and time-series cleaning. | Shows that the PyData stack alone is enough for a credit-plus-portfolio risk system at small or medium scale. | [S] [PyData Chicago 2016](https://pydata.org/chicago2016/schedule/presentation/12/) ⚠ >3y (page blocked) |
| **Recent solo projects on GitHub (for calibration)** | Several 2026 Python "market-risk-engine" repos combine VaR/ES, Kupiec/Christoffersen/Basel traffic-light backtesting, stress tests and a Streamlit or Dash UI, and one uses PostgreSQL. | Confirms the common solo pattern: one Python package, a backtest module and a thin UI. These are low-star repos, so they show common practice, not authority. | [P] search via GitHub API: [marksguo/frtb-ima-risk-monitor](https://github.com/marksguo/frtb-ima-risk-monitor), [chenxi-bot21/market-risk-engine](https://github.com/chenxi-bot21/market-risk-engine), [ShrishDhuria/market-risk-engine](https://github.com/ShrishDhuria/market-risk-engine) |

**Synthesis.** All the big platforms share the same shape: **a versioned data store → a dependency graph of pure computations → results stored with run IDs → API → thin UIs.** Riskcore should adopt that shape from day one in miniature, as folder boundaries rather than infrastructure.

---

## 3. Layer-by-layer comparison

### 3.1 Data layer

| Option | What it is | License | Fit for Riskcore | Source |
|---|---|---|---|---|
| **Parquet files (via pandas/pyarrow)** | Columnar files on disk or S3 | Apache (Arrow) | ✅ Stage 1 raw and curated storage. Portable, diffable by run, readable by DuckDB, Polars and pandas. | [unverified] general knowledge; DuckDB reads Parquet [P] [duckdb repo](https://github.com/duckdb/duckdb) |
| **DuckDB** | In-process analytical SQL. Queries pandas, Polars and Arrow objects directly (read-only scans). Returns `.df()`, `.pl()`, `.arrow()`, `.fetchnumpy()`. Persistent single-file DB. | MIT | ✅✅ **Stage 1 to 2 primary store.** Zero ops, SQL over Parquet. **Constraint:** only *one process* can open a database read-write; several processes can open it read-only. Multi-writer setups need DuckLake with a Postgres catalog, or the beta "Quack" protocol. | [P] [DuckDB README](https://github.com/duckdb/duckdb), [P] [Python client docs](https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/clients/python/overview.md), [P] [Concurrency docs](https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/connect/concurrency.md) |
| **SQLite** | Embedded row-store | Public domain [unverified] | OK for small app state (users, saved portfolios), but DuckDB covers analytics better. Optional. | [unverified] |
| **PostgreSQL** | Server RDBMS | PostgreSQL licence [unverified] | ✅ **Stage 2 to 3** system of record for multi-user state (portfolios, loan tapes, run metadata, audit) and for concurrent writes. It is also the catalog DuckDB recommends for DuckLake. | DuckLake + Postgres recommendation: [P] [concurrency docs](https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/connect/concurrency.md) |
| **TimescaleDB** | Postgres extension for time series | Dual: Apache 2.0 core plus proprietary **TSL** for features in `/tsl`. Company now "Tiger Data". | Only worth it if intraday ticks arrive. Daily NAV and price data do not need it. Stage 3 at most. | [P] [timescale/timescaledb](https://github.com/timescale/timescaledb) |
| **QuestDB** | Low-latency time-series DB. SQL extensions `SAMPLE BY`, `LATEST ON`, `ASOF JOIN`. Supports the Postgres wire protocol and InfluxDB line protocol. | Apache 2.0 | Overkill for daily risk. Consider only for a stage-3 real-time or intraday market data feed. | [P] [questdb/questdb](https://github.com/questdb/questdb) |
| **ArcticDB** | Versioned DataFrame DB on S3 or LMDB | **BSL 1.1: no free production or commercial use** | ❌ for a commercial product unless licensed. Fine for personal, non-production experiments. | [P] [ArcticDB](https://github.com/man-group/ArcticDB) |
| **pandas vs Polars** | Polars is a Rust, multi-threaded engine with a lazy API, a query optimiser and a streaming engine for data larger than RAM. MIT. | – | Keep **pandas** in `metrics/` (the user knows it, and scipy, statsmodels and plotly interoperate). Use **Polars** (or DuckDB SQL) in ETL and loan-book aggregation, where row counts reach 10^6 and above. Convert at the boundary via Arrow. | [P] [pola-rs/polars](https://github.com/pola-rs/polars) |

### 3.2 Pipelines and scheduling

| Option | Model | License / ops | Fit | Source |
|---|---|---|---|---|
| **cron / Windows Task Scheduler + `python -m riskcore.pipelines.daily`** | Plain scheduler | none | ✅ Stage 1. A good enough start. | [unverified] |
| **GitHub Actions `schedule:`** | Cron in CI | free for public repos | ✅ Stage 1 to 2 for a nightly "fetch prices → write Parquet → commit or upload artifact" job. **Caveat:** in public repos, scheduled workflows are **auto-disabled after 60 days without repo activity**, silently. Only new commits reset the timer, per one source. Scheduled runs can also be delayed. | [S] [zenn.dev article](https://zenn.dev/hellorusk/articles/fc6d4696f5b269?locale=en), [S] [dev.to](https://dev.to/procwire/why-your-scheduled-github-actions-workflow-runs-late-or-stops-running-entirely-173h), [P-ish] [gh-action-keepalive repo](https://github.com/efrecon/gh-action-keepalive) (title states the rule; README not opened). The GitHub docs page was **blocked**. |
| **Prefect** | `@flow`/`@task` decorators on plain Python. Cron and event schedules, retries, caching. Self-hosted server UI on :4200, or Prefect Cloud. | Apache 2.0 | ✅ **Stage 2 recommendation.** Lowest boilerplate for a solo Python developer. Comparisons consistently call it the lightest option for small teams. | [P] [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect); [S] [ZenML comparison](https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow), [S] [DZone](https://dzone.com/articles/airflow-vs-dagster-vs-prefect-which-scheduler-fits) |
| **Dagster** | **Asset-based**: you declare data assets as functions, and Dagster shows their lineage. Strong testability. | Apache 2.0 | ✅ **Stage 3 alternative.** The asset model maps closely onto "SecDB-style dependency graph" and onto regulatory lineage (e.g. "which PD curve fed this ECL number?"). Heavier to learn. | [P] [dagster-io/dagster](https://github.com/dagster-io/dagster) |
| **Airflow** | DAG scheduler | Apache 2.0 [unverified] | ❌ for a solo developer. Comparisons note it needs more care: the metadata DB, scheduler tuning and executors. | [S] [DZone](https://dzone.com/articles/airflow-vs-dagster-vs-prefect-which-scheduler-fits), [S] [getorchestra 2026](https://www.getorchestra.io/blog/dagster-vs-prefect-vs-airflow-complete-data-orchestration-comparison-2026) |

### 3.3 Caching

| Option | Notes | Fit | Source |
|---|---|---|---|
| **`st.cache_data` / `st.cache_resource`** | `cache_data` returns a **copy** of serialisable results (DataFrames). `cache_resource` keeps a singleton for connections and models, which must be thread-safe. Both support `ttl` and `max_entries`. The cache is **in-memory and per process**: it is lost on restart and not shared across replicas. | ✅ Stage 1 to 2 UI-level caching | [P] [Streamlit caching docs](https://raw.githubusercontent.com/streamlit/docs/main/content/develop/concepts/architecture/caching.md) |
| **diskcache** | Pure Python, disk-backed, thread-safe *and process-safe*, LRU/LFU eviction, memoisation recipes. | ✅ Stage 1 to 2 for yfinance responses and expensive Monte Carlo results, shared between the pipeline process and the UI process. Note: docs list Python 3.6 to 3.10 support, and the release cadence looks slow, so check activity before relying on it. | [P] [python-diskcache](https://github.com/grantjenks/python-diskcache) |
| **Redis** | In-memory server. **Redis 8+ is tri-licensed RSALv2 / SSPLv1 / AGPLv3.** | Stage 3 only (multi-replica API, job queues). Note the licence. Valkey is a BSD fork [unverified]. | [P] [redis/redis](https://github.com/redis/redis) |
| **"Results store as cache"** | Persist each risk run to `results/run_id=…/*.parquet` and have the UI read the latest run | ✅ **The most important "cache"**: it makes the UI fast and the numbers reproducible. | design recommendation |

### 3.4 Compute

| Option | Notes | Fit | Source |
|---|---|---|---|
| **numpy (vectorised)** | Already in use | ✅ Default. Historical/parametric VaR and MC on about 50 assets × 10^5 paths is a few hundred MB, which vectorises fine. | [unverified] sizing estimate |
| **numba** | LLVM JIT for NumPy-style code. `@njit`, `prange` auto-parallel loops, GPU support. BSD-2. | ✅ Stage 2 for path-dependent loops numpy cannot vectorise: loan-level amortisation, prepayment and default simulation per month, or drawdown-based stress paths. | [P] [numba/numba](https://github.com/numba/numba) |
| **JAX** | XLA `jit`, `vmap`, `grad`. CPU/GPU/TPU. Apache 2.0. | Optional stage 3: GPU Monte Carlo, or autodiff Greeks and sensitivities (∂ES/∂w). Steeper learning curve, so not needed for v1. | [P] [jax-ml/jax](https://github.com/jax-ml/jax) |
| **Polars / DuckDB** | Multi-threaded aggregation | ✅ Loan-book roll-ups (ECL by stage, segment or vintage) | [P] links above |
| **Dask** | Parallel task scheduling; New BSD | Stage 3 if a single machine is not enough | [P] [dask/dask](https://github.com/dask/dask) |
| **Ray** | Distributed runtime (tasks, actors, objects) plus AI libraries; Apache 2.0 | Stage 3 if you add a distributed scenario grid or ML PD models at scale | [P] [ray-project/ray](https://github.com/ray-project/ray) |

### 3.5 Frontends

| Option | Architecture | Pros for a risk dashboard | Cons | License | Source |
|---|---|---|---|---|---|
| **Streamlit** (current) | Script reruns top to bottom on each interaction. Multipage apps, caching, **native OIDC auth** (`st.login()`, `st.user`, `st.logout()`, configured in `secrets.toml`). | Fastest to build. The user already knows it. Auth is now built in, which covers stage 2. | The rerun model gets awkward for complex cross-filtering and long jobs. Note: "external pull requests are paused" on the repo. | Apache 2.0 | [P] [streamlit repo](https://github.com/streamlit/streamlit), [P] [auth docs](https://raw.githubusercontent.com/streamlit/docs/main/content/develop/concepts/connections/authentication.md) |
| **Dash** | Flask + React + Plotly.js, explicit callbacks | Best for "production" dashboards with heavy plotly cross-filtering. Background callbacks. Riskcore already uses plotly. | More boilerplate. Auth, scaling and job queues sit in paid Dash Enterprise. | MIT | [P] [plotly/dash](https://github.com/plotly/dash); [S] [Kanaries comparison](https://docs.kanaries.net/topics/Streamlit/streamlit-vs-dash) |
| **Panel (HoloViz)** | Works with Bokeh, Plotly, Matplotlib and more. Runs on Tornado, Flask, Django or FastAPI, or in the browser via Pyodide. | Most flexible. Good for notebook-to-app. | Smaller community. More concepts to learn. | BSD-3 | [P] [holoviz/panel](https://github.com/holoviz/panel) |
| **Shiny for Python** | Formal reactive graph, modules, Express and Core APIs | Reactive model avoids Streamlit's full reruns. Shinylive runs in the browser. | Smaller Python ecosystem than Streamlit. | MIT | [P] [posit-dev/py-shiny](https://github.com/posit-dev/py-shiny) |
| **NiceGUI** | FastAPI backend + Vue/Quasar frontend over socket.io | Event-driven (no reruns), and FastAPI sits underneath, so the API and the UI can share one process. | Less "data-app" oriented. Smaller ecosystem. | MIT | [P] [zauberzeug/nicegui](https://github.com/zauberzeug/nicegui) |
| **React + FastAPI** | Separate SPA and API | Enterprise-grade UX, RBAC, many users. This is the Aladdin pattern (Angular/React on services). | Requires JS/TS skills, and roughly doubles the codebase. | – | [S] BlackRock stack, see §2 |
| **Evidence.dev** | Reports as SQL + Markdown that build to a static site. DuckDB in its stack. | Excellent for **static, scheduled board, ALCO or risk-committee reports** (v2 NBFC monthly ECL pack) next to an interactive app. | Not interactive what-if. | MIT | [P] [evidence-dev/evidence](https://github.com/evidence-dev/evidence) |
| **Observable Framework** | JS static data apps | Similar niche to Evidence | JS-first | – | **[unverified]**: could not fetch observablehq.com in this session |

General comparison sources: [S] [Ploomber survey](https://ploomber.io/blog/survey-python-frameworks/), [S] [Deepnote alternatives](https://deepnote.com/compare/alternatives/streamlit), [S] [Panel author's rationale](https://medium.com/@marcskovmadsen/i-prefer-to-use-panel-for-my-data-apps-here-is-why-1ff5d2b98e8f) (date unverified).

### 3.6 Deployment

| Option | Free-tier facts | Fit | Source |
|---|---|---|---|
| **Streamlit Community Cloud** | CPU 0.078 to 2 cores, **memory 690 MB to 2.7 GB**, storage up to 50 GB (docs say "as of February 2024"). **Apps sleep after 12 h without traffic.** Deploys from a GitHub repo. | ✅ Stage 1 public demo. Keep MC path counts modest. No persistent writable DB, so data must come from the repo, an artifact or object storage. | [P] [streamlit/docs source](https://raw.githubusercontent.com/streamlit/docs/main/content/deploy/community-cloud/manage-your-app/_index.md) |
| **Hugging Face Spaces** | Default hardware: 16 GB RAM, 2 CPU, 50 GB **non-persistent** disk. **Current docs: Gradio and Docker Spaces require a paid plan (PRO or Team); static Spaces are free.** Free Spaces auto-sleep. Secrets supported. | Now **paid** for a Docker or Streamlit app. Older blogs saying "free CPU basic" are out of date. | [P] [hub-docs spaces-overview](https://raw.githubusercontent.com/huggingface/hub-docs/main/docs/hub/spaces-overview.md); older claim of 48 h sleep [S] [eesel](https://www.eesel.ai/blog/hugging-face-pricing) |
| **Render** | Free web services **spin down after 15 min idle**, take about 1 min to cold-start, and get 750 instance-hours/month. The free Postgres has an expiry (search titles mention "30-day DB"). | Stage 2 option (paid instance plus managed Postgres). | [S] [Render article](https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026), [S] [justinmckelvey](https://justinmckelvey.com/blog/is-render-free); render.com docs **blocked** |
| **Fly.io** | Free allowances removed for orgs created after 2024-10-07. Trial only, then pay-as-you-go (a shared 256 MB VM is about $1.94/month). | Stage 2 to 3: cheap always-on Docker. | [S] [Orb](https://www.withorb.com/blog/flyio-pricing), [S] [ExpressTech](https://expresstech.io/7-fly-io-alternatives-in-2026-real-pricing-after-the-free-tier-died/); fly.io **blocked** |
| **Railway** | $5 one-time trial credit. Hobby plan is $5/month including $5 of usage. | Stage 2: easiest "app + Postgres" in one project. | [S] [saaspricepulse](https://www.saaspricepulse.com/tools/railway), [S] [makerkit](https://makerkit.dev/pricing-calculator/railway) |
| **Docker** | – | ✅ From stage 2, ship one image (`riskcore` + UI) so it runs on any of the above or on-prem at an NBFC. | design recommendation |

### 3.7 Testing and model validation

| Layer | Tool / practice | Notes | Source |
|---|---|---|---|
| Unit | **pytest** (already used) | Golden-number tests on fixed synthetic data (seeded) | repo |
| Property-based | **Hypothesis** | Generates inputs and shrinks failures to a minimal example. Invariants to test: VaR is monotone in confidence level; CVaR ≥ VaR; sum of risk contributions = portfolio vol; weights scale linearly; ECL ≥ 0 and Stage 3 ECL ≥ Stage 1 for the same exposure. Numpy and pandas strategy extras exist per the docs (extras page not opened, **[unverified]**). | [P] [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) |
| VaR backtesting | Exception counting with **Kupiec POF** (unconditional coverage), **Christoffersen** (independence / conditional coverage) and the **Basel traffic light** (250 days at 99%: green 0 to 4, yellow 5 to 9, red ≥ 10 exceptions) | Thresholds are standard, but I could **not open** the BIS 1996 framework or the MathWorks docs (blocked), so they are **[unverified] in this session**. Several 2026 open-source engines implement exactly this trio ([P] repos in §2). | BIS URL (blocked): https://www.bis.org/publ/bcbsc223.pdf ⚠ >3y |
| ECL / PD validation (v2) | Discrimination (AUC/Gini, KS), calibration (binomial / Hosmer-Lemeshow), stability (PSI), back-testing PD versus realised default rates | **[unverified]** in this session. Defer to the credit-risk agent's sources. | – |
| Data validation | pandera or pydantic schemas on ingest | **[unverified]**: not researched here | – |

---

## 4. Recommended stack and reasoning table

| Component | Choice (stage 1 → 2) | Alternatives considered | Why |
|---|---|---|---|
| Language/core | Python 3.11+ package `riskcore` with pure functions | – | The user's strength. Athena shows Python scales as the risk language ([S] TechRepublic). |
| DataFrames | **pandas** in models; **Polars** in ETL and loan-book aggregation | Polars everywhere | Lowest switching cost. Polars' lazy/streaming engine is useful only where row counts are large ([P] Polars). |
| Storage (raw/curated) | **Parquet** partitioned by `source/date` | CSV, ArcticDB | Open format survives vendor death (lesson from zipline). ArcticDB is BSL ([P]). |
| Analytical DB | **DuckDB** single file `riskcore.duckdb` + SQL views over Parquet | SQLite, Postgres | Zero-ops, MIT, queries pandas and Polars directly ([P] DuckDB docs). |
| System of record (stage 2+) | **PostgreSQL** (managed on Railway, Render or Neon) | Keep DuckDB only | DuckDB is single-writer ([P] concurrency docs). Multi-user writes, audit and RBAC need a server DB. Postgres can later serve as the DuckLake catalog. |
| Time-series DB | **None** until intraday | TimescaleDB, QuestDB | Daily data does not justify the ops. Revisit at stage 3 (QuestDB is Apache 2.0, Timescale has TSL parts). |
| Data providers | **Plugin interface** `providers/{yfinance,synthetic,csv_upload,…}` | Hard-coded yfinance | OpenBB's provider/extension pattern ([P]). Also isolates yfinance fragility. |
| Orchestration | Stage 1: **cron or GitHub Actions**. Stage 2: **Prefect**. Stage 3: Prefect or **Dagster** | Airflow | Prefect is decorator-light and Apache 2.0 ([P]). Dagster's asset lineage suits regulatory audit ([P]). Airflow is ops-heavy ([S]). |
| Caching | `st.cache_data` (UI) + **diskcache** (fetch/MC) + **persisted run results** | Redis | Streamlit cache is per process and in memory ([P]). diskcache is process-safe ([P]). Redis 8 licensing and ops are only worth it at stage 3 ([P]). |
| Compute | numpy → **numba** for loops → JAX optional | Dask, Ray | Scale is small. numba speeds up loan-level simulation loops. Dask and Ray only for clusters ([P] each). |
| UI | **Streamlit** (multipage + `st.login` OIDC) | Dash, Panel, Shiny, NiceGUI | Already built, and auth is native now ([P]). Move to Dash only if cross-filter UX hurts. Use React only at stage 3. |
| Static reports | **Evidence.dev** over the DuckDB file (v2 monthly ECL / committee pack) | Observable, PDF via Jinja | MIT, SQL + Markdown, static output ([P]). |
| API (stage 2+) | **FastAPI** `riskcore.api` | Flask | Same shape as OpenBB (core → REST) and Aladdin (services + SDK). FastAPI choice itself is **[unverified]** beyond OpenBB using it ([P]). |
| Hosting | Stage 1: **Streamlit Community Cloud**. Stage 2: **Docker on Railway, Render or Fly** + managed Postgres. Stage 3: container platform or on-prem k8s at an NBFC | HF Spaces | Community Cloud is free but limited to 2.7 GB and sleeps after 12 h ([P]). HF Docker Spaces are now paid ([P]). |
| Testing | pytest + **Hypothesis** + VaR backtest module (Kupiec/Christoffersen/traffic light) + golden datasets | – | Property tests catch numerical edge cases ([P] Hypothesis). Backtesting is the industry-standard model check (thresholds **[unverified]** here). |
| CI | GitHub Actions: lint (ruff), pytest, nightly data job | – | Watch the 60-day disable rule ([S]). |

---

## 5. Upgrade path

### Stage 1: Solo / local (now to v1.x). Cost: $0
- Same repo, refactored into `providers/`, `models/`, `pipelines/`, `store/`, `ui/`.
- `python -m riskcore.pipelines.daily` writes `data/raw/*.parquet` → `data/curated/*.parquet` → `riskcore.duckdb` and `data/results/run_id=…/`.
- Streamlit reads **results** (fast) and recomputes only what-if requests on demand (cached).
- Scheduling: local cron, or a GitHub Actions nightly job that uploads Parquet as an artifact or commits it to a data branch. Add a keepalive commit for the 60-day rule.
- Deploy a public demo on Streamlit Community Cloud (synthetic data plus yfinance).
- Tests: pytest, Hypothesis invariants, and a VaR backtest report.

### Stage 2: Hosted multi-user (v2 NBFC pilot). Cost: about $5 to $30/month
- Add **Postgres** for users, portfolios, loan tapes, `runs` (run_id, inputs hash, code version, timestamps) and audit log. DuckDB stays the analytical engine, reading Parquet and Postgres.
- **Prefect** flows: `ingest_market`, `ingest_loan_tape`, `compute_portfolio_risk`, `compute_ecl`, `backtest_var`, with retries and schedules.
- **Streamlit `st.login()`** with Google or Entra OIDC, and per-tenant row filtering in queries.
- **FastAPI** `riskcore.api` exposes `/runs`, `/portfolio/{id}/risk`, `/ecl/{run}` (the UI can still import the core directly).
- **Docker** image deployed to Railway, Render or Fly. Parquet in S3-compatible storage (R2, B2 or S3).
- Evidence.dev monthly ECL pack built in CI from the DuckDB file.

### Stage 3: Serious / enterprise (multiple NBFCs, regulatory reliance)
- Swap the orchestrator to **Dagster** (asset lineage for "which PD/LGD vintage produced this ECL").
- Data lake with table format (DuckLake on Postgres catalog per DuckDB docs, or Iceberg **[unverified]**); immutable snapshots per reporting date.
- API-first: FastAPI services + Python SDK (Aladdin SDK pattern) + React or Dash UI; RBAC, SSO, audit.
- Redis or Valkey for job queues and shared caches. numba, then JAX or Ray, for large MC or scenario grids. QuestDB if intraday data arrives.
- Formal model validation: independent challenger models, backtesting MI, model inventory, and change control tied to code version.
- Kubernetes or managed containers. On-prem option for NBFC data-residency needs (RBI requirements **[unverified]**; see the regulatory agent).

---

## 6. Architecture diagram

```
                 +-------------------- providers/ (plugins) ---------------------+
                 | yfinance | synthetic | csv/xlsx upload | loan_tape | (paid feed) |
                 +---------------------------+-----------------------------------+
                                             | (pipelines/ ingest, validate)
                                             v
   data/raw/  (Parquet, immutable, partitioned by source/date)
                                             |
                                             v  (pipelines/ transform)
   data/curated/ (prices, returns, holdings, loans)  <---->  riskcore.duckdb (views)
                                             |                      ^
                                             v                      | stage2+: Postgres
   +-------------------------- models/ (pure functions) ------------------------+
   | market: returns, vol, beta, VaR/ES (hist/param/MC), risk contrib          |
   | stress: scenarios, shocks              credit (v2): PD, LGD, EAD, ECL     |
   | validation: VaR backtest (Kupiec/Christoffersen/traffic light), PD calib  |
   +------------------------------------+---------------------------------------+
                                        | (pipelines/ run -> run_id)
                                        v
   data/results/run_id=.../*.parquet  + runs table (inputs hash, git sha, time)
                 |                          |                         |
                 v                          v                         v
          ui/ Streamlit              api/ FastAPI (stage2+)     reports/ Evidence.dev
      (st.cache_data, st.login)       -> SDK / other UIs         (monthly ECL pack)

   Orchestration: cron/GH Actions (S1) -> Prefect (S2) -> Dagster (S3)
   Caching: st.cache_data (UI) | diskcache (fetch, MC) | results store (canonical)
```

---

## 7. Proposed folder layout

```
Riskcore/
├── pyproject.toml              # replace requirements.txt; extras: [ui], [api], [credit], [dev]
├── README.md
├── app.py                      # thin shim -> riskcore.ui.app (keeps `streamlit run app.py`)
├── riskcore/
│   ├── __init__.py
│   ├── config.py               # paths, settings (pydantic-settings or env)
│   ├── providers/              # OpenBB-style data plugins
│   │   ├── base.py             # Protocol: get_prices(tickers, start, end) -> DataFrame
│   │   ├── yfinance.py         # (from data.py)
│   │   ├── synthetic.py        # (from data.py / sample.py)
│   │   └── loan_tape.py        # v2: CSV/XLSX loan-book loader + schema
│   ├── store/
│   │   ├── parquet.py          # write/read raw, curated, results (run_id partitions)
│   │   ├── duck.py             # DuckDB connection + views
│   │   └── runs.py             # run metadata (inputs hash, git sha) -> DuckDB / Postgres
│   ├── models/
│   │   ├── market/
│   │   │   ├── returns.py
│   │   │   ├── var.py          # hist / parametric / MC VaR + ES  (from metrics.py)
│   │   │   ├── performance.py  # sharpe, beta, drawdown
│   │   │   └── attribution.py  # risk contributions
│   │   ├── stress/
│   │   │   └── scenarios.py    # (from stress.py) + scenario library YAML
│   │   ├── credit/             # v2 NBFC
│   │   │   ├── staging.py      # SICR / DPD-based stage 1/2/3
│   │   │   ├── pd.py  lgd.py  ead.py
│   │   │   └── ecl.py          # 12m vs lifetime ECL, macro overlays
│   │   └── validation/
│   │       ├── var_backtest.py # Kupiec, Christoffersen, traffic light
│   │       └── pd_backtest.py  # AUC/Gini, calibration, PSI
│   ├── pipelines/
│   │   ├── daily_market.py     # ingest -> curate -> compute -> results
│   │   ├── monthly_ecl.py      # v2
│   │   └── flows.py            # stage 2: Prefect @flow wrappers (thin)
│   ├── api/                    # stage 2: FastAPI app (routers: runs, portfolio, ecl)
│   └── ui/
│       ├── app.py              # Streamlit entry (multipage)
│       ├── pages/              # 1_Portfolio.py, 2_Stress.py, 3_Backtest.py, 4_LoanBook.py
│       └── components/         # charts.py (plotly), tables.py
├── data/                       # gitignored: raw/, curated/, results/, riskcore.duckdb
├── reports/                    # Evidence.dev project (stage 2)
├── tests/
│   ├── unit/                   # per-module golden tests
│   ├── property/               # Hypothesis invariants
│   └── validation/             # backtest on fixed synthetic series
├── docker/Dockerfile
└── .github/workflows/{ci.yml,nightly.yml}
```

Design rules:
1. `models/` never does I/O. It takes DataFrames and arrays and returns DataFrames and dataclasses.
2. `ui/` never calls providers directly. It reads results or calls `pipelines` functions.
3. Every computed number carries a `run_id`.

---

## 8. Key risks and caveats found

1. **ArcticDB is not free for commercial or production use** (BSL 1.1) ([P]). Do not adopt it for a product.
2. **Hugging Face Docker/Streamlit Spaces now need a paid plan** per current hub-docs ([P]). Many 2025 to 2026 blogs still say "free".
3. **Fly.io has no free tier for new orgs since Oct 2024** ([S]).
4. **DuckDB is single-writer across processes** ([P]). A Streamlit app and a pipeline writing at the same time will conflict, so write to Parquet and have the DB read it, or move to Postgres at stage 2.
5. **GitHub Actions cron is silently disabled after 60 days of inactivity on public repos** ([S]).
6. **Streamlit Community Cloud is capped at 2.7 GB RAM and sleeps after 12 h idle** ([P]).
7. **Redis ≥ 8 is RSAL/SSPL/AGPL** ([P]). Choose deliberately.

---

## 9. Bibliography

**Primary, opened in this session [P]**
- Streamlit Community Cloud limits (docs source): https://raw.githubusercontent.com/streamlit/docs/main/content/deploy/community-cloud/manage-your-app/_index.md (states "as of February 2024")
- Streamlit caching docs: https://raw.githubusercontent.com/streamlit/docs/main/content/develop/concepts/architecture/caching.md
- Streamlit authentication docs: https://raw.githubusercontent.com/streamlit/docs/main/content/develop/concepts/connections/authentication.md
- Streamlit repo: https://github.com/streamlit/streamlit
- Hugging Face Spaces overview (hub-docs): https://raw.githubusercontent.com/huggingface/hub-docs/main/docs/hub/spaces-overview.md
- DuckDB repo: https://github.com/duckdb/duckdb
- DuckDB Python client docs: https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/clients/python/overview.md
- DuckDB concurrency docs: https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/connect/concurrency.md
- ArcticDB repo: https://github.com/man-group/ArcticDB and README: https://raw.githubusercontent.com/man-group/ArcticDB/master/README.md
- Arctic (legacy): https://github.com/man-group/arctic
- TimescaleDB: https://github.com/timescale/timescaledb
- QuestDB: https://github.com/questdb/questdb
- Polars: https://github.com/pola-rs/polars
- Prefect: https://github.com/PrefectHQ/prefect
- Dagster: https://github.com/dagster-io/dagster
- diskcache: https://github.com/grantjenks/python-diskcache
- Redis: https://github.com/redis/redis
- numba: https://github.com/numba/numba
- JAX: https://github.com/jax-ml/jax
- Dask: https://github.com/dask/dask
- Ray: https://github.com/ray-project/ray
- Hypothesis: https://github.com/HypothesisWorks/hypothesis
- Dash: https://github.com/plotly/dash
- Panel: https://github.com/holoviz/panel
- Shiny for Python: https://github.com/posit-dev/py-shiny
- NiceGUI: https://github.com/zauberzeug/nicegui
- Evidence: https://github.com/evidence-dev/evidence
- OpenBB: https://github.com/OpenBB-finance/OpenBB and https://github.com/OpenBB-finance/OpenBB/tree/develop/openbb_platform
- zipline (Quantopian): https://github.com/quantopian/zipline
- zipline-reloaded: https://github.com/stefan-jansen/zipline-reloaded
- Example 2026 risk-engine repos: https://github.com/marksguo/frtb-ima-risk-monitor, https://github.com/chenxi-bot21/market-risk-engine, https://github.com/ShrishDhuria/market-risk-engine

**Search-result only [S]: links seen in WebSearch results, pages not opened (proxy blocked or budget exhausted)**
- TechRepublic on Athena (c. 2019 ⚠): https://www.techrepublic.com/article/jpmorgans-athena-has-35-million-lines-of-python-code-and-wont-be-updated-to-python-3-in-time/
- eFinancialCareers 2021 ⚠: https://www.efinancialcareers.com/news/2021/02/jpmorgan-still-has-its-python-2-issue
- Python Bytes #152 (c. 2019 ⚠): https://pythonbytes.fm/episodes/show/152/you-have-35-million-lines-of-python-2-now-what
- eFinancialCareers 2017 SecDB/Quartz/Athena ⚠: https://www.efinancialcareers.com/news/2017/03/secdb-quartz-athena-analytics
- HN "An oral history of Bank Python" (2021 ⚠): https://news.ycombinator.com/item?id=29104047
- BlackRock Engineering: https://blackrock-eng.medium.com/ ; Aladdin SDK: https://engineering.blackrock.com/open-sourcing-the-aladdinsdk-empower-python-developers-with-a-quantitative-edge-7f63376061e6 ; Messaging: https://medium.com/blackrock-engineering/the-blackrock-messaging-system-aeae461e4211
- Man Group / Bloomberg ArcticDB press (2023-02-27 ⚠): https://www.man.com/news-centre/man-group-brings-powerful-dataframe-database-product-arcticdb-to-market-with-bloomberg
- PyData Chicago 2016 ⚠: https://pydata.org/chicago2016/schedule/presentation/12/
- Orchestrator comparisons: https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow , https://dzone.com/articles/airflow-vs-dagster-vs-prefect-which-scheduler-fits , https://www.getorchestra.io/blog/dagster-vs-prefect-vs-airflow-complete-data-orchestration-comparison-2026
- GH Actions 60-day rule: https://zenn.dev/hellorusk/articles/fc6d4696f5b269?locale=en , https://dev.to/procwire/why-your-scheduled-github-actions-workflow-runs-late-or-stops-running-entirely-173h , https://github.com/efrecon/gh-action-keepalive
- Frontend comparisons: https://docs.kanaries.net/topics/Streamlit/streamlit-vs-dash , https://ploomber.io/blog/survey-python-frameworks/ , https://deepnote.com/compare/alternatives/streamlit , https://medium.com/@marcskovmadsen/i-prefer-to-use-panel-for-my-data-apps-here-is-why-1ff5d2b98e8f
- Render: https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026 , https://justinmckelvey.com/blog/is-render-free
- Fly.io: https://www.withorb.com/blog/flyio-pricing , https://expresstech.io/7-fly-io-alternatives-in-2026-real-pricing-after-the-free-tier-died/
- Railway: https://www.saaspricepulse.com/tools/railway , https://makerkit.dev/pricing-calculator/railway
- HF pricing blog (older 48 h sleep claim): https://www.eesel.ai/blog/hugging-face-pricing

**Blocked or unverified**
- BIS 1996 backtesting framework (traffic light): https://www.bis.org/publ/bcbsc223.pdf (blocked) ⚠
- Cal Paterson, "An oral history of Bank Python": calpaterson.com (blocked)
- Observable Framework: not fetched
- Official docs at docs.streamlit.io, duckdb.org, arcticdb.io, huggingface.co, render.com, fly.io, docs.railway.com and docs.github.com were blocked; GitHub-hosted sources were used instead where available.
