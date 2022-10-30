import cvlib as cl
import cv2 as cv

img = cv.imread('100won.jpg')
conf = 0.5 # 사물 인식을 진행할 confidence의 역치 값
model_name = "yolov4" # 사물을 인식할 모델 이름

cap = cv.VideoCapture(0)
while cap.isOpened():
    #img = cv.imread('oring.png')
    ret, img = cap.read()
    result = cl.detect_common_objects(img, confidence=conf, model=model_name)

    #output_path = "/cat_dog_detect.jpg" # 결과가 반영된 이미지 파일 저장 디렉토리

    result_img = cl.object_detection.draw_bbox(img, *result) # result 결과를 이미지에 반영
    cv.imshow('result',result_img)
    #cv.imwrite(output_path, result_img) # 반영된 이미지 파일 저장
    #display(Image(filename = output_path)) # 이미지 출력
    if cv.waitKey(1)&0xff==27:
        break

cap.release()
cv.destroyAllWindows()
