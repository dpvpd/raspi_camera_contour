# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os
import sys
import cv2 as cv

dir = os.getcwd() + '/'
_translate = QtCore.QCoreApplication.translate
ui = uic.loadUiType(dir+'untitled.ui')[0]
distance = lambda p1,p2:(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**.5
MINRAD = 20

binary = cv.ADAPTIVE_THRESH_GAUSSIAN_C
#binary = cv.ADAPTIVE_THRESH_MEAN_C
#binary = cv.THRESH_BINARY + cv.THRESH_OTSU
#binary = 0


class Form(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1501,795)
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())