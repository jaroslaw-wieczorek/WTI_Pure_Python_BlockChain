# -*- coding: utf-8 -*-
import re
import hashlib
import datetime
import binascii
import operator 
from datetime import timezone
from functools import reduce

from .transIN import TransIN
from .transOUT import TransOUT
from .transaction import Transaction
from .unspentOutTrans import UnspentOutTrans

from Cryptodome.PublicKey import RSA 
from Cryptodome.Signature import PKCS1_v1_5 
from Cryptodome.Hash import SHA256 
from base64 import b64encode, b64decode 


class TransMethods():
    
    def __init__(self):
        self.__key = open("rsa_keys/key", "r").read()
        self.__pub_key = open("rsa_keys/key.pub", "r").read()
    
    def concIN(self, x):
        """
            Concatenate fileds of InTrans for Transaction ID  
        """
        return str(x.transOutId) + '' +str(x.transOutIndex)
    
    
    
    def concOUT(self, x):
        
        """
            Concatenate fileds of OutTrans for Transaction ID 
        """
        return str(x.address) + '' +str(x.amount)
    
    
    
    def getTransactionId(self, transaction: Transaction) -> str:
        
        """
          Methods return string contains Transaction ID
          
        """
        # Concatenate data from transIN objects list: 
        # transOutId & transOutIndexand reduce to one string
        transINContent : str = reduce(lambda x,y:  x+y, 
                                      map(self.concIN, transaction.transINs))    
       
        # Concatenate data from transOUT objects list: 
        # transOutId & transOutIndexand reduce to one string
        transOUTContent : str = reduce(lambda x,y:  x+y, 
                                       map(self.concOUT, transaction.transOUTs))
       
        # Create hash - id of transaction
        h=hashlib.sha256((transINContent+transOUTContent).encode("utf-8"))
   
        print(h.hexdigest())      
        return h.hexdigest() #return string 
    
    
    
    
    def validateTransaction(self, transaction:Transaction, 
                            aUnspentOutTrans:UnspentOutTrans) -> bool:
       
        """
           Validate properly of the whole Transaction: 
           Verifies properly the transaction structure.
           Verifies properly the transaction id.
           Verifies properly the input transactions.
           Verifies properly the  output transactions.
           Verifies properly the equal sums of InTrans and OutTrans
            
        """
        if not self.isValidTransactionStructure(transaction):
            return False
        
        if self.getTransactionId(transaction) != transaction.transID:
            print("[*] Invalid tx id: " + transaction.transID)
            return False
        
        # Two lambda functions labda x,y, x and y  - prepare logic values to reduce
        # Next lambda preprare list fo first with results of validateTransIN    
        hasValidInTrans : bool = reduce(lambda x,y: x and y,
                                list(map(lambda transIN: 
                                    self.validateTransIN(transIN, 
                                                         transaction, 
                                                         aUnspentOutTrans),
                                                         transaction.transINs,
                                                         default=True)))                               
            
        if not hasValidInTrans:
             print('[*] some of the transINs are invalid in trans: ' + transaction.transID)
             return False
        
       
        # get all InMoney
        totalInTransValues : float = reduce(lambda x,y: x + y, 
                                     list(map(lambda transIN: self.getTransInAmount(transIN, aUnspentOutTrans), transaction.transINs)))
        
        # get all OutMoney
        totalOutTransValues : float = reduce(lambda x, y: x + y, map(self.getTransOutAmount,  transaction.transOUTs))
          
        # check 
        if totalOutTransValues != totalInTransValues:
            print('totalOutTransValues != totalInTransValues in tx: ' + transaction.transID)
        return False



    def validateBlockTransactions(self, aTransactions, aUnspentOutTrans : UnspentOutTrans, blockIndex : float):
        coinbaseTrans = aTransactions[0]
        
        """
           Validate block of TransactionsOutTrans
            
        """
        
        if not self.validateCoinbaseTrans(coinbaseTrans, blockIndex):
            print('invalid coinbase transaction: ' + str(coinbaseTrans))
            return False

        # check for duplicate txIns. Each txIn can be included only once
        
        transIns = list(map(lambda x: x.transINs, aTransactions))
        
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
        if transaction.transINs.length != 1:
            print('one transIn must be specified in the coinbase transaction')
            return False

        if transaction.transINs[0].transOutIndex != blockIndex:
            print('the txIn signature in coinbase tx must be the block height')
            return False

        if len(transaction.transOUTs) != 1:
            print('invalid number of transOut in coinbase transaction')
            return False

        if transaction.transOUTs[0].amount != self.COINBASE_AMOUNT:
            print('invalid coinbase amount in coinbase transaction')
            return False
        return True
    


    def validateInTrans(self, transIN:TransIN, transaction:Transaction, aUnspentOutTrans : UnspentOutTrans) -> bool:
        referencedUnTransOut: UnspentOutTrans = aUnspentOutTrans.find([lambda uTransOut: uTransOut in uTransOut.transOutId == transIN.transOutId and uTransOut.transOutIndex == transIN.transOutIndex])
 
        if referencedUnTransOut == None:
            print('[*] referenced transOut not found: ' + str(transIN))
            return False
        
        # TO check ! 
        address = referencedUnTransOut.address
        
        publ_key = RSA.importKey(address) 
        
        signer = PKCS1_v1_5.new(publ_key)
        newHash = SHA256.new()
        dataToVerify = (transaction.transID)
        newHash.update(dataToVerify.encode("utf-8"))
        
        validSignature : bool = signer.verify(newHash, transIN.signature)
        
        if not validSignature:
            print("Invalid transIn signature: %s transId: %s address: %s" % transIN.signature, transaction.id, referencedUnTransOut.address)
            return False
        return True
    
        
    def getTransInAmount(self, transIN : TransIN, aUnspentOutTrans : UnspentOutTrans) -> float:
        return self.findUnspentOutTrans(transIN.transOutId, transIN.transOutIndex, aUnspentOutTrans).amount
    
    
    
    def getTransOutAmount(self, transOut : TransOUT):
        return transOut.amount
    
    
    
    def findUnspentOutTrans(self, transOutId: str, transOutIndex: int, aUnspentOutTrans: UnspentOutTrans):
        for uTransOut in aUnspentOutTrans:
            if uTransOut.transOutId == transOutId and uTransOut.transOutIndex == transOutIndex:
                return uTransOut
    
    
    def getCoinbaseTransaction(self, address: str, blockIndex : int) -> Transaction:
        t = Transaction()
        newtransIN = TransIN()
        newtransIN.signature = ''
        newtransIN.transOutId = ''
        newtransIN.transOutIndex = blockIndex
        
        t.transINs = [newtransIN]
        t.transOUTs = [TransOUT(address, self.COINBASE_AMOUNT)]
        t.transID = self.getTransactionId(t)
        
        return t
    
   
    def signTransIN(self, transaction: Transaction, transInIndex: int, aUnspentOutTrans: UnspentOutTrans):
        
        transIN : TransIN = transaction.transINs[transInIndex]
        dataToSign = str(transaction.transID)
        referencedUnspentOutTrans : UnspentOutTrans = self.findUnspentOutTrans(transIN.transOutId, transIN.transOutIndex, aUnspentOutTrans)

        
        if referencedUnspentOutTrans is None:
            print("could not find referenced transOUT")
            raise Exception
        
        referencedAddress = referencedUnspentOutTrans.address
        
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
   
    
    def updateUnspentOutTrans(self, aTransactions : list, aUnspentOutsTrans : UnspentOutTrans) -> UnspentOutTrans:

        # t - Transaction
        newUnSpentOutsTrans_elements = []
        for t in aTransactions:
            for out in t.transOUTs:
                newUnSpentOutsTrans_elements.append(UnspentOutTrans(t.transOutId, t.transOutIndex, out.address, out.transOutIndex))
        
        newUnSpentOutsTrans : UnspentOutTrans = reduce(operator.concat, newUnSpentOutsTrans_elements, [])
        
     
        consumed_elements = []
        for t in aTransactions:
            for transIN in reduce(operator.concat, t.transINs, []):
                    consumed_elements.append(self.UnspentOutTrans(transIN.transOutId, transIN.transOutIndex, '', 0))
    
    
        consumedOutsTrans : UnspentOutTrans = consumed_elements
  
        
        resultingUnspnetOutsTrans = None
        # UnspentOutTrans as uto
        resultingUnspnetOutsTrans_all= []
        for uto in aUnspentOutsTrans:
            if not self.findUnspentOutTrans(uto.trasOutId, uto.trasOutIndex, consumedOutsTrans):
                resultingUnspnetOutsTrans_all.append(uto)
        
        resultingUnspnetOutsTrans = reduce(operator.concat, resultingUnspnetOutsTrans_all, newUnSpentOutsTrans)
        return resultingUnspnetOutsTrans
  

     
   # def newUnspentOutTrans():
   #     return list(lambda transOut, index: self.UnspentOutTrans(t.transID, index, transOut.address, transOut.amount))
    def processTransactions(self, aTransactions: Transaction, aUnspentOutTrans: UnspentOutTrans, blockIndex):
        if not self.validateBlockTransactions(aTransactions, aUnspentOutTrans, blockIndex):
            print('invalid block transaciton')
            return None
        return self.updateUnspentOutTrans(aTransactions, aUnspentOutTrans)
    
        
    def toHexString(self, binStr):
        return binascii.hexlify(binStr)

    def hexString2binary(self, hexStr):
        return binascii.unhexlify(hexStr)
   
    
    
    def getPublicKey(self):
        publ_key = RSA.importKey(self.__pub_key) 
        return publ_key
    
    
    def isValidInTransStructure(self, transIN: TransIN) -> bool :
        if transIN == None:
            print('transIN is None')
            return False
    
        elif type(transIN.signature) != str:
            print('invalid singature type in transIN')
            return False
        
        elif type(transIN.transOutId) != str:
            print('invalid transOutId type in transIN')
            return False
        
        elif type(transIN.transOutIndex) != int:
            print('invalid transOutIndex type in transIN')
            return False
        else:
            return True
    
    
    def isValidOutTransStructure(self, transOUT : TransOUT) -> bool:
        if transOUT == None:
            print('transOUT is None')
            return False
    
        elif type(transOUT.address) != str:
            print('invalid address type in transOUT')
            return False
        
        elif not self.isValidAddress(transOUT.address):
            print('not valid transOUT address')
            return False
        
        elif type(transOUT.amount) != int:
            print('invalid amount type in transOUT')
            return False
       
        else:
            return True
        
    # To do: implement
    def isValidTransactionStructure(self, transaction:Transaction): 
        if type(transaction.id) != str:
            print('transactionId missing')
            return False
        
        if not isinstance(transaction.TransINs, list):
            print('invalid TransIns type in transaction')
            return False
        
         # validation structures in transaction.transINs
        if not reduce(lambda x,y: x and y, map(self.isValidInTransStructure,
                                               transaction.transINs), True):
            print('invalid some structure in transactionINs')
            return False
    
        # validation type - expected list for input transaction.transOUTs
        if not isinstance(transaction.transOUTs, list):
            print('invalid transOUTs type in transaction')
            return False
 
        # validation structures in transaction.transOUTs
        if not reduce(lambda x,y: x and y, map(self.isValidOutTransStructure,
                                               transaction.transOUTs), True):
            print('invalid some structure in transactionOUTs')
            return False
        
        return True
    
    #validation Address in publicKey
    def isValidAddress(self, address : str) -> bool :
        if len(address) != 130:
            print(address, ' - invalid len of public key')
            return False
        elif re.match(r"^[a-fA-F0-9]+$", address) == None:
            print('public key must contain only hex characters')
            return False
        elif address.startswith("04"):
            print('public key must start with 04')
            return False
        else:
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
    

   
   