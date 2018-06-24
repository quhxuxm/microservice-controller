#!/usr/bin/python
# -*- coding: utf-8 -*-


import importlib
import logging
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

import const
from component import DefaultComponent
from util import Singleton


class EngineException(Exception):
    pass


@Singleton
class Engine:
    """
    The engine used to manage the flow of each step for the components
    """

    def __init__(self):
        self.__logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.__initialize_pool()
        self.__initialize_components()

    def __initialize_pool(self):
        self.__process_pool = ThreadPoolExecutor(const.ENGINE_EXECUTOR_PROCESS_POOL_SIZE)

    def __initialize_components(self):
        self.__components = {}
        configuration = ConfigParser()
        configuration.read(const.GLOBAL_CONFIG_FILE_PATH)
        for name in configuration.sections():
            if not name.startswith(const.COMPONENT_MODULE_PACKAGE_NAME):
                continue
            short_name = name[len(const.COMPONENT_MODULE_PACKAGE_NAME) + 1:]
            component_instance = None
            try:
                component_module = importlib.import_module(name)
                component_instance = component_module.Component(short_name, configuration)
            except ModuleNotFoundError as e:
                self.__logger.debug("Can not found the module [%s]." % name)
            if component_instance is not None:
                self.__logger.info("Success to find component module [%s]." % name)
                self.__components[short_name] = component_instance
            else:
                self.__logger.info(
                    "Can not find component module [%s], initialize component with default implementation." % name)
                self.__components[short_name] = DefaultComponent(short_name, configuration)

    def __verify_component(self, name):
        if name not in self.__components:
            raise EngineException("The component [%s] not exist, fail to build." % name)

    def p4_fetch(self, name):
        def exec():
            try:
                self.__verify_component(name)
                self.__components[name].p4_fetch()
            except Exception as e:
                self.__logger.error("Fail to fetch the code from P4 for component [%s]." % name, exc_info=e)

        return self.__process_pool.submit(exec)

    def build(self, name):
        def exec():
            try:
                self.__verify_component(name)
                self.__components[name].build()
            except Exception as e:
                self.__logger.error("Fail to build the code for component [%s]." % name, exc_info=e)

        return self.__process_pool.submit(exec)

    def deploy(self, name):
        def exec():
            try:
                self.__verify_component(name)
                self.__components[name].deploy_apache()
                self.__components[name].deploy_tomcat()
                self.__components[name].deploy()
            except Exception as e:
                self.__logger.error("Fail to deploy the component [%s]." % name, exc_info=e)

        return self.__process_pool.submit(exec)

    def start(self, name):
        def exec():
            try:
                self.__verify_component(name)
                self.__components[name].start()
            except Exception as e:
                self.__logger.error("Fail to start the component [%s]." % name, exc_info=e)

        return self.__process_pool.submit(exec)

    def stop(self, name):
        def exec():
            try:
                self.__verify_component(name)
                self.__components[name].stop()
            except Exception as e:
                self.__logger.error("Fail to stop the component [%s]." % name, exc_info=e)

        return self.__process_pool.submit(exec)

    @property
    def components(self):
        return self.__components
