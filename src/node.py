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


from src.wallet import Wallet
from src.block import Block
from src.transIN import TransIN
from src.transOUT import TransOUT
from src.transaction import Transaction

from src.blockHeader import BlockHeader
from src.blockPayload import BlockPayload

from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 



class Node(implements(GenericNode)):
    #Constant variables:
    #Firsttransaction
    first_transaction = None #TO_DO add the first transaction!
    #Firstblock
    first_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0), BlockPayload(first_transaction))
    
    __key = open("ssh_keys/private", "r").read()     
    #Difficulty:
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

    def calculateHash(self, BlockHeader, BlockPayload): #TO_DO FIX THIS
        h=hashlib.sha256((str(BlockHeader)+''+str(BlockPayload)).encode("utf-8"))
        return h.hexdigest()

    def generateNextBlockHeader(self):          #Creates the NextBlockHeader and fills it with the appropriate values
        previousBlock = self.getLatestBlock()
        difficulty = self.getDifficulty()
        nonce = 0
        nextIndex = previousBlock.index + 1
        nextTimestamp = self.getCurrentTimestamp()
        newBlockHeader = BlockHeader(nextIndex, previousBlock.hash, nextTimestamp, difficulty, nonce)
        return newBlockHeader

    def generateNextBlockPayload(self, transactions): #TO_DO TRANSACTIONS AND PAYLOAD NOT YET IMPLEMENTED
        pass

    def findNextBlock(self,block):    #Proof of work, finding the hash that matches the given difficulty for a block
        while True:
            nonce = 0
            hash = self.calculateHash(block.blockHeader, block.blockPayload)
            if self.hashDifficultyCheck(hash, block.blockHeader.difficulty):
                block.blockHeader.nonce = nonce
                block.currentHash = hash
                return block
            nonce += 1

    def hashDifficultyCheck(self, hash, difficulty): #Checks if the hash when written in binary starts with enough zeroes
        hashinbinary = bin(int(hash, 16))[2:].zfill(len(hash) * 4)
        return hashinbinary.startswith('0'*difficulty)

    def isValidBlockStructure(self, block):         #Checks the Block fields if they contain the right types
        return type(block.blockHeader) is BlockHeader &\
               type(block.blockPayload) is BlockPayload &\
               type(block.blockHeader.index) is int &\
               type(block.blockHeader.previousHash) is str &\
               type(block.blockHeader.timestamp) is float &\
               type(block.blockHeader.difficulty) is int &\
               type(block.blockHeader.nonce) is int &\
               type(block.currentHash) is str &\
               type(block.blockPayload.data) is object

    def isTimestampValid(self, newBlock, previousBlock):    #Checks if the Timestamp is within the specified time
        return previousBlock.blockHeader.timestamp - 60 < newBlock.blockHeader.timestamp &\
                newBlock.blockHeader.timestamp - 60 < self.getCurrentTimestamp()

    def hashMatchesBlockContent(self, block):       #Validation of the block hash
        return self.calculateHash(block.blockHeader, block.blockPayload) == block.currentHash

    def hasValidHash(self, block):          #Checks the if the hash is correctly calculated, including difficulty
        if not self.hashMatchesBlockContent(block):
            print("invalid hash got:"+ block.currentHash)
            return False
        if not self.hashDifficultyCheck(block.currentHash, block.blockHeader.difficulty):
            print("hash difficulty is not valid, should be:"+ block.blockHeader.difficulty + "got" + bin(int(block.currentHash, 16))[2:].zfill(len(block.currentHash) * 4))
            return False
        return True


    def isNewBlockValid(self, newBlock, previousBlock): #Checks the validity of any new block
        if not self.isValidBlockStructure(newBlock):
            print("invalid block structure")
            return False
        if previousBlock.blockHeader.index + 1 != newBlock.blockHeader.index:
            print("invalid index")
            return False
        if previousBlock.currentHash != newBlock.blockHeader.previousHash:
            print("invalid previous hash")
            return False
        if not self.isTimestampValid(newBlock, previousBlock):
            print("invalid timestamp")
        if not self.hasValidHash(newBlock):
            return False
        return True


    def addBlockToChain(self, block):
        if self.isNewBlockValid(block, self.getLatestBlock()):
            pass
        pass #TO_DO missing UnspentTransOut

    def generateRawNextBlock(self,transactions):
        newBlock = self.findNextBlock(Block(self.generateNextBlockHeader(), self.generateNextBlockPayload(transactions)))
        #TO_DO

    def getDifficulty(self):        #Calculates the current difficulty
        latestBlock= self.blockchain[-1]
        if latestBlock.index % self.DIFFICULTY_ADJUSTMENT_INTERVAL == 0 & isinstance(int,latestBlock.index % self.DIFFICULTY_ADJUSTMENT_INTERVAL) & isinstance(int,latestBlock.index) & latestBlock.index != 0:
            return self.getAdjustedDifficulty(latestBlock)
        else:
            return latestBlock.difficulty

    def getAdjustedDifficulty(self, latestBlock):   #Adjusts the difficulty if necessary based on hashrate
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
        h=hashlib.sha256((txInContent+txOutContent).encode("utf-8"))
       # print(h.digest()) 
        print(h.hexdigest())      
        return h.hexdigest() #return string 
    
    
    def signTransIN(self, transaction: Transaction, transInIndex: int, prvivateKey: str, unspentsTransOuts: list):

        
        transIn = transaction.transIN[transInIndex]
        dataToSign = transaction.transID
        
        
        #rsakey = RSA.importKey(key) 
        #signer = PKCS1_v1_5.new(rsakey) 
        #digest = SHA256.new() 
        # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
        #digest.update(b64decode(data)) 
        #sign = signer.sign(digest) 
        #     return b64encode(sign)
        # refUnspentOutTrans = findUnspentOutTrans(transIn.transOutId, trans.transOutIndex, unspentsTransOuts)
        # refAddress = refUnspentOutTrans.address;
        # key =  
        """
        const txIn: TxIn = transaction.txIns[txInIndex];
        const dataToSign = transaction.id;
        const referencedUnspentTxOut: UnspentTxOut = findUnspentTxOut(txIn.txOutId, txIn.txOutIndex, aUnspentTxOuts);
        const referencedAddress = referencedUnspentTxOut.address;
        const key = ec.keyFromPrivate(privateKey, 'hex');
        const signature: string = toHexString(key.sign(dataToSign).toDER());
        return signature;
   
        """
        return str
