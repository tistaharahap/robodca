from abc import abstractmethod
from enum import Enum


class StrategyRecommendation(Enum):
    DoNothing = 0
    Buy = 1
    StrongBuy = 2
    Sell = -1
    StrongSell = -2


class Strategy(object):

    def __init__(self, pair, candle_count: int = 529):
        self.pair = pair
        self.candle_count = candle_count
        self.ohlcv = []

    @abstractmethod
    async def get_recommendation(self) -> StrategyRecommendation:
        raise NotImplementedError('The abstract method get_recommendation must be implemented')