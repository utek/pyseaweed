# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


class BadFidFormat(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
