#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""

import sys
sys.path += ['./ src/']
import json
import unittest
import hashlib



from app.src.wallet import Wallet
from app.src.node import Node
from app.src.transactionPool import TransactionPool




from PyQt5.QtWidgets import QApplication, QDialog

from app.gui.mainwindow_ui import Ui_WalletDialog

class MainWindow(QDialog, Ui_WalletDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)



def show_gui():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

def tests():
    unittest.main()

def main():
    print("Untitled Coin")
    pool = TransactionPool()
    w0 = Wallet(48348)
    w1 = Wallet("1")
    n = Node(w0, pool)

    print("wallet1")
    print(w1.getBalance(w1.getPublicFromWallet(), n.getUnspentTransOuts()))
    print("wallet0")
    print(w0.getBalance(w0.getPublicFromWallet(), n.getUnspentTransOuts()))
    trans = w0.createTransaction(w1.getPublicFromWallet(), 50, w0.getPrivateFromWallet(), n.getUnspentTransOuts(),[])
    pool.addToTransactionPool(trans, n.getUnspentTransOuts())
    n.generateNextBlock()
    print(n.getBlockchain())
    print("wallet1")
    print(w1.getBalance(w1.getPublicFromWallet(), n.getUnspentTransOuts()))
    print("wallet0")
    print(w0.getBalance(w0.getPublicFromWallet(), n.getUnspentTransOuts()))
    trans2 = w0.createTransaction(w1.getPublicFromWallet(), 50, w0.getPrivateFromWallet(), n.getUnspentTransOuts(),pool.getTransactionPool())
    pool.addToTransactionPool(trans2, n.getUnspentTransOuts())
    n.generateNextBlock()
    print("wallet1")
    print(w1.getBalance(w1.getPublicFromWallet(), n.getUnspentTransOuts()))
    print("wallet0")
    print(w0.getBalance(w0.getPublicFromWallet(), n.getUnspentTransOuts()))
    trans3 = w0.createTransaction(w1.getPublicFromWallet(), 25, w0.getPrivateFromWallet(), n.getUnspentTransOuts(),
    pool.getTransactionPool())
    pool.addToTransactionPool(trans3, n.getUnspentTransOuts())
    n.generateNextBlock()
    print("wallet1")
    print(w1.getBalance(w1.getPublicFromWallet(), n.getUnspentTransOuts()))
    print("wallet0")
    print(w0.getBalance(w0.getPublicFromWallet(), n.getUnspentTransOuts()))
    trans4 = w0.createTransaction(w1.getPublicFromWallet(), 6.666, w0.getPrivateFromWallet(), n.getUnspentTransOuts(),
    pool.getTransactionPool())
    pool.addToTransactionPool(trans4, n.getUnspentTransOuts())
    n.generateNextBlock()
    print("wallet1")
    print(w1.getBalance(w1.getPublicFromWallet(), n.getUnspentTransOuts()))
    print("wallet0")
    print(w0.getBalance(w0.getPublicFromWallet(), n.getUnspentTransOuts()))
    trans5 = w0.createTransaction(w1.getPublicFromWallet(), 69.69696, w0.getPrivateFromWallet(), n.getUnspentTransOuts(),
    pool.getTransactionPool())
    pool.addToTransactionPool(trans5, n.getUnspentTransOuts())
    trans6 = w0.createTransaction(w1.getPublicFromWallet(), 9, w0.getPrivateFromWallet(), n.getUnspentTransOuts(),
    pool.getTransactionPool())
    pool.addToTransactionPool(trans6, n.getUnspentTransOuts())
    n.generateNextBlock()
    print("wallet1")
    print(w1.getBalance(w1.getPublicFromWallet(), n.getUnspentTransOuts()))
    print("wallet0")
    print(w0.getBalance(w0.getPublicFromWallet(), n.getUnspentTransOuts()))
    print(n.getBlockchain())

if __name__ == "__main__":
    main()

    



    
