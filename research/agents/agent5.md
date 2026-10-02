# Agent 5 — Academic Research Literature Map for Riskcore

Scope: the academic and regulatory basis for Riskcore v1 (investment portfolio risk) and v2 (NBFC loan-book risk: PD/LGD/EAD, IFRS 9 / Ind AS 109 ECL, concentration, stress).

## Method and verification notes

- **Tools:** WebSearch was used to check each item's title, authors, year and link, usually against the publisher, SSRN, RePEc/IDEAS, BIS or IMF page. Partway through, the shared session hit its **200-search budget**. WebFetch was **blocked by the egress proxy** for arxiv.org, bis.org, rbi.org.in, crossref, semanticscholar and elsevier. So the IFRS 9 / ECL section (topic 7) and some recent ML items could not be checked online.
- **Verified column:**
  - `Yes` — a search result confirmed title, authors, year and the link (or DOI).
  - `Partial` — the citation was confirmed, but the DOI or link shown comes from the citation record or from memory and was not opened.
  - `Unverified` — written from domain knowledge and not checked. Re-check these before citing.
- **Citation-chasing:** I followed citations up to 2 levels for VaR/ES backtesting, Black-Litterman, granularity adjustment and survival/LGD. Examples: Kupiec → Christoffersen → Lopez → Acerbi-Szekely → Du-Escanciano → Fissler-Ziegel / Nolde-Ziegel; Gordy 2003 → Martin-Wilde → Gordy 2004 → Gordy-Lütkebohmert → Pykhtin → Düllmann-Masschelein → Cespedes.

---

## 1. VaR / CVaR / Expected Shortfall / Backtesting

| # | Title | Authors | Year | Summary | Application to Riskcore | Link | Verified |
|---|---|---|---|---|---|---|---|
| 1 | RiskMetrics — Technical Document (4th ed.) | J.P. Morgan / Reuters (Longerstaey et al.) | 1996 | Industry standard for parametric (delta-normal) VaR, with EWMA volatility (λ=0.94 daily) and cash-flow mapping. | Default parametric VaR engine and EWMA covariance in v1; the λ values are standard defaults. | https://www.msci.com/documents/10199/5915b101-4206-4ba0-aee2-3449d5c7e95a | Yes |
| 2 | Return to RiskMetrics: The Evolution of a Standard | J. Mina, J.Y. Xiao | 2001 | Updates RiskMetrics: historical simulation, Monte Carlo, full revaluation, and how to choose between them. | Blueprint for supporting HS / MC / parametric behind one API. | https://www.dofin.ase.ro/acodirlasu/lect/riskmgdofin/rrmfinal.pdf | Yes |
| 3 | Coherent Measures of Risk | P. Artzner, F. Delbaen, J.-M. Eber, D. Heath | 1999 | Sets out four axioms for a "coherent" risk measure: monotonicity, subadditivity, positive homogeneity and translation invariance. VaR is not subadditive. | Theoretical reason to make ES/CVaR the main tail metric; property tests for the risk-measure module. | https://doi.org/10.1111/1467-9965.00068 | Yes |
| 4 | Optimization of Conditional Value-at-Risk | R.T. Rockafellar, S. Uryasev | 2000 | Shows CVaR minimisation can be written as a linear program over scenarios, with VaR obtained as a by-product. J. Risk 2(3):21–41. | Use for the CVaR optimiser (cvxpy LP) and for computing ES from scenarios. | https://www.semanticscholar.org/paper/58444c142b6ea5c71a435cac7a0b4c66d6c68869 | Yes |
| 5 | Conditional Value-at-Risk for General Loss Distributions | R.T. Rockafellar, S. Uryasev | 2002 | Extends CVaR to discrete or non-smooth distributions and defines CVaR+/CVaR−. JBF 26(7):1443–1471. | Correct ES for discrete historical scenarios, including how to handle ties at the quantile. | https://doi.org/10.1016/S0378-4266(02)00271-6 | Yes |
| 6 | On the Coherence of Expected Shortfall | C. Acerbi, D. Tasche | 2002 | Compares definitions of ES/TCE/WCE and gives the version that is always coherent. JBF 26(7):1487–1503. | The ES estimator formula to implement for historical-simulation P&L vectors. | https://doi.org/10.1016/S0378-4266(02)00283-2 | Yes |
| 7 | Techniques for Verifying the Accuracy of Risk Measurement Models | P. Kupiec | 1995 | Proportion-of-failures (POF) likelihood-ratio test for VaR exceptions; shows the test has low power in small samples. J. Derivatives 3(2):73–84. | Unconditional-coverage backtest in the backtesting module. | https://doi.org/10.3905/jod.1995.407942 (SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7065) | Yes |
| 8 | Evaluating Interval Forecasts | P. Christoffersen | 1998 | Independence and conditional-coverage LR tests, using a Markov chain on the exception sequence. IER 39:841–862. | Tests whether VaR exceptions cluster; pairs with Kupiec in the backtest report. | https://doi.org/10.2307/2527341 | Yes |
| 9 | Regulatory Evaluation of Value-at-Risk Models | J.A. Lopez | 1999 | Proposes loss-function-based evaluation of VaR models alongside hypothesis tests (FRBSF WP 99-06). | Adds a loss-function score so VaR models can be ranked. | https://www.frbsf.org/wp-content/uploads/wpjl99-06.pdf | Yes |
| 10 | VaR without correlations for portfolios of derivative securities (Filtered Historical Simulation) | G. Barone-Adesi, K. Giannopoulos, L. Vosper | 1999 | Filters historical returns with GARCH and rescales them by current volatility; correlations are handled implicitly. J. Futures Markets 19(5):583–602. | FHS engine (`arch` library + bootstrap); reacts faster than plain HS in volatile markets. | https://onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1096-9934(199908)19:5%3C583::AID-FUT5%3E3.0.CO;2-S | Yes |
| 11 | The Hidden Dangers of Historical Simulation | M. Pritsker | 2001/2006 | Shows plain and age-weighted HS react slowly to changes in volatility and understate risk. | Reason to offer FHS/EWMA-HS and to document HS limitations. | https://www.ssrn.com/abstract=278438 | Yes |
| 12 | Estimation of tail-related risk measures for heteroscedastic financial time series: an extreme value approach | A.J. McNeil, R. Frey | 2000 | Two-step GARCH + GPD (peaks-over-threshold) method for conditional VaR/ES; backtests well. JEF 7(3–4):271–300. | EVT tail option for ES at 99%+; India-relevant fat tails. | https://doi.org/10.1016/S0927-5398(00)00012-8 | Yes |
| 13 | Estimation of tail-related risk measures in the Indian stock market: An extreme value approach | M. Karmakar | 2013 | Applies conditional EVT to Indian indices and finds it beats normal/t GARCH. Rev. Financial Econ. | India-specific evidence that an EVT/FHS default is justified for NSE portfolios. | https://onlinelibrary.wiley.com/doi/abs/10.1016/j.rfe.2013.05.001 | Yes |
| 14 | Backtesting Expected Shortfall | C. Acerbi, B. Székely | 2014 | Three model-free ES backtests (Z1, Z2, Z3) whose significance is set by simulation. Risk, Nov 2014. | ES backtest (Z2 is simplest) once ES is the headline metric. | https://www.risk.net (Risk magazine, Nov 2014; no stable URL found) | Partial |
| 15 | Backtesting Expected Shortfall: Accounting for Tail Risk | Z. Du, J.C. Escanciano | 2017 | Cumulative-violation ES backtests with asymptotic theory. Management Science 63(4). | Alternative ES backtest with analytic p-values (no simulation needed). | https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2015.2342 | Yes |
| 16 | Making and Evaluating Point Forecasts | T. Gneiting | 2011 | Introduces elicitability and shows ES alone is not elicitable. JASA 106:746–762. | Explains why ES backtesting is harder than VaR; guides how forecasts are scored. | https://doi.org/10.1198/jasa.2011.r10138 | Partial (DOI from memory) |
| 17 | Expected Shortfall is jointly elicitable with Value at Risk — Implications for backtesting | T. Fissler, J. Ziegel, T. Gneiting | 2015/2016 | VaR and ES are jointly elicitable, which allows comparative backtests using a joint scoring function. | Scoring function for comparing VaR/ES models (model selection dashboard). | https://arxiv.org/abs/1507.00244 | Yes |
| 18 | Elicitability and backtesting: Perspectives for banking regulation | N. Nolde, J. Ziegel | 2017 | Frames traditional vs comparative backtests for regulators; Annals of Applied Statistics. | Design of the backtest "traffic light" plus comparative tests. | https://arxiv.org/abs/1608.05498 | Yes |
| 19 | Minimum capital requirements for market risk (FRTB, d457) | Basel Committee on Banking Supervision | 2019 | Final FRTB standard: 97.5% ES with liquidity horizons, stressed calibration, P&L attribution and backtesting. | Regulatory reference for ES at 97.5%, stressed-period ES and liquidity-horizon scaling. | https://www.bis.org/bcbs/publ/d457.pdf | Yes |

