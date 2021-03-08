from robodca.domains.exchange.service import fetch_candles
from robodca.domains.technicalanalysis.indicators.billwilliams import AccelerationDecelerationOscillator
from robodca.domains.technicalanalysis.indicators.billwilliams import AwesomeOscillator
from robodca.domains.technicalanalysis.indicators.billwilliams import WilliamsAlligatorJaws, WilliamsAlligatorTeeth
from robodca.domains.technicalanalysis.indicators.billwilliams import WilliamsAlligatorLips
from .base import Strategy, StrategyRecommendation


class BWBLv4DCA(Strategy):

    async def get_recommendation(self) -> StrategyRecommendation:
        self.ohlcv = await fetch_candles(symbol=self.pair,
                                         timeframe=self.timeframe,
                                         candles_count=529)

        self.indicators = {
            'ao': AwesomeOscillator(sources=self.ohlcv.get('closes')),
            'ac': AccelerationDecelerationOscillator(sources=self.ohlcv.get('closes')),
            'jaws': WilliamsAlligatorJaws(highs=self.ohlcv.get('highs'),
                                          lows=self.ohlcv.get('lows')),
            'teeth': WilliamsAlligatorTeeth(highs=self.ohlcv.get('highs'),
                                            lows=self.ohlcv.get('lows')),
            'lips': WilliamsAlligatorLips(highs=self.ohlcv.get('highs'),
                                          lows=self.ohlcv.get('lows'))
        }
