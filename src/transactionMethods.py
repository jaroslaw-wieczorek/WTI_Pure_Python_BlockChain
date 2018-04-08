# -*- coding: utf-8 -*-

import hashlib
import datetime
from datetime import timezone
from functools import reduce


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
    def isValidTransactionStructure(self, transaction:Transaction):
        return True
    
   
    def validateTransIn(self, transIn:TransIN, transaction:Transaction, aUnspentOutTrans : UnspentOutTrans) -> bool:
        referencedUnTransOut: UnspentOutTrans = aUnspentOutTrans.find([lambda uTransOut: uTransOut in uTransOut.transOutId == transIn.transOutId and uTransOut.transOutIndex == transIn.transOutIndex])
 
        if referencedUnTransOut == None:
            print('[*] referenced transOut not found: ' + str(transIn))
        return False
       
        
        # TO check ! 
        address = referencedUnTransOut.address;
        
        publ_key = RSA.importKey(address) 
        
        signer = PKCS1_v1_5.new(publ_key)
        newHash = SHA256.new()
        dataToVerify = (transaction.transID)
        newHash.update(dataToVerify.encode("utf-8"))
        
        validSignature : bool = signer.verify(newHash, transIn.signature)
        
        if not validSignature:
            print("Invalid transIn signature: %s transId: %s address: %s" % transIn.signature, transaction.id, referencedUnTransOut.address)
            return False
        
        return True
    
    # Conitune in this element
    
    def findUnspentTransOut(self, transId: str, index: int, aUnspentTransOut: UnspentOutTrans):
        for uTransOut in aUnspentTransOut:
            if uTransOut.transOutId == transId and uTransOut.transOutIndex == index:
                return uTransOut
        
    
    
    def getTransInAmount(self, transIn : TransIN, aUnspentTransOuts : UnspentOutTrans) -> float:
        return UnspentOutTrans(transIn.transOutId, transIn.transOutIndex, aUnspentTransOuts).amount;
    
    
    
    def validateTransaction(self, transaction:Transaction, aUnspentOutTrans:UnspentOutTrans):
       
        if not self.isValidTransactionStructure(transaction):
            return False
        
        if self.getTransactionId(transaction) != transaction.transID:
            print("[*] Invalid tx id: " + transaction.transID)
            return False
        
        hasValidTransINs : bool = reduce((lambda transIn: 
                                            self.validateTransIN(transIn,
                                            transaction, aUnspentOutTrans), 
                                            transaction.transIN
                                        ))
        print(hasValidTransINs)
        
        if not hasValidTransINs:
             print('[*] some of the transINs are invalid in trans: ' + transaction.transID);
             return False
         
        totalTransInValues : float = reduce((lambda x,y: self.getTransInAmount(x, aUnspentOutTrans) + self.getTransInAmount(y, aUnspentOutTrans), transaction.transIn))
        


    def newUnspentOutTrans(self):
        pass
        
        
        """
        const newUnspentTxOuts: UnspentTxOut[] = newTransactions
        .map((t) => {
            return t.txOuts.map((txOut, index) => new UnspentTxOut(t.id, index, txOut.address, txOut.amount));
        })
        .reduce((a, b) => a.concat(b), []);
        """
     

    
    
    def signTransIN(self, transaction: Transaction, transInIndex: int, aUnspentOutTrans: UnspentOutTrans):
        
        transIn = transaction.transIN[transInIndex]
        dataToSign = str(transaction.transID)
        print(dataToSign)

        refUnspentOutTrans : UnspentOutTrans = self.findUnspentTransOut(transIn.transOutId, transIn.transOutIndex, aUnspentOutTrans)
        refAddress = refUnspentOutTrans.address;
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

    def validateBlockTransactions(self,aTransactions, aUnspentTxOuts, blockIndex):
        coinbaseTx = aTransactions[0]
        if not self.validateCoinbaseTx(self,coinbaseTx, blockIndex):
            print('invalid coinbase transaction: ' + coinbaseTx)
            return False

        # check for duplicate txIns. Each txIn can be included only once
        txIns = list(map(lambda x: x.transIN, aTransactions))

        if len(txIns) != len(set(txIns)):
            return False


        # all but coinbase transactions
        normalTransactions = aTransactions[1:]
        return reduce((lambda a, b: a & b), list(map(lambda tx: self.validateTransaction(tx, aUnspentTxOuts), normalTransactions)), True)


