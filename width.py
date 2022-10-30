import cv2 as cv
import numpy as np
import math

dis = 300 #mm
alpha = 83 /2  #deg
alpha_radian = math.radians(alpha)
beta = 90-alpha
beta_radian = math.radians(beta)

#print(math.sin(alpha))
#print(math.sin(alpha_radian))
#print((3**.5)/2) # sqrt(3)/2 = sin 60

img = cv.imread('width/6.png')
img_blur = cv.GaussianBlur(img,(0,0),5)
img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
#img_bin = cv.adaptiveThreshold(img_gray,127,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,15,2)
ret,img_bin = cv.threshold(img_gray,127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
contours, hierarchy = cv.findContours(img_bin,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
ih, iw, ichannel = img.shape

for c in range(len(contours[:])):
    cv.drawContours(img,[contours[c]],0,(0,255,0),4)
cnt = contours[0]
x,y,w,h = cv.boundingRect(cnt)
cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


#l = dis/math.sin(beta_radian)
imgwidth = 2* (dis*math.tan(alpha_radian))#(l*math.sin(alpha_radian))

def deg(a, width, x1, x2):
    if x1==x2 or width<2:
        return 0
    center = width//2
    r1 = ((x1/center)-1)*a
    r2 = ((x2/center)-1)*a
    if r1==0:
        return dis*math.tan(math.radians(r2))
    elif r2==0:
        return dis*math.tan(math.radians(abs(r1)))
    elif r1<0 and r2<0:
        return dis*(math.tan(math.radians(abs(r1)))-math.tan(math.radians(abs(r2))))
    elif r1>0 and r2>0:
        return dis*(math.tan(math.radians(abs(r2)))-math.tan(math.radians(abs(r1))))
    elif r1<0 and r2>0:
        return dis*(math.tan(math.radians(abs(r2)))+math.tan(math.radians(abs(r1))))
    return 0


print(x,y,w,h)
print(deg(alpha,iw,x,x+w))
#theta, gamma = deg(alpha,iw,x,x+w)
#theta_rad = math.radians(abs(theta))
#gamma_rad = math.radians(abs(gamma))
#ww = (math.tan(theta_rad)+math.tan(gamma_rad))*h
#print(ww)
#print(imgwidth)
print((w/iw)*imgwidth)

cv.imshow('asdf',img)

while True:
    #if cv.waitKey(1)&0xff==27:
        cv.destroyAllWindows()
        break