# -*- coding: utf-8 -*-
from cmd import Cmd


class CmdLineEntry(Cmd):
    def __init__(self):
        super().__init__()

    def do_help(self, arg):
        pass

    def do_build(self, *args):
        pass

    def do_deploy(self, *args):
        pass

class WebEntry:
    pass