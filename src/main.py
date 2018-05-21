#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from engine import Engine

if __name__ == "__main__":
    configFilePath = os.path.join(os.path.curdir, "microservice-controller.config")
    engine = Engine(configFilePath)
    engine.build()
