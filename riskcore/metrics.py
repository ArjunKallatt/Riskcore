"""Core portfolio risk metrics. All functions take simple (daily) returns."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

TRADING_DAYS = 252


def portfolio_returns(returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Daily-rebalanced portfolio return series."""
    w = weights.reindex(returns.columns).fillna(0.0)
    return returns.mul(w, axis=1).sum(axis=1)


def annual_return(r: pd.Series) -> float:
    return float((1 + r).prod() ** (TRADING_DAYS / len(r)) - 1)


def annual_vol(r: pd.Series) -> float:
    return float(r.std(ddof=1) * np.sqrt(TRADING_DAYS))


def sharpe(r: pd.Series, rf: float = 0.0) -> float:
    vol = annual_vol(r)
    return float((annual_return(r) - rf) / vol) if vol else float("nan")


def beta(r: pd.Series, benchmark: pd.Series) -> float:
    df = pd.concat([r, benchmark], axis=1).dropna()
    var = df.iloc[:, 1].var(ddof=1)
    return float(df.iloc[:, 0].cov(df.iloc[:, 1]) / var) if var else float("nan")


def drawdown_series(r: pd.Series) -> pd.Series:
    wealth = (1 + r).cumprod()
    return wealth / wealth.cummax() - 1


def max_drawdown(r: pd.Series) -> float:
    return float(drawdown_series(r).min())


def var_historical(r: pd.Series, level: float = 0.95) -> float:
    """1-day VaR as a positive loss fraction."""
    return float(-np.quantile(r, 1 - level))


def cvar_historical(r: pd.Series, level: float = 0.95) -> float:
    """Expected shortfall: mean loss in the tail beyond VaR."""
    cutoff = np.quantile(r, 1 - level)
    tail = r[r <= cutoff]
    return float(-tail.mean())


def var_parametric(r: pd.Series, level: float = 0.95) -> float:
    return float(-(r.mean() + norm.ppf(1 - level) * r.std(ddof=1)))


def risk_contributions(returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Each asset's share of total portfolio volatility (sums to 1)."""
    w = weights.reindex(returns.columns).fillna(0.0).to_numpy()
    cov = returns.cov().to_numpy()
    port_var = w @ cov @ w
    if port_var == 0:
        return pd.Series(0.0, index=returns.columns)
    return pd.Series(w * (cov @ w) / port_var, index=returns.columns)
