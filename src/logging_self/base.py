import logging
import os
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("base")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s.%(msecs)d|pid(%(process)d)|%(threadName)s|svr_not_defined|%(filename)s:%(lineno)d|%(levelname)s|%(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
)
logger.addHandler(stream_handler)


def init_logger(instance_name, log_path, log_level=logging.INFO):
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)

    global logger
    logger = logging.getLogger(instance_name)
    logger.setLevel(log_level)

    file_handler = logging.handlers.TimedRotatingFileHandler(f"{log_path}/{instance_name}.log", 'H', 1, 0)
    file_handler.suffix = "%Y%m%d%H"
    file_handler.setFormatter(
        logging.Formatter(
            f"%(asctime)s.%(msecs)d|pid(%(process)d)|{instance_name}|%(threadName)s|%(filename)s:%(lineno)d|%(levelname)s|%(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(file_handler)
    global stream_handler
    logger.removeHandler(stream_handler)
