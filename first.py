# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import os
import sys
import cv2 as cv
import pickle


dir = os.getcwd() + '/'
_translate = QtCore.QCoreApplication.translate
ui = uic.loadUiType(dir+'first.ui')[0]
distance = lambda p1,p2:(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**.5
area = lambda p1,p2:abs(p1[0]-p2[0])*abs(p1[1]-p2[1])

fontSize,textOrg = 2,(20,70)

cap = cv.VideoCapture(0)

class Form(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1034,584)
        self.setupUi(self)
        self.loadOptionValues()
        self.pushButton.clicked.connect(self.takeAPicture)
        self.pushButton_2.clicked.connect(self.saveOptionValues)
        self.show()
    
    def loadOptionValues(self):
        try:
            with open('optionsave.pyvars','rb') as f:
                self.blurStdDev.setValue(pickle.load(f))
                self.houghResolution.setValue(pickle.load(f))
                self.MINRAD.setValue(pickle.load(f))
                self.param1.setValue(pickle.load(f))
                self.param2.setValue(pickle.load(f))
                self.houghMinrad.setValue(pickle.load(f))
                self.houghMaxrad.setValue(pickle.load(f))
                self.circleRange.setValue(pickle.load(f))
                self.distStdDev.setValue(pickle.load(f))
                self.blurStdDev_2.setValue(pickle.load(f))
        except:
            pass

    def saveOptionValues(self):
        with open('optionsave.pyvars','wb') as f:
            pickle.dump(self.blurStdDev.value(),f)
            pickle.dump(self.houghResolution.value(),f)
            pickle.dump(self.MINRAD.value(),f)
            pickle.dump(self.param1.value(),f)
            pickle.dump(self.param2.value(),f)
            pickle.dump(self.houghMinrad.value(),f)
            pickle.dump(self.houghMaxrad.value(),f)
            pickle.dump(self.circleRange.value(),f)
            pickle.dump(self.distStdDev.value(),f)
            pickle.dump(self.blurStdDev_2.value(),f)
            
    
    def isBothCircle(self,contours,centers) -> bool:
        for c in range(len(contours[:])):
            centre = centers[c]
            l = []
            for i in contours[c][:10]:
                l.append(distance(centre,list(i[0])))
            mean = sum(l)/len(l)
            a = 0
            for i in l:
                a+=(i-mean)**2
            sigma = (a/len(l))**.5
            #print(sigma)
            if sigma > self.distStdDev.value():
                return False
        return True

    def takeAPicture(self):
        #labelsize = (781,561)  #original
        labelsize = (781,439)  #16:9 MBP 1080p webcam
        #labelsize = (747,561)  #raspberry pi V2 cam

        #?????? ??????
        #ret, img = cap.read()
        #?????? ?????? ????????????
        img = cv.imread('test3.jpeg')
        
        #???????????? ??????
        img_blur = cv.GaussianBlur(img,(1,1),self.blurStdDev.value())
        #????????? ??????
        #img_blur = cv.medianBlur(img,5)

        #????????? ????????????
        img_gray = cv.cvtColor(img_blur,cv.COLOR_BGR2GRAY)

        #?????? ?????????
        binary = eval(self.threshold.currentText())
        ret, img_binary = cv.threshold(img_gray,127,255,binary)

        #?????? ??????
        circles = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,self.houghResolution.value(),self.MINRAD.value(),param1=self.param1.value(),param2=self.param2.value(),minRadius=self.houghMinrad.value(),maxRadius=self.houghMaxrad.value())

        #??????????????? ?????? ??????????????? ???
        if circles is not None:
            #????????????
            if len(circles[0]) > 2:
                img = cv.putText(img,'Too many circles detected.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(0,255,0),2)
            #1 or 2??? ??????
            else:
                #????????? ?????? ?????????
                rects = []
                for i in circles[0,:]:
                    aas = i[2] + self.circleRange.value()
                    r1 = int(i[0]-aas),int(i[1]-aas)
                    r2 = int(i[0]+aas),int(i[1]+aas)
                    rects.append((r1,r2))
                    #cv.rectangle(img,r1,r2,(0,0,255),1)
                

                #????????? ????????? ???????????????
                rect = rects[0]

                #???????????? ???????????? ??? ?????? ??? ???????????????
                if len(circles[0])==2:
                    if area(rects[0][0],rects[0][1]) > area(rects[1][0],rects[1][1]):
                        rect = rects[0]
                    else:
                        rect = rects[1]

                #????????? ?????? ????????? ???????????? ??????
                im = img[rect[0][1]:rect[1][1],rect[0][0]:rect[1][0]]
                
                #????????? ????????? ??????, ??????, ?????????
                try:
                    im_blur = cv.GaussianBlur(im,(1,1),self.blurStdDev_2.value())
                except:
                    im_blur = cv.medianBlur(im,int(self.blurStdDev_2.value()))
                im_gray = cv.cvtColor(im_blur,cv.COLOR_BGR2GRAY)
                ret, im_binary = cv.threshold(im_gray,127,255,binary)

                #????????? ????????? ????????? ??????
                contours, hierarchy = cv.findContours(im_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
                centers = []
                for c in range(len(contours[:])):
                    cv.drawContours(im,[contours[c]],0,(0,255,0),1)
                    M = cv.moments(contours[c])
                    try:
                        cx = int(M['m10']/M['m00'])
                    except ZeroDivisionError:
                        cx = int(M['m10'])
                    try:
                        cy = int(M['m01']/M['m00'])
                    except ZeroDivisionError:
                        cy = int(M['m01'])
                    centre = (cx,cy)
                    centers.append(centre)

                    cv.circle(im,(cx,cy),2,(255,0,0),-1)
                cv.imshow('cropped image',im)

                if self.isBothCircle(contours,centers):
                    img = cv.putText(img,'Perfect Circle.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(255,0,0),2)
                else:
                    img = cv.putText(img,'Not a Circle.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(0,0,255),2)

                #???????????? ????????? ?????????
                for i in rects:
                    cv.rectangle(img,i[0],i[1],(127,255,0),3)

        #??? ?????????
        else:
            img = cv.putText(img,'No circles detected.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(0,255,0),2)

        #????????? ??????
        img1 = cv.resize(img, dsize=labelsize, interpolation=cv.INTER_AREA)
        img1 = cv.cvtColor(img1,cv.COLOR_BGR2RGB)
        h,w,c = img1.shape
        qImg = QtGui.QImage(img1.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.imglabel.setPixmap(pixmap)

        

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())