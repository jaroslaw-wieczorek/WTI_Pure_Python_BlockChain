# -*- coding: utf-8 -*-

from interface import implements
from src.generics.interfaces import GenericUnspentOutTrans



class UnspentOutTrans(implements(GenericUnspentOutTrans)):
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def __repr__(self):
        return str(self.__dict__)
