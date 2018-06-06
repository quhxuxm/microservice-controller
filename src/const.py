#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

GLOBAL_CONFIG_FILE_PATH = os.path.join(os.path.abspath(os.path.curdir), "configuration.ini")
LOGGING_CONFIG_FILE_PATH = os.path.join(os.path.abspath(os.path.curdir), "logging.ini")
LOGGING_LOG_FILE_DIR_PATH = os.path.join(os.path.abspath(os.path.curdir), "logs")
COMPONENT_MODULE_PACKAGE_NAME = "component"
ENGINE_EXECUTOR_PROCESS_POOL_SIZE = 4
