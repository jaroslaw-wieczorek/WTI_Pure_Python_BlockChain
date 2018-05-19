# -*- coding: utf-8 -*-

from interface import implements

from .generics.interfaces import UI

import os
import re
import sys
import hashlib
import datetime
import binascii
import operator 
from datetime import timezone
from functools import reduce

from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 

from Crypto import Random

# importing data accc
lib_path = os.path.abspath(os.path.join(__file__, '..','..','rsa_keys/key.pem'))
sys.path.append(lib_path)



class Wallet(implements(UI)):
    
    def __init__(self, address):
        # PRIVATE KEY
        self.__privateFileKey = open(lib_path, "r").read()
       
        # PUBLIC KEY
        self.__publicKey = None
        #self.__pub_key = open("key.pub", "r").read()
        super()
        
    def getPrivateFromWallet(self) -> str: 
        self.__privKey = RSA.importKey(self.__privateFileKey) 
        return self.__privKey
    
    def getPublicFromWallet(self) -> str: 
        self.__publKey = self.getPrivateFromWallet().publickey().exportKey()
        return self.__publKey
    
    
    def generatePrivateKey(self) -> str:
        '''
            Generate an RSA keypair in PEM format
            param: bits The key length in bits
            Return private key and public key
        '''
        rng = Random.new().read
        new_key = RSA.generate(1024, rng) 
        self.__privKey = new_key.exportKey("PEM") 
        
        with open(lib_path, 'wb') as pem:
            pem.write(self.__privKey)
            pem.close()
        
        return str(lib_path)
    

    def initWallet(self):
        if os.path.isfile(lib_path):
            return
        else:
            newPrivateKey = self.generatePrivateKey()
            print("new wallet with private key created to : " % newPrivateKey)
   
    
    def deleteWallet(self):
        if os.path.isfile(lib_path):
            os.remove(lib_path)
            


