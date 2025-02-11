from ultralytics import YOLO
import cv2
import math
import serial

# arduino = serial.Serial('/dev/ttyUSB0', 9600)

def countFrameCenter(frame):
    return frame.shape[:2]

    # w = x
    # h = y
    
# 619,332

def draw_targets(frame,Color = (255,0,0)):
    
    h , w = countFrameCenter(frame)


    # cv2.circle(frame,(w//2,h//2),6,(255,0,0),-1)
    cv2.circle(frame,(619,426),6,(0,255,255),-1)

    # cv2.line(frame,(w//2,0),(w//2,h),(0,0,0),2)
    # cv2.line(frame,(0,h//2),(w,h//2),(0,0,0),2)

    # cv2.line(frame,(0,348),(1280,348),(0,0,0),2)
    # cv2.line(frame,(591,0),(591,720),(0,0,0),2)

    cv2.rectangle(frame,(590,400),(638 ,446),(0,0,0),2)

    # x ekseni kaydırma

    # cv2.rectangle(frame,(w//2 -70,h//2-10),(w//2 -15,h//2+25),(255,0,0),2)

    # cv2.rectangle(frame,(567,290),(625,370),Color,2)
    

    # cv2.rectangle(frame,(w//2 -30,0),(w//2+30,h),(0,0,0),2)
    

def target_ballon(frame, object_center):
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

"""

def trackingXaxis(frame, object_center):
    h, w = countFrameCenter(frame)  
    
    # 593
    try:
        x1, y1 = object_center  
                

        frame_center_x = w//2

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
        print("Kamerada tespit edilecek nesnenin merkezi yok")
    

    
def display_Information(frame,x1,y1,x2,y2,score,cls_name):
    
        #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        org = [x1,y1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(frame,cls_name, org, font, fontScale, color, thickness)
        
    
def count_object_center(frame,x1,x2,y1,y2):
    x_center = int((x1+x2)/2)
    y_center = int((x1+x2)/2)    

    center = (x_center,y_center)

    return center

"/dev/video2"

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


model = YOLO("best.pt")

classNames = ["kirmizi_balon"]


while True:
    success, frame = cap.read()
     
    if success:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_3channel = cv2.merge([gray, gray, gray]) 

        results = model(gray_3channel, stream=True)

        

        for r in results:
            boxes = r.boxes

            for box in boxes:

                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 

                center = count_object_center(frame,x1,x2,y1,y2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                score = math.ceil((box.conf[0] * 100)) / 100
                print("Score --->", score)

                cls_id = int(box.cls[0])
                
                
                class_name = classNames[cls_id]
                print("Class name -->", class_name)

                display_Information(frame,x1, y1, x2, y2, score,class_name)

                trackingXaxis(frame,center)
                trackingYaxis(frame,center)

                target_ballon(frame , center)
           

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()