## 2. Factor Models and Risk Attribution

| # | Title | Authors | Year | Summary | Application | Link | Verified |
|---|---|---|---|---|---|---|---|
| 20 | Common Risk Factors in the Returns on Stocks and Bonds | E.F. Fama, K.R. French | 1993 | Three-factor model (MKT, SMB, HML) plus bond term/default factors. JFE 33:3–56. | Base factor set for returns-based factor risk and attribution. | https://doi.org/10.1016/0304-405X(93)90023-5 | Yes |
| 21 | A Five-Factor Asset Pricing Model | E.F. Fama, K.R. French | 2015 | Adds profitability (RMW) and investment (CMA) factors; HML becomes redundant. JFE 116(1):1–22. | Extended factor set for style attribution. | https://doi.org/10.1016/j.jfineco.2014.10.010 | Yes |
| 22 | On Persistence in Mutual Fund Performance | M.M. Carhart | 1997 | Adds a momentum (UMD) factor; fund persistence is explained by factors and costs. JF 52(1):57–82. | Four-factor model; momentum exposure of portfolios. | https://doi.org/10.1111/j.1540-6261.1997.tb03808.x | Yes |
| 23 | Extra-Market Components of Covariance in Security Returns | B. Rosenberg | 1974 | Founding paper of fundamental multi-factor risk models: factor loadings come from firm characteristics. JFQA 9(2):263–274. | Conceptual basis for a Barra-style cross-sectional (fundamental) factor model. | https://econpapers.repec.org/RePEc:cup:jfinqa:v:9:y:1974:i:02:p:263-274_01 | Yes |
| 24 | The Barra US Equity Model (USE4) — Methodology Notes | J. Menchero, D.J. Orr, J. Wang (MSCI) | 2011 | Country + industry + style factors; WLS cross-sectional regression; eigenfactor and volatility-regime adjustments; Bayesian shrinkage of specific risk. | Most detailed public recipe for building a Barra-like Indian equity model (factor covariance, specific risk, bias tests). | https://www.top1000funds.com/wp-content/uploads/2011/09/USE4_Methodology_Notes_August_2011.pdf | Yes |
| 25 | Four Factor Model in Indian Equities Market (IIMA WP 2013-09-05) | S.K. Agarwalla, J. Jacob, J.R. Varma | 2013 | Builds Fama-French + momentum factor returns for India from CMIE Prowess (1993 onwards); data library kept up to date at IIMA. | **Free Indian factor-return data** for v1 attribution and factor VaR. | https://econpapers.repec.org/RePEc:iim:iimawp:12130 ; data: https://faculty.iima.ac.in/iffm/Indian-Fama-French-Momentum/ | Yes |
| 26 | Size, Value, and Momentum in Indian Equities | S.K. Agarwalla, J. Jacob, J.R. Varma | 2017 | Peer-reviewed version (Vikalpa) documenting Indian factor premia. | Citable source for factor behaviour in Indian markets. | https://journals.sagepub.com/doi/full/10.1177/0256090917733848 | Yes |
| 27 | Betting Against Beta in the Indian Market | S.K. Agarwalla, J. Jacob, J.R. Varma, E. Vasudevan | 2014 | Builds a BAB (low-beta) factor for India. | Optional low-vol/BAB factor for the Indian style model. | https://faculty.iima.ac.in/iffm/Indian-Equities/2014-07-01-Betting-Against-Beta-SSRN-id2464097.pdf | Yes (co-author list partial) |

## 3. Portfolio Construction and Covariance Estimation

