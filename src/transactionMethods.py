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
    
    
    def getTransactionId(self, transaction: Transaction) -> str:
        
        # Concatenate data from transIN objects list: 
        # transOutId & transOutIndexand reduce to one string
        transINContent : str = reduce(lambda x,y:  x+y, 
                                      map(self.concIN, transaction.transIN))    
       
        # Concatenate data from transOUT objects list: 
        # transOutId & transOutIndexand reduce to one string
        transOUTContent : str = reduce(lambda x,y:  x+y, 
                                       map(self.concOUT, transaction.transOUT))
       
        # Create hash - id of transaction
        h=hashlib.sha256((transINContent+transOUTContent).encode("utf-8"))
   
        print(h.hexdigest())      
        return h.hexdigest() #return string 
    
    
    
    def validateTransaction(self, transaction:Transaction, 
                            aUnspentOutTrans:UnspentOutTrans) -> bool:
       
        if not self.isValidTransactionStructure(transaction):
            return False
        
        if self.getTransactionId(transaction) != transaction.transID:
            print("[*] Invalid tx id: " + transaction.transID)
            return False
        
        # Two lambda functions labda x,y, x and y  - prepare logic values to reduce
        # Next lambda preprare list fo first with results of validateTransIN    
        hasValidInTrans : bool = reduce(lambda x,y: x and y,
                                list(map(lambda transIn: 
                                    self.validateTransIN(transIn, 
                                                         transaction, 
                                                         aUnspentOutTrans),
                                                         transaction.transIN,
                                                         default=True)))                               
            
        if not hasValidInTrans:
             print('[*] some of the transINs are invalid in trans: ' + transaction.transID);
             return False
        
       
        # get all InMoney
        totalInTransValues : float = reduce(lambda x,y: x + y, 
                                     list(map(lambda transIn: self.getTransInAmount(transIn, aUnspentOutTrans), transaction.transIn)))
        
        # get all OutMoney
        totalOutTransValues : float = reduce(lambda x, y: x + y, map(self.getTransOutAmount,  transaction.transOut))
          
        # check 
        if totalOutTransValues != totalInTransValues:
            print('totalOutTransValues != totalInTransValues in tx: ' + transaction.id)
        return False;



    def validateBlockTransactions(self, aTransactions, aUnspentOutTrans : UnspentOutTrans, blockIndex : float):
        coinbaseTrans = aTransactions[0]
        
        if not self.validateCoinbaseTrans(self,coinbaseTrans, blockIndex):
            print('invalid coinbase transaction: ' + coinbaseTrans)
            return False

        # check for duplicate txIns. Each txIn can be included only once
        
        transIns = list(map(lambda x: x.transIN, aTransactions))
        
        #Check dupliactes 1
        if self.hasDupliactes(transIns):
            return False
        
        #Check  dupliactes 2
        if len(transIns) != len(set(transIns)):
            print("Some duplicate transIN")
            return False
        
        
        # all but coinbase transactions
        normalTransactions = aTransactions[1:]
        return reduce((lambda a, b: a and b), list(map(lambda x: self.validateTransaction(x, aUnspentOutTrans), normalTransactions)), True)
    
    
    # NEED CHANGE TO CHEK ON KEYS
    def hasDuplicates(self, transIns : TransIN) -> bool:
        seen = set()
        for x in transIns:
            if x in seen: return True
            seen.add(x)
        return False
    
    
    
    def validateCoinbaseTrans(self, transaction, blockIndex):
        if transaction == None:
            print('the first transaction in the block must be coinbase transaction')
            return False

        if self.getTransactionId(transaction) != transaction.transID :
            print('invalid coinbase tx id: ' + transaction.transID)
            return False
        if transaction.transIN.length != 1:
            print('one transIn must be specified in the coinbase transaction')
            return False

        if transaction.transIN[0].transOutIndex != blockIndex:
            print('the txIn signature in coinbase tx must be the block height')
            return False

        if len(transaction.transOUT) != 1:
            print('invalid number of transOut in coinbase transaction')
            return False

        if transaction.transOUT[0].amount != self.COINBASE_AMOUNT:
            print('invalid coinbase amount in coinbase transaction')
            return False
        return True
    


    def validateInTrans(self, transIn:TransIN, transaction:Transaction, aUnspentOutTrans : UnspentOutTrans) -> bool:
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
    
        
    def getTransInAmount(self, transIn : TransIN, aUnspentOutTrans : UnspentOutTrans) -> float:
        return self.findUnspentTransOut(transIn.transOutId, transIn.transOutIndex, aUnspentOutTrans).amount;
    
    
    
    def getTransOutAmount(self, transOut : TransOUT):
        return transOut.amount
    
    
    
    def findUnspentOutTrans(self, transOutId: str, transOutIndex: int, aUnspentTransOut: UnspentOutTrans):
        for uTransOut in aUnspentTransOut:
            if uTransOut.transOutId == transOutId and uTransOut.transOutIndex == transOutIndex:
                return uTransOut
    
    
    def getCoinbaseTransaction(self, address: str, blockIndex : float) -> Transaction: 
        t = Transaction()
        newtransIN = TransIN()
        newtransIN.signature = ''
        newtransIN.transOutId = ''
        newtransIN.transOutIndex = blockIndex
        
        t.transIN = [newtransIN]
        t.transOUT = [TransOUT(address, self.COINBASE_AMOUNT)];
        t.transID = self.getTransactionId(t);
        
        return t;
    
    
   
    def signTransIN(self, transaction: Transaction, transInIndex: int, aUnspentOutTrans: UnspentOutTrans):
        
        transIn : TransIN = transaction.transIN[transInIndex]
        dataToSign = str(transaction.transID)
        referencedUnspentOutTrans : UnspentOutTrans = self.findUnspentTransOut(transIn.transOutId, transIn.transOutIndex, aUnspentOutTrans)

        
        if referencedUnspentOutTrans is None:
            print("could not find referenced transOUT")
            raise Exception
        
        referencedAddress = referencedUnspentOutTrans.address;
        
        if  self.getPublicKey(self.__privateKey) != referencedAddress:
            print('trying to sign an input with private' + ' key that does not match the address that is referenced in transIN')
            raise Exception
        
        
        priv_key = RSA.importKey(self.__key) 
        
        signer = PKCS1_v1_5.new(priv_key) 
        newHash = SHA256.new()
        # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
        newHash.update(dataToSign.encode("utf-8"))
         
        #Return singature: 
        signature : str = signer.sign(newHash)
      
        return signature 
    
    
    def updateUnspentOutTrans(aTransactions : Transaction, aUnspentOutTrans : UnspentOutTrans) -> UnspentOutTrans:
        pass
    
         
    
    def newUnspentOutTrans():
        pass
    
    # To do: implement
    def isValidTransactionStructure(self, transaction:Transaction):
       
        if not type(transaction.id, str):
            print('transactionId missing')
            return False
        
        if not isinstance(transaction.TransIN, list):
            print('invalid TransIns type in transaction')
            return False
        
        if not reduce(isValidTransOutStructure, transaction.transOUT):
            return False
    
        return True
    
   
   


        

    
    
 
    
    def verify(self, transaction: Transaction, signature):
        dataToVerify = (transaction.transID)
        print(dataToVerify)
        
        #public key for tests
        publ_key = RSA.importKey(self.__pub_key) 
        signer = PKCS1_v1_5.new(publ_key)
        newHash = SHA256.new()
        
        newHash.update(dataToVerify.encode("utf-8"))
        return signer.verify(newHash, signature)
    

   
    
    def processTransactions(self, aTransactions, aUnspentTxOuts, blockIndex):
        if not self.validateBlockTransactions(aTransactions, aUnspentTxOuts, blockIndex):
            print('invalid block transactions')
            return None
        return self.updateUnspentTxOuts(aTransactions, aUnspentTxOuts) #TO_DO NOT IMPLEMENTED yet
