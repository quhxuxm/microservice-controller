#!/usr/bin/python
# -*- coding: utf-8 -*-
from src.component import AbstractComponent


class Component(AbstractComponent):
    def info(self):
        pass

    def deploy(self):
        pass

    @property
    def name(self):
        return "cfgs"

    def build(self):
        pass

    def build_config(self):
        pass

    def config(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
