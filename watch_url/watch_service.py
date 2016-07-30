"""watch_url."""
import logging
import yaml

# from nameko.events import Event, EventDispatcher, event_handler
from nameko.runners import ServiceRunner
from nameko.testing.utils import get_container

from watch_url import WatchURLService

logging.basicConfig(level=logging.DEBUG)
try:
    from config_common import LOGGING
    logging.config.dictConfig(LOGGING)
except:
    print 'No LOGGING configuration found.'
logger = logging.getLogger(__name__)

def get_config(path):
    with open(path) as f:
        y = f.read()
        c = yaml.load(y)
    return c

# config = {'AMQP_URI': 'amqp://guest:guest@localhost:5672/'}
# runner = ServiceRunner(config)
c = get_config('config.yaml')
runner = ServiceRunner(c)
runner.add_service(WatchURLService)
# container_a = get_container(runner, WatchURLService)
runner.start()
try:
    runner.wait()
except KeyboardInterrupt:
    runner.kill()
runner.stop()
# sys.exit()
