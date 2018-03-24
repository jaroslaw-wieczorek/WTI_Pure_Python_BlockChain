#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""

from interface import implements, Interface


class UI(Interface):
    
    def __init__(self, address):
        pass
    def method(self):
        pass


class Wallet(implements(UI)):
    def __init__(self, address):
        super()
        pass
    
    def method(self):
        print("to działa")
    
    def method_b(self):
        print("to działa")
        

class GenericBlockHeader(Interface):
    def __init__(self, index, previousHash, timestamp, difficulty, nonce):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        
class BlockHeader(implements(GenericBlockHeader)):
    def __init__(self, index, previousHash, timestamp, difficulty, nonce):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        

class GenericBlock(Interface):
    
    def __init__(self, BlockHeader):
          # number, currentHash, previousHash, timestamp, Transaction, difficulty, number
          pass
        
    def method(self, a, b):
        pass
    

class Block(implements(GenericBlock)):
    def __init__(self, BlockHeader):
        pass
    
    def method(self, a, b):
        return "This should work"




class Transaction():
    pass

class TransIN():
    pass

class TransOUT():
    pass

    
h = BlockHeader(0, "dfsfisd", 1318320, 1, 0)

b = Block(h)

print(b.method(4,4))

w = Wallet(48348)
Wallet(23)
