#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""

from interface import implements, Interface


class UI(Interface):
    
    def __init__(self, address):
        pass 
    def method(self):
        pass


class Wallet(implements(UI)):
    def __init__(self, address):
        super()
        pass
    def method(self, f):
        print("to działa")
    
    def method_b(self):
        print("to działa")



class GenericBlock(Interface):
    def method(self, a, b):
        pass

class Block(implements(GenericBlock)):
    def method(self, a,b):
        return "This should work"


b = Block()

print(b.method(4,4))

w = Wallet(48348)

w.method_b()