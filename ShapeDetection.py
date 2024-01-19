import cv2
import numpy as np


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(2)
# cap = cv2.VideoCapture('shapes.mp4')
cap.set(3, frameWidth)  # 3-> Width
cap.set(4, frameHeight) # 4-> Height

def empty():
    pass

def getContours(frame, newFrame):
    contours, ret = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        contourArea = cv2.contourArea(cnt)
        area = cv2.getTrackbarPos("Area", "Parameters")
        if contourArea > area:
            cv2.drawContours(newFrame, cnt, -1, (255,0,0), 10)
            contourPeri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 00.2 * contourPeri, True)
            print(len(approx))

            

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(newFrame, (x,y), ((x+w), (y+h)), (0,0,255), 2)

            cv2.putText(newFrame, "Points : " +str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,0), 2)
            cv2.putText(newFrame, "Area : " +str(int(contourArea)), (x + w + 20, y + 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,0), 2)
    


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 540, 220)
cv2.createTrackbar("Threshold1", "Parameters", 52, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 255, 255, empty)
cv2.createTrackbar("Area", "Parameters", 10000, 50000, empty)


while True:
    ret, frame = cap.read()
    newFrame = frame.copy()
    frameBlur = cv2.GaussianBlur(frame, (7,7), 1)
    frameGray = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

    frameCanny = cv2.Canny(frameGray, threshold1, threshold2)
    kernal5 = np.ones((5,5))
    frameDilation = cv2.dilate(frameCanny, kernal5, iterations=1)

    getContours(frameDilation,newFrame)

    cv2.imshow('Result', newFrame)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()