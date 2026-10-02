# Riskcore

A lightweight, "mini-Aladdin" portfolio risk engine for Indian markets.

- **Metrics:** return, volatility, beta, Sharpe, drawdown, historical/parametric VaR, CVaR, risk contributions
- **Stress tests:** 2020 crash replay, +200 bps rates, 10% INR depreciation, 2008-style bear (sensitivity-based)
- **Dashboard:** Streamlit; edit holdings in the sidebar for what-if rebalancing
- **Data:** Yahoo Finance (`.NS` tickers), automatic synthetic fallback when offline

```
pip install -r requirements.txt
pytest
streamlit run app.py
```

Roadmap: mutual funds & bonds via QuantLib, optimization (PyPortfolioOpt), loan-book (PD/LGD/EAD) module on synthetic data.

Research: see [research/REPORT.md](research/REPORT.md) for the landscape, data, regulation and 6-week roadmap.
