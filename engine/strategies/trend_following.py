import pandas as pd
from .strategy_base import StrategyBase

class STRAT_1(StrategyBase):

    def generate_signals(self, df):
        df = df.copy()

        df["fast_ma"] = df["close"].rolling(self.params["fast_ma"]).mean()
        df["slow_ma"] = df["close"].rolling(self.params["slow_ma"]).mean()

        df["signal"] = 0

        df.loc[df["fast_ma"] > df["slow_ma"], "signal"] = 1
        df.loc[df["fast_ma"] < df["slow_ma"], "signal"] = -1

        return df
