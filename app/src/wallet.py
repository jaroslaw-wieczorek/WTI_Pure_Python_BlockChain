# -*- coding: utf-8 -*-

from interface import implements

from .generics.interfaces import UI

import os
import re
import sys
import json
import hashlib
import datetime
import binascii
import operator 
import itertools
from datetime import timezone
from functools import reduce

from Cryptodome.PublicKey import RSA 
from Cryptodome.Signature import PKCS1_v1_5 
from Cryptodome.Hash import SHA256 
from base64 import b64encode, b64decode 

from Cryptodome import Random
from .unspentOutTrans import UnspentOutTrans
from .transactionMethods import TransMethods
from .transactionPool import TransactionPool
from .transOUT import TransOUT
from .transIN import TransIN
from .transaction import Transaction


# importing data accc
lib_path = os.path.abspath(os.path.join(__file__, '..','..','rsa_keys/key.pem'))
current_file_path = os.path.abspath(os.path.join(__file__))
sys.path.append(lib_path)
sys.path.append(current_file_path)


class Wallet(implements(UI), TransMethods):
    
    def __init__(self, address):
        # PRIVATE KEY
        self.__privateFileKey = open(lib_path, "r").read()
       
        self.__privateKey = RSA.importKey(self.__privateFileKey) 
        self.__publicKey = self.getPrivateFromWallet().publickey().exportKey()
               
        
        #self.__pub_key = open("key.pub", "r").read()
        super()
        
    def getPrivateFromWallet(self) -> str: 
        #self.__privateKey = RSA.importKey(self.__privateFileKey) 
        return self.__privateKey 
    
    
    def getPublicFromWallet(self) -> str: 
        #self.__publKey = self.getPrivateFromWallet().publickey().exportKey()
        return self.__publicKey
    
    
    def generatePrivateKey(self) -> str:
        '''
            Generate an RSA keypair in PEM format
            param: bits The key length in bits
            Return private key and public key
        '''
        rng = Random.new().read
        new_key = RSA.generate(1024, rng) 
        self.__privateKey = new_key.exportKey("PEM") 
        
        with open(lib_path, 'wb') as pem:
            pem.write(self.__privateKey)
            pem.close()
        
        return str(lib_path)
    

    def initWallet(self):
        if os.path.isfile(lib_path):
            return
        else:
            newPrivateKey = self.generatePrivateKey()
            print("new wallet with private key created to : " % newPrivateKey)
   
    
    def deleteWallet(self):
        if os.path.isfile(lib_path):
            os.remove(lib_path)
            
    
    def getBalance(self, address : str, unspentOutTrans : UnspentOutTrans):
        balance=0
        found_unspent_transactions = map(self.findUnspentOutTrans(address, unspentOutTrans), unspentOutTrans)
        for trans in found_unspent_transactions:
            balance += trans.amount
     
        return balance


    def findUnspentOutTrans(self, ownerAddres : str, unspentOutsTrans : UnspentOutTrans):
        return list(filter((lambda trans: trans.address == ownerAddres), unspentOutsTrans))
    
    
    def findOutsTransForAmount(self, amount, myUnspentOutsTrans: UnspentOutTrans):
        currentAmount = 0
        includeUnspentOutTrans = []
        for myUnspentOutTrans in myUnspentOutsTrans:
            includeUnspentOutTrans.insert(myUnspentOutTrans)
            currentAmount = currentAmount + myUnspentOutTrans.amount
            if currentAmount >= amount:
                leftOverAmount = currentAmount - amount
                return {includeUnspentOutTrans, leftOverAmount}
        eMsg = 'Cannot create transaction from the available unspent transaction outputs.' + ' Required amount: ' + str(amount) 
        + '. Available unspentOutsTrans: ' + json.dumps(myUnspentOutsTrans)
        raise Exception(eMsg)
        

    def createOutsTrans(self, receiverAddress : str, myAddress : str, amount, leftOverAmount):
        outTrans1 : TransOUT = TransOUT(receiverAddress, amount)
        if leftOverAmount == 0:
            return [outTrans1]
        else:
            leftOverAmount = TransOUT(myAddress, leftOverAmount)
            return [outTrans1, leftOverAmount]
    
    
    def first_true(iterable, default=False, pred=None):
        return next(filter(pred, iterable), default)


    def filterTranPoolTrans(unspentOutsTrans : UnspentOutTrans, 
                            transactionPool : Transaction) -> UnspentOutTrans:
        transINs : TransIN = list(itertools.flatten(map(
                (lambda trans : trans.transINs) , transactionPool)))

        removable : list = []
        
        for unspent in unspentOutsTrans:
            transIN = (transINs, None, (
                    lambda transIn: transIn.transOutId == unspent.transOutId
                    and transIn.transOutIndex == unspent.transOutIndex
                    ))
            if transIN == None:
                pass
            else:
                removable.append(unspent)
        
        filteredTransactions = [trans for trans in unspentOutsTrans 
                                      if trans not in removable]
       
        return filteredTransactions
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        