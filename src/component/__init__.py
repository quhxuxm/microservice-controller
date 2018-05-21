#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
from P4 import P4


class ComponentException(Exception):
    pass


class AbstractComponent(metaclass=ABC):

    def __init__(self, globalConfig):
        self.__globalConfig = globalConfig

    def p4fetch(self):
        p4 = P4()
        p4.user = self.__globalConfig.get("p4", "user")
        p4.password = self.__globalConfig.get("p4", "password")
        p4.port = "%s:%s" % (
            self.__globalConfig.get("p4", "host"), self.__globalConfig.get("p4", "post"))
        p4.client = self.__globalConfig[self.name, "p4.client.name"]
        # TODO if not exist create
        try:
            p4.connect()
            p4.run_sync()
        except Exception as e:
            print(e)

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def config(self):
        pass

    @abstractmethod
    def deploy(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass
