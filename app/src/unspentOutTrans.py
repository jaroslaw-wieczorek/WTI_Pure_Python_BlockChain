# -*- coding: utf-8 -*-

from interface import implements
from .generics.interfaces import GenericUnspentOutTrans



class UnspentOutTrans(implements(GenericUnspentOutTrans)):
    def __init__(self, transOutId, transOutIndex, address: str, amount: int):
        self.amount = amount
        self.address = address
        self.transOutId = transOutId
        self.transOutIndex = transOutIndex


    def __repr__(self):
        return str(self.__dict__)
