#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
from time import sleep

from engine import Engine

logger = logging.getLogger(__name__)


def check_result(component_name, action_name, future_obj, status):
    while future_obj.running():
        logger.info("[%s] is still working on [%s]." % (component_name, action_name))
        sleep(2)
    component_exception = future_obj.exception()
    if component_exception is None:
        logger.info("Success to execute [%s] for [%s]" % (action_name, component_name))
        status["%s:%s" % (component_name, action_name)] = "[SUCCESS]"
    else:
        status["%s:%s" % (component_name, action_name)] = "[FAIL: %s]" % str(component_exception)


if __name__ == "__main__":
    engine = Engine()
    final_status = {}
    for c_name in engine.components.keys():
        fetch_result = engine.p4_fetch(c_name)
        check_result(c_name, "p4_fetch", fetch_result, final_status)
        build_config_result = engine.build_config(c_name)
        check_result(c_name, "build_config", build_config_result, final_status)
        build_result = engine.build(c_name)
        check_result(c_name, "build", build_result, final_status)
    logger.info("#" * 10 + "RESULT:" + "#" * 10)
    logger.info("\n".join(["[%s] = %s" % (key, value) for key, value in final_status.items()]))
