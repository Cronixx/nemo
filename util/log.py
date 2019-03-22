import logging
import os


def configure_logging(fn=None,
                      log_dir=None,
                      threshold=logging.DEBUG,
                      fmt='[%(asctime)s] %(name)s - %(levelname)s: %(message)s',
                      date_fmt='%Y/%m/%d %H:%M:%S'):

    if fn is not None and log_dir is not None:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        fn = os.path.join(log_dir, fn)
    logging.basicConfig(level=threshold, format=fmt, datefmt=date_fmt, filename=fn)


if __name__ == '__main__':
    pass
