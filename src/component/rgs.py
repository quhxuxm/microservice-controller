#!/usr/bin/python
# -*- coding: utf-8 -*-
from component import DefaultComponent


class Component(DefaultComponent):
    def info(self):
        pass

    def deploy(self):
        super().deploy()

    def build_config(self):
        print("Start to build RGS.")

    def config(self):
        print("Configuring RGS")

    def start(self):
        print("Starting RGS")

    def stop(self):
        print("Stoping RGS")
