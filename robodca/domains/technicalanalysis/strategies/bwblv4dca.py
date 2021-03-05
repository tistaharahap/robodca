from .base import Strategy, StrategyRecommendation
from robodca.domains.exchange.service import get_candles


class BWBLv4DCA(Strategy):

    async def get_recommendation(self) -> StrategyRecommendation:
        self.ohlcv = await get_candles()