| # | Title | Authors | Year | Summary | Application | Link | Verified |
|---|---|---|---|---|---|---|---|
| 28 | Portfolio Selection | H. Markowitz | 1952 | Mean-variance efficient frontier. JF 7(1):77–91. | Base optimiser; efficient-frontier plot. | https://doi.org/10.1111/j.1540-6261.1952.tb01525.x | Yes |
| 29 | The Markowitz Optimization Enigma: Is "Optimized" Optimal? | R.O. Michaud | 1989 | MV optimisation tends to maximise estimation error, producing unstable and concentrated weights. FAJ 45(1):31–42. | Reason to add shrinkage, constraints and resampling options. | (FAJ 45(1); no direct link verified) | Partial |
| 30 | Global Portfolio Optimization | F. Black, R. Litterman | 1992 | Bayesian mix of market-implied equilibrium returns with investor views. FAJ 48(5):28–43. | Black-Litterman module that uses market-cap equilibrium as the prior. | https://doi.org/10.2469/faj.v48.n5.28 | Yes |
| 31 | The Intuition Behind Black-Litterman Model Portfolios | G. He, R. Litterman | 1999 (SSRN 2002) | Shows the BL portfolio equals scaled equilibrium weights plus weighted view portfolios; gives practical choices for τ and Ω. | Implementation reference and test cases for BL. | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=334304 | Yes |
| 32 | A Step-by-Step Guide to the Black-Litterman Model: Incorporating User-Specified Confidence Levels | T.M. Idzorek | 2004/2005 | Converts a 0–100% confidence per view into Ω. | User-friendly "confidence %" inputs in the UI. | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3479867 | Yes |
| 33 | The Properties of Equally Weighted Risk Contribution Portfolios | S. Maillard, T. Roncalli, J. Teïletche | 2010 | The ERC (risk-parity) portfolio exists, is unique, and lies between minimum-variance and 1/N. JPM 36(4):60–70. | Risk-parity optimiser plus risk-contribution decomposition (Euler allocation). | https://www.pm-research.com/content/iijpormgmt/36/4/60 | Yes |
| 34 | Building Diversified Portfolios that Outperform Out-of-Sample (HRP) | M. López de Prado | 2016 | Hierarchical Risk Parity: tree clustering, quasi-diagonalisation, recursive bisection; no covariance inversion needed. JPM 42(4):59–69. | HRP allocator that is robust with ill-conditioned covariance (small Indian universes). | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678 | Yes |
| 35 | A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices | O. Ledoit, M. Wolf | 2004 | Optimal linear shrinkage toward a scaled identity. JMVA 88:365–411. | Default covariance estimator (sklearn `LedoitWolf`). | https://doi.org/10.1016/S0047-259X(03)00096-4 | Partial (DOI from memory) |
| 36 | Honey, I Shrunk the Sample Covariance Matrix | O. Ledoit, M. Wolf | 2004 | Shrinkage toward a constant-correlation target for portfolio selection. JPM 30(4):110–119. | Alternative shrinkage target for equity portfolios. | https://www.researchgate.net/publication/23695464_Honey_I_Shrunk_the_Sample_Covariance_Matrix | Yes |
| 37 | Analytical Nonlinear Shrinkage of Large-Dimensional Covariance Matrices | O. Ledoit, M. Wolf | 2020 | Closed-form nonlinear eigenvalue shrinkage. Annals of Statistics 48(5):3043–3065. | Advanced covariance option for large universes. | https://doi.org/10.1214/19-AOS1921 | Yes |
| 38 | Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy? | V. DeMiguel, L. Garlappi, R. Uppal | 2009 | 14 optimisers fail to consistently beat 1/N out of sample. RFS 22(5):1915–1953. | 1/N benchmark in every optimiser backtest; argues for humility in the defaults. | https://doi.org/10.1093/rfs/hhm075 | Yes |

## 4. Stress Testing and Scenario Analysis

| # | Title | Authors | Year | Summary | Application | Link | Verified |
|---|---|---|---|---|---|---|---|
| 39 | Stress Testing in a Value at Risk Framework | P.H. Kupiec | 1998 | Conditional stress: shock some factors and set the rest to their conditional expectation given the covariance. J. Derivatives 6(1):7–24. | Core of "shock Nifty −20%, infer the other factors" scenario propagation. | https://jod.pm-research.com/content/6/1/7 | Yes |
| 40 | How to Find Plausible, Severe and Useful Stress Scenarios | T. Breuer, M. Jandačka, K. Rheinberger, M. Summer | 2009 | Worst-case search over a Mahalanobis plausibility ellipsoid. IJCB 5(3):205–224. | "Worst plausible scenario" feature (a quadratic optimisation over factor shocks). | https://ideas.repec.org/a/ijc/ijcjou/y2009q3a7.html | Yes |
| 41 | Coherent Stress Testing: A Bayesian Approach to the Analysis of Financial Stress | R. Rebonato | 2010 | Bayesian nets combine expert-elicited stress events with causal structure (Wiley book). | Possible narrative-scenario builder with probabilities (v2+). | https://onlinelibrary.wiley.com/doi/book/10.1002/9781118374719 | Yes |
| 42 | A Bayesian Approach to Stress Testing and Scenario Analysis | R. Rebonato, A. Denev | 2010 | Journal of Investment Management article version of the BN approach. | Same as above, as an article. | https://www.researchgate.net/publication/228232370_A_Bayesian_Approach_to_Stress_Testing_and_Scenario_Analysis | Yes |
| 43 | Stress Scenario Selection by Empirical Likelihood | P. Glasserman, C. Kang, W. Kang | 2015 | Reverse stress test: the most likely factor scenario given loss > threshold, estimated nonparametrically. Quant. Finance 15(1):25–41. | Reverse stress test for v1 portfolios using HS scenarios. | https://doi.org/10.2139/ssrn.2101465 | Yes |
| 44 | A Macroeconomic Reverse Stress Test | P. Grundke, K. Pliszka | 2018 | Finds macro scenarios that push a bank past its default boundary (credit + IRR). RQFA 50:1093–1130; Bundesbank DP 30/2015. | Reverse stress test for the NBFC book: which GDP/rate path breaches CRAR. | https://www.bundesbank.de/en/publications/research/discussion-papers/a-macroeconomic-reverse-stress-test-703956 | Yes |
| 45 | Stress Testing Principles (d450) | Basel Committee on Banking Supervision | 2018 | Nine high-level principles: governance, scenario design, data, model validation. | Governance checklist for the stress-testing module and documentation. | https://www.bis.org/bcbs/publ/d450.htm | Yes |
| 46 | Macrofinancial Stress Testing — Principles and Practices | IMF (H. Oura, L. Schumacher et al.) | 2012 | Seven best-practice principles drawn from FSAP stress tests. | Design principles for macro → PD satellite models in v2. | https://www.imf.org/external/np/pp/eng/2012/082212.pdf | Yes |
| 47 | Next Generation Balance Sheet Stress Testing (IMF WP/11/83) | C. Schmieder, C. Puhr, M. Hasan | 2011 | Balance-sheet-based solvency stress-test framework (PD/LGD macro satellites, RWA, earnings). | Template for the NBFC solvency stress test (capital, provisions, P&L). | https://www.imf.org (WP/11/83; exact URL not opened) | Partial |
| 48 | How to Capture Macro-Financial Spillover Effects in Stress Tests? (IMF WP/14/103) | IMF staff (Schmieder et al.) | 2014 | Feedback and spillover effects in stress tests. | Second-round effects in v2 stress (optional). | https://www.imf.org/external/pubs/ft/wp/2014/wp14103.pdf | Partial (authors not confirmed) |

