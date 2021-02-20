import logging


def init_logging():
    logging.root.setLevel(logging.NOTSET)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.NOTSET)
    logging.root.addHandler(handler)


def get_logger(__name__):
    return logging.getLogger(__name__)
