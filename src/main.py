#!/usr/bin/python
# -*- coding: utf-8 -*-


from engine import Engine

if __name__ == "__main__":
    engine = Engine()
    for c_name in engine.components.keys():
        engine.p4_fetch(c_name)
        result = engine.build(c_name)
        result.get()
