# -*- coding: utf-8 -*-
import __init__ as jsonapi

class JsonapiFault(Exception):
    def __init__(self, msg, api_version=jsonapi.version):
        super(JsonapiFault, self).__init__(msg)
        self.msg         = msg
        self.version     = api_version

def specification_must(msg, condition):
    if not condition:
        raise JsonapiFault(msg)

def specification_must_not(msg, condition):
    if condition:
        raise JsonapiFault(msg)

