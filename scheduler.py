import uvloop
import asyncio
from os import environ
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from robodca.domains.technicalanalysis.service import pulse

TIMEFRAME = environ.get('TIMEFRAME')
timeframe_args = {
    '15': {
        'minute': '15',
        'jitter': '10'
    },
    '60': {
        'minute': '0',
        'jitter': '10',
    },
    '120': {
        'minute': '0',
        'jitter': '10',
        'hour': '*/2'
    },
    '240': {
        'minute': '0',
        'jitter': '10',
        'hour': '*/4'
    },
    '360': {
        'minute': '0',
        'jitter': '10',
        'hour': '*/6'
    },
    '720': {
        'minute': '0',
        'jitter': '10',
        'hour': '*/12'
    },
    'D': {
        'minute': '0',
        'jitter': '10',
        'hour': '0'
    }
}
job_args = timeframe_args.get(TIMEFRAME)
if not job_args:
    raise NotImplementedError('The timeframe configured is not supported')

uvloop.install()

scheduler = AsyncIOScheduler()
scheduler.add_job(pulse, 'cron', **job_args)
scheduler.start()
print(f'RoboDCA TA Domain is running, press Ctrl+C to exit')

try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
