#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar 24 18:27:18 2018

"""
import sys
import datetime
from datetime import timezone
import hashlib
from functools import reduce

import os
from interface import implements
from copy import deepcopy


from .generics.interfaces import GenericNode
from .wallet import Wallet
from .block import Block
from .transIN import TransIN
from .transOUT import TransOUT
from .utilities import Utilities
from .transaction import Transaction
from .unspentOutTrans import UnspentOutTrans
from .transactionMethods import TransMethods
from .transactionPool import TransactionPool
from .blockHeader import BlockHeader
from .blockPayload import BlockPayload
from .wallet import Wallet
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from base64 import b64encode, b64decode



class Node(implements(GenericNode),TransMethods):
    '''
    '''
    #Difficulty:
    #in seconds
    BLOCK_GENERATION_INTERVAL = 10
    #in blocks
    DIFFICULTY_ADJUSTMENT_INTERVAL = 10
    #How much do you get for finding a block
    COINBASE_AMOUNT = 50
    pubfirst_path = os.path.abspath(os.path.join(__file__, '..', '..', 'rsa_keys/FirstPUB.pub'))

    def __init__(self, wallet, transpool):
        self.wallet = wallet
        self.transpoll = transpool
        self.__firstpublicFileKey = open(self.pubfirst_path, "r").read()
        self.__firstpublicKey = RSA.importKey(self.__firstpublicFileKey)

        self.first_transaction = self.getCoinbaseTransaction(self.__firstpublicKey.exportKey(),
                                                             0)
        self.first_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0),
                                 BlockPayload([self.first_transaction]))
        self.first_block.currentHash = self.calculateHash(self.first_block.blockHeader, self.first_block.blockPayload)
        self.blockchain = [self.first_block]
        self.unspentTransOuts = self.processTransactions(self.blockchain[0].blockPayload.data, [], 0)

    def getBlockchain(self):
        """Returns the whole blockchain."""
        return self.blockchain

    def getCurrentTimestamp(self):
        """Gets the current timestamp in a proper POSIX format (double)."""
        return datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()

    def getLatestBlock(self):
        """Gets the last block from the Blockchain."""
        return self.blockchain[-1]

    def getUnspentTransOuts(self):
        """Returns a deepcopy of the unspent Transaction Outs."""
        return deepcopy(self.unspentTransOuts)

    def setUnspentTransOuts(self, newUnspentTransOuts):
        """Replaces unspentTransOuts and prints that it happened."""
        print("Replacing UnspentTransOuts with new ones.")
        self.unspentTransOuts = newUnspentTransOuts

    def calculateHash(self, BlockHeader, BlockPayload): #TODO VERIFY the consistency of hash generation
        """Calculates the hash for the supplied BlockHeader and BlockPayload."""
        h=hashlib.sha256((str(BlockHeader)+''+str(BlockPayload)).encode("utf-8"))
        return h.hexdigest()

    def generateNextBlockHeader(self):
        """Creates the NextBlockHeader based on the current chain and fills it with the appropriate values."""
        previousBlock = self.getLatestBlock()
        difficulty = self.getDifficulty()
        nonce = 0
        nextIndex = previousBlock.blockHeader.index + 1
        nextTimestamp = self.getCurrentTimestamp()
        newBlockHeader = BlockHeader(nextIndex, previousBlock.currentHash, nextTimestamp, difficulty, nonce)
        return newBlockHeader

    def generateNextBlockPayload(self, transactions):
        """Creates a BlockPayload filled with supplied transactions."""
        return BlockPayload(transactions)

    def generateNextBlockWithTransaction(self, receiverAddress, ammountToSend):
        """Creates a new block for the purpose of including a new transaction.
        This method generates the coinbase transaction and the outgoing transaction
         and calls generateRawNextBlock to add the transactions to the blockchain."""
        if not self.isValidAddress(receiverAddress):
            print("Receivers address is not valid. We do not support interdimensional transactions.")
        if not isinstance(ammountToSend, float):
            print("ammountToSend is not a float. That is not how numbers work.")
        coinbaseTrans = self.getCoinbaseTransaction(self.wallet.getPublicFromWallet(), self.getLatestBlock().index + 1)
        transaction = self.wallet.createTransaction(receiverAddress, ammountToSend, self.wallet.getPrivateFromWallet(),
                                               self.getUnspentTxOuts(), self.transpoll.getTransactionPool())
        transactionList = [coinbaseTrans, transaction]
        return self.generateRawNextBlock(transactionList)


    def findNextBlock(self, block):
        """Proof of work, finds the hash that matches the given difficulty for a block."""
        while True:
            nonce = 0
            hash = self.calculateHash(block.blockHeader, block.blockPayload)
            if self.hashDifficultyCheck(hash, block.blockHeader.difficulty):
                block.blockHeader.nonce = nonce
                block.currentHash = hash
                return block
            nonce += 1

    def hashDifficultyCheck(self, hash, difficulty):
        """Checks if the hash when written in binary starts with enough zeroes."""
        hashinbinary = bin(int(hash, 16))[2:].zfill(len(hash) * 4)
        return hashinbinary.startswith('0'*difficulty)

    def isValidBlockStructure(self, block):
        """Checks the Block fields if they contain the right types."""
        return isinstance(block.blockHeader,BlockHeader) & \
               isinstance(block.blockPayload, BlockPayload) & \
               isinstance(block.blockHeader.index, int) & \
               isinstance(block.blockHeader.previousHash, str) & \
               isinstance(block.blockHeader.timestamp, float) & \
               isinstance(block.blockHeader.difficulty, int) & \
               isinstance(block.blockHeader.nonce, int) & \
               isinstance(block.currentHash, str) & \
               isinstance(block.blockPayload.data, object)

    def isTimestampValid(self, newBlock, previousBlock):
        """Checks if the Timestamp is within the specified time"""
        return previousBlock.blockHeader.timestamp - 60 < newBlock.blockHeader.timestamp and\
                newBlock.blockHeader.timestamp - 60 < self.getCurrentTimestamp()

    def hashMatchesBlockContent(self, block):
        """Validation of the block hash."""
        return self.calculateHash(block.blockHeader, block.blockPayload) == block.currentHash

    def hasValidHash(self, block):
        """Checks the if the hash is correctly calculated, including difficulty."""
        if not self.hashMatchesBlockContent(block):
            print("invalid hash got:"+ block.currentHash)
            return False
        if not self.hashDifficultyCheck(block.currentHash, block.blockHeader.difficulty):
            print("hash difficulty is not valid, should be:"+ block.blockHeader.difficulty + "got" + bin(int(block.currentHash, 16))[2:].zfill(len(block.currentHash) * 4))
            return False
        return True

    def isNewBlockValid(self, newBlock, previousBlock):
        """Checks the validity of any new block."""
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
            print("invalid hash")
            return False
        return True

    def addBlockToChain(self, newBlock):
        """Attempts to add a supplied block to the chain. Checks the necessary requirements, processes transactions, sets UnspentTXOuts and updates the Pool."""
        if self.isNewBlockValid(newBlock, self.getLatestBlock()):
            unspentOuts = self.processTransactions(newBlock.blockPayload.data, self.getUnspentTransOuts(), newBlock.blockHeader.index)
            if  unspentOuts == None:
                print("Block transactions are not valid.")
                return False
            else:
                self.blockchain.append(newBlock)
                self.setUnspentTransOuts(unspentOuts)
                self.transpoll.updateTransactionPool(self.unspentTransOuts)
                return True
        return False

    def generateRawNextBlock(self, transactions):
        """Creates the block, fills it with supplied transactions and attempts to add it to the chain and broadcast the success."""
        newBlock = self.findNextBlock(Block(self.generateNextBlockHeader(), self.generateNextBlockPayload(transactions)))
        if self.addBlockToChain(newBlock):
            #self.broadcastLatest() #TODO not implemented
            return newBlock
        else:
            return None

    def getDifficulty(self):
        """Calculates the current difficulty."""
        latestBlock = self.blockchain[-1]
        if len(self.blockchain) - 1 % self.DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and len(self.blockchain) - 1 != 0:
            return self.getAdjustedDifficulty(latestBlock)
        else:
            return latestBlock.blockHeader.difficulty

    def getAdjustedDifficulty(self, latestBlock):
        """Adjusts the difficulty if necessary based on the hashrate calculated from previous blocks."""
        prevAdjustmentBlock = self.blockchain[len(self.blockchain) - self.DIFFICULTY_ADJUSTMENT_INTERVAL]
        timeExpected = self.BLOCK_GENERATION_INTERVAL * self.DIFFICULTY_ADJUSTMENT_INTERVAL
        timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp
        if timeTaken < timeExpected / 2:
            return prevAdjustmentBlock.difficulty + 1
        elif timeTaken > timeExpected * 2:
            return prevAdjustmentBlock.difficulty - 1
        else:
            return prevAdjustmentBlock.difficulty

    def getSumDifficulty(self, aBlockchain):
        """Calculates the sum difficulty of a given chain."""
        return reduce((lambda x, y: x + y), list(map(lambda block: 2**block.blockHeader.difficulty, aBlockchain)))

    def generateNextBlock(self):
        """Creates a Coinbase transaction then adds the transactions awaiting in the Transaction Pool, lastly it uses generateRawNextBlock to create the actual block."""
        coinbaseTrans = self.getCoinbaseTransaction(self.wallet.getPublicFromWallet(), len(self.getBlockchain()))
        blockData = [coinbaseTrans] + self.transpoll.getTransactionPool()
        return self.generateRawNextBlock(blockData)

    def validateBlockChain(self, blockchaintovalidate: []) -> []:
        """Checks the validity of a given blockchain, return unspent transOuts if it is valid."""
        if not str(blockchaintovalidate[0]) == str(self.first_block):
            print("This is not even the correct blockchain are you even trying?")
            return None
        #Block is valid if the structure is valid and the transactions are valid.
        aUnspentTransOuts = []
        for previousBlock, currentBlock, nxtBlock in Utilities.previous_and_next(blockchaintovalidate):
            if not previousBlock == None and not self.isNewBlockValid(currentBlock, previousBlock):
                return None

            aUnspentTransOuts = self.processTransactions(currentBlock.data, aUnspentTransOuts, currentBlock.index)
            if aUnspentTransOuts == None:
                print("Invalid transactions")
                return None
        return aUnspentTransOuts

    def replaceChain(self, newBlocks):
        """If the Node receives a new blockchain this is used to verify and replace it if necessary."""
        aUnspentTransOuts = self.isValidChain(newBlocks)
        if aUnspentTransOuts is not None: validChain = True

        if validChain and self.getSumDifficulty(newBlocks) > self.getSumDifficulty(self.getBlockchain()):
            print("Received a better blockchain, exchanging it for your old one for free!")
            self.blockchain = newBlocks
            self.setUnspentTransOuts(aUnspentTransOuts)
            self.transpoll.updateTransactionPool(self.unspentTransOuts)
            #broadcastLatest()                       #TODO
        else:
            print("Received a new blockchain but it doesn't look good. In to the trash it goes")

    def getOwnersUnspentTransactionOutputs(self):
        return self.wallet.findUnspentTransOuts(self.wallet.getPublicFromWallet(), self.getUnspentTransOuts()) #TODO import findUnspentTransOuts from wallet