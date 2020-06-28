import cv2                             #importing modules
import numpy as np
from drum_styles import draw,drum_press 
cap=cv2.VideoCapture(1)
while True:
    ret,frame=cap.read()               #accessing the frames
    frame=cv2.flip(frame,1)
    #frame=cv2.GaussianBlur(frame,(9,9),0)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #_, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  #converting to Hue_Saturation_Vue format
    #mask=cv2.inRange(hsv,lower_red,upper_red)
    #kernel=np.ones((5,5),np.float32)/25
    #mask=cv2.filter2D(mask,-1,kernel)
    #mask=cv2.blur(mask,(3,3))
    draw(frame)                                #creating the rectangular drums
    kernel1=np.ones((4,4),np.uint8)             #kernels for smoothing the frames
    kernel2=np.ones((15,15),np.uint8)
    lower_red=np.array([136,87,111])           #creating the mask for red color
    upper_red=np.array([179,255,255])
    mask1=cv2.inRange(hsv, lower_red,upper_red)
    
    lower_red=np.array([0,110,100])
    upper_red= np.array([3,255,255])
    mask2=cv2.inRange(hsv, lower_red,upper_red)
    mask=mask1+mask2                           #final mask
    
    mask=cv2.erode(mask,kernel1,iterations = 1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel2)
    x,y,w,h=0,0,0,0
    
    contours,hierarchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    try:
          for i in range (0,10):
               x,y,w,h=cv2.boundingRect(contours[i])
               if(w*h)>2000:
                    break

    except:
          pass
      
    cv2.rectangle(frame,(x,y),(x+w,y+h),(240, 128, 48),1)
    drum_press(frame,x,y,w,h)
    cv2.imshow('ROCK-o-DRUM',frame)
    #cv2.imshow('MASK_red',mask)
    
    
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()