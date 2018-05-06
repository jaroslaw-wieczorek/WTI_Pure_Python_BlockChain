from copy import deepcopy


class TransactionPool:
    transactionPool = []

    def getTransactionPool(self):
        """Returns the local pool of Transactions."""
        return deepcopy(self.transactionPool)

    def addToTransactionPool(self, transaction, unspentTxOuts):
        """Adds transactions to the Pool, validates before hand."""
        if not validateTransaction(transaction, unspentTxOuts):
            raise ValueError("Invalid tx, can not add.")
        if not isValidTxForPool(transaction, self.transactionPool):
            raise ValueError("Invalid tx, can not add.")
        print("Adding to the pool")
        print(transaction)
        self.transactionPool.append(transaction)

    def hasTxIn(self, txIn, unspentTxOuts):
        """Returns True if txIn Id and Index exist in the unspentTxOuts."""
        foundTxIn = [x for x in unspentTxOuts if x.txOutId == txIn.txOutId and x.txOutIndex == txIn.txOutIndex][0]
        if foundTxIn:   #TO_DO Verify if this works properly.
            return True

    def updateTransactionPool(self, unspentTxOut):
        """Updates the pool by removing invalid transactions.
        Invalid transactions can be:
        *Transactions already mined,
        *The unspent out was spent by some other transaction, making this one invalid."""

        invalidTxs = []
        for tx in self.transactionPool:
            for txIn in tx.transIN:
                if not self.hasTxIn(txIn, unspentTxOut):
                    invalidTxs.append(tx)
                    break
        if len(invalidTxs) > 0:
            print("Removing transactions from the Pool:")
            print(invalidTxs)
            print("They where probably mined or spent elsewhere.")
            self.transactionPool = list(set(self.transactionPool)-set(invalidTxs))
            #We should not have duplicate values, and this approach is suprisingly fast!
            #252s vs 0.75s for 500000 array.
            #Which is a good thing because theoretically we could have very big lists here.
            #Source: https://stackoverflow.com/a/30353802
