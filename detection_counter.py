import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
from utils import putTextRect as ptr

with open("polyCords","rb") as f:
        data = pickle.load(f)
        polylines,area_name = data['polylines'], data['area_name']

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

model=YOLO('yolov8s.pt')

cap=cv2.VideoCapture('')

count=0

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
   
    count += 1
    if count % 3 != 0:
       continue

    frame=cv2.resize(frame,(1020,500))
    frame_copy = frame.copy()
    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    
    list1 = []
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        
        c=class_list[d]
        # print("Object identified as -> ",class_list[d])
        cx=int(x1+x2)//2
        cy=int(y1+y2)//2

        if 'car' in c or 'cars' in c or 'truck' in c or 'trucks' in c or 'bus' in c or 'buss' in c:
            list1.append([cx,cy])
            # cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,255),2)

    counter = []
    list2 = []
    empty_spaces = ""

    for i, polyline in enumerate(polylines):
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)
        ptr(frame, f'{area_name[i]}', tuple(polyline[0]), 1, 1)

        area_empty = True

        for j, centroid in enumerate(list1):
            cx1 = centroid[0]
            cy1 = centroid[1]
            result = cv2.pointPolygonTest(polyline, ((cx1, cy1)), False)

            if result >= 0:
                cv2.circle(frame, (cx1, cy1), 3, (255, 0, 0), -1)
                cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
                counter.append(cx1)
                list2.append(i)
                area_empty = False
                break
        
        if area_empty:
            print("Area", area_name[i], "is empty.")
            empty_spaces += area_name[i] + ", "

        # ptr(frame, f'CarCounter: - {empty_spaces}, (50, 150 + i * 40), 2, 2)

    car_count = len(counter)
    free_space = len(polylines) - len(list2)
    ptr(frame, f'Occupied: - {car_count}', (50, 60), 2, 2)
    ptr(frame, f'Available: - {free_space}', (51, 100), 2, 2)
    ptr(frame, f'Empty Spaces: {empty_spaces}', (52, 140), 2, 2)

    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
