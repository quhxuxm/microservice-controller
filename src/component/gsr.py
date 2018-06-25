#!/usr/bin/python
# -*- coding: utf-8 -*-
from component import DefaultComponent


class Component(DefaultComponent):
    def info(self):
        pass

    def config(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def deploy(self):
        super().deploy()
