from os import environ

from .strategies.base import Strategy
from .strategies.bwblv4dca import BWBLv4DCA

STRATEGY = environ.get('STRATEGY')
PAIR = environ.get('PAIR')
TIMEFRAME = environ.get('TIMEFRAME')


def get_strategy(name: str, pair: str, timeframe: str) -> Strategy:
    strats = {
        'BWBLv4DCA': BWBLv4DCA
    }

    strat = strats.get('name')
    if not strat:
        raise NotImplementedError(f'Strategy {name} is not available, bailing..')

    return strat(pair=pair,
                 timeframe=timeframe)


async def pulse():
    pass
