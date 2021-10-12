import cv2 as cv
import numpy as np
import mediapipe as mp
import time,math
import handtracking as ht
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam , hcam = 800,480


cam = cv.VideoCapture(0)
cam.set(3,wcam) #3 id=s prop id for width of cam
cam.set(4,hcam)

detector = ht.HandDetector(detectioncon=0.6)

#volume controlling using pycaw code

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
min_vol,max_vol,_  = volume.GetVolumeRange()
#print(min_vol,max_vol)


while 1:
    ret,frame = cam.read()
    frame = detector.findhands(frame)
    lmlist = detector.findposition(frame,draw=False)
    volbar=400
    volper=1
    if len(lmlist)!=0:
            #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]

        length = math.hypot(x2-x1,y2-y1)
            # hand range 22 - 195
            # vol range -64 - 0
        vol  = np.interp(length,[30,195],[min_vol,max_vol])
        volbar  = np.interp(length,[22,195],[400,200])
        volper  = np.interp(length,[22,195],[0,100])
            #print(int(length),vol)

        volume.SetMasterVolumeLevel(vol, None)

        cv.circle(frame,(x1,y1),15,(200,100,100),cv.FILLED)
        cv.circle(frame,(x2,y2),15,(200,100,100),cv.FILLED)
        cv.line(frame,(x1,y1),(x2,y2),(200,100,100),3)

            #print(length)
        if length<=30:
            cv.circle(frame,((x1+x2)//2,(y1+y2)//2),15,(0,255,0),cv.FILLED)

    cv.rectangle(frame,(40,200),(70,400),(0,255,0),3)
    cv.rectangle(frame,(40,int(volbar)),(70,400),(0,255,0),cv.FILLED)
    cv.putText(frame,f'{int(volper)}%',(35,440),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)

    cv.imshow('web-cam',frame)
    cv.waitKey(1)
        

cam.release()        
cv.destroyAllWindows()