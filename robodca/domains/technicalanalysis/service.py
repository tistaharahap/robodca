from os import environ
from typing import List
from robodca.domains.exchange.service import get_candles
from .strategies.base import Strategy
from .strategies.bwblv4dca import BWBLv4DCA


STRATEGY = environ.get('STRATEGY')
PAIR = environ.get('PAIR')


def get_strategy(name: str, pair: str) -> Strategy:
    strats = {
        'BWBLv4DCA': BWBLv4DCA
    }

    strat = strats.get('name')
    if not strat:
        raise NotImplementedError(f'Strategy {name} is not available, bailing..')

    return strat(pair=pair)


async def pulse():
    pass
