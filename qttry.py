# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import os
import sys
import cv2 as cv

dir = os.getcwd() + '/'
_translate = QtCore.QCoreApplication.translate
ui = uic.loadUiType(dir+'untitled.ui')[0]
distance = lambda p1,p2:(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**.5
MINRAD = 20

#binary = cv.ADAPTIVE_THRESH_GAUSSIAN_C
binary = cv.ADAPTIVE_THRESH_MEAN_C
#binary = cv.THRESH_BINARY + cv.THRESH_OTSU
#binary = 0
cap = cv.VideoCapture(0)

class Form(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1501,795)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.takeAPicture)
        self.show()

    def takeAPicture(self):
        labelsize = (491,276)
        ret, img = cap.read()
        #img = cv.imread('donut.jpeg')
        img1 = cv.resize(img, dsize=labelsize, interpolation=cv.INTER_AREA)
        img1 = cv.cvtColor(img1,cv.COLOR_BGR2RGB)
        h,w,c = img1.shape
        qImg = QtGui.QImage(img1.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)
        
        img_blur = cv.GaussianBlur(img,(0,0),5)
        img_blur_rs = cv.resize(img_blur, dsize=labelsize, interpolation=cv.INTER_AREA)
        img_blur_rs = cv.cvtColor(img_blur_rs,cv.COLOR_BGR2RGB)
        h,w,c = img_blur_rs.shape
        qImg = QtGui.QImage(img_blur_rs.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label_2.setPixmap(pixmap)

        img_gray = cv.cvtColor(img_blur,cv.COLOR_BGR2GRAY)
        #cv.imshow('gray',img_gray)
        img_gray_rs = cv.resize(img_gray, dsize=labelsize, interpolation=cv.INTER_AREA)
        img_gray_rs = cv.cvtColor(img_gray_rs,cv.COLOR_GRAY2RGB)
        h,w,c = img_gray_rs.shape
        qImg = QtGui.QImage(img_gray_rs.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label_5.setPixmap(pixmap)

        ret, img_binary = cv.threshold(img_gray,127,255,binary)
        img_binary_rs = cv.resize(img_binary, dsize=labelsize, interpolation=cv.INTER_AREA)
        img_binary_rs = cv.cvtColor(img_binary_rs,cv.COLOR_GRAY2RGB)
        h,w,c = img_binary_rs.shape
        qImg = QtGui.QImage(img_binary_rs.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label_3.setPixmap(pixmap)
        
        img_contour = img
        contours, hierarchy = cv.findContours(img_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
        diss = []
        for c in range(len(contours[:-1])):
            cv.drawContours(img_contour,[contours[c]],0,(0,255,0),2)
            M = cv.moments(contours[c])
            try:
                cx = int(M['m10']/M['m00'])
            except:
                cx = int(M['m10'])
            try:
                cy = int(M['m01']/M['m00'])
            except:
                cy = int(M['m01'])
            centre = (cx,cy)
            
            l = []
            for i in contours[c][:10]:
                l.append(distance(centre,list(i[0])))
            a = 0
            mean = sum(l)/len(l)
                
            #dic = {'data':l,'mean':mean,'sigma':}
            cv.circle(img_contour,(cx,cy),2,(255*((c+1)%2),0,255*(c%2)),-1)
        img_contour_rs = cv.resize(img_contour, dsize=labelsize, interpolation=cv.INTER_AREA)
        img_contour_rs = cv.cvtColor(img_contour_rs,cv.COLOR_BGR2RGB)
        h,w,c = img_contour_rs.shape
        qImg = QtGui.QImage(img_contour_rs.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label_4.setPixmap(pixmap)

        img_circle = img
        circles = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,0.125,MINRAD,param1=80,param2=37.5,minRadius=0,maxRadius=0)
        if circles is not None:
            for i in circles[0,:]:
                cv.circle(img_circle,(int(i[0]),int(i[1])),int(i[2]),(0,0,255),2)
                aas = i[2]#//(2**.5)
                r1 = i[0]-aas,i[1]-aas
                r2 = i[0]+aas,i[1]+aas
                cv.rectangle(img_circle,(int(r1[0]),int(r1[1])),(int(r2[0]),int(r2[1])),(0,0,255),2)
        img_circle_rs = cv.resize(img_circle, dsize=labelsize, interpolation=cv.INTER_AREA)
        img_circle_rs = cv.cvtColor(img_circle_rs,cv.COLOR_BGR2RGB)
        h,w,c = img_circle_rs.shape
        qImg = QtGui.QImage(img_circle_rs.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label_6.setPixmap(pixmap)
        


if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())