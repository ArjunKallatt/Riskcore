"""Sample Indian portfolio. Betas are estimated from data; duration/fx are static."""
import pandas as pd

SAMPLE = pd.DataFrame(
    [
        # ticker, class, value (INR), duration, fx_exposure
        ("RELIANCE.NS", "Equity", 300_000, 0.0, 0.0),
        ("TCS.NS", "Equity", 250_000, 0.0, 0.6),
        ("HDFCBANK.NS", "Equity", 250_000, 0.0, 0.0),
        ("INFY.NS", "Equity", 150_000, 0.0, 0.6),
        ("GOLDBEES.NS", "Gold", 150_000, 0.0, 0.3),
        ("LIQUIDBEES.NS", "Bond", 100_000, 0.1, 0.0),
    ],
    columns=["ticker", "asset_class", "value", "duration", "fx_exposure"],
).set_index("ticker")

BENCHMARK = "^NSEI"
