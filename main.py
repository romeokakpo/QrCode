#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 19:43:59 2022

@author: romeo
"""
import sys
import pyqrcode
import png


from PyQt5.QtWidgets import (QWidget,QApplication, QMainWindow,QDesktopWidget,
                             QLabel,QHBoxLayout,QLineEdit,QPushButton,QVBoxLayout,
                             QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QSize


class QrCode:
    def __init__(self,text):
        self.text = text
        self.image = "preview.jpg"
        
    def generate(self):
        code = pyqrcode.create(self.text)
        new_link = self.text.replace(" ", "_")
        self.image = "qrcodes/"+new_link+".png"
        code.png(self.image, scale=6)
    
class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        #Le code QR
        self.CODEQR = QrCode('')
        
        #Configuration de la fenêtre
        self.widgetCode = QWidget()
        self.setWindowTitle("QrCode")
        self.setFixedSize(400, 400)
        self.center()
        self.style()
        self.layout()
        self.setCentralWidget(self.widgetCode)
        self.setStatusBarMessage()
        
        self.butonGenerate.clicked.connect(self.generate)
        self.buttonReset.clicked.connect(self.clearImg)

        
    def center(self):
        """"
            Méthode pour centrer la fenêtre
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def layout(self):
        mainLayout = QVBoxLayout(self.widgetCode)
        
        title = QLabel("QRCode Generator")
        title.setIndent(5)
        
        #2
        layout = QHBoxLayout()
        
        self._input = QLineEdit()
        self._input.setPlaceholderText("Enter the text to code:")
        self.butonGenerate = QPushButton("Generate")
        
        layout.addWidget(self._input,2)
        layout.addWidget(self.butonGenerate,1)
        
        #3
        layout2 = QVBoxLayout()
        
        ### Code Qr View ###
        self.qrView = QLabel()
        qpix = QPixmap(self.CODEQR.image)
        qpix = qpix.scaled(250, 250, Qt.KeepAspectRatio)
        
        self.qrView.setPixmap(qpix)
        
        self.qrView.setFixedSize(250,250)
        ###
        
        self.buttonReset = QPushButton("Reset")
        self.buttonReset.setObjectName('reset')
        self.buttonReset.setFixedWidth(150)
        
        buttonLayout =  QHBoxLayout()
        buttonLayout.addWidget(self.buttonReset)
        
        layout2.addWidget(self.qrView,0,Qt.AlignHCenter)
        layout2.addLayout(buttonLayout)
        
        mainLayout.addWidget(title)
        mainLayout.addLayout(layout)
        mainLayout.addLayout(layout2)
        
    
    def style(self):
        """
            Méthode pour gérer le style de la fenêtre
        """
        self.setStyleSheet(open('style.css').read())
        
    def setStatusBarMessage(self):
        self.statusBar().showMessage("By Roméo KAKPO")
    
    def generate(self):
        if self._input.text():
            self.CODEQR.text = self._input.text()
            self.CODEQR.generate()
            qpix = QPixmap(self.CODEQR.image)
            qpix = qpix.scaled(250, 250, Qt.KeepAspectRatio)
            self.qrView.setPixmap(qpix)
    
    def clearImg(self):
        self._input.setText("")
        self.CODEQR.text = ''
        self.CODEQR.image = "preview.jpg"
        qpix = QPixmap(self.CODEQR.image)
        qpix = qpix.scaled(250, 250, Qt.KeepAspectRatio)
        self.qrView.setPixmap(qpix)
             

#Vérification si une instance de l'application est en cours
app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
#Création de la fenêtre
fen = Window()
fen.show()

app.exec_()