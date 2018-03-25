#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""


import sys
sys.path += ['src/generics']

from src.node import Node

from src.transIN import TransIN
from src.transOUT import TransOUT
from src.transaction import Transaction
from src.unspentOutTrans import UnspentOutTrans
from src.blockPayload import BlockPayload
from src.blockHeader import BlockHeader
from src.block import Block
from src.wallet import Wallet



# Tests

txIN = [TransIN("transOutIdIN_TransIN","transOutIndexIN_TransIN","signaureIN_TransIN"), TransIN("transOutIdIN_TransIN_2","transOutIndexIN_TransIN_2","signaureIN_TransIN_2")]
txOUT = [TransOUT("addresIN_TransOUT",13)]

t = Transaction("idTransactionIN_Transaction", txIN, txOUT)
print(t)

p = BlockPayload(t)

h = BlockHeader(0, "previousHash_BlockHeader", 1318320, 1, 0)

uT = [UnspentOutTrans(txIN[0].transOutId, txIN[0].transOutIndex, "AddressIN_UnspentOutTrans", 7), UnspentOutTrans(txIN[1].transOutId, txIN[1].transOutIndex, "2_AddressIN_UnspentOutTrans", 3)]


n = Node()
print(n.calculateHash(h,p))

#n.findNextBlock(b)
n.signTransIN(t, 0, uT)
w = Wallet(48348)
Wallet(23)
