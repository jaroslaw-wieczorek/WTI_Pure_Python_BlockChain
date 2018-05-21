#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:38:34 2018

@author: afar
"""

import sys
sys.path += ['./ src/']

import unittest
import hashlib



from app.src.wallet import Wallet




from PyQt5.QtWidgets import QApplication, QMainWindow

from app.gui.mainwindow_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)



def show_gui():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

def tests():
    unittest.main()

def main():
    print("Untitled Coin")
    w = Wallet(48348)


if __name__ == "__main__":
    main()

    



    
