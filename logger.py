from config import LOGS_PATH
import logging
import os

"""
# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
"""

if not os.path.isdir(LOGS_PATH):
    os.mkdir(LOGS_PATH)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%d-%m-%Y / %H:%M:%S")

file_handler = logging.FileHandler(f"{LOGS_PATH}/logs.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
