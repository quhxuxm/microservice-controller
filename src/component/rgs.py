#!/usr/bin/python
# -*- coding: utf-8 -*-
from src.component import AbstractComponent


class Component(AbstractComponent):
    def build(self):
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
