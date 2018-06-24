# -*- coding: utf-8 -*-
import logging
from cmd import Cmd

from engine import Engine

logger = logging.getLogger(__name__)


class MainEntry(Cmd):
    prompt = ">>"

    def __init__(self):
        super().__init__()
        self.__final_status = {}

    def __check_result(self, component_name, action_name, future_obj):
        component_exception = future_obj.exception()
        if component_exception is None:
            logger.info("Success to execute [%s] for [%s]" % (action_name, component_name))
            self.__final_status["%s:%s" % (component_name, action_name)] = "[SUCCESS]"
        else:
            self.__final_status["%s:%s" % (component_name, action_name)] = "[FAIL: %s]" % str(component_exception)

    def do_web(self, arg):
        print("Starting the web entry")

    def do_p4fetch(self, component_name):
        action_name = self.do_p4fetch.__name__
        engine = Engine()
        if component_name is not None and len(component_name.strip()) > 0:
            logger.info("Fetch P4 source code for component [%s]" % component_name)
            build_result = engine.p4_fetch(component_name)
            self.__check_result(component_name, self.do_p4fetch.__name__, build_result)
            self.__print_final_status()
            return
        for c_name in engine.components.keys():
            logger.info("Fetch P4 source code for component [%s]" % c_name)
            build_result = engine.p4_fetch(c_name)
            self.__check_result(c_name, action_name, build_result)
        self.__print_final_status()

    def do_build(self, component_name):
        action_name = self.do_build.__name__
        engine = Engine()
        if component_name is not None and len(component_name.strip()) > 0:
            logger.info("Build source code for component [%s]" % component_name)
            build_result = engine.build(component_name)
            self.__check_result(component_name, action_name, build_result)
            self.__print_final_status()
            return
        for c_name in engine.components.keys():
            logger.info("Build source code for component [%s]" % c_name)
            build_result = engine.build(c_name)
            self.__check_result(c_name, action_name, build_result)
        self.__print_final_status()

    def do_deploy(self, component_name):
        action_name = self.do_deploy.__name__
        engine = Engine()
        if component_name is not None and len(component_name.strip()) > 0:
            logger.info("Build source code for component [%s]" % component_name)
            build_result = engine.deploy(component_name)
            self.__check_result(component_name, action_name, build_result)
            self.__print_final_status()
            return
        for c_name in engine.components.keys():
            logger.info("Build source code for component [%s]" % c_name)
            build_result = engine.deploy(c_name)
            self.__check_result(c_name, action_name, build_result)
        self.__print_final_status()

    def __print_final_status(self):
        logger.info("\n".join(["[%s] = %s" % (key, value) for key, value in self.final_status.items()]))

    @property
    def final_status(self):
        return self.__final_status
