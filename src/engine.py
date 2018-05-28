#!/usr/bin/python
# -*- coding: utf-8 -*-


import importlib
from multiprocessing import Pool

import const
from util import Singleton, ConfigurationHolder


class EngineException(Exception):
    pass


@Singleton
class EngineExecutor:
    def __init__(self, func):
        self.__func = func
        self.__process_pool = Pool(const.ENGINE_EXECUTOR_PROCESS_POOL_SIZE)

    def __call__(self, *args):
        self.__process_pool.map(self.__func, *args)


@Singleton
class Engine:

    def __init__(self):
        self.__initialize_components()

    def __initialize_components(self):
        self.__components = {}
        configuration = ConfigurationHolder(const.GLOBAL_CONFIG_FILE_PATH).configuration
        for name in configuration.sections():
            if not name.startswith(const.COMPONENT_MODULE_PACKAGE_NAME):
                continue
            short_name = name[len(const.COMPONENT_MODULE_PACKAGE_NAME) + 1:]
            component_module = importlib.import_module(name)
            try:
                component_instance = component_module.Component(configuration)
                self.__components[short_name] = component_instance
            except Exception as e:
                print(e)

    def __verify_component(self, name):
        if name not in self.__components:
            raise EngineException("The component [%s] not exist, fail to build." % name)

    @EngineExecutor
    def build(self, name):
        self.__verify_component(name)
        self.__components[name].build()

    @EngineExecutor
    def deploy(self, name):
        self.__verify_component(name)
        self.__components[name].deploy()

    @EngineExecutor
    def config(self, name):
        self.__verify_component(name)
        self.__components[name].config()

    @EngineExecutor
    def start(self, name):
        self.__verify_component(name)
        self.__components[name].start()

    @EngineExecutor
    def stop(self, name):
        self.__verify_component(name)
        self.__components[name].stop()

    @property
    def components(self):
        return self.__components
