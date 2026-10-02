"""Scenario stress testing via simple factor sensitivities.

Each holding carries: beta (to equity market), duration (years, for rate
sensitivity) and fx_exposure (fraction of value in foreign currency).
P&L% per holding ~= beta*mkt_shock - duration*rate_shock + fx_exposure*fx_shock
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Scenario:
    name: str
    market: float = 0.0  # equity market return, e.g. -0.38
    rates_bps: float = 0.0  # parallel yield shift in bps
    fx: float = 0.0  # change in foreign-currency value vs INR (INR depreciation = +)


SCENARIOS = [
    Scenario("2020 COVID crash replay", market=-0.38, rates_bps=-75, fx=0.05),
    Scenario("200 bps rate hike", market=-0.08, rates_bps=200),
    Scenario("10% INR depreciation", market=-0.05, fx=0.10),
    Scenario("2008-style equity bear", market=-0.55, rates_bps=-150, fx=0.15),
]


def stress(holdings: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """holdings: index=asset, columns=value, beta, duration, fx_exposure."""
    pct = (
        holdings["beta"] * scenario.market
        - holdings["duration"] * scenario.rates_bps / 10_000
        + holdings["fx_exposure"] * scenario.fx
    )
    out = pd.DataFrame({"value": holdings["value"], "pnl_pct": pct})
    out["pnl"] = out["value"] * out["pnl_pct"]
    return out


def run_all(holdings: pd.DataFrame, scenarios: list[Scenario] = SCENARIOS) -> pd.DataFrame:
    total = holdings["value"].sum()
    rows = []
    for s in scenarios:
        pnl = stress(holdings, s)["pnl"].sum()
        rows.append({"scenario": s.name, "pnl": pnl, "pnl_pct": pnl / total})
    return pd.DataFrame(rows).set_index("scenario")
