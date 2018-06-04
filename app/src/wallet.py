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
pub_path = os.path.abspath(os.path.join(__file__, '..','..','rsa_keys/key.pub'))
lib_path1 = os.path.abspath(os.path.join(__file__, '..','..','rsa_keys/key1.pem'))
pub_path1 = os.path.abspath(os.path.join(__file__, '..','..','rsa_keys/key1.pub'))


current_file_path = os.path.abspath(os.path.join(__file__))
sys.path.append(lib_path)
sys.path.append(current_file_path)


class Wallet(implements(UI), TransMethods):
    
    def __init__(self, address):
        # PRIVATE KEY
        if address == "1":
            self.__privateFileKey = open(lib_path1, "r").read()
            self.__publicFileKey = open(pub_path1, "r").read()

        else:
            self.__privateFileKey = open(lib_path, "r").read()
            self.__publicFileKey = open(pub_path, "r").read()

        self.__privateKey = RSA.importKey(self.__privateFileKey)
        self.__publicKey = RSA.importKey(self.__publicFileKey)
               
#        TransMethods.__init__(self, self.__privateFileKey)
        super()
        #self.__pub_key = open("key.pub", "r").read()
       # super(TransMethods, self).__init__()
        
    def getPrivateFromWallet(self) -> str:
        return self.__privateKey.exportKey()
    
    
    def getPublicFromWallet(self) -> str: 
        return self.__publicKey.exportKey()
    
    
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

    def generatekeypair(self, name):
        pathpub = os.path.abspath(os.path.join(__file__, '..', '..', 'rsa_keys/'+name+'.pub'))
        pathpriv = os.path.abspath(os.path.join(__file__, '..', '..', 'rsa_keys/'+name+'.pem'))

        rng = Random.new().read
        new_key = RSA.generate(1024, rng)

        with open(pathpriv, 'wb') as pem:
            pem.write(new_key.exportKey("PEM"))
            pem.close()
        with open(pathpub, 'wb') as pem:
            pem.write(new_key.publickey().exportKey("PEM"))
            pem.close()
        return str(pathpub)

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
        found_unspent_transactions = self.findUnspentOutTrans(address, unspentOutTrans)
        for trans in found_unspent_transactions:
            balance += trans.amount
     
        return balance



    def createOutsTrans(self, receiverAddress : str, myAddress : str, amount, leftOverAmount):
        outTrans1 : TransOUT = TransOUT(receiverAddress, amount)
        if leftOverAmount == 0:
            return [outTrans1]
        else:
            leftOverAmount = TransOUT(myAddress, leftOverAmount)
            return [outTrans1, leftOverAmount]
    
    
    def first_true(iterable, default=False, pred=None):
        return next(filter(pred, iterable), default)


    def findUnspentOutTrans(self, ownerAddres : str, unspentOutsTrans : UnspentOutTrans):
        return list(filter((lambda trans: trans.address == ownerAddres), unspentOutsTrans))

    
    def findOutsTransForAmount(self, amount, myUnspentOutsTrans: UnspentOutTrans):
        currentAmount = 0
        includeUnspentOutTrans = []
        for myUnspentOutTrans in myUnspentOutsTrans:
            includeUnspentOutTrans.append(myUnspentOutTrans)
            currentAmount = currentAmount + myUnspentOutTrans.amount
            if currentAmount >= amount:
                leftOverAmount = currentAmount - amount
                return includeUnspentOutTrans, leftOverAmount
        eMsg = "Cannot create transaction from the available unspent transaction outputs." #+ " Required amount: " + str(amount) + ". Available unspentOutsTrans: " + json.dumps(myUnspentOutsTrans)
        raise Exception(eMsg)

    def flatten(self, listOfLists):
        "Flatten one level of nesting"
        return itertools.chain.from_iterable(listOfLists)

    def filterTranPoolTrans(self, unspentOutsTrans : UnspentOutTrans, 
                            transactionPool : Transaction) -> UnspentOutTrans:
        transINs = list(self.flatten(map(lambda trans: trans.transINs, transactionPool)))

        removable : list = []
        
        for unspent in unspentOutsTrans:
            transIN = list(next((transIn for transIn in transINs if transIn.transOutId == unspent.transOutId
                    and transIn.transOutIndex == unspent.transOutIndex), [None]))
           #transIN = map(lambda transIn: transIn.transOutId == unspent.transOutId
           #        and transIn.transOutIndex == unspent.transOutIndex, transINs)
            if transIN[0] == None:
                pass
            else:
                removable.append(unspent)
        
        filteredTransactions = [trans for trans in unspentOutsTrans 
                                      if trans not in removable]
       
        return filteredTransactions
        
    
    def toUnsignedInTrans(self, unspent:UnspentOutTrans):
        return TransIN(unspent.transOutId, unspent.transOutIndex, "")
        
    def createTransaction(self, receiverAddress : str, amount : float,
                          privateKey : str, unspentOutsTrans : list, 
                          transPool : list) ->Transaction:
        myAddress : str = self.getPublicFromWallet()
        myUnspentOutsTransA = list(filter((lambda uOutTrans: uOutTrans.address == myAddress), unspentOutsTrans))
        
        myUnspentOutsTrans  = self.filterTranPoolTrans(myUnspentOutsTransA, transPool)
        
        # filter from unspentOutputs such inputs that are referenced in pool
        includedUnspentOutsTrans, leftOverAmount = self.findOutsTransForAmount(amount, myUnspentOutsTrans)
        
        unsignedInTrans = list(map(self.toUnsignedInTrans, includedUnspentOutsTrans))
        
        trans = Transaction("", unsignedInTrans, self.createOutsTrans(receiverAddress, myAddress, amount, leftOverAmount))
        trans.transID = self.getTransactionId(trans)
        
        for index, transIN in enumerate(trans.transINs):
            transIN.signature = self.signTransIN(trans, index, unspentOutsTrans, self.getPrivateFromWallet())
            
        return trans
    















