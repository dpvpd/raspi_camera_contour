import cv2 as cv


distance = lambda p1,p2:(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**.5


img = 'oring.png'
img_color = cv.GaussianBlur(cv.imread(img),(0,0),5)
img_gray = cv.cvtColor(img_color,cv.COLOR_BGR2GRAY)
ret, img_binary = cv.threshold(img_gray,127,255,0)
contours, hierarchy = cv.findContours(img_binary,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)


diss = []
for c in range(len(contours[:-1])):
    cv.drawContours(img_color,[contours[c]],0,(0,255,0),3)
    M = cv.moments(contours[c])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
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
cv.waitKey(0)