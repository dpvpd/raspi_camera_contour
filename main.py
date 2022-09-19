from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

cam = PiCamera()
cam.resolution = (480,320)
cam.framerate = 32
rawCapture = PiRGBArray(cam,size=(480,320))

