from os import environ, getcwd
from typing import Dict

import ccxt
import numpy as np

from robodca.constants import Constants

EXCHANGE = environ.get('EXCHANGE')
API_KEY = environ.get('API_KEY')
API_SECRET = environ.get('API_SECRET')
TIMEFRAME = environ.get('1h')


def get_ccxt_client(exchange: str, api_key: str = None, api_secret: str = None, testnet: bool = True) -> ccxt.Exchange:
    try:
        exc = getattr(ccxt, exchange)
    except AttributeError:
        raise AttributeError(f'The exchange {exchange} is not supported')

    current_path = getcwd()
    with open(f'{current_path}/version.txt', 'r') as f:
        version = f.readline()

    headers = {
        'User-Agent': f'{Constants.UserAgent}/v{version}'
    }

    if api_key and api_secret:
        exchange = exc({
            'apiKey': api_key,
            'secret': api_secret,
            'headers': headers
        })
    else:
        exchange = exc({
            'headers': headers
        })

    if testnet:
        if 'test' in exchange.urls:
            exchange.urls['api'] = exchange.urls['test']
        else:
            raise NotImplementedError('Testnet is wanted but the exchange does not support testnet')

    return exchange


async def fetch_candles(symbol: str, timeframe: str = '1h', candles_count: int = 529,
                        trade_on_close: bool = False) -> Dict[str, np.ndarray]:
    client = get_ccxt_client(exchange=EXCHANGE,
                             testnet=False)
    if not client.has['fetchOHLCV']:
        raise TypeError(f'The exchange {EXCHANGE} does not let candles to be retrieved')

    ohlcv = client.fetch_ohlcv(symbol=symbol,
                               timeframe=timeframe,
                               limit=candles_count)

    opens = list(map(lambda x: x[1], ohlcv))
    highs = list(map(lambda x: x[2], ohlcv))
    lows = list(map(lambda x: x[3], ohlcv))
    closes = list(map(lambda x: x[4], ohlcv))
    volumes = list(map(lambda x: x[5], ohlcv))

    if trade_on_close:
        opens.pop(1)
        highs.pop(1)
        lows.pop(1)
        closes.pop(1)
        volumes.pop(1)

    return {
        'opens': np.array(opens),
        'highs': np.array(highs),
        'lows': np.array(lows),
        'closes': np.array(closes),
        'volumes': np.array(volumes)
    }
