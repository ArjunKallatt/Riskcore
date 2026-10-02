"""Streamlit dashboard: streamlit run app.py"""
import pandas as pd
import plotly.express as px
import streamlit as st

from riskcore import metrics as m
from riskcore.data import get_prices
from riskcore.sample import BENCHMARK, SAMPLE
from riskcore.stress import SCENARIOS, run_all

st.set_page_config(page_title="Riskcore", layout="wide")
st.title("Riskcore – portfolio risk dashboard")

with st.sidebar:
    years = st.slider("History (years)", 1, 5, 3)
    level = st.select_slider("VaR confidence", [0.90, 0.95, 0.99], value=0.95)
    st.caption("Edit holdings (INR value) – this is the what-if rebalancer.")
    holdings = st.data_editor(SAMPLE, num_rows="dynamic")


@st.cache_data(show_spinner="Loading prices…")
def _load(tickers, years):
    return get_prices(list(tickers), years)


tickers = list(holdings.index)
prices, synthetic = _load(tuple(tickers + [BENCHMARK]), years)
if synthetic:
    st.warning("Live prices unavailable – showing synthetic demo data.")

rets = prices.pct_change().dropna()
bench = rets[BENCHMARK] if BENCHMARK in rets else rets.mean(axis=1)
asset_rets = rets[[t for t in tickers if t in rets.columns]]
holdings = holdings.loc[asset_rets.columns]
weights = holdings["value"] / holdings["value"].sum()
port = m.portfolio_returns(asset_rets, weights)

holdings = holdings.assign(beta=[m.beta(asset_rets[t], bench) for t in holdings.index])

c = st.columns(5)
c[0].metric("Portfolio value", f"₹{holdings['value'].sum():,.0f}")
c[1].metric("Ann. return", f"{m.annual_return(port):.1%}")
c[2].metric("Ann. volatility", f"{m.annual_vol(port):.1%}")
c[3].metric(f"1d VaR {level:.0%}", f"{m.var_historical(port, level):.2%}")
c[4].metric(f"1d CVaR {level:.0%}", f"{m.cvar_historical(port, level):.2%}")
c = st.columns(3)
c[0].metric("Beta vs Nifty", f"{m.beta(port, bench):.2f}")
c[1].metric("Max drawdown", f"{m.max_drawdown(port):.1%}")
c[2].metric("Sharpe (rf=0)", f"{m.sharpe(port):.2f}")

t1, t2, t3, t4 = st.tabs(["Risk", "Correlation", "Drawdown", "Stress tests"])
with t1:
    rc = m.risk_contributions(asset_rets, weights).rename("risk share")
    df = pd.concat([weights.rename("weight"), rc], axis=1).rename_axis("ticker").reset_index()
    st.plotly_chart(px.bar(df.melt("ticker"), x="ticker", y="value", color="variable",
                           barmode="group"), use_container_width=True)
    st.caption("Weight vs share of total volatility – a big gap means hidden concentration.")
with t2:
    st.plotly_chart(px.imshow(asset_rets.corr(), zmin=-1, zmax=1, text_auto=".2f",
                              color_continuous_scale="RdBu_r"), use_container_width=True)
with t3:
    st.plotly_chart(px.area(m.drawdown_series(port)), use_container_width=True)
with t4:
    res = run_all(holdings, SCENARIOS)
    st.dataframe(res.style.format({"pnl": "₹{:,.0f}", "pnl_pct": "{:.1%}"}))
    st.caption("Sensitivity-based: beta × market shock − duration × Δrates + FX exposure × Δfx.")
