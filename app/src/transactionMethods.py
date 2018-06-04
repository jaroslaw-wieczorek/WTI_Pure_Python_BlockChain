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



        pass

    def concIN(self, x):
        """
            Concatenate fileds of InTrans for Transaction ID  
        """
        return str(x.transOutId) + '' + str(x.transOutIndex)

    def concOUT(self, x):

        """
            Concatenate fileds of OutTrans for Transaction ID 
        """
        return str(x.address) + '' + str(x.amount)

    def getTransactionId(self, transaction: Transaction) -> str:

        """
          Methods return string contains Transaction ID
          
        """
        # Concatenate data from transIN objects list: 
        # transOutId & transOutIndexand reduce to one string
        transINContent: str = reduce(lambda x, y: x + y,
                                     map(self.concIN, transaction.transINs))

        # Concatenate data from transOUT objects list: 
        # transOutId & transOutIndexand reduce to one string
        transOUTContent: str = reduce(lambda x, y: x + y,
                                      map(self.concOUT, transaction.transOUTs))

        # Create hash - id of transaction
        h = hashlib.sha256((transINContent + transOUTContent).encode("utf-8"))

        print(h.hexdigest())
        return h.hexdigest()  # return string

    def validateTransaction(self, transaction: Transaction,
                            aUnspentOutTrans: UnspentOutTrans) -> bool:

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
            raise ValueError("[*] Invalid tx id: " + transaction.transID)
            return False

        # Two lambda functions labda x,y, x and y  - prepare logic values to reduce
        # Next lambda preprare list fo first with results of validateTransIN    
        hasValidInTrans: bool = reduce(lambda x, y: x and y, list(map(lambda transIN: self.validateInTrans(transIN, transaction, aUnspentOutTrans), transaction.transINs)))

        if not hasValidInTrans:
            raise ValueError('[*] some of the transINs are invalid in trans: ' + transaction.transID)
            return False

        # get all InMoney
        totalInTransValues: float = reduce(lambda x, y: x + y,
                                           list(map(lambda transIN: self.getTransInAmount(transIN, aUnspentOutTrans),
                                                    transaction.transINs)))

        # get all OutMoney
        totalOutTransValues: float = reduce(lambda x, y: x + y, map(self.getTransOutAmount, transaction.transOUTs))

        # check 
        if totalOutTransValues != totalInTransValues:
            raise ValueError('totalOutTransValues != totalInTransValues in tx: ' + transaction.transID)
            return False

        return True

    def validateBlockTransactions(self, aTransactions, aUnspentOutTrans: UnspentOutTrans, blockIndex: float):
        coinbaseTrans = aTransactions[0]

        """
           Validate block of TransactionsOutTrans
            
        """

        if not self.validateCoinbaseTrans(coinbaseTrans, blockIndex):
            raise ValueError('invalid coinbase transaction: ' + str(coinbaseTrans))
            return False

        # check for duplicate txIns. Each txIn can be included only once

        transIns = list(map(lambda x: x.transINs, aTransactions))

        # Check dupliactes 1
        if self.hasDuplicates(transIns):
            return False

        # Check  dupliactes 2

        # if len(transIns) != len(set(tuple ((a) for a in transIns))):
        #    raise ValueError("Some duplicate transIN")
        #    return False

        # all but coinbase transactions
        normalTransactions = aTransactions[1:]
        return reduce((lambda a, b: a and b),
                      list(map(lambda x: self.validateTransaction(x, aUnspentOutTrans), normalTransactions)), True)

    # NEED CHANGE TO CHEK ON KEYS
    def hasDuplicates(self, transactions: list) -> bool:
        setTrans = set()
        listTrans = list()
        for transIns in transactions:
            for trans in transIns:
                if trans in setTrans:
                    return True
                setTrans.add(trans)
                listTrans.append(trans)
                
        if len(setTrans) != len(listTrans):
            return True
                
        return False
        
    def validateCoinbaseTrans(self, transaction, blockIndex):
        if transaction == None:
            raise ValueError('the first transaction in the block must be coinbase transaction')
            return False

        if self.getTransactionId(transaction) != transaction.transID:
            raise ValueError('invalid coinbase tx id: ' + transaction.transID)
            return False
        if len(transaction.transINs) != 1:
            raise ValueError('one transIn must be specified in the coinbase transaction')
            return False

        if transaction.transINs[0].transOutIndex != blockIndex:
            raise ValueError('the txIn signature in coinbase tx must be the block height')
            return False

        if len(transaction.transOUTs) != 1:
            raise ValueError('invalid number of transOut in coinbase transaction')
            return False

        if transaction.transOUTs[0].amount != self.COINBASE_AMOUNT:
            raise ValueError('invalid coinbase amount in coinbase transaction')
            return False
        return True

    def validateInTrans(self, transIN: TransIN, transaction: Transaction, aUnspentOutTrans: UnspentOutTrans) -> bool:
        referencedUnTransOut: UnspentOutTrans = list(map(lambda uTransOut: uTransOut if uTransOut.transOutId == transIN.transOutId and uTransOut.transOutIndex == transIN.transOutIndex else None , aUnspentOutTrans))
        referencedUnTransOut = list(filter(lambda i: i != None, referencedUnTransOut))
        for uTransOut in referencedUnTransOut:
            if uTransOut.transOutId == transIN.transOutId and uTransOut.transOutIndex == transIN.transOutIndex:
                referencedUnTransOut = uTransOut
                break
            else:
                referencedUnTransOut = None
        if referencedUnTransOut == None:
            raise ValueError('[*] referenced transOut not found: ' + str(transIN))
            return False

        # TO check ! 
        address = referencedUnTransOut.address

        key_to_validation = RSA.importKey(address)

        signer = PKCS1_v1_5.new(key_to_validation)
        newHash = SHA256.new()
        dataToVerify = (transaction.transID)
        newHash.update(dataToVerify.encode("utf-8"))

        validSignature: bool = signer.verify(newHash, transIN.signature)

        if not validSignature:
            raise ValueError("Invalid transIn signature: %s transId: %s address: %s" % transIN.signature, transaction.id,
                  referencedUnTransOut.address)
            return False
        return True

    def getTransInAmount(self, transIN: TransIN, aUnspentOutTrans: UnspentOutTrans) -> float:
        return self.findUnspentOutTrans(transIN.transOutId, transIN.transOutIndex, aUnspentOutTrans).amount

    def getTransOutAmount(self, transOut: TransOUT):
        return transOut.amount

    def findUnspentOutTrans(self, transOutId, transOutIndex, aUnspentOutTrans):
        for uTransOut in aUnspentOutTrans:
            if uTransOut.transOutId == transOutId and uTransOut.transOutIndex == transOutIndex:
                return uTransOut

    def getCoinbaseTransaction(self, address: str, blockIndex: int) -> Transaction:
        newtransIN = TransIN('', blockIndex, '')
        t = Transaction(None, [newtransIN], [TransOUT(address, self.COINBASE_AMOUNT)])
        t.transID = self.getTransactionId(t)
        return t

    def signTransIN(self, transaction: Transaction, transInIndex: int, aUnspentOutTrans: UnspentOutTrans, privkey):

        transIN: TransIN = transaction.transINs[transInIndex]
        dataToSign = str(transaction.transID)
        referencedUnspentOutTrans = TransMethods.findUnspentOutTrans(self, transIN.transOutId, transIN.transOutIndex, aUnspentOutTrans)

        if referencedUnspentOutTrans is None:
            raise ValueError("could not find referenced transOUT")

        private = RSA.importKey(privkey)
        referencedAddress = referencedUnspentOutTrans.address
        public = private.publickey().exportKey()
        if public != referencedAddress:
            raise ValueError('trying to sign an input with private' + ' key that does not match the address that is referenced in transIN')


        key_to_sign = private

        signer = PKCS1_v1_5.new(key_to_sign)
        newHash = SHA256.new()
        # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
        newHash.update(dataToSign.encode("utf-8"))

        # Return singature:
        signature: str = signer.sign(newHash)

        return signature

    def updateUnspentOutTrans(self, aTransactions: list, aUnspentOutsTrans: UnspentOutTrans) -> UnspentOutTrans:
        # t - Transaction
        newUnSpentOutsTrans_elements = []
        for t in aTransactions:
            for index, out in enumerate(t.transOUTs):
                newUnSpentOutsTrans_elements.append(UnspentOutTrans(t.transID, index, out.address, out.amount))

        # newUnSpentOutsTrans : UnspentOutTrans = reduce(operator.concat, newUnSpentOutsTrans_elements, [])
        newUnSpentOutsTrans: UnspentOutTrans = newUnSpentOutsTrans_elements

        consumed_elements = []
        for t in aTransactions:
            concate = map(lambda x: x, t.transINs)
            for transIN in concate:
                consumed_elements.append(UnspentOutTrans(transIN.transOutId, transIN.transOutIndex, '', 0))

        consumedOutsTrans: UnspentOutTrans = consumed_elements

        resultingUnspnetOutsTrans = None
        # UnspentOutTrans as uto
        resultingUnspnetOutsTrans_all = []
        for uto in aUnspentOutsTrans:
            if not self.findUnspentOutTrans(uto.transOutId, uto.transOutIndex, consumedOutsTrans):
                resultingUnspnetOutsTrans_all.append(uto)

        resultingUnspnetOutsTrans = operator.iadd(resultingUnspnetOutsTrans_all, newUnSpentOutsTrans)
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

    def getPublicKey(self, priv_key):
        publ_key = RSA.importKey(priv_key).publickey().exportKey()
        return publ_key

    def isValidInTransStructure(self, transIN: TransIN) -> bool:
        if transIN == None:
            raise ValueError('transIN is None')
            return False

        elif type(transIN.signature) != bytes:
            raise ValueError('invalid singature type in transIN')
            return False

        elif type(transIN.transOutId) != str:
            raise ValueError('invalid transOutId type in transIN')
            return False

        elif type(transIN.transOutIndex) != int:
            raise ValueError('invalid transOutIndex type in transIN')
            return False
        else:
            return True

    def isValidOutTransStructure(self, transOUT: TransOUT) -> bool:
        if transOUT == None:
            raise ValueError('transOUT is None')
            return False

        elif type(transOUT.address) != bytes:
            raise ValueError('invalid address type in transOUT')
            return False

        elif not self.isValidAddress(transOUT.address):
            raise ValueError('not valid transOUT address')
            return False

        elif not isinstance(transOUT.amount, float) and  not isinstance(transOUT.amount, int):
            raise ValueError('invalid amount type in transOUT')
            return False

        else:
            return True

    # To do: implement
    def isValidTransactionStructure(self, transaction: Transaction):
        if type(transaction.transID) != str:
            raise ValueError('transactionId missing')
            return False

        if not isinstance(transaction.transINs, list):
            raise ValueError('invalid TransIns type in transaction')
            return False

            # validation structures in transaction.transINs
        if not reduce(lambda x, y: x and y, map(self.isValidInTransStructure,
                                                transaction.transINs), True):
            raise ValueError('invalid some structure in transactionINs')
            return False

        # validation type - expected list for input transaction.transOUTs
        if not isinstance(transaction.transOUTs, list):
            raise ValueError('invalid transOUTs type in transaction')
            return False

        # validation structures in transaction.transOUTs
        if not reduce(lambda x, y: x and y, map(self.isValidOutTransStructure,
                                                transaction.transOUTs), True):
            raise ValueError('invalid some structure in transactionOUTs')
            return False

        return True

    # validation Address in publicKey
    def isValidAddress(self, address: str) -> bool:
        if len(address) != 271:
            raise ValueError(address, ' - invalid len of public key')
            return False
        #elif re.match(r"^[a-fA-F0-9]+$", address) is None:
        #    raise ValueError('public key must contain only hex characters')
            return False
        #elif address.startswith("04"):
        #    raise ValueError('public key must start with 04')
        #   return False
        else:
            return True

    def verify(self, transaction: Transaction, signature):
        dataToVerify = (transaction.transID)
        print(dataToVerify)

        # public key for tests
        key_to_verify = self.__pub_key
        signer = PKCS1_v1_5.new(key_to_verify)
        newHash = SHA256.new()

        newHash.update(dataToVerify.encode("utf-8"))
        return signer.verify(newHash, signature)
