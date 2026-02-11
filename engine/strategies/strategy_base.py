from abc import ABC, abstractmethod
import pandas as pd

class StrategyBase(ABC):

    def __init__(self, params):
        self.params = params

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame):
        pass
