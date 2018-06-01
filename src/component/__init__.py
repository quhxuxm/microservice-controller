#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

from P4 import P4

import const


class ComponentException(Exception):
    pass


def customized(func):
    def exec(*args, **kwargs):
        self = args[0]
        self.customized_action.append(func.__name__)
        func(*args, **kwargs)

    return exec


class DefaultComponent:

    def __init__(self, name, config):
        self.__config = config
        self.__name = name
        self.__customized_action = []

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

    def info(self):
        pass

    def build(self):
        print("Begin to build component [%s]." % self.name)
        build_cmd = "%s %s" % (self.mvn_cmd_path, self.build_cmd)
        build_result = subprocess.run(build_cmd, stdout=sys.stdout, cwd=self.build_dir)
        if build_result and build_result.returncode == 0:
            print("Success to build component [%s]." % self.name)
            return
        print("Fail to build component [%s]." % self.name)

    def build_config_apache(self):
        pass

    def build_config_tomcat(self):
        pass

    def config(self):
        pass

    def deploy_apache(self):
        pass

    def deploy_tomcat(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    @property
    def name(self):
        return self.__name

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

    @property
    def customized_action(self):
        return self.__customized_action


__all__ = [ComponentException, DefaultComponent]
