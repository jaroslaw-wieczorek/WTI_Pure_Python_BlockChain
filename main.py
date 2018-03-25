#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""


import sys
sys.path += ['src/generics']

from src.wallet import Wallet
from src.node import Node

from src.transIN import TransIN
from src.transOUT import TransOUT
from src.transaction import Transaction
from src.blockPayload import BlockPayload
from src.blockHeader import BlockHeader
from src.block import Block



# Tests

txIN = [TransIN(1,2,"signaure"), TransIN(1,1,"signaure")]
txOUT = [TransOUT("ADRES_WALLETA",50)]

t = Transaction(1, txIN, txOUT)
print(t)

p = BlockPayload(t)

h = BlockHeader(0, "dfsfisd", 1318320, 1, 0)

b = Block(h,p)

n = Node()
n.getTransactionId(t)

n.findNextBlock(b)

w = Wallet(48348)
Wallet(23)
