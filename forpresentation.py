import cv2 as cv
from copy import deepcopy

MINRAD = 30

#img = cv.imread('pearlgirl.jpg')
#img = cv.imread('monalisa.jpg')
#img = cv.imread('starrynight.jpeg')
#img = cv.imread('gleaners.jpeg')
img = cv.imread('test/r2.png')

img_blur = cv.GaussianBlur(img,(11,11),5)
img_gray = cv.cvtColor(img_blur,cv.COLOR_BGR2GRAY)

ret, img_threshold = cv.threshold(img_gray,127,255,cv.THRESH_BINARY)

img_adaptive = cv.adaptiveThreshold(img_gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,15,2)
circles = cv.HoughCircles(img_threshold,cv.HOUGH_GRADIENT,0.25,MINRAD,param1=50,param2=28,minRadius=0,maxRadius=300)

contours1, hierarchy = cv.findContours(img_threshold,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
contours2, hierarchy = cv.findContours(img_adaptive,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)

img1 = deepcopy(img)
img2 = deepcopy(img)
for c in range(len(contours1[:])):
    cv.drawContours(img1,[contours1[c]],0,(0,255,0),2)
if circles is not None:
    for i in circles[0,:]:
        aas = i[2]
        r1 = int(i[0]-aas),int(i[1]-aas)
        r2 = int(i[0]+aas),int(i[1]+aas)
        cv.rectangle(img2,r1,r2,(0,0,255),2)
else:
    print('None')
cv.imwrite('ppt/threshold11.png', img1)
cv.imwrite('ppt/threshold1.png', img_threshold)
cv.imwrite('ppt/adaptivethreshold11.png', img2)#_threshold)