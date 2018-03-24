# -*- coding: utf-8 -*-

from interface import implements

from src.generics.interfaces import UI


class Wallet(implements(UI)):
    def __init__(self, address):
        super()
        pass
    
    def method(self):
        print("to działa")
    
    def method_b(self):
        print("to działa")


