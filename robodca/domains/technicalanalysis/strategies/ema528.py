from decimal import Decimal
from .base import Strategy, StrategyRecommendation
from robodca.domains.exchange.service import fetch_candles
from robodca.domains.technicalanalysis.indicators.movingaverages import EMA


class EMA528(Strategy):

    async def get_recommendation(self) -> StrategyRecommendation:
        self.ohlcv = await fetch_candles(symbol=self.pair,
                                         timeframe=self.timeframe,
                                         candles_count=529)

        self.indicators = {
            'ema528': EMA(sources=self.ohlcv.get('closes'),
                          period=528)
        }

        in_buy_zone = Decimal(self.ohlcv.get('closes')[-1]) < Decimal(self.indicators.get('ema528')[-1])

        return StrategyRecommendation.Buy if in_buy_zone else StrategyRecommendation.DoNothing
