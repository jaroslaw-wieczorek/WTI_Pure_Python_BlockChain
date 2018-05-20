#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""


import unittest
import hashlib

from .src.node import Node

from .src.transIN import TransIN
from .src.transOUT import TransOUT
from .src.transaction import Transaction
from .src.transactionPool import TransactionPool
from .src.unspentOutTrans import UnspentOutTrans
from .src.blockPayload import BlockPayload
from .src.blockHeader import BlockHeader
from .src.block import Block
from .src.wallet import Wallet


import sys
#sys.path += ['src/generics']

from PyQt5.QtWidgets import QApplication, QMainWindow

from .gui.mainwindow_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)



# Tests

txIN = [TransIN("transOutIdIN_TransIN","transOutIndexIN_TransIN","signaureIN_TransIN"), TransIN("transOutIdIN_TransIN_2","transOutIndexIN_TransIN_2","signaureIN_TransIN_2")]
txOUT = [TransOUT("addresIN_TransOUT",13)]

t = Transaction("idTransactionIN_Transaction", txIN, txOUT)
t2=  Transaction("idTransactionIN_Transaction", txIN, txOUT)
#print(t)

#p = BlockPayload(t)


#h = BlockHeader(0, "previousHash_BlockHeader", 1318320, 1, 0)

#b = Block(h,p)
#b2 = Block(h,p)
#print(b)

#uT = UnspentOutTrans(txIN[0].transOutId, txIN[0].transOutIndex, "AddressIN_UnspentOutTrans", 7)
#tp = TransactionPool()
#tp.addToTransactionPool(t, uT)
#tp.addToTransactionPool(t2, uT)


n = Node()
#print(n.calculateHash(h,p))
#print("Difficulty")
#print(n.getSumDifficulty([b,b2]))

#n.findNextBlock(b)
#print(n.signTransIN(t, 0, uT))
#print(n.verify(t,n.signTransIN(t, 0, uT)))

w = Wallet(48348)
Wallet(23)
#print(n.getCurrentTimestamp())

#w.filterTranPoolTrans(uT,tp)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    unittest.main()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()

    



    
