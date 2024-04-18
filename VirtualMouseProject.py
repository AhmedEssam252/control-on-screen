import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

wCam , hCam  = 640 , 480
frameR = 80
smoothening = 5

pTime = 0
ploxX, ploxY = 0, 0
cloxX, cloxY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector()
wScr, hScr = pyautogui.size()

pyautogui.PAUSE = 0

while True:
    success , img = cap.read()
    img = detector.findHands(img)
    lmList,bbox  = detector.findPosition(img)

    if len(lmList) != 0:
        x1,y1 = lmList[8][1:]   
        x2,y2 = lmList[12][1:]
        x4,y4 = lmList[4][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR), (wCam-frameR,hCam-frameR),(0,255,0),2)

        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        if fingers[1] == 1 and fingers[2] == 0:

            # smoothen cursor
            cloxX = ploxX + (x3 - ploxX) / smoothening
            cloxY = ploxY + (y3 - ploxY) / smoothening

            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)

            if x3 > 0 and x3 < wScr and y3 > 0 and y3 < hScr:
                pyautogui.moveTo(cloxX, cloxY)

            ploxX, ploxY = cloxX, cloxY

        if fingers[0] == 0 and fingers[1] == 1 :

            length2, img, lineInfo2 = detector.findDistance(4, 8, img)        
            cv2.circle(img,(x4,y4),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)

            print(length2)

            if length2 < 40:
                if x3 > 0 and x3 < wScr and y3 > 0 and y3 < hScr:
                    cv2.circle(img,(lineInfo2[4],lineInfo2[5]),15,(0,255,0),cv2.FILLED)
                    pyautogui.click()

        if fingers[1] == 1 and fingers[2] == 1:
            
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 50:
                if x3 > 0 and x3 < wScr and y3 > 0 and y3 < hScr:
                    cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                    pyautogui.scroll(-20)

            if length > 50:
                if x3 > 0 and x3 < wScr and y3 > 0 and y3 < hScr:
                    pyautogui.scroll(20)
                
    # calculate fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # show fps
    cv2.putText(img, str(int(fps)), (40, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image" , img)
    cv2.waitKey(1)