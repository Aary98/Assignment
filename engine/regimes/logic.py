import pandas as pd

def detect_regime(df, config):

    ma = df["close"].rolling(config["trend_ma"]).mean()
    atr = (df["high"] - df["low"]).rolling(config["atr_window"]).mean()

    if df["close"].iloc[-1] > ma.iloc[-1]:
        return "trend"

    if atr.iloc[-1] > atr.mean():
        return "volatile"

    return "range"
