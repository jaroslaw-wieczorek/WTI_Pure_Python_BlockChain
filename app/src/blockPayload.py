#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:28:44 2018

"""


from interface import implements
from .generics.interfaces import GenericBlockPayload


class BlockPayload(implements(GenericBlockPayload)):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.__dict__)
