import logging
import logging.config

log_config = {
    "version": 1,
    "formatters": {
        "my_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "my_formatter",
            "filename": "perky.log"
        },
    },
    "loggers": {
        "perky": {
            "handlers": ["file_handler"],
            "level": "INFO",
        }
    },
}


logging.config.dictConfig(log_config)
log = logging.getLogger('perky')


def perky(param):
    return param / 0


number = 42
try:
    log.info('Посмотрим как у него получится...')
    perky(number)
    log.info('Он смог!')
except Exception:
    log.exception(f'Дерзкий не справился c {number}')