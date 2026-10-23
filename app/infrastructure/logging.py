import logging

LOG_FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(fmt=LOG_FMT, datefmt=DATE_FMT))
    logger.addHandler(stream_handler)
    return logger
