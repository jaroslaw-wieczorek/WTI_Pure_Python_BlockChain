from copy import deepcopy

import itertools

from .transactionMethods import TransMethods

class TransactionPool(TransMethods):
    transactionPool = []

    def getTransactionPool(self):
        """Returns the local pool of Transactions."""
        return deepcopy(self.transactionPool)

    def getTransactionPoolIns(self, xTransactionPool):
        """Returns all transaction ins for the given TransactionPool."""
        return list(itertools.chain.from_iterable(list(map(lambda trans: trans.transINs, xTransactionPool))))
        #Fast Python flatten:
        #https://stackoverflow.com/a/952952

    def addToTransactionPool(self, transaction, unspentTransOuts):
        """Adds transactions to the Pool, validates before hand."""
        if not self.validateTransaction(transaction, unspentTransOuts):
            raise ValueError("Invalid trans, can not add.")
        if not self.isValidTransForPool(transaction, self.transactionPool):
            raise ValueError("Invalid trans, can not add.")
        print("Adding to the pool")
        print(transaction)
        self.transactionPool.append(transaction)

    def hasTransIn(self, transIn, unspentTransOuts):
        """Returns True if transIn Id and Index exist in the unspentransOuts."""
        foundTransIn = [x for x in unspentTransOuts if x.transOutId == transIn.transOutId and x.transOutIndex == transIn.transOutIndex]
        if len(foundTransIn)>0:   #TO_DO Verify if this works properly.
            return True

    def updateTransactionPool(self, unspentTransOut):
        """Updates the pool by removing invalid transactions.
        Invalid transactions can be:
        *Transactions already mined,
        *The unspent out was spent by some other transaction, making this one invalid."""

        invalidTransactions = []
        for trans in self.transactionPool:
            for transIn in trans.transINs:
                if not self.hasTransIn(transIn, unspentTransOut):
                    invalidTransactions.append(trans)
                    break
        if len(invalidTransactions) > 0:
            print("Removing transactions from the Pool:")
            print(invalidTransactions)
            print("They where probably mined or spent elsewhere.")
            self.transactionPool = list(set(self.transactionPool)-set(invalidTransactions))
            #We should not have duplicate values, and this approach is suprisingly fast!
            #252s vs 0.75s for 500000 array.
            #Which is a good thing because theoretically we could have very big lists here.
            #Source: https://stackoverflow.com/a/30353802

    def containsTransIn(self, transIns,transIn):
        """Returns the transaction if it exists in the list."""
        trans = [x for x in transIns if x.transOutId == transIn.transOutId and x.transOutIndex == transIn.transOutIndex]
        if len(trans) > 0:
            return trans
        else:
            return []

    def isValidTransForPool(self, trans, xTransactionPool):
        """Checks if the transaction is not a duplicate of an already existing transaction in the Pool."""
        transPoolIns = self.getTransactionPoolIns(xTransactionPool)
        for transIn in trans.transINs:
            if self.containsTransIn(transPoolIns, transIn):
                print("TransactionIn already exists in the Pool.")
                return False
        return True
