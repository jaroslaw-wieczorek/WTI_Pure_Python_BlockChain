from copy import deepcopy


class TransactionPool:
    transactionPool = []

    def getTransactionPool(self):
        return deepcopy(self.transactionPool)

    def addToTransactionPool(self, transaction, unspentTxOuts):
        if not validateTransaction(transaction, unspentTxOuts):
            raise ValueError("Invalid tx, can not add.")
        if not isValidTxForPool(transaction, self.transactionPool):
            raise ValueError("Invalid tx, can not add.")
        print("Adding to the pool")
        print(transaction)
        self.transactionPool.append(transaction)

    def hasTxIn(self, txIn, unspentTxOuts):
        foundTxIn = [x for x in unspentTxOuts if x.txOutId == txIn.txOutId and x.txOutIndex == txIn.txOutIndex][0]
        if foundTxIn:   #TO_DO Verify if this works properly.
            return True
