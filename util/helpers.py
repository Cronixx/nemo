import logging


logger = logging.getLogger(__name__)
default_data_dir = "../data"


def print_sep(sep='=', num=80):
    print(sep*num)


def pickle_to(obj, filename, data_dir=default_data_dir):
    import pickle, os
    if not os.path.exists(data_dir):
        logger.warning("Directory {} doesn't exist. Trying to create it.".format(data_dir))
        os.makedirs(data_dir)
    with open(os.path.join(data_dir, filename), mode="wb") as file:
        logger.debug("Pickling {} to file: {}".format(obj.__class__, os.path.join(data_dir, filename)))
        pickle.dump(obj, file)


def from_file(cls, filename, data_dir=default_data_dir):
    import pickle, os
    if not os.path.exists(data_dir):
        raise FileNotFoundError("No data directory.")
    fp = os.path.join(data_dir, filename)
    with open(fp, mode="rb") as file:
        logger.info("Creating {} from file: {}".format(cls.__name__, fp))
        return pickle.load(file)
