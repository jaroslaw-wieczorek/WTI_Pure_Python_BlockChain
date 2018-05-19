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

#txIN = [TransIN("transOutIdIN_TransIN","transOutIndexIN_TransIN","signaureIN_TransIN"), TransIN("transOutIdIN_TransIN_2","transOutIndexIN_TransIN_2","signaureIN_TransIN_2")]
#txOUT = [TransOUT("addresIN_TransOUT",13)]

#t = Transaction("idTransactionIN_Transaction", txIN, txOUT)
#t2=  Transaction("idTransactionIN_Transaction", txIN, txOUT)
#print(t)

#p = BlockPayload(t)


#h = BlockHeader(0, "previousHash_BlockHeader", 1318320, 1, 0)

#b = Block(h,p)
#b2 = Block(h,p)
#print(b)



#uT = [UnspentOutTrans(txIN[0].transOutId, txIN[0].transOutIndex, "AddressIN_UnspentOutTrans", 7), UnspentOutTrans(txIN[1].transOutId, txIN[1].transOutIndex, "2_AddressIN_UnspentOutTrans", 3)]

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


class EqualityTest(unittest.TestCase):

    def testExpectEqual(self):
        self.assertEqual(1, 3 - 2)

    def testExpectNotEqual(self):
        self.assertNotEqual(2, 3 - 2)




class SimplisticTest(unittest.TestCase):

    # basic assert True test
    def testPass(self):
        x = True
        self.assertTrue(x)
   
    # basic assert False test  
    def testFail(self):
        x = False
        self.assertFalse(x) 
       
    # basic assert Equal    
    def testEqual(self):
        x = 2 
        self.assertEqual(x, 2)
        
    def testPass(self):
        return

    def test_doNothing(self):
        pass


class AlmostEqualTest(unittest.TestCase):
   # Not pass Equal 1.1 != 1.8999999999996
    #def testEqual(self):
    #    self.assertEqual(1.1, 3.3 - 2.2)

    def testAlmostEqual(self):
        self.assertAlmostEqual(1.1, 3.3 - 2.2, places=1)

    def testNotAlmostEqual(self):
        self.assertNotAlmostEqual(1.1, 3.3 - 2.0, places=1)


   
    
    
class UntitledCoinTest(unittest.TestCase):
    
    def testInstances(self):
        self.assertIsInstance(b, Block)
      
   
    def testEqualBlock(self):
        self.assertIs(b, b)
        
    def testEqualHashFromBlock(self):
        
        first_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0), BlockPayload(t))
        secound_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0), BlockPayload(t))
        hf = (hashlib.sha256(str(first_block).encode("utf-8"))).hexdigest()
        hf2 = (hashlib.sha256(str(secound_block).encode("utf-8"))).hexdigest()
     
        self.assertEqual(hf,hf2)
    


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    unittest.main()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()

    



    
