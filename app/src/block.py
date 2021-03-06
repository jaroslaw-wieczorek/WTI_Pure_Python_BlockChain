#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:28:34 2018

"""

from interface import implements
from .generics.interfaces import GenericBlock


class Block(implements(GenericBlock)):    
    def __init__(self, blockHeader, blockPayload):

        self.blockHeader = blockHeader
        self.blockPayload = blockPayload
        self.currentHash = None


    def __repr__(self):
        return str(self.__dict__)

