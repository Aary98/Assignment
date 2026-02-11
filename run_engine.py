import argparse
import json
import pandas as pd
from engine.regimes.logic import detect_regime
from engine.strategy_loader import load_strategy_class


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def main(config_path: str):

    
    config = load_config(config_path)

   
    df = pd.read_csv(config["data_file"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    trades = []
    position = None

    for i in range(len(df) - 1):

        today_slice = df.iloc[: i + 1].copy()

        regime = detect_regime(today_slice, config)


        regime_map = {
            "trend": "trend_following",
            "range": "range_play",
            "volatile": "volatility_breakout",
            "low_vol": "mean_reversion"
        }

        strategy_key = regime_map.get(regime)

        strategy_config = config["strategies"].get(strategy_key)

        if not strategy_config or not strategy_config["enabled"]:
            continue

        StrategyClass = load_strategy_class(strategy_config["logic_id"])

        strategy = StrategyClass(strategy_config["params"])

        signals_df = strategy.generate_signals(today_slice)

        signal = signals_df["signal"].iloc[-1]


        next_open = df["open"].iloc[i + 1]
        next_date = df["date"].iloc[i + 1]

        if position is None and signal == 1:
            position = {
                "entry_dt": next_date,
                "entry_price": next_open,
                "qty": 1,
                "side": "LONG",
                "strategy_used": strategy_config["logic_id"],
                "regime": regime,
                "entry_index": i + 1
            }

        elif position is not None and signal == -1:
            exit_price = next_open
            pnl = (exit_price - position["entry_price"]) * position["qty"]

            trades.append({
                **position,
                "exit_dt": next_date,
                "exit_price": exit_price,
                "pnl": pnl,
                "bars_held": (i + 1) - position["entry_index"]
            })

            position = None

    trades_df = pd.DataFrame(trades)
    trades_df = trades_df.sort_values("entry_dt")

    trades_df.to_excel("outputs/orders.xlsx", index=False)

    print("Backtest Complete! File saved in outputs/orders.xlsx")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config JSON")
    args = parser.parse_args()

    main(args.config)
