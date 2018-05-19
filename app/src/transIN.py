#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:27:56 2018

"""

class TransIN():
    def __init__(self, transOutId,  transOutIndex, signature):
        self.transOutId = transOutId
        self.transOutIndex = transOutIndex
        self.signature = signature

    def __repr__(self):
        return str(self.__dict__)
