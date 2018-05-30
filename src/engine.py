#!/usr/bin/python
# -*- coding: utf-8 -*-


import importlib
from configparser import ConfigParser
from multiprocessing.pool import ThreadPool

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
        self.__initialize_pool()
        self.__initialize_components()

    def __initialize_pool(self):
        self.__process_pool = ThreadPool(const.ENGINE_EXECUTOR_PROCESS_POOL_SIZE)

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
                print(e)
            if component_instance is not None:
                print("Success to find component module [%s]." % name)
                self.__components[short_name] = component_instance
            else:
                print("Can not find component module [%s], the processo will use default one." % name)
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
                print(e)

        return self.__process_pool.apply_async(exec, [])

    def build(self, name):
        def exec():
            try:
                self.__verify_component(name)
                self.__components[name].build()
            except Exception as e:
                print(e)

        return self.__process_pool.apply_async(exec, [])

    def deploy(self, name):
        def exec():
            self.__verify_component(name)
            self.__components[name].deploy()

        return self.__process_pool.apply_async(exec, [])

    def build_config(self, name):
        def exec():
            self.__verify_component(name)
            self.__components[name].build_config()

        return self.__process_pool.apply_async(exec, [])

    def start(self, name):
        def exec():
            self.__verify_component(name)
            self.__components[name].start()

        return self.__process_pool.apply_async(exec, [])

    def stop(self, name):
        def exec():
            self.__verify_component(name)
            self.__components[name].stop()

        return self.__process_pool.apply_async(exec, [])

    @property
    def components(self):
        return self.__components
