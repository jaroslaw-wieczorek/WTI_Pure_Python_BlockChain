#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:28:34 2018

@author: afar
"""

from interface import implements
from src.generics.interfaces import GenericBlock


class Block(implements(GenericBlock)):    
    def __init__(self, blockHeader, blockPayload):

        self.blockHeader = blockHeader
        self.blockPayload = blockPayload
        self.currentHash = None


    def __repr__(self):
        return str(self.__dict__)
