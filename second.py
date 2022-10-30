# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import os
import sys
import cv2 as cv
import pickle
import math

output = ''


dir = os.getcwd() + '/'
_translate = QtCore.QCoreApplication.translate
ui = uic.loadUiType(dir+'second.ui')[0]
distance = lambda p1,p2:(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**.5
area = lambda p1,p2:abs(p1[0]-p2[0])*abs(p1[1]-p2[1])
#types = [('PNG file','.png'),('JPEG file','jpeg'),('JPG file','.jpg'),('BITMAP IMAGE','.bmp')]
ftypes = 'image files (*.png *.jpeg *.jpg *.bmp);; all files (*.*)'

fontSize,textOrg = 2,(10,80)


class Form(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1213,584)
        self.setupUi(self)
        self.loadOptionValues()
        self.output = ''
        self.pushButton.clicked.connect(self.takeAPicture)
        self.pushButton_2.clicked.connect(self.saveOptionValues)
        self.FindFile.clicked.connect(self.setFilePath)
        self.pushButton_3.clicked.connect(self.loadImage)
        self.pushButton_4.clicked.connect(exit)
        self.show()

    def setFilePath(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image File',dir,ftypes)[0].replace('\\','/')
        #print(path)
        self.FilePath.setText(_translate("Dialog", path))
        return
    
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
                self.distance.setValue(pickle.load(f))
                self.CamAngle.setValue(pickle.load(f))
                self.FilePath.setText(pickle.load(f))
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
            pickle.dump(self.distance.value(),f)
            pickle.dump(self.CamAngle.value(),f)
            pickle.dump(self.FilePath.text(),f)
            
    
    def isBothCircle(self,contours,centers) -> bool:
        global output
        for c in range(2):#range(len(contours)):#
            centre = centers[c]
            l = []
            for i in contours[c]:
                l.append(distance(centre,list(i[0])))
            mean = sum(l)/len(l)
            a = 0
            for i in l:
                a+=(i-mean)**2
            sigma = (a/len(l))**.5
            if sigma > self.distStdDev.value():
                return False
        return True
    def isCircle(self,contours,centers) -> tuple:
        output = ''
        l = []
        for i in contours:
            l.append(distance(centers,list(i[0])))
        mean = sum(l)/len(l)
        a = 0
        for i in l:
            a+=(i-mean)**2
        sigma = (a/len(l))**.5
        output += 'Std.Dev. = '+str(sigma)+'\n'

        if sigma > self.distStdDev.value():
            return False,output
        return True,output

    def takeAPicture(self):
        cap = cv.VideoCapture(0)
        while cap.isOpened():
            ret, img = cap.read()
            self.calc(img)
            break
        cap.release()
        cv.imshow('asdf',img)

    def loadImage(self):
        FileName = self.FilePath.text()
        try:
            img = cv.imread(FileName)
            #self.calc(img)
        except:
            QtWidgets.QMessageBox.critical(self,'Wrong File!','Wrotten File Path is Wrong. \nPlease check the Path or File is exist. ',QtWidgets.QMessageBox.Yes)
            return

        self.calc(img)
    
    def calc(self,img):
        #labelsize = (781,561)  #original
        #labelsize = (781,439)  #16:9 MBP 1080p webcam
        labelsize = (748,561)  #4:3 ZFold3 120mp rearside cam
        #labelsize = (747,561)  #raspberry pi V2 cam
        self.output = ''

        #사진 찍기
        #ret, img = cap.read()
        #또는 사진 불러오기
        #img = cv.imread('width/5_5_2.png')
        #img = cv.imread('test/r2.png')
        
        #가우시안 블러
        img_blur = cv.GaussianBlur(img,(1,1),self.blurStdDev.value())
        #미디안 블러
        #img_blur = cv.medianBlur(img,5)

        #블러를 흑백으로
        img_gray = cv.cvtColor(img_blur,cv.COLOR_BGR2GRAY)

        #사진 이진화
        binary = eval(self.threshold.currentText())
        ret, img_binary = cv.threshold(img_gray,127,255,binary)

        #허프 서클
        circles = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,self.houghResolution.value(),self.MINRAD.value(),param1=self.param1.value(),param2=self.param2.value(),minRadius=self.houghMinrad.value(),maxRadius=self.houghMaxrad.value())

        #허프서클로 원이 검출되었을 때
        if circles is not None:
            #과다검출
            #if len(circles[0]) > 2:
            #    img = cv.putText(img,'Too many circles detected.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(0,255,0),4)
            #1 or 2개 검출
            if False:
                pass
            else:
                #사각형 범위 구하기
                rects = []
                for i in circles[0,:]:
                    aas = i[2] + self.circleRange.value()
                    r1 = int(i[0]-aas),int(i[1]-aas)
                    r2 = int(i[0]+aas),int(i[1]+aas)
                    rects.append((r1,r2))
                    #cv.rectangle(img,r1,r2,(0,0,255),1)
                

                #기본은 첫번째 사각형으로
                rect = rects[0]

                #사각형이 두개라면 둘 중에 큰 사각형으로
                if len(circles[0])==2:
                    if area(rects[0][0],rects[0][1]) > area(rects[1][0],rects[1][1]):
                        rect = rects[0]
                    else:
                        rect = rects[1]

                #위에서 고른 사각형 범위만큼 크롭
                im = img[rect[0][1]:rect[1][1],rect[0][0]:rect[1][0]]
                
                #크롭한 이미지 블러, 흑백, 이진화
                try:
                    im_blur = cv.GaussianBlur(im,(1,1),self.blurStdDev_2.value())
                except:
                    im_blur = cv.medianBlur(im,int(self.blurStdDev_2.value()))
                im_gray = cv.cvtColor(im_blur,cv.COLOR_BGR2GRAY)
                ret, im_binary = cv.threshold(im_gray,127,255,binary)

                #크롭한 이미지 컨투어 검출
                contours, hierarchy = cv.findContours(im_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
                centers = []
                for c in range(len(contours[:])):
                    cv.drawContours(im,[contours[c]],0,(0,255,0),1)
                    cnt = contours[c]

                    cnx,cny,cnw,cnh = cv.boundingRect(cnt)
                    cnx += rect[0][0]
                    cny += rect[0][1]
                    img = cv.rectangle(img,(cnx,cny),(cnx+cnw,cny+cnh),(0xC0,0xFF,0xEE),2)
                    dis = self.distance.value()
                    ang = self.CamAngle.value()/2
                    ih, iw, ichannel = img.shape
                    x1,x2 = cnx,cnx+cnw
                    r = 0
                    if x1==x2 or iw<2:
                        r = 0
                    else:
                        center = iw//2
                        r1 = ((x1/center)-1)*ang
                        r2 = ((x2/center)-1)*ang
                        if r1==0:
                            r = dis*math.tan(math.radians(r2))
                        elif r2==0:
                            r = dis*math.tan(math.radians(abs(r1)))
                        elif r1<0 and r2<0:
                            r = dis*(math.tan(math.radians(abs(r1)))-math.tan(math.radians(abs(r2))))
                        elif r1>0 and r2>0:
                            r = dis*(math.tan(math.radians(abs(r2)))-math.tan(math.radians(abs(r1))))
                        elif r1<0 and r2>0:
                            r = dis*(math.tan(math.radians(abs(r2)))+math.tan(math.radians(abs(r1))))
                        else:
                            r = 0

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
                    asdfasdf, asdfasdfasdf = self.isCircle(contours[c],centre)
                    if r>=1:
                        if asdfasdf:
                            img = cv.putText(img,'width %f'%(r),(cnx,cny),cv.FONT_HERSHEY_SIMPLEX,fontSize/2,(255,0,0),4)
                            self.output += 'Diameter = '+str(r)+'\n'
                            self.output += asdfasdfasdf
                            self.output+='\n'

                    cv.circle(im,(cx,cy),2,(255,0,0),-1)
                cv.imshow('cropped image',im)
                self.ValueOutput.setText(_translate("MainWindow", self.output))
                if self.isBothCircle(contours,centers):
                    img = cv.putText(img,'Perfect Circle.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(255,0,0),4)
                else:
                    img = cv.putText(img,'Not a Circle.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(0,0,255),4)

                #이미지에 사각형 그리기
                for i in rects:
                    cv.rectangle(img,i[0],i[1],(127,255,0),3)

        #원 미검출
        else:
            img = cv.putText(img,'No circles detected.',textOrg,cv.FONT_HERSHEY_SIMPLEX,fontSize,(0,255,0),4)

        #이미지 출력
        img1 = cv.resize(img, dsize=labelsize, interpolation=cv.INTER_AREA)
        img1 = cv.cvtColor(img1,cv.COLOR_BGR2RGB)
        h,w,c = img1.shape
        qImg = QtGui.QImage(img1.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.imglabel.setPixmap(pixmap)

        

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    form = Form()
    #cap.release()
    sys.exit(app.exec_())