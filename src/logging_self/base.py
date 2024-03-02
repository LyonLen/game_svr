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


def init_logger(svr_name, log_path, log_level=logging.INFO, instance_id=None):
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)

    global logger
    logger = logging.getLogger("svr_name")
    logger.setLevel(log_level)

    if instance_id is None:
        instance_id = os.getpid()
    file_handler = logging.handlers.TimedRotatingFileHandler(f"{log_path}/{svr_name}_{instance_id}.log", 'H', 1, 0)
    file_handler.suffix = "%Y%m%d%H"
    file_handler.setFormatter(
        logging.Formatter(
            f"%(asctime)s.%(msecs)d|pid(%(process)d)|{svr_name}_{instance_id}|%(threadName)s|%(filename)s:%(lineno)d|%(levelname)s|%(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(file_handler)
    global stream_handler
    logger.removeHandler(stream_handler)