## 5. Credit Risk: Structural, Portfolio, PD/LGD/EAD Models

| # | Title | Authors | Year | Summary | Application | Link | Verified |
|---|---|---|---|---|---|---|---|
| 49 | On the Pricing of Corporate Debt: The Risk Structure of Interest Rates | R.C. Merton | 1974 | Equity as a call option on firm assets; default when assets < debt. JF 29(2):449–470. | Basis of the latent-variable (asset value) default model behind Vasicek/IRB; optional market-implied PD for listed borrowers. | https://doi.org/10.1111/j.1540-6261.1974.tb03058.x | Yes |
| 50 | The Distribution of Loan Portfolio Value | O. Vasicek | 2002 | Closed-form large-portfolio loss distribution under a one-factor Gaussian model. Risk 15(12):160–162. | **Core v2 portfolio credit VaR / economic capital engine** (one formula). | https://www.bankofgreece.gr/MediaAttachments/Vasicek.pdf | Yes |
| 51 | A Risk-Factor Model Foundation for Ratings-Based Bank Capital Rules | M.B. Gordy | 2003 | ASRF model: exposure-level capital is portfolio-invariant only under one systematic factor and infinite granularity. JFI 12(3):199–232. | Justifies the IRB formula in v2 and explains why a granularity adjustment is needed for NBFC books. | https://doi.org/10.1016/S1042-9573(03)00040-8 | Yes |
| 52 | An Explanatory Note on the Basel II IRB Risk Weight Functions | BCBS | 2005 | Derives the IRB formula, asset correlations, maturity adjustment and the 99.9% confidence level. | Exact formulas and correlation functions to implement the IRB-style capital module. | https://www.bis.org/bcbs/irbriskweight.pdf | Yes |
| 53 | CreditMetrics — Technical Document | G.M. Gupton, C.C. Finger, M. Bhatia (J.P. Morgan) | 1997 | Rating-migration mark-to-market credit VaR using a Merton-style asset-correlation simulation. | Monte Carlo credit VaR with migration (v2 advanced). | https://www.msci.com/documents/10199/93396227-d449-4229-9143-24a94dab122f | Yes |
| 54 | CreditRisk+: A Credit Risk Management Framework | Credit Suisse First Boston | 1997 | Actuarial default-mode model: Poisson defaults with gamma sector factors; analytic loss distribution via a recursion. | Fast analytic loss distribution for granular retail/MSME NBFC books (no Monte Carlo). | (original CSFB URL defunct; described in https://www.wias-berlin.de/people/schoenma/hrs_JOR.pdf) | Partial |
| 55 | A Comparative Anatomy of Credit Risk Models | M.B. Gordy | 2000 (FEDS 1998-47) | Maps CreditMetrics and CreditRisk+ onto a common framework; differences come down mainly to distributional assumptions. JBF 24. | Guide to choosing between Vasicek, CreditMetrics and CR+ engines and keeping them consistent. | https://www.federalreserve.gov/pubs/feds/1998/199847/199847pap.pdf | Yes |
| 56 | Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy | E.I. Altman | 1968 | Z-score built from five ratios using MDA. JF 23(4):589–609. | Baseline corporate/MSME PD scorecard and a benchmark model. | https://doi.org/10.1111/j.1540-6261.1968.tb00843.x | Yes |
| 57 | Survival Analysis Methods for Personal Loan Data | M. Stepanova, L. Thomas | 2002 | Cox PH models for time to default and early repayment. Operations Research 50(2):277–289. | Lifetime PD term structure for IFRS 9 Stage 2 from survival curves. | https://doi.org/10.1287/opre.50.2.277.426 | Yes |
| 58 | Credit Scoring with Macroeconomic Variables Using Survival Analysis | T. Bellotti, J. Crook | 2009 | Discrete-time survival with time-varying macro covariates (interest rate, unemployment). JORS 60(12):1699–1707. | **Forward-looking PD**: put macro scenarios into lifetime PD for ECL and stress. | https://www.researchgate.net/publication/233706892 | Yes |
| 59 | Neural Network Survival Analysis for Personal Loan Data | B. Baesens, T. Van Gestel, M. Stepanova, D. Van den Poel, J. Vanthienen | 2005 | NN-based survival models vs Cox PH. JORS 56(9). | ML survival option for the lifetime PD module. | https://ideas.repec.org/a/pal/jorsoc/v56y2005i9d10.1057_palgrave.jors.2601990.html | Yes (authors partial) |
| 60 | Time to Default in Credit Scoring Using Survival Analysis: A Benchmark Study | L. Dirick, G. Claeskens, B. Baesens | 2017 | Benchmarks survival models (Cox, AFT, mixture cure) on 10 datasets. JORS 68. | Model selection for lifetime PD; mixture cure suits loans that never default. | https://link.springer.com/article/10.1057/s41274-016-0128-9 | Yes |
| 61 | Benchmarking State-of-the-Art Classification Algorithms for Credit Scoring: An Update of Research | S. Lessmann, B. Baesens, H.-V. Seow, L.C. Thomas | 2015 | 41 classifiers on 8 datasets; heterogeneous ensembles and RF lead; LR is still a strong baseline. EJOR 247:124–136. | Defines the PD model zoo and evaluation metrics (AUC, Brier, H-measure). | https://doi.org/10.1016/j.ejor.2015.05.030 | Yes |
| 62 | (Benchmark of) state-of-the-art machine learning algorithms for credit scoring (arXiv 2205.10535) | (not confirmed) | 2022 | Recent ML benchmark (GBMs/XGBoost/LightGBM vs LR). Title only partly seen in search results. | Updates Lessmann with gradient boosting results. | https://arxiv.org/abs/2205.10535 | Unverified (title truncated) |
| 63 | XGBoost: A Scalable Tree Boosting System | T. Chen, C. Guestrin | 2016 | Regularised gradient boosting; strongest tabular PD learner in recent benchmarks. KDD 2016. | Challenger PD model; SHAP explanations for model risk. | https://arxiv.org/abs/1603.02754 | Unverified |
| 64 | A Unified Approach to Interpreting Model Predictions (SHAP) | S. Lundberg, S.-I. Lee | 2017 | Shapley-value explanations for any model. NeurIPS 2017. | Explainability needed for ML PD models (RBI model-risk expectations). | https://arxiv.org/abs/1705.07874 | Unverified |
| 65 | Benchmarking Regression Algorithms for Loss Given Default Modeling | G. Loterman, I. Brown, D. Martens, C. Mues, B. Baesens | 2012 | 24 LGD techniques on 6 bank datasets; R² of only 4–43%; non-linear models (SVM/NN) do better; two-stage models help. IJF 28(1):161–170. | LGD model options and realistic accuracy expectations. | https://doi.org/10.1016/j.ijforecast.2011.01.006 (abstract: http://www.defaultrisk.com/pa_recov_34.htm) | Partial (DOI from memory) |
| 66 | A Zero-Adjusted Gamma Model for Mortgage Loan Loss Given Default | E.N.C. Tong, C. Mues, L. Thomas | 2013 | Mixed discrete-continuous model with a point mass at zero loss. IJF 29(4):548–562. | LGD for secured NBFC products (LAP, home loans) with many zero-loss cures. | https://doi.org/10.1016/j.ijforecast.2013.03.003 | Yes |
| 67 | Exposure at Default Models With and Without the Credit Conversion Factor | E.N.C. Tong, C. Mues, I. Brown, L.C. Thomas | 2016 | Compares CCF, utilisation-change and direct EAD models (zero-adjusted gamma). EJOR. | EAD module for revolving and undrawn lines (credit lines, OD facilities). | https://www.sciencedirect.com/science/article/pii/S0377221716001004 | Yes |
| 68 | Exposure at Default Modeling with Default Intensities | J. Witzany | 2011 | Models EAD/CCF jointly with default timing. European Financial and Accounting Journal. | Alternative EAD approach where drawdown speeds up near default. | http://efaj.vse.cz/pdfs/efa/2011/04/03.pdf | Yes |
| 69 | Modeling Loss Given Default (FDIC CFR WP 2018-03) | P. Li et al. | 2018 | Survey and comparison of LGD models (fractional response, beta, mixtures). | LGD method survey for implementation choices. | https://www.fdic.gov/analysis/cfr/working-papers/2018/cfr-wp2018-03.pdf | Partial (co-authors not confirmed) |

## 6. Concentration Risk

| # | Title | Authors | Year | Summary | Application | Link | Verified |
|---|---|---|---|---|---|---|---|
| 70 | Studies on Credit Risk Concentration (BCBS WP 15) | BCBS Research Task Force | 2006 | Overview of name vs sector concentration, HHI, granularity adjustment and multi-factor approaches. | **Roadmap for the v2 concentration module.** | https://www.bis.org/publ/bcbs_wp15.pdf | Yes |
| 71 | Unsystematic Credit Risk | R. Martin, T. Wilde | 2002 | Rigorous derivation of the granularity adjustment via second-order VaR sensitivity. Risk 15(11):123–128. | Analytic GA formula. | https://www.researchgate.net/publication/284700625_Unsystematic_credit_risk | Yes |
| 72 | Granularity Adjustment in Portfolio Credit Risk Measurement | M.B. Gordy | 2004 | Survey and primer on GA (in Szegö, *Risk Measures for the 21st Century*, Wiley, 109–121). | Derivation reference. | (book chapter; no URL) | Partial |
| 73 | Granularity Adjustment for Regulatory Capital Assessment | M.B. Gordy, E. Lütkebohmert | 2013 | Simple, supervisor-friendly GA for the IRB ASRF model, with an upper-bound version for incomplete data. IJCB 9(3):33–71. | **Name-concentration add-on** to Vasicek capital for NBFC books with large single-borrower exposures. | https://www.researchgate.net/publication/275031591 | Yes |
| 74 | Multi-Factor Adjustment | M. Pykhtin | 2004 | Analytic adjustment of ASRF VaR/ES for multiple correlated sector factors. Risk, March 2004, 85–90. | Sector (industry/geography) concentration add-on. | (Risk magazine; no stable URL) | Partial |
| 75 | Sector Concentration in Loan Portfolios and Economic Capital (NBB WP 105) | K. Düllmann, N. Masschelein | 2006 | Measures the capital effect of sector concentration using German credit-register data. | Calibration evidence and HHI vs model-based comparison. | https://www.nbb.be/doc/ts/publications/wp/wp105en.pdf | Yes (authors from memory) |
| 76 | A Simple Multi-Factor "Factor Adjustment" for the Treatment of Diversification in Credit Capital Rules | J.C. Garcia Cespedes, J.A. de Juan Herrero, A. Kreinin, D. Rosen | 2006 | Diversification factor as a function of a capital-diversification index (HHI-like) and average sector correlation. | Cheap sector-diversification scalar for dashboards. | https://www.bis.org/bcbs/events/crcp05cespedes.pdf | Yes (authors from memory) |
| 77 | A Tractable Model to Measure Sector Concentration Risk in Credit Portfolios | K. Düllmann et al. | 2007 | Tractable model for sector concentration. JFSR. | Alternative to Pykhtin. | https://link.springer.com/article/10.1007/s10693-007-0014-3 | Partial |
| 78 | Measuring Concentration Risk — A Partial Portfolio Approach (IMF WP/16/158) | IMF staff | 2016 | Concentration-risk capital for partial portfolios (supervisory data). | Approach when only the largest exposures are known (common for NBFCs). | https://www.imf.org/external/pubs/ft/wp/2016/wp16158.pdf | Partial (authors not confirmed) |
| 79 | Understanding the Effect of Concentration Risk in the Banks' Credit Portfolio: Indian Cases | A. Bandyopadhyay (MPRA 24822) | 2010 | HHI and GA applied to Indian bank portfolios. | Indian calibration evidence. | https://mpra.ub.uni-muenchen.de/24822/ | Partial (author from memory) |

## 7. IFRS 9 / Ind AS 109 Expected Credit Loss

> Verification gap: the search budget ran out at this topic, and the relevant domains (bis.org, rbi.org.in, arxiv.org) were blocked for WebFetch. Items 82–90 are from domain knowledge. **Re-verify before citing.**

| # | Title | Authors | Year | Summary | Application | Link | Verified |
|---|---|---|---|---|---|---|---|
| 80 | Deriving the term-structure of loan write-off risk under IFRS 9 by using survival analysis: A benchmark study | (not confirmed; likely A. Botha et al.) | 2026 | Benchmarks survival models for write-off (LGD-related) term structures under IFRS 9. | Lifetime LGD/write-off curves in ECL. | https://arxiv.org/pdf/2603.11897 | Partial (title seen in results only) |
| 81 | The TruEnd-procedure: Treating trailing zero-valued balances in credit data | (not confirmed; likely A. Botha et al.) | 2024 | Data-preparation method for loan performance histories. | Data cleaning for NBFC loan-tape histories before PD/LGD estimation. | https://arxiv.org/abs/2404.17008 | Partial (title seen in results only) |
| 82 | IFRS 9 and CECL Credit Risk Modelling and Validation: A Practical Guide with Examples Worked in R and SAS | T. Bellini | 2019 | Practitioner book covering one-year and lifetime PD (GLM, survival, ML), LGD, EAD, staging, scenarios and validation. Academic Press. | **Primary implementation manual for v2 ECL.** | ISBN 978-0-12-814940-9 (Elsevier/Academic Press) | Unverified (WebFetch blocked) |
| 83 | Guidance on Credit Risk and Accounting for Expected Credit Losses (d350) | BCBS | 2015 | Eleven supervisory principles for ECL: governance, SICR assessment, use of forward-looking information, validation. | Governance and validation checklist for the ECL module. | https://www.bis.org/bcbs/publ/d350.htm | Unverified |
| 84 | Discussion Paper on Introduction of Expected Credit Loss Framework for Provisioning by Banks | Reserve Bank of India | Jan 2023 | Proposes ECL for Indian SCBs: 3-stage IFRS 9-style model, with a default backstop of 90 DPD and SICR at 30 DPD. | Indian regulatory alignment (NBFCs in Upper/Middle layers already apply Ind AS 109). | https://www.rbi.org.in (exact URL not opened) | Unverified |
| 85 | Draft Directions on Expected Credit Loss provisioning (banks / AIFIs) | Reserve Bank of India | 2025 | Draft rules following the 2023 discussion paper, including prudential floors per stage. | Floor checks against model ECL. | https://www.rbi.org.in | Unverified |
| 86 | The new era of expected credit loss provisioning | B.H. Cohen, G.A. Edwards Jr. | 2017 | BIS Quarterly Review (Mar 2017) overview of IFRS 9 vs CECL and the procyclicality debate. | Background explainer; procyclicality caveat for stress results. | https://www.bis.org/publ/qtrpdf/r_qt1703f.htm | Unverified |
| 87 | IFRS 9 Impairment: Lifetime PD Modelling with Markov Chains / rating-transition matrices (e.g. Jarrow, Lando & Turnbull 1997, RFS) | R. Jarrow, D. Lando, S. Turnbull | 1997 | Markov rating-transition model for the credit-spread term structure; transition matrices are a standard way to get lifetime PD. | Lifetime PD from DPD-bucket transition matrices (0, 1–30, 31–60, 61–90, 90+), the most practical approach for NBFCs. | https://doi.org/10.1093/rfs/10.2.481 | Unverified |
| 88 | The Cyclical Behaviour of Expected Credit Loss Provisioning / "IFRS 9 and procyclicality" | J. Abad, J. Suarez | 2017/2018 | Shows ECL provisions spike at downturn onset (cliff effects from Stage 1→2 transfers). | Explains ECL sensitivity under stress; supports stage-transfer sensitivity reports. | (CEMFI/ESRB working paper; URL unverified) | Unverified |
| 89 | Wilson, "Portfolio Credit Risk" (CreditPortfolioView) | T.C. Wilson | 1997 | Macro-driven default rates via a logit of macro index (Risk, Sept/Oct 1997). | Satellite model: macro → sector PD for forward-looking ECL and stress. | (Risk magazine; no URL) | Unverified |
| 90 | Forward-looking point-in-time PD: Z-factor / Vasicek credit-cycle index approach | (e.g. Belkin, Suchower & Forest 1998, "A one-parameter representation of credit risk and transition matrices", CreditMetrics Monitor) | 1998 | Pulls a single systematic "Z" credit-cycle index out of transition matrices and conditions PD on it. | Simplest forward-looking PD overlay: map macro scenarios → Z → PIT PD by stage. | (CreditMetrics Monitor Q3 1998; URL unverified) | Unverified |

---

## Top 5 Must-Reads

1. **Vasicek (2002), "The Distribution of Loan Portfolio Value"**, together with **Gordy (2003) ASRF** (#50, #51). Riskcore's v2 credit-portfolio engine is a single closed-form formula, and that same formula is the Basel IRB function (#52). Reading both gives the portfolio loss distribution, economic capital, stress (shifting the systematic factor) and the reason granularity adjustments are needed. This is the most useful reading per hour spent.
2. **Acerbi & Tasche (2002), "On the Coherence of Expected Shortfall"**, read with **Artzner et al. (1999)** (#6, #3). It sets the ES definition the v1 risk engine has to implement correctly for discrete historical scenarios, and gives the theory behind making ES the headline metric, which is what FRTB does (#19).
3. **Christoffersen (1998), "Evaluating Interval Forecasts"**, which builds on Kupiec (1995) (#8, #7). A risk platform is not credible without backtesting. These two LR tests are the standard for VaR model validation and fit in about 50 lines of Python.
4. **Gordy & Lütkebohmert (2013), "Granularity Adjustment for Regulatory Capital Assessment"** (#73), with BCBS WP15 (#70) as context. NBFC books are often concentrated in a few large borrowers or sectors. This paper gives a closed-form, data-light name-concentration add-on that sets Riskcore v2 apart from simple HHI dashboards.
5. **Bellotti & Crook (2009), "Credit Scoring with Macroeconomic Variables Using Survival Analysis"** (#58), extended by Stepanova & Thomas (2002) (#57). IFRS 9 / Ind AS 109 requires lifetime and forward-looking PD. A discrete-time survival model with macro covariates provides both the lifetime PD term structure and the macro-scenario link, and the same model can also run the credit stress test.

Runner-up for v1 portfolio construction: López de Prado (2016) HRP (#34) plus Ledoit-Wolf (2004) (#35). Robust allocation for small, ill-conditioned Indian universes.

---

## Bibliography (verified items marked ✓; partial ~; unverified ?)

- ✓ Acerbi, C., & Tasche, D. (2002). On the coherence of expected shortfall. *Journal of Banking & Finance*, 26(7), 1487–1503. https://doi.org/10.1016/S0378-4266(02)00283-2
- ~ Acerbi, C., & Székely, B. (2014). Backtesting expected shortfall. *Risk*, November.
- ✓ Agarwalla, S.K., Jacob, J., & Varma, J.R. (2013). Four factor model in Indian equities market. IIMA WP 2013-09-05. https://econpapers.repec.org/RePEc:iim:iimawp:12130
- ✓ Agarwalla, S.K., Jacob, J., & Varma, J.R. (2017). Size, value, and momentum in Indian equities. *Vikalpa*. https://doi.org/10.1177/0256090917733848
- ✓ Agarwalla, S.K., Jacob, J., Varma, J.R., & Vasudevan, E. (2014). Betting against beta in the Indian market. SSRN 2464097.
- ✓ Altman, E.I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance*, 23(4), 589–609. https://doi.org/10.1111/j.1540-6261.1968.tb00843.x
- ✓ Artzner, P., Delbaen, F., Eber, J.-M., & Heath, D. (1999). Coherent measures of risk. *Mathematical Finance*, 9(3), 203–228. https://doi.org/10.1111/1467-9965.00068
- ? Abad, J., & Suarez, J. (2017/2018). Assessing the cyclical implications of IFRS 9. Working paper.
- ✓ Baesens, B., et al. (2005). Neural network survival analysis for personal loan data. *JORS*, 56(9).
- ✓ Barone-Adesi, G., Giannopoulos, K., & Vosper, L. (1999). VaR without correlations for portfolios of derivative securities. *Journal of Futures Markets*, 19(5), 583–602.
- ✓ BCBS (2005). An explanatory note on the Basel II IRB risk weight functions. https://www.bis.org/bcbs/irbriskweight.pdf
- ✓ BCBS (2006). Studies on credit risk concentration. Working Paper 15. https://www.bis.org/publ/bcbs_wp15.pdf
- ? BCBS (2015). Guidance on credit risk and accounting for expected credit losses (d350).
- ✓ BCBS (2018). Stress testing principles (d450). https://www.bis.org/bcbs/publ/d450.htm
- ✓ BCBS (2019). Minimum capital requirements for market risk (d457). https://www.bis.org/bcbs/publ/d457.pdf
- ? Belkin, B., Suchower, S., & Forest, L. (1998). A one-parameter representation of credit risk and transition matrices. *CreditMetrics Monitor*.
- ? Bellini, T. (2019). *IFRS 9 and CECL Credit Risk Modelling and Validation*. Academic Press. ISBN 978-0-12-814940-9.
- ✓ Bellotti, T., & Crook, J. (2009). Credit scoring with macroeconomic variables using survival analysis. *JORS*, 60(12), 1699–1707.
- ✓ Black, F., & Litterman, R. (1992). Global portfolio optimization. *Financial Analysts Journal*, 48(5), 28–43. https://doi.org/10.2469/faj.v48.n5.28
- ✓ Breuer, T., Jandačka, M., Rheinberger, K., & Summer, M. (2009). How to find plausible, severe, and useful stress scenarios. *IJCB*, 5(3), 205–224.
- ✓ Carhart, M.M. (1997). On persistence in mutual fund performance. *Journal of Finance*, 52(1), 57–82. https://doi.org/10.1111/j.1540-6261.1997.tb03808.x
- ✓ Cespedes, J.C.G., et al. (2006). A simple multi-factor "factor adjustment" for the treatment of diversification in credit capital rules. *Journal of Credit Risk*.
- ? Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. KDD. arXiv:1603.02754.
- ✓ Christoffersen, P. (1998). Evaluating interval forecasts. *International Economic Review*, 39, 841–862. https://doi.org/10.2307/2527341
- ? Cohen, B.H., & Edwards, G.A. (2017). The new era of expected credit loss provisioning. *BIS Quarterly Review*, March.
- ~ Credit Suisse First Boston (1997). *CreditRisk+: A Credit Risk Management Framework*.
- ✓ DeMiguel, V., Garlappi, L., & Uppal, R. (2009). Optimal versus naive diversification. *RFS*, 22(5), 1915–1953. https://doi.org/10.1093/rfs/hhm075
- ✓ Dirick, L., Claeskens, G., & Baesens, B. (2017). Time to default in credit scoring using survival analysis: a benchmark study. *JORS*. https://doi.org/10.1057/s41274-016-0128-9
- ✓ Du, Z., & Escanciano, J.C. (2017). Backtesting expected shortfall: accounting for tail risk. *Management Science*, 63(4). https://doi.org/10.1287/mnsc.2015.2342
- ✓ Düllmann, K., & Masschelein, N. (2006). Sector concentration in loan portfolios and economic capital. NBB WP 105.
- ✓ Fama, E.F., & French, K.R. (1993). Common risk factors in the returns on stocks and bonds. *JFE*, 33, 3–56. https://doi.org/10.1016/0304-405X(93)90023-5
- ✓ Fama, E.F., & French, K.R. (2015). A five-factor asset pricing model. *JFE*, 116(1), 1–22. https://doi.org/10.1016/j.jfineco.2014.10.010
- ✓ Fissler, T., Ziegel, J., & Gneiting, T. (2016). Expected shortfall is jointly elicitable with value at risk. arXiv:1507.00244.
- ✓ Glasserman, P., Kang, C., & Kang, W. (2015). Stress scenario selection by empirical likelihood. *Quantitative Finance*, 15(1), 25–41.
- ~ Gneiting, T. (2011). Making and evaluating point forecasts. *JASA*, 106, 746–762.
- ✓ Gordy, M.B. (2000). A comparative anatomy of credit risk models. *JBF*, 24 (FEDS 1998-47).
- ✓ Gordy, M.B. (2003). A risk-factor model foundation for ratings-based bank capital rules. *JFI*, 12(3), 199–232. https://doi.org/10.1016/S1042-9573(03)00040-8
- ~ Gordy, M.B. (2004). Granularity adjustment in portfolio credit risk measurement. In Szegö (ed.), *Risk Measures for the 21st Century*, Wiley.
- ✓ Gordy, M.B., & Lütkebohmert, E. (2013). Granularity adjustment for regulatory capital assessment. *IJCB*, 9(3), 33–71.
- ✓ Grundke, P., & Pliszka, K. (2018). A macroeconomic reverse stress test. *RQFA*, 50, 1093–1130.
- ✓ Gupton, G.M., Finger, C.C., & Bhatia, M. (1997). *CreditMetrics — Technical Document*. J.P. Morgan.
- ✓ He, G., & Litterman, R. (1999). The intuition behind Black-Litterman model portfolios. SSRN 334304.
- ✓ Idzorek, T. (2004). A step-by-step guide to the Black-Litterman model. SSRN 3479867.
- ✓ IMF (Oura, H., Schumacher, L., et al.) (2012). Macrofinancial stress testing — principles and practices.
- ? Jarrow, R., Lando, D., & Turnbull, S. (1997). A Markov model for the term structure of credit risk spreads. *RFS*, 10(2), 481–523.
- ✓ J.P. Morgan/Reuters (1996). *RiskMetrics — Technical Document*, 4th ed.
- ✓ Karmakar, M. (2013). Estimation of tail-related risk measures in the Indian stock market: an extreme value approach. *Review of Financial Economics*.
- ✓ Kupiec, P. (1995). Techniques for verifying the accuracy of risk measurement models. *Journal of Derivatives*, 3(2), 73–84. https://doi.org/10.3905/jod.1995.407942
- ✓ Kupiec, P. (1998). Stress testing in a value at risk framework. *Journal of Derivatives*, 6(1), 7–24.
- ✓ Ledoit, O., & Wolf, M. (2004a). Honey, I shrunk the sample covariance matrix. *JPM*, 30(4), 110–119.
- ~ Ledoit, O., & Wolf, M. (2004b). A well-conditioned estimator for large-dimensional covariance matrices. *JMVA*, 88, 365–411.
- ✓ Ledoit, O., & Wolf, M. (2020). Analytical nonlinear shrinkage of large-dimensional covariance matrices. *Annals of Statistics*, 48(5), 3043–3065.
- ✓ Lessmann, S., Baesens, B., Seow, H.-V., & Thomas, L.C. (2015). Benchmarking state-of-the-art classification algorithms for credit scoring. *EJOR*, 247, 124–136. https://doi.org/10.1016/j.ejor.2015.05.030
- ~ Li, P., et al. (2018). Modeling loss given default. FDIC CFR WP 2018-03.
- ✓ Lopez, J.A. (1999). Regulatory evaluation of value-at-risk models. FRBSF WP 99-06.
- ✓ López de Prado, M. (2016). Building diversified portfolios that outperform out of sample. *JPM*, 42(4), 59–69. SSRN 2708678.
- ~ Loterman, G., Brown, I., Martens, D., Mues, C., & Baesens, B. (2012). Benchmarking regression algorithms for loss given default modeling. *IJF*, 28(1), 161–170.
- ? Lundberg, S., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. NeurIPS. arXiv:1705.07874.
- ✓ Maillard, S., Roncalli, T., & Teïletche, J. (2010). The properties of equally weighted risk contribution portfolios. *JPM*, 36(4), 60–70.
- ✓ Markowitz, H. (1952). Portfolio selection. *Journal of Finance*, 7(1), 77–91. https://doi.org/10.1111/j.1540-6261.1952.tb01525.x
- ✓ Martin, R., & Wilde, T. (2002). Unsystematic credit risk. *Risk*, 15(11), 123–128.
- ✓ McNeil, A.J., & Frey, R. (2000). Estimation of tail-related risk measures for heteroscedastic financial time series. *JEF*, 7, 271–300. https://doi.org/10.1016/S0927-5398(00)00012-8
- ✓ Menchero, J., Orr, D.J., & Wang, J. (2011). *The Barra US Equity Model (USE4) Methodology Notes*. MSCI.
- ✓ Merton, R.C. (1974). On the pricing of corporate debt. *Journal of Finance*, 29(2), 449–470. https://doi.org/10.1111/j.1540-6261.1974.tb03058.x
- ~ Michaud, R.O. (1989). The Markowitz optimization enigma. *FAJ*, 45(1), 31–42.
- ✓ Mina, J., & Xiao, J.Y. (2001). *Return to RiskMetrics: The Evolution of a Standard*. RiskMetrics Group.
- ✓ Nolde, N., & Ziegel, J. (2017). Elicitability and backtesting: perspectives for banking regulation. *Annals of Applied Statistics*. arXiv:1608.05498.
- ✓ Pritsker, M. (2006). The hidden dangers of historical simulation. *JBF* 30(2). SSRN 278438.
- ~ Pykhtin, M. (2004). Multi-factor adjustment. *Risk*, March, 85–90.
- ? Reserve Bank of India (2023). Discussion paper on introduction of expected credit loss framework for provisioning by banks.
- ✓ Rebonato, R. (2010). *Coherent Stress Testing: A Bayesian Approach*. Wiley. https://doi.org/10.1002/9781118374719
- ✓ Rebonato, R., & Denev, A. (2010). A Bayesian approach to stress testing and scenario analysis. *Journal of Investment Management*.
- ✓ Rockafellar, R.T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk*, 2(3), 21–41.
- ✓ Rockafellar, R.T., & Uryasev, S. (2002). Conditional value-at-risk for general loss distributions. *JBF*, 26(7), 1443–1471. https://doi.org/10.1016/S0378-4266(02)00271-6
- ✓ Rosenberg, B. (1974). Extra-market components of covariance in security returns. *JFQA*, 9(2), 263–274.
- ~ Schmieder, C., Puhr, C., & Hasan, M. (2011). Next generation balance sheet stress testing. IMF WP/11/83.
- ✓ Stepanova, M., & Thomas, L. (2002). Survival analysis methods for personal loan data. *Operations Research*, 50(2), 277–289. https://doi.org/10.1287/opre.50.2.277.426
- ✓ Tong, E.N.C., Mues, C., & Thomas, L. (2013). A zero-adjusted gamma model for mortgage loan loss given default. *IJF*, 29(4), 548–562. https://doi.org/10.1016/j.ijforecast.2013.03.003
- ✓ Tong, E.N.C., Mues, C., Brown, I., & Thomas, L.C. (2016). Exposure at default models with and without the credit conversion factor. *EJOR*.
- ✓ Vasicek, O. (2002). The distribution of loan portfolio value. *Risk*, 15(12), 160–162.
- ? Wilson, T.C. (1997). Portfolio credit risk I/II. *Risk*.
- ✓ Witzany, J. (2011). Exposure at default modeling with default intensities. *European Financial and Accounting Journal*.

**Totals:** 90 entries. About 66 fully verified, about 13 partial, and about 11 unverified (concentrated in IFRS 9/ECL and recent ML).
