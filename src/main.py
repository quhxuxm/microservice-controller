#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
import os
from logging.config import fileConfig

import const
from entry import MainEntry


def initialize_logging():
    if not os.path.isdir(const.LOGGING_LOG_FILE_DIR_PATH):
        os.mkdir(const.LOGGING_LOG_FILE_DIR_PATH)
    fileConfig(const.LOGGING_CONFIG_FILE_PATH)


initialize_logging()

logger = logging.getLogger("root." + __name__)

if __name__ == "__main__":
    main_entry = MainEntry()
    main_entry.cmdloop("Begin to start Micro Service Controller ...")
