import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
from utils import putTextRect as ptr

# Loading the polyCords file, consisting all the saved coordinates of the RoIs
# Loading the polylines list data and the area_name data
with open("polyCords","rb") as f:
        data = pickle.load(f)
        polylines, area_name = data['polylines'], data['area_name']

# Loading coco.txt data, COCO i.e. the Common Objects in Context, has by default 80 classes of objects pre-trained
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# Loading the YOLO v8 model for Object Detection
model = YOLO('yolov8s.pt')

# Loading the video feed - Plaksha_Parking2 to be used for Plaksha
cap = cv2.VideoCapture('')

count = 0

# Reading the video feed frame by frame, and when completed, set to the beginning to again start the loop
while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
   
    count += 1
    if count % 3 != 0:
       continue

    # Setting frame size to 1020x500
    frame = cv2.resize(frame,(1020,500))
    frame_copy = frame.copy()

    # Predicting the YOLO model on the every fram of the video feed
    # YOLO model is trained on the COCO dataset, which has the data of all types of vehicles required
    results = model.predict(frame)

    # Fetching the bounding boxes from the prediction results
    # Extracting bounding box coordinates and class predictions.
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    
    list1 = []
    for index, row in px.iterrows():

        # Storing all the coordinates of the bounding box formed and the class information detected
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        
        c = class_list[d]
        # print("Object identified as -> ",class_list[d])

        # Finding the middle point of the bounding box, required to do further calculations
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2

        # Filtering the vehicles required to be detected and appending in the list
        # Can uncomment the code line to form the bounding box created around the detected object, here vehicles filterd above
        if 'car' in c or 'cars' in c or 'truck' in c or 'trucks' in c or 'bus' in c or 'buss' in c:
            list1.append([cx, cy])
            # cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,255),2)

    counter = []
    list2 = []
    empty_spaces = ""

    # By default, all the RoIs are marked as green colors i.e the polygons
    for i, polyline in enumerate(polylines):
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)
        ptr(frame, f'{area_name[i]}', tuple(polyline[0]), 1, 1)

        area_empty = True

        # Testing for the center point caclulated above to be present within the polygon i.e the RoIs
        for j, centroid in enumerate(list1):
            cx1 = centroid[0]
            cy1 = centroid[1]
            result = cv2.pointPolygonTest(polyline, ((cx1, cy1)), False)

            # The center points of all the bounding boxes of the detected vehicle are marked by blue dot
            # Code block to filter out the available i.e. the free spots among all the spots
            if result >= 0:
                cv2.circle(frame, (cx1, cy1), 3, (255, 0, 0), -1)

                # If the object is present, the RoIs are marked by Red color
                cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
                counter.append(cx1)
                list2.append(i)
                area_empty = False
                break
        
        # Is the area_empty is set to True i.e. the RoI is empty 
        if area_empty:
            print("Area", area_name[i], "is empty.")
            empty_spaces += area_name[i] + ", "

        # ptr(frame, f'CarCounter: - {empty_spaces}, (50, 150 + i * 40), 2, 2)

    # Code block to create the rectangle box to display the counter values
    car_count = len(counter)
    free_space = len(polylines) - len(list2)
    ptr(frame, f'Occupied: - {car_count}', (50, 60), 2, 2)
    ptr(frame, f'Available: - {free_space}', (51, 100), 2, 2)
    ptr(frame, f'Empty Spaces: {empty_spaces}', (52, 140), 2, 2)

    cv2.imshow('FRAME', frame)
    key = cv2.waitKey(1) & 0xFF

    # Keyboard event, where:
    # key 'q' -> to stop the video feed and exit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
