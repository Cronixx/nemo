import logging
from util.log import configure_logging
from core.nemo import Nemo


configure_logging(fn="test.log", log_dir="data/log")
logger = logging.getLogger(__name__)
logger.info("Initialized logger {}".format(logger))

n = Nemo()
n.puke()
