import json
import logging
import logging.config


class LoggerCore:

    def __init__(self, path_to_file: str):
        self.path = path_to_file
        self._set_configurate()

    def _get_configurate_logging(self) -> json:
        with open(self.path) as file:
            data = json.load(file)
        return data

    def _set_configurate(self) -> None:
        logging.config.dictConfig(self._get_configurate_logging())


def get_my_logger(name: str) -> logging:
    return logging.getLogger(name)


def debugorator(debug_on: bool):
    def decorator(function):
        async def wrapper(*args, **kwargs):
            result = await function(*args, **kwargs)
            if debug_on:
                logger_debug = get_my_logger("primes")
                print("I am here")
                logger_debug.debug(f"Function {function.__name__} {args[0].username}")
            return result

        return wrapper

    return decorator
