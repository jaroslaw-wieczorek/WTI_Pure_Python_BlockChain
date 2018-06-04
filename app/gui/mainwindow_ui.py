# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/afar/WTI_Pure_Python_BlockChain/app/gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WalletDialog(object):
    def setupUi(self, WalletDialog):
        WalletDialog.setObjectName("WalletDialog")
        WalletDialog.resize(394, 551)
        self.verticalLayout = QtWidgets.QVBoxLayout(WalletDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_my_address = QtWidgets.QLabel(WalletDialog)
        self.label_my_address.setAlignment(QtCore.Qt.AlignCenter)
        self.label_my_address.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_my_address.setObjectName("label_my_address")
        self.verticalLayout.addWidget(self.label_my_address)
        self.label_balance = QtWidgets.QLabel(WalletDialog)
        self.label_balance.setObjectName("label_balance")
        self.verticalLayout.addWidget(self.label_balance)
        self.line_edit_balance = QtWidgets.QLineEdit(WalletDialog)
        self.line_edit_balance.setObjectName("line_edit_balance")
        self.verticalLayout.addWidget(self.line_edit_balance)
        self.label_address_reciver = QtWidgets.QLabel(WalletDialog)
        self.label_address_reciver.setObjectName("label_address_reciver")
        self.verticalLayout.addWidget(self.label_address_reciver)
        self.line_edit_address = QtWidgets.QLineEdit(WalletDialog)
        self.line_edit_address.setObjectName("line_edit_address")
        self.verticalLayout.addWidget(self.line_edit_address)
        self.label_value = QtWidgets.QLabel(WalletDialog)
        self.label_value.setObjectName("label_value")
        self.verticalLayout.addWidget(self.label_value)
        self.line_edit_value = QtWidgets.QLineEdit(WalletDialog)
        self.line_edit_value.setObjectName("line_edit_value")
        self.verticalLayout.addWidget(self.line_edit_value)
        self.label_status = QtWidgets.QLabel(WalletDialog)
        self.label_status.setObjectName("label_status")
        self.verticalLayout.addWidget(self.label_status)
        self.text_edit_status = QtWidgets.QTextEdit(WalletDialog)
        self.text_edit_status.setObjectName("text_edit_status")
        self.verticalLayout.addWidget(self.text_edit_status)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.push_button_pay = QtWidgets.QPushButton(WalletDialog)
        self.push_button_pay.setObjectName("push_button_pay")
        self.horizontal_layout.addWidget(self.push_button_pay)
        self.push_button_refresh = QtWidgets.QPushButton(WalletDialog)
        self.push_button_refresh.setObjectName("push_button_refresh")
        self.horizontal_layout.addWidget(self.push_button_refresh)
        self.verticalLayout.addLayout(self.horizontal_layout)

        self.retranslateUi(WalletDialog)
        QtCore.QMetaObject.connectSlotsByName(WalletDialog)

    def retranslateUi(self, WalletDialog):
        _translate = QtCore.QCoreApplication.translate
        WalletDialog.setWindowTitle(_translate("WalletDialog", "Dialog"))
        self.label_my_address.setText(_translate("WalletDialog", "Wallet: ${myaddress}"))
        self.label_balance.setText(_translate("WalletDialog", "Saldo:"))
        self.label_address_reciver.setText(_translate("WalletDialog", "Adres odbiorcy:"))
        self.label_value.setText(_translate("WalletDialog", "Kwota:"))
        self.label_status.setText(_translate("WalletDialog", "Status:"))
        self.text_edit_status.setHtml(_translate("WalletDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.push_button_pay.setText(_translate("WalletDialog", "Zapłać"))
        self.push_button_refresh.setText(_translate("WalletDialog", "Odśwież saldo"))

