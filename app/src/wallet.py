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


# importing data accc
lib_path = os.path.abspath(os.path.join(__file__, '..', 'gui'))
sys.path.append(lib_path)


class Wallet(implements(UI)):
    
    def __init__(self, address):
        
        privateKeyLocation = 
        super()
        
        
    def method(self):
        print("to działa")
    
    def method_b(self):
        print("to działa")


