# -*- coding: utf-8 -*-

import hashlib
import datetime
from datetime import timezone


from src.transIN import TransIN
from src.transOUT import TransOUT
from src.transaction import Transaction
from src.unspentOutTrans import UnspentOutTrans

from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 

class TransMethods():
    
    __key = open("rsa_keys/private", "r").read()

    __pub_key = open("rsa_keys/key.pub", "r").read()
    def __init__(self):
        self.__key = open("rsa_keys/private", "r").read()

        self.__pub_key = open("rsa_keys/key.pub", "r").read()
    
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
   
        print(h.hexdigest())      
        return h.hexdigest() #return string 
    
    # To do: implement
    def isValidTransactionStructure(transaction:Transaction):
        return True
   
    def validateTransaction(self, transaction:Transaction, aUnspentOutTrans:UnspentOutTrans):
        if not self.isValidTransactionStructure(transaction):
            return False
        if self.getTransactionId(transaction) != transaction.transID:
            print("Invalid tx id: " + transaction.transID)
            return False
     #   hasValidTransINs : bool = 
    
    def newUnspentOutTrans(self):
        
        """
        const newUnspentTxOuts: UnspentTxOut[] = newTransactions
        .map((t) => {
            return t.txOuts.map((txOut, index) => new UnspentTxOut(t.id, index, txOut.address, txOut.amount));
        })
        .reduce((a, b) => a.concat(b), []);
        """
        pass
    
    """
    def findUnspentOutTrans(ransIn.transOutId, trans.transOutIndex, unspentsTransOuts):
        pass
    """
    
    def signTransIN(self, transaction: Transaction, transInIndex: int, unspentsTransOuts: list):
        
        transIn = transaction.transIN[transInIndex]
        dataToSign = str(transaction.transID)
        print(dataToSign)

        # refUnspentOutTrans = findUnspentOutTrans(transIn.transOutId, trans.transOutIndex, unspentsTransOuts)
        # refAddress = refUnspentOutTrans.address;
        priv_key = RSA.importKey(self.__key) 
        signer = PKCS1_v1_5.new(priv_key) 
        newHash = SHA256.new()
        # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
        newHash.update(dataToSign.encode("utf-8"))
        return signer.sign(newHash)
   
    
    def verify(self, transaction: Transaction, signature):
        dataToVerify = (transaction.transID)
        print(dataToVerify)
        
        #public key for tests
        publ_key = RSA.importKey(self.__pub_key) 
        signer = PKCS1_v1_5.new(publ_key)
        newHash = SHA256.new()
    
        newHash.update(dataToVerify.encode("utf-8"))
        return signer.verify(newHash, signature)

    def validateCoinbaseTx(self, transaction, blockIndex):
        if transaction == None:
            print('the first transaction in the block must be coinbase transaction')
            return False

        if self.getTransactionId(transaction) != transaction.transID :
            print('invalid coinbase tx id: ' + transaction.transID)
            return False
        if transaction.transIN.length != 1:
            print('one txIn must be specified in the coinbase transaction')
            return False

        if transaction.transIN[0].transOutIndex != blockIndex:
            print('the txIn signature in coinbase tx must be the block height')
            return False

        if transaction.txOuts.length != 1:
            print('invalid number of txOuts in coinbase transaction')
            return False

        if transaction.txOuts[0].amount != self.COINBASE_AMOUNT:
            print('invalid coinbase amount in coinbase transaction')
            return False
        return True
