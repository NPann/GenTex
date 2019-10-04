from . import comat, features, texmeas, template, sphere
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

__version__ = '0.1.2'
