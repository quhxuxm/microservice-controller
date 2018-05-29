#!/usr/bin/python
# -*- coding: utf-8 -*-
from component import AbstractComponent


class Component(AbstractComponent):
    def info(self):
        pass

    def deploy(self):
        pass

    def build(self):
        print("Start to build RGS.")

    def build_config(self):
        print("Start to build RGS.")

    def config(self):
        print("Configuring RGS")

    def start(self):
        print("Starting RGS")

    def stop(self):
        print("Stoping RGS")

    @property
    def name(self):
        return "rgs"
