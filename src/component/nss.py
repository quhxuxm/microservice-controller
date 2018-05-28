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
        return "nss"

    def build(self):
        pass

    def config(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
