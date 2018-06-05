#!/usr/bin/python
# -*- coding: utf-8 -*-


from engine import Engine
import  cmd
class CmdEntry(cmd.Cmd):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    engine = Engine()
    for c_name in engine.components.keys():
        fetch_result = engine.p4_fetch(c_name)
        build_config_result = engine.build_config(c_name)
        build_result = engine.build(c_name)
        fetch_result.get()
        build_result.get()
