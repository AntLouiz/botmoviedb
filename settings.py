import logging
from decouple import config

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
MOVIE_DB_TOKEN = config('MOVIE_DB_TOKEN')

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
