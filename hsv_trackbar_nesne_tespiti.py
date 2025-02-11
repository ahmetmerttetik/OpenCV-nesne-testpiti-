import cv2
import numpy as np
import serial
import time


def nothing(x):
    pass

name_window = "Trackbars"

cv2.namedWindow(name_window)

cv2.createTrackbar("L-H", name_window, 0, 179, nothing)
cv2.createTrackbar("L-S", name_window, 0, 255, nothing)
cv2.createTrackbar("L-V", name_window, 0, 255, nothing)
cv2.createTrackbar("U-H", name_window, 0, 179, nothing)
cv2.createTrackbar("U-S", name_window, 0, 255, nothing)
cv2.createTrackbar("U-V", name_window, 0, 255, nothing)



# arduino = serial.Serial('/dev/ttyUSB0', 9600)

def countFrameCenter(frame):
    return frame.shape[:2]

    # w = x
    # h = y
    
# 619,332

def draw_targets(frame,Color = (255,0,0)):
    
    h , w = countFrameCenter(frame)


    # cv2.circle(frame,(w//2,h//2),6,(255,0,0),-1)  # görüntünün merkezine küçük daire çizer

    cv2.circle(frame,(619,426),6,(0,255,255),-1)  # Robot koldaki lazerin görüntüde denk geldiği piksel değerleri

    # cv2.line(frame,(w//2,0),(w//2,h),(0,0,0),2)  # görüntünün yükseklik (height) değerinin yarısından  enine , genilşiğine (width) kadar çizgi çizer
    # cv2.line(frame,(0,h//2),(w,h//2),(0,0,0),2)   # görüntünün genişlik (width) değerinin yarısından , uzunluğuna (height) kadar çizgi çizer


    # cv2.line(frame,(0,348),(1280,348),(0,0,0),2)  # bu değerler ise robot kolda lazer var. Lazerin görüntüye denk geldiği piksel değerlerine göre
    # cv2.line(frame,(591,0),(591,720),(0,0,0),2)   # çizilecek çizgiler belirlenmiştir.

    cv2.rectangle(frame,(590,400),(638 ,446),(0,0,0),2)

    # x ekseni kaydırma

    # cv2.rectangle(frame,(w//2 -70,h//2-10),(w//2 -15,h//2+25),(255,0,0),2)

    # cv2.rectangle(frame,(567,290),(625,370),Color,2)
    

    # cv2.rectangle(frame,(w//2 -30,0),(w//2+30,h),(0,0,0),2)
    

def hitBallon(frame, object_center):
    h, w = countFrameCenter(frame)  

    try:
        x1, y1 = object_center  
                

        start_pointX , start_pointY = (590,400)
        end_pointX , end_pointY = (638 ,446)


        # start_pointX , start_pointY = (w//2 -30,h//2-25)
        # end_pointX , end_pointY = (w//2 + 30,h//2+25)

        #### (0,348),(1280,348)

        if start_pointX < x1 < end_pointX and start_pointY < y1 < end_pointY:
            m = "lazer acilacak : x : {} , w : {}".format(x1,y1)
            cv2.putText(frame , m , (25,25),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(25,25,25),2)
            print("lazer acilacak")
            # arduino.write(b'a')
            time.sleep(2)
            # arduino.write(b'k')
            draw_targets(frame , (0,255,0))

        else:
            m = "Lazer kapanacak : x : {} , w : {}".format(x1,y1)
            cv2.putText(frame , m , (25,25),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(25, 25,25),2)
            # arduino.write(b'k')
            print("lazer kapanacak")
    except Exception:
        pass
    

"""
startPoint = (w//2 -30,0)
endPoint = (w//2+30,h)

bu alanın içindeyse seri haberleşmede stop komutunu yani b's' i gönder
ayrıca takip sistemine bak hareketli balonları patlatmak için en optimum çözümü ara

"""

def trackingXaxis(frame, object_center):
    h, w = countFrameCenter(frame)  
    
    # 593
    try:
        x1, y1 = object_center  
                


        deltaX = 614 - x1

        if deltaX > 0:
            # arduino.write(b'l')
            print("kol sola donecek")

        elif deltaX < 0:
            # arduino.write(b'r')
            print("kol saga donecek")
        else:
            print("kol durdu")
    except Exception:
        pass


def trackingYaxis(frame, object_center):
    h, w = countFrameCenter(frame)

    # 614,382

    if object_center is not None:
        try:
            _, y1 = object_center  

            frame_center_y = h // 2

            deltaY = 382 - y1 

            if deltaY > 0:
                # arduino.write(b'u')
                print("kol yukari cikacak")
            elif deltaY < 0:
                # arduino.write(b'b')
                print("kol asagı inecek")
            else:
                print("kol durdu")
        except Exception as e:
            pass
    else:
        print("Kamerada tespit edilecek nesne bulunamadi")
    


