#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:27:18 2018

@author: afar
"""

import datetime
from datetime import timezone
import hashlib

from interface import implements 
from src.generics.interfaces import GenericNode

from src.block import Block
from src.transIN import TransIN
from src.transOUT import TransOUT
from src.transaction import Transaction

from src.blockHeader import BlockHeader
from src.blockPayload import BlockPayload




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

        h.update(bin(str(BlockHeader)+''+str(BlockPayload)).encode("utf-8"))
        return h.hexdigest()

    def generateNextBlockHeader(self):
        previousBlock = self.getLatestBlock()
        difficulty = self.getDifficulty()
        nonce = 0
        nextIndex = previousBlock.index + 1
        nextTimestamp = self.getCurrentTimestamp()
        newBlockHeader = BlockHeader(nextIndex, previousBlock.hash, nextTimestamp, difficulty, nonce)
        return newBlockHeader

    def generateNextBlockPayload(self, transactions): #TO_DO TRANSACTIONS AND PAYLOAD NOT YET IMPLEMENTED
        pass

    def findNextBlock(self,block):
        while True:
            nonce = 0
            hash = self.calculateHash(block.blockHeader, block.blockPayload)
            if self.hashDifficultyCheck(hash, block.blockHeader.difficulty):
                block.blockHeader.nonce = nonce
                block.currentHash = hash
                return block
            nonce += 1

    def hashDifficultyCheck(self, hash, difficulty):
        hashinbinary = bin(int(hash, 16))[2:].zfill(len(hash) * 4)
        return hashinbinary.startswith('0'*difficulty)

    def isValidBlockStructure(self, block):
        return type(block.blockHeader) is BlockHeader &\
               type(block.blockPayload) is BlockPayload &\
               type(block.blockHeader.index) is int &\
               type(block.blockHeader.previousHash) is str &\
               type(block.blockHeader.timestamp) is float &\
               type(block.blockHeader.difficulty) is int &\
               type(block.blockHeader.nonce) is int &\
               type(block.currentHash) is str &\
               type(block.blockPayload.data) is object

    def isBlockValid(self, newBlock, previousBlock):
        pass #TO_DO

    def addBlockToChain(self, block):
        pass #TO_DO

    def generateRawNextBlock(self,transactions):
        newBlock = self.findNextBlock(Block(self.generateNextBlockHeader(), self.generateNextBlockPayload(transactions)))
        #TO_DO

    def getDifficulty(self):
        latestBlock= self.blockchain[-1]
        if latestBlock.index % self.DIFFICULTY_ADJUSTMENT_INTERVAL == 0 & isinstance(int,latestBlock.index % self.DIFFICULTY_ADJUSTMENT_INTERVAL) & isinstance(int,latestBlock.index) & latestBlock.index != 0:
            return self.getAdjustedDifficulty(latestBlock)
        else:
            return latestBlock.difficulty

    def getAdjustedDifficulty(self, latestBlock):
        prevAdjustmentBlock = self.blockchain[len(self.blockchain) - self.DIFFICULTY_ADJUSTMENT_INTERVAL]
        timeExpected = self.BLOCK_GENERATION_INTERVAL * self.DIFFICULTY_ADJUSTMENT_INTERVAL
        timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp
        if timeTaken < timeExpected / 2:
            return prevAdjustmentBlock.difficulty + 1
        elif timeTaken > timeExpected * 2:
            return prevAdjustmentBlock.difficulty - 1
        else:
            return prevAdjustmentBlock.difficulty

    
    def concIN(self, x):
        return str(x.transOutId) + '' +str(x.transOutIndex)
    
    def concOUT(self, x):
        return str(x.address) + '' +str(x.amount)
    
    def getTransactionId(self, transactions: Transaction) -> str:
        txInContent = ""
        for x in transactions.transIN:
            txInContent += self.concIN(x)
         
        txOutContent = ""
        for x in transactions.transOUT:
            txOutContent += self.concOUT(x)
        
        print(hashlib.sha256((txInContent+txOutContent).encode("utf-8")).digest())      
        return