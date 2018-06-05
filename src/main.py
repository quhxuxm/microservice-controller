#!/usr/bin/python
# -*- coding: utf-8 -*-


from time import sleep

from engine import Engine


def check_result(component_name, action_name, future_obj, status):
    while future_obj.running():
        print("[%s] is still working on [%s]." % (component_name, action_name))
        sleep(2)
    component_exception = future_obj.exception()
    if component_exception is None:
        print("Success to execute [%s] for [%s]" % (action_name, component_name))
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
    print("\n".join(final_status))
