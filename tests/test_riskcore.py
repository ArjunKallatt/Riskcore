import numpy as np
import pandas as pd
import pytest

from riskcore import metrics as m
from riskcore.data import synthetic_prices
from riskcore.stress import Scenario, run_all, stress


def _rets():
    return synthetic_prices(["A", "B", "C"], years=2).pct_change().dropna()


def test_cvar_exceeds_var():
    p = _rets()["A"]
    assert m.cvar_historical(p, 0.95) >= m.var_historical(p, 0.95) > 0


def test_beta_of_self_is_one():
    p = _rets()["A"]
    assert m.beta(p, p) == pytest.approx(1.0)


def test_max_drawdown_known():
    r = pd.Series([0.1, -0.5, 0.2])  # 1.1 -> 0.55
    assert m.max_drawdown(r) == pytest.approx(-0.5)


def test_risk_contributions_sum_to_one():
    r = _rets()
    w = pd.Series({"A": 0.5, "B": 0.3, "C": 0.2})
    assert m.risk_contributions(r, w).sum() == pytest.approx(1.0)


def test_stress_math():
    h = pd.DataFrame({"value": [100.0], "beta": [1.0], "duration": [5.0],
                      "fx_exposure": [0.5]}, index=["X"])
    s = Scenario("t", market=-0.1, rates_bps=100, fx=0.1)
    # -0.1 - 5*0.01 + 0.5*0.1 = -0.1
    assert stress(h, s)["pnl"].iloc[0] == pytest.approx(-10.0)
    assert run_all(h, [s])["pnl_pct"].iloc[0] == pytest.approx(-0.1)
