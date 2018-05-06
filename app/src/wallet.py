# -*- coding: utf-8 -*-

from interface import implements

from .generics.interfaces import UI


class Wallet(implements(UI)):
    
    
    def __init__(self, address):
        super()
        
        
    def method(self):
        print("to działa")
    
    def method_b(self):
        print("to działa")


