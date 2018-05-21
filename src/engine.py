#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser

from src.component import ComponentException


class EngineException(Exception):
    pass


class Engine:
    def __init__(self, configFilePath):
        self.__config = ConfigParser()
        self.__configFilePath = configFilePath
        self.__config.read(configFilePath, encoding="UTF-8")
        self.__components = {}
        for name in self.__config.sections():
            componentClass = __import__("component.%s.Component" % name)
            componentInstance = componentClass()
            self.__components[name] = componentInstance

    def __component(self, func):
        def execute(*args, **kargs):
            name = args[1]
            if not self.__config.has_section("component.%s" % name):
                raise EngineException("The component [%s] not configured in the configuration file [%s]" % (
                    name, self.__configFilePath))
            if self.__components.get(name) is None:
                raise EngineException("The component [%s] not exist, fail to build." % name)
            try:
                func(*args, **kargs)
            except ComponentException as e:
                print("Fail to execute [%s] on component [%s] because of exception [%s]." % (
                    func.__name__, name, str(e)))

        return execute

    @__component
    def build(self, name):
        self.__components[name].build()

    @__component
    def deploy(self, name):
        self.__components[name].deploy()

    @__component
    def config(self, name):
        self.__components[name].config()

    @__component
    def start(self, name):
        self.__components[name].start()

    @__component
    def stop(self, name):
        self.__components[name].stop()

    @property
    def components(self):
        return self.__components
