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


class GenericNode(Interface):
    def __init__(self):
        pass


class Node(implements(GenericNode)):
    first_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0), BlockPayload(None))
    def __init__(self):
        self.blockchain = [self.first_block]




class GenericBlockHeader(Interface):
    def __init__(self, index, previousHash, timestamp, difficulty, nonce):
        pass
    
        
        
class BlockHeader(implements(GenericBlockHeader)):
    def __init__(self, index, previousHash, timestamp, difficulty, nonce):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        
        
class GenericBlockPayload(Interface):
    def __init__(self, data):
        pass


class BlockPayload(implements(GenericBlockPayload)):
    def __init__(self, data):
        self.data = data
        
        
        

class GenericBlock(Interface):
    
    def __init__(self, BlockHeader, BlockPayload):
        
          # number, currentHash, previousHash, timestamp, Transaction, difficulty, number
          pass
        
    def method(self, a, b):
        pass
    

class Block(implements(GenericBlock)):
    def __init__(self, BlockHeader, BlockPayload):
        pass
    
    def method(self, a, b):
        return "This should work"


class GenericTransaction(Interface):
    def __init__(self, transID, transIN, transOUT):
        pass


class Transaction(implements(GenericTransaction)):
    def __init__(self, transID, transIN, transOUT):
        self.transID = transID
        self.transIN = transIN
        self.transOUT = transOUT
        

class TransIN():
    def __init__(self):
        pass

class TransOUT():
    def __init__(self):
 
        pass

    
t = Transaction(1,None,None)

p = BlockPayload(t)


h = BlockHeader(0, "dfsfisd", 1318320, 1, 0)

b = Block(h,p)

print(b.method(4,4))

w = Wallet(48348)
Wallet(23)
