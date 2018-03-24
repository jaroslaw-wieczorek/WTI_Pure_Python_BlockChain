#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""
import datetime
from datetime import timezone
from interface import implements, Interface
import hashlib

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
        
    def __repr__(self):
        return str(self.__dict__)


class GenericBlockPayload(Interface):
    def __init__(self, data):
        pass


class BlockPayload(implements(GenericBlockPayload)):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.__dict__)


class GenericBlock(Interface):
    
    def __init__(self, blockHeader, blockPayload):
        self.blockHeader = blockHeader
        self.blockPayload = blockPayload
        self.currentHash = None

       # number, currentHash, previousHash, timestamp, Transaction, difficulty, number

    def __repr__(self):
        return str(self.__dict__)

    

class Block(implements(GenericBlock)):
    
    def __init__(self, blockHeader, blockPayload):

        self.blockHeader = blockHeader
        self.blockPayload = blockPayload
        self.currentHash = None


    def __repr__(self):
        return str(self.__dict__)




class GenericTransaction(Interface):
    def __init__(self, transID, transIN, transOUT):
        pass


class Transaction(implements(GenericTransaction)):
    def __init__(self, transID, transIN, transOUT):
        self.transID = transID
        self.transIN = transIN
        self.transOUT = transOUT
        
    def __repr__(self):
        return str(self.__dict__)


class TransIN():
    def __init__(self, transOutId,  transOutIndex, signature):
        self.transOutId = transOutId
        self.transOutIndex = transOutIndex
        self.signature = signature

    def __repr__(self):
        return str(self.__dict__)

class TransOUT():
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def __repr__(self):
        return str(self.__dict__)


class Node(implements(GenericNode)):
    #Constant variables:
    #Firsttransaction
    first_transaction = None #TO_DO add the first transaction!
    #Firstblock
    first_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0), BlockPayload(first_transaction))

    #Diff:
    #in seconds
    BLOCK_GENERATION_INTERVAL = 10;
    #in blocks
    DIFFICULTY_ADJUSTMENT_INTERVAL = 10;

    def __init__(self):
        self.blockchain = [self.first_block]

    def getBlockchain(self):
        return self.blockchain

    def getCurrentTimestamp(self):
        return datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
    def getLatestBlock(self):
        return self.blockchain[-1]

    def calculateHash(self, BlockHeader, BlockPayload):
        h = hashlib.new('sha256')
        h.update(str({BlockHeader, BlockPayload}).encode("utf-8"))
        return h.hexdigest()

    def generateNextBlockHeader(self):
        previousBlock = self.getLatestBlock()
        nextIndex = previousBlock.index + 1
        nextTimestamp = self.getCurrentTimestamp()
        newBlockHeader = BlockHeader(nextIndex, previousBlock.hash, nextTimestamp, "diff", "nonce",); #TO_DO add difficulty and nonce magic!
        return newBlockHeader


    def getDifficulty(self, aBlockchain):
        latestBlock= aBlockchain[self.blockchain.length - 1]
        if latestBlock.index % self.DIFFICULTY_ADJUSTMENT_INTERVAL == 0 & isinstance(int,latestBlock.index % self.DIFFICULTY_ADJUSTMENT_INTERVAL) & isinstance(int,latestBlock.index) & latestBlock.index != 0:
            return self.getAdjustedDifficulty(latestBlock, aBlockchain)
        else:
            return latestBlock.difficulty

    def getAdjustedDifficulty(self, latestBlock, aBlockchain):
            prevAdjustmentBlock = aBlockchain[self.blockchain.length - self.DIFFICULTY_ADJUSTMENT_INTERVAL]
            timeExpected = self.BLOCK_GENERATION_INTERVAL * self.DIFFICULTY_ADJUSTMENT_INTERVAL
            timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp
            if timeTaken < timeExpected / 2:
                return prevAdjustmentBlock.difficulty + 1
            elif timeTaken > timeExpected * 2:
                return prevAdjustmentBlock.difficulty - 1
            else:
                return prevAdjustmentBlock.difficulty;


# Tests

txIN = TransIN(1,2,"signaure")
txOUT = TransOUT("ADRES_WALLETA",50)

t = Transaction(1, txIN, txOUT)
print(t)

p = BlockPayload(t)

h = BlockHeader(0, "dfsfisd", 1318320, 1, 0)

b = Block(h,p)

n = Node()
print(n.calculateHash(h,p))

w = Wallet(48348)
Wallet(23)
