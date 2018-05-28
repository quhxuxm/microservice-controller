#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser


class Singleton:
    """
    The decoration used to make a class as singleton
    """

    def __init__(self, clazz):
        self.__clazz = clazz
        self.__instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is not None:
            return self.__instance
        self.__instance = self.__clazz(*args, **kwargs)
        return self.__instance


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
