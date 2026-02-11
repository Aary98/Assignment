import pandas as pd
import json
import sys
from engine.regimes.logic import detect_regime
from engine.strategies.trend_following import STRAT_1


with open("configs/engine.json") as f:
    config = json.load(f)


df = pd.read_csv(config["data_file"])
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

trades = []

position = 0
entry_price = 0
entry_date = None


for i in range(60, len(df)-1):

    df_slice = df.iloc[:i]

    regime = detect_regime(df_slice, config["regime_classifier"])

    
    strategy = STRAT_1(config["strategies"]["trend_following"]["params"])

    signals = strategy.generate_signals(df_slice)

    signal = signals["signal"].iloc[-1]

    
    if signal == 1 and position == 0:
        position = 1
        entry_price = df["open"].iloc[i+1]
        entry_date = df["date"].iloc[i+1]

    
    elif signal == -1 and position == 1:
        exit_price = df["open"].iloc[i+1]
        exit_date = df["date"].iloc[i+1]

        pnl = exit_price - entry_price

        trades.append({
            "entry_dt": entry_date,
            "entry_price": entry_price,
            "qty": 1,
            "side": "LONG",
            "strategy_used": "STRAT_1",
            "regime": regime,
            "exit_dt": exit_date,
            "exit_price": exit_price,
            "pnl": pnl
        })

        position = 0

trades_df = pd.DataFrame(trades)
trades_df.to_excel("outputs/orders.xlsx", index=False)

print("Backtest Complete! File saved in outputs/orders.xlsx")
