import os
import logging

from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv('LOG_LEVEL')

# define a custom logging
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
# log_oa.addHandler(logging.FileHandler(__name__ + ".log"))

match log_level:
    case 'DEBUG':
        log.setLevel(logging.DEBUG)
    case 'INFO':
        log.setLevel(logging.INFO)
    case 'WARNING':
        log.setLevel(logging.WARNING)
    case 'ERROR':
        log.setLevel(logging.ERROR)
    case 'CRITICAL':
        log.setLevel(logging.CRITICAL)
    case _:
        log.setLevel(logging.INFO)
        log.warning("The log_level must be DEBUG, INFO, WARNING, ERROR or CRITICAL")
        log.warning("Log level set to 'INFO'")

