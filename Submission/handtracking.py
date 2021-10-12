import cv2 as cv
import numpy as np
import mediapipe as mp
import time



class HandDetector():
    def __init__(self,mode=False,maxhands=2,detectioncon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detectioncon=detectioncon
        self.trackcon=trackcon
        
        self.mpHands= mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.detectioncon,self.trackcon)
        self.mp_draw = mp.solutions.drawing_utils

    def findhands(self,img,draw=True):
        
        img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result= self.hands.process(img_rgb)
        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img,hand,self.mpHands.HAND_CONNECTIONS)
        return img

    def findposition(self,img,handno=0,draw=True):
        
        lmlist=[]
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),5,(255,0,255),cv.FILLED)
        return lmlist



def main():
    ptime = 0
    ctime = 0
    frame = cv.VideoCapture(0)
    detector = HandDetector()
    while 1:
        ret , img = frame.read()
        img = detector.findhands(img)
        lmlist = detector.findposition(img)
        if len(lmlist)!=0:
            print(lmlist[4])

        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime=ctime
        cv.putText(img,str(int(fps)),(20,80),cv.FONT_HERSHEY_COMPLEX,2,(255,100,0),3)   # 2 scale 3(thickness of text)
        cv.imshow('web-cam',img)
        if cv.waitKey(1)==ord('q'):
            break
    
