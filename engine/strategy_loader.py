from engine.strategies.trend_following import TrendFollowing
from engine.strategies.mean_reversion import MeanReversion
from engine.strategies.volatility_breakout import VolatilityBreakout
from engine.strategies.range_play import RangePlay


def load_strategy_class(logic_id: str):

    mapping = {
        "STRAT_1": TrendFollowing,
        "STRAT_2": MeanReversion,
        "STRAT_3": VolatilityBreakout,
        "STRAT_4": RangePlay,
    }

    if logic_id not in mapping:
        raise ValueError(f"Strategy {logic_id} not implemented")

    return mapping[logic_id]
