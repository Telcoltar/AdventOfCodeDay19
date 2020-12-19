import logging
from logging.config import fileConfig

fileConfig("log.ini")

logger = logging.getLogger("dev")




if __name__ == '__main__':
    logger.debug("Hi")

