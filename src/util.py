#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser


class Singleton:
    """
    The decoration used to make a class as singleton
    """
    instances = {}

    def __init__(self, clazz):
        self.__clazz = clazz

    def __call__(self, *args, **kwargs):
        if self.__clazz in Singleton.instances:
            return Singleton.instances[self.__clazz]
        instance = self.__clazz(*args, **kwargs)
        Singleton.instances[self.__clazz] = instance
        return instance


@Singleton
class ConfigurationHolder:
    """
    The configuration file holder
    """

    def __init__(self, path):
        self.__config = ConfigParser()
        self.__config.read(path)

    @property
    def configuration(self):
        return self.__config


__all__ = [Singleton, ConfigurationHolder]
