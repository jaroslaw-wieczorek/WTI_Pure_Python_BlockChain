# -*- coding: utf-8 -*-


from interface import implements, Interface

class UI(Interface):
    
    def __init__(self, address):
        pass
    def method(self):
        pass


class GenericNode(Interface):
    def __init__(self):
        pass


class GenericBlockHeader(Interface):
    def __init__(self, index, previousHash, timestamp, difficulty, nonce):
        pass
    
        
class GenericBlockPayload(Interface):
    def __init__(self, data):
        pass
    
    
    
class GenericBlock(Interface):
    
    def __init__(self, blockHeader, blockPayload):
        pass

       # number, currentHash, previousHash, timestamp, Transaction, difficulty, number

    def __repr__(self):
        return str(self.__dict__)

    

class GenericUnspentOutTrans(Interface):
    def __init__(self, transOutId, transOutIndex, address: str, amount: int):
        pass


class GenericTransaction(Interface):
    def __init__(self, transOutId, transOutIndex, address, amount):
        pass
