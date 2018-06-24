#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys
from configparser import ConfigParser, NoOptionError
from zipfile import ZipFile

from P4 import P4, P4Exception

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
    __logger = logging.getLogger(__name__)

    def __init__(self, name, config):
        self.__config = config
        self.__name = name
        self.__customized_action = []
        self.__tokens = {}
        self.__init_tokens()

    def __init_tokens(self):
        if self.__get_component_config_value("token.file") is None:
            return
        token_resource_dir_path = os.path.join(self.resources_dir_path, self.__config.get("core", "resources.token"))
        token_resource_file_path = os.path.join(token_resource_dir_path,
                                                self.__get_component_config_value("token.file"))
        token_file_config_parser = ConfigParser()
        token_file_config_parser.read(token_resource_file_path)
        for k, v in token_file_config_parser.items("DEFAULT"):
            self.__tokens[k] = v

    def p4_fetch(self):
        p4 = P4()
        p4.exception_level = 1
        p4.user = self.p4user
        p4.password = self.p4password
        p4.port = self.p4port
        p4.client = self.p4client
        # TODO if not exist create
        try:
            DefaultComponent.__logger.info("Begin to sync component [%s] from p4 client [%s]" % (self.name, p4.client))
            p4.connect()
            p4.run_sync()
        except P4Exception:
            for e in p4.errors:
                DefaultComponent.__logger.error("Fail to sync component [%s] code." % self.name, e)

    def info(self):
        pass

    def build(self):
        DefaultComponent.__logger.info("Begin to build component [%s]." % self.name)
        build_cmd = "%s %s" % (self.mvn_cmd_path, self.build_cmd)
        build_result = subprocess.run(build_cmd, stdout=sys.stdout, cwd=self.build_dir_path)
        if build_result and build_result.returncode == 0:
            DefaultComponent.__logger.info("Success to build component [%s]." % self.name)
            return
        DefaultComponent.__logger.info("Fail to build component [%s]." % self.name)

    def deploy_apache(self):
        DefaultComponent.__extract_zip(self.apache_zip_path, self.apache_deploy_path)

    def deploy_tomcat(self):
        DefaultComponent.__extract_zip(self.tomcat_zip_path, self.tomcat_deploy_path)

    @staticmethod
    def __extract_zip(resource_path, target_path):
        logging.info("Begin to extract apache to [%s]" % str(target_path))
        resource_zip_file = ZipFile(resource_path)
        resource_zip_file.extractall(target_path)
        logging.info("Success to extract apache to [%s]" % str(target_path))
        return

    def deploy(self):
        self.__extract_zip(self.build_result_path, self.deploy_target_path)
        self._replace_token()

    def config(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def _replace_token(self):
        for dir_root_path, sub_dir_names, file_names in os.walk(self.deploy_target_path):
            if not file_names:
                continue
            for file_name in file_names:
                if file_name.endswith(".tmpl"):
                    output_file_name = file_name[0: file_name.find(".tmpl")]
                    tmpl_file_absolute_path = os.path.join(dir_root_path, file_name)
                    output_file_absolute_path = os.path.join(dir_root_path, output_file_name)
                    with open(tmpl_file_absolute_path, "r") as tmpl_file:
                        with open(output_file_absolute_path, "w") as output_file:
                            for line in tmpl_file:
                                replaced_line = line
                                for k, v in self.tokens.items():
                                    replaced_line = replaced_line.replace("@" + k.upper() + "@", v)
                                output_file.write(replaced_line)

    def __get_component_config_value(self, key):
        section_name = "%s.%s" % (const.COMPONENT_MODULE_PACKAGE_NAME, self.name)
        if not self.__config.has_section(section_name):
            return None
        try:
            return self.__config.get(section_name, key)
        except NoOptionError:
            return None

    @property
    def p4user(self):
        return self.__config.get("p4", "user")

    @property
    def p4password(self):
        return self.__config.get("p4", "password")

    @property
    def p4port(self):
        return "%s:%s" % (
            self.__config.get("p4", "host"), self.__config.get("p4", "port"))

    @property
    def p4client(self):
        return self.__get_component_config_value("p4.client.name")

    @property
    def name(self):
        return self.__name

    @property
    def code_base_dir_path(self):
        return os.path.join(os.path.abspath(self.__config.get("p4", "workspace.root.path")),
                            self.__get_component_config_value("p4.client.name"))

    @property
    def resources_dir_path(self):
        return os.path.abspath("resources")

    @property
    def tomcat_zip_path(self):
        tomcat_zip_file_path = os.path.join(self.resources_dir_path, self.__config.get("core", "resources.tomcat"))
        return tomcat_zip_file_path

    @property
    def tomcat_deploy_path(self):
        tomcat_deploy_path = os.path.join(self.__config.get("core", "deploy.target.dir.root"),
                                          self.__config.get("core", "deploy.target.dir.relative.tomcat"))
        return tomcat_deploy_path

    @property
    def apache_zip_path(self):
        apache_zip_file_path = os.path.join(self.resources_dir_path, self.__config.get("core", "resources.apache"))
        return apache_zip_file_path

    @property
    def apache_deploy_path(self):
        apache_deploy_path = os.path.join(self.__config.get("core", "deploy.target.dir.root"),
                                          self.__config.get("core", "deploy.target.dir.relative.apache"))
        return apache_deploy_path

    @property
    def build_dir_path(self):
        return os.path.join(self.code_base_dir_path, self.__get_component_config_value("build.dir"))

    @property
    def build_result_path(self):
        return os.path.join(self.code_base_dir_path, self.__get_component_config_value("build.result"))

    @property
    def deploy_target_root_dir_path(self):
        return os.path.abspath(self.__config.get("core", "deploy.target.dir.root"))

    @property
    def deploy_target_root_components_dir_path(self):
        return os.path.join(self.deploy_target_root_dir_path,
                            self.__config.get("core", "deploy.target.dir.relative.components"))

    @property
    def mvn_cmd_path(self):
        return os.path.abspath(self.__config.get("core", "maven.path"))

    @property
    def build_cmd(self):
        return self.__get_component_config_value("build.cmd")

    @property
    def deploy_target_path(self):
        deploy_relative_path = self.__get_component_config_value(
            "deploy.target.dir")
        if deploy_relative_path is None:
            deploy_relative_path = self.name
        deploy_path = os.path.join(self.deploy_target_root_components_dir_path,
                                   deploy_relative_path)
        return deploy_path

    @property
    def customized_action(self):
        return self.__customized_action

    @property
    def tokens(self):
        return self.__tokens


__all__ = [ComponentException, DefaultComponent]
