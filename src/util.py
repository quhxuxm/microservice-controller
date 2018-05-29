#!/usr/bin/python
# -*- coding: utf-8 -*-


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
