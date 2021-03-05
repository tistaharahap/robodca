from os import environ, getcwd
from robodca.constants import Constants
import ccxt


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


async def get_candles(pair: str, count: int = 529):
    client = get_ccxt_client(exchange=EXCHANGE,
                             api_key=API_KEY,
                             api_secret=API_SECRET)

    ohlcv = client.fetch_ohlcv(symbol=pair,
                               timeframe=TIMEFRAME,
                               limit=count)
    return ohlcv
