#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging


class Singleton:
    """
    The decoration used to make a class as singleton
    """
    __logger = logging.getLogger(__name__+".Singleton")

    def __init__(self, clazz):
        Singleton.__logger.debug("Begin to prepare singleton instance, class = [%s]" % clazz.__name__)
        self.__clazz = clazz
        self.__instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is not None:
            Singleton.__logger.debug(
                "Singleton instance initialized already, return the instance of  [%s] directly." % self.__instance.__class__.__name__)
            return self.__instance
        self.__instance = self.__clazz(*args, **kwargs)
        Singleton.__logger.debug(
            "Singleton instance did not initialized, initialize the instance of  [%s]." % self.__clazz.__name__)
        return self.__instance
