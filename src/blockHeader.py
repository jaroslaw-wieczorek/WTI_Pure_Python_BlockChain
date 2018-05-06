#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:28:38 2018

"""
from interface import implements
from src.generics.interfaces import GenericBlockHeader

                
class BlockHeader(implements(GenericBlockHeader)):
    def __init__(self, index, previousHash, timestamp, difficulty, nonce):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        
    def __repr__(self):
        return str(self.__dict__)
