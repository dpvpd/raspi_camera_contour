import cv2 as cv
from copy import deepcopy

img = cv.imread('blackring.png')
#print(type(img))


MINRAD = 20

img_mean = cv.blur(img, (211,211))
ret,img_binary = cv.threshold(cv.cvtColor(img_mean,cv.COLOR_BGR2GRAY),127,255,cv.THRESH_BINARY + cv.THRESH_OTSU)
contours1, hierarchy = cv.findContours(img_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
#circles_1 = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,0.25,MINRAD,param1=50,param2=30,minRadius=0,maxRadius=0)

img_median = cv.medianBlur(img,211)
ret,img_binary = cv.threshold(cv.cvtColor(img_median,cv.COLOR_BGR2GRAY),127,255,cv.THRESH_BINARY + cv.THRESH_OTSU)
contours2, hierarchy = cv.findContours(img_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
#circles_2 = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,0.25,MINRAD,param1=50,param2=30,minRadius=0,maxRadius=0)

img_gaussian = cv.GaussianBlur(img,(211,211),5)
ret,img_binary = cv.threshold(cv.cvtColor(img_gaussian,cv.COLOR_BGR2GRAY),127,255,cv.THRESH_BINARY + cv.THRESH_OTSU)
contours3, hierarchy = cv.findContours(img_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
#circles_3 = cv.HoughCircles(img_binary,cv.HOUGH_GRADIENT,0.25,MINRAD,param1=50,param2=30,minRadius=0,maxRadius=0)

img_mean = deepcopy(img)
img_median = deepcopy(img)
img_gaussian = deepcopy(img)
for c in range(len(contours1[:])):
    cv.drawContours(img_mean,[contours1[c]],0,(0,255,0),4)
for c in range(len(contours2[:])):
    cv.drawContours(img_median,[contours2[c]],0,(0,255,0),4)
for c in range(len(contours3[:])):
    cv.drawContours(img_gaussian,[contours3[c]],0,(0,255,0),4)
'''
if circles_1 is not None:
    for i in circles_1[0,:]:
        cv.circle(img,(int(i[0]),int(i[1])),int(i[2]),(0,0,255),1)

if circles_2 is not None:
    for i in circles_2[0,:]:
        cv.circle(img,(int(i[0]),int(i[1])),int(i[2]),(0,255,0),1)

if circles_3 is not None:
    for i in circles_3[0,:]:
        cv.circle(img,(int(i[0]),int(i[1])),int(i[2]),(255,0,0),1)
'''

cv.imwrite('blur/mean.png', img_mean)
cv.imwrite('blur/median.png', img_median)
cv.imwrite('blur/gaussian.png', img_gaussian)
cv.imwrite('blur/origin.png', img)
