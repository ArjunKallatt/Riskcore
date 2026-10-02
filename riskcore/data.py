"""Price loading: Yahoo Finance (NSE tickers end in .NS) with synthetic fallback."""
from __future__ import annotations

import numpy as np
import pandas as pd


def load_prices(tickers: list[str], years: int = 3) -> pd.DataFrame:
    """Download adjusted close prices; raises if nothing usable comes back."""
    import yfinance as yf

    raw = yf.download(tickers, period=f"{years}y", auto_adjust=True, progress=False)
    prices = raw["Close"] if "Close" in raw else raw
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(tickers[0])
    prices = prices.dropna(how="all").ffill().dropna(axis=1, how="all")
    if prices.empty:
        raise RuntimeError("no price data returned")
    return prices


def synthetic_prices(tickers: list[str], years: int = 3, seed: int = 42) -> pd.DataFrame:
    """Correlated GBM prices so the app works offline / for demos."""
    rng = np.random.default_rng(seed)
    n, k = years * 252, len(tickers)
    common = rng.normal(0.0004, 0.01, size=(n, 1))
    idio = rng.normal(0.0002, 0.012, size=(n, k))
    loadings = rng.uniform(0.6, 1.4, size=(1, k))
    rets = common * loadings + idio
    idx = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n)
    return pd.DataFrame(100 * np.cumprod(1 + rets, axis=0), index=idx, columns=tickers)


def get_prices(tickers: list[str], years: int = 3) -> tuple[pd.DataFrame, bool]:
    """Return (prices, is_synthetic)."""
    try:
        return load_prices(tickers, years), False
    except Exception:
        return synthetic_prices(tickers, years), True
