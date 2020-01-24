"""
ABOUT: Set up logging for program execution
AUTHOR: djbhatia@ucsd.edu

Jan. 2020
"""
import os
import sys
import logging
from datetime import datetime

class MattLOG:
    """
    MattLog is used for managing logging.
    """
    def __init__(self):
        pass

    def create_log(self, name):
        """
        Create logging file for program.
        Reference: https://stackoverflow.com/questions/28330317/print-timestamp-for-logging-in-python/28330410#28330410

        :param name: Name of logger
        :return: logging object
        """
        # Format Log File Name and Logging Style
        filename = datetime.now().strftime("%Y-%m-%d_%H:%M")
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s - %(message)s",
                                      datefmt="%m-%d-%Y %I:%M:%S %p")
        # Idenitfy where Logs should be saved
        # handler = logging.FileHandler("~/MouseBehavior/logs/{}.log".format(filename), mode='w')
        handler = logging.FileHandler("logs/{}.log".format(filename), mode='w')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
        return logger
