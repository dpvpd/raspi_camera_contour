import cv2 as cv

img = cv.imread('oring.png')
img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#img_bin = cv.adaptiveThreshold(img_gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,51,7)
ret,img_bin = cv.threshold(img_gray,127,255,cv.THRESH_BINARY)
'''
contour,hierarchy = cv.findContours(img_bin,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
for c in range(len(contour[:])):
    cv.drawContours(img,[contour[c]],0,(0,255,0),2)
    '''
cv.imshow('contour',img_bin)
while True:
    if cv.waitKey(1)&0xff==27:
        cv.destroyAllWindows()
        break