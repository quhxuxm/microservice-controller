#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from abc import ABC
from abc import abstractmethod

from P4 import P4

import const


class ComponentException(Exception):
    pass


class AbstractComponent(ABC):

    def __init__(self, config):
        self.__config = config

    def p4_fetch(self):
        p4 = P4()
        p4.user = self.__config.get("p4", "user")
        p4.password = self.__config.get("p4", "password")
        p4.port = "%s:%s" % (
            self.__config.get("p4", "host"), self.__config.get("p4", "port"))
        p4.client = self.__config.get("%s.%s" % (const.COMPONENT_MODULE_PACKAGE_NAME, self.name), "p4.client.name")
        # TODO if not exist create
        try:
            print("Begin to sync component [%s] from p4 client [%s]" % (self.name, p4.client))
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
    def build_config(self):
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

    def __get_component_config_value(self, key):
        return self.__config.get("%s.%s" % (const.COMPONENT_MODULE_PACKAGE_NAME, self.name), key)

    @property
    def code_base_dir_path(self):
        return os.path.join(os.path.abspath(self.__config.get("p4", "workspace.root.path")),
                            self.__get_component_config_value("p4.client.name"))

    @property
    def build_dir(self):
        return os.path.join(self.code_base_dir_path, self.__get_component_config_value("build.dir"))

    @property
    def mvn_cmd_path(self):
        return self.__config.get("core", "maven.path")

    @property
    def build_cmd(self):
        return self.__get_component_config_value("build.cmd")


__all__ = [ComponentException, AbstractComponent]
