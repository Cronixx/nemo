import logging
import os


def configure_logging(fn=None,
                      log_dir=None,
                      threshold=logging.DEBUG,
                      fmt='[%(asctime)s] %(name)s - %(levelname)s: %(message)s',
                      date_fmt='%Y/%m/%d %H:%M:%S'):
    log_file = None
    if (log_dir is not None) and (fn is not None):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, fn)
    logging.basicConfig(level=threshold, format=fmt, datefmt=date_fmt, filename=log_file)