def dost_dusman(frame,object_center,hsv_frame  , boundingBox,blue_l, blue_u):
    
    
    
    x1, y1 = boundingBox[0] 
    x2, y2 = boundingBox[1]  
    x3, y3 = boundingBox[2]  
    x4, y4 = boundingBox[3]  

    x = min(x1, x2, x3, x4)
    y = min(y1, y2, y3, y4)
    w = max(x1, x2, x3, x4) - x
    h = max(y1, y2, y3, y4) - y

    roi = hsv_frame[y:y+h, x:x+w]

    mean_color = cv2.mean(roi)[:3]

    hue = mean_color[0]

    color_label = "Dusman"


    trackingXaxis(frame,object_center)
    trackingYaxis(frame,object_center)


    if blue_l[0] <= hue <= blue_u[0]:
        color_label = "Dost (Mavi)"
    else:
            color_label = "Dusman"
            trackingXaxis(frame,object_center)
            trackingYaxis(frame,object_center)

    cv2.putText(frame, color_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


# blueLower = (110,50,50)
# blueUpper = (130,255,255)

# (75, 100, 100), (130, 255, 255)
blueLower = (75,100,100)
blueUpper = (130,255,255)

orangeLower = (0,100,100)
orangeUpper = (50,255,255)

yellowLower = (22, 100, 100)
yellowUpper = (38, 255, 255)


lower_laser = (100, 150, 150)  
upper_laser = (140, 255, 255)  



# redLower = (17, 10, 100)
# redUpper = (50, 60, 200)
# (0, 100, 100), (10, 255, 255)
redLower = (0, 52, 92)
redUpper = (179, 225, 255)

whiteLower = (0, 0, 200)
whiteUpper = (180, 30, 255)

lazer_Red_l = (134,114,148)
lazer_Red_u = (179,255,255)


redLower = (0, 92, 112)
redUpper = (179, 225, 255)

# [45 , 107 , 93 ]
# [98 , 233 , 227]


# [5 , 213 , 186]       
# [124 , 255 ,255]

green_lower = (45 , 107 , 93)
green_upper = (98 , 233 , 227)

laser_green_lower = (5 , 213 , 186)
laser_green_upper = (124 , 255 ,255) 

laser_red_lower = (111 , 179 , 149 )
laser_red_upper = (179 ,255 ,255)


## 111 , 179 , 149 
## 179 ,255 ,255


# "/dev/video2"


cap = cv2.VideoCapture(0)


cap.set(3,1280)
cap.set(4,720)


while True:
    suc , frame = cap.read()

    if suc:
        
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        imgBlur = cv2.GaussianBlur(frame,(9,9),1)

        hsv = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2HSV)

        lh = cv2.getTrackbarPos("L-H", name_window)
        ls = cv2.getTrackbarPos("L-S", name_window)
        lv = cv2.getTrackbarPos("L-V", name_window)
        uh = cv2.getTrackbarPos("U-H", name_window)
        us = cv2.getTrackbarPos("U-S", name_window)
        uv = cv2.getTrackbarPos("U-V", name_window)

        lower = np.array([lh, ls, lv])
        upper = np.array([uh, us, uv])  

        mask_trackbar = cv2.inRange(hsv,lower,upper)

        # mask_green = cv2.inRange(hsv,green_lower,green_upper)
        # mask_lazer_green = cv2.inRange(hsv,laser_green_lower,laser_green_upper)

        # mask = mask_green | mask_lazer_green

        mask = mask_trackbar

        # cv2.imshow("hsv_frame", hsv)

        # cv2.imshow("mask_image",mask)

        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask,None,iterations=2)
        # cv2.imshow("erozyon+dilation",mask)

        mask_copy = mask.copy()

        (contours,hierarchy) = cv2.findContours(mask_copy,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        center = None 
        new_center = None 

        if len(contours) > 0 :

            c = max(contours,key = cv2.contourArea)

            rect = cv2.minAreaRect(c)

            ((x,y),(width,height),rotation) = rect

            s = "x : {} , y : {} , height : {} , width : {} , rotation : {} ".format(np.round(x),np.round(y),np.round(height),np.round(width),np.round(rotation))


            box = cv2.boxPoints(rect)
            box = np.int64(box)

            """
            # Dikdörtgenin köşe noktalarını al
            box = cv2.boxPoints(rect)
            box = np.int64(box)

            # Dikdörtgenin eksenlere paralel koordinatlarını al
            x, y, w, h = cv2.boundingRect(box)

            # Çerçeveye eksenlere paralel dikdörtgen çiz
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            """

            M = cv2.moments(c)
            center = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))

            # cv2.circle(frame, (int(new_center[0]), int(new_center[1])), 5, (0, 255, 0), -1)  # Tahmin: Yeşil

            # cv2.line(frame, center, (int(new_center[0]), int(new_center[1])), (255, 255, 0), 2)  # Çizgi

            cv2.drawContours(frame,[box],0,(0,255,255),2)

            cv2.circle(frame,center,5,(255,0,255),-1)

            cv2.putText(frame , s , (50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)

            dost_dusman(frame,center,hsv,box,blueLower,blueUpper)



        # cv2.imshow("frame",frame)

        draw_targets(frame)

        # trackingXaxis(frame , center)
        # trackingYaxis(frame ,center)

        
        # hitBallon(frame,center)


        cv2.imshow("mask",mask)

        cv2.imshow("orjinal_tespit_edilen_resim",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# arduino.close()


cap.release()
cv2.destroyAllWindows()