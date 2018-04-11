#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:27:37 2018

"""

from interface import implements
from src.generics.interfaces import GenericTransaction


class Transaction(implements(GenericTransaction)):
    def __init__(self, transID, transIN, transOUT):
        self.transID = transID
        self.transIN = transIN
        self.transOUT = transOUT
        
    def __repr__(self):
        return str(self.__dict__)

