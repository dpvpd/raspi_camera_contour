#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
import cv2 as cv

'''
cam = PiCamera()
cam.resolution = (480,320)
cam.framerate = 32
rawCapture = PiRGBArray(cam,size=(480,320))
'''

distance = lambda p1,p2:(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**.5

MINRAD = 20

binary = cv.ADAPTIVE_THRESH_GAUSSIAN_C
#binary = cv.ADAPTIVE_THRESH_MEAN_C
#binary = cv.THRESH_BINARY + cv.THRESH_OTSU
#binary = 0

cap = cv.VideoCapture(0)
while cap.isOpened():
    #img = cv.imread('oring.png')
    ret, img = cap.read()
    
    img_color = cv.GaussianBlur(img,(0,0),3.5)
    #img_color = cv.medianBlur(img,49)
    img_gray = cv.cvtColor(img_color,cv.COLOR_BGR2GRAY)
    ret, img_binary = cv.threshold(img_gray,127,255,binary)
    contours, hierarchy = cv.findContours(img_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
    #contours, hierarchy = cv.findContours(img_color,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
    #_,img_binary2 = cv.threshold(cv.cvtColor(cv.GaussianBlur(img,(0,0),10),cv.COLOR_BGR2GRAY),127,255,binary)
    circles = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,0.25,MINRAD,param1=50,param2=30,minRadius=0,maxRadius=0)
    img_color = img#_binary
    
    
    
    if circles is not None:
        for i in circles[0,:]:
            cv.circle(img_color,(int(i[0]),int(i[1])),int(i[2]),(0,0,255),2)
            aas = i[2]#//(2**.5)
            r1 = i[0]-aas,i[1]-aas
            r2 = i[0]+aas,i[1]+aas
            cv.rectangle(img_color,(int(r1[0]),int(r1[1])),(int(r2[0]),int(r2[1])),(0,0,255),2)
            #print(i)
            #exit()
    

    diss = []
    for c in range(len(contours[:-1])):
        cv.drawContours(img_color,[contours[c]],0,(0,255,0),3)
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
        #print(contours[c][0][0])
        l = []
        for i in contours[c][:10]:
            #print(i,i.shape)
            l.append(distance(centre,list(i[0])))
        a = 0
        mean = sum(l)/len(l)
        #for i in range(len(l)):
            
        #dic = {'data':l,'mean':mean,'sigma':}
        cv.circle(img_color,(cx,cy),2,(255*((c+1)%2),0,255*(c%2)),-1)
    #print(contours)
    cv.imshow('result',img_color)
    if cv.waitKey(1)&0xff==27:
        break
cap.release()

cv.destroyAllWindows()

