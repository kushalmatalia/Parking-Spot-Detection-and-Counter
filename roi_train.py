import cv2
import numpy as np
from utils import putTextRect as ptr
import pickle

cap = cv2.VideoCapture('')

drawing = False
area_name = []
paused = False

try:
    with open("polyCords","rb") as f:
                data = pickle.load(f)
                polylines,area_name = data['polylines'], data['area_name']
except:
    polylines = []

points = []
current_name = " "

def draw(event, x, y, flags, param):
    global points, drawing, paused
    drawing = True

    if event==cv2.EVENT_LBUTTONDOWN:
        # print(x, y)
        points=[(x,y)]
        paused = not paused

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x,y))

    elif event==cv2.EVENT_LBUTTONUP:
        drawing = False
        current_name = str(len(area_name) + 1)
        # current_name = input('areaname: - ')
        # if current_name:
        area_name.append(current_name)
        polylines.append(np.array(points,np.int32))
        # print("polylines ---> ", len(polylines))
        # print("points ---> ", len(points))
        paused = not paused

    elif event == cv2.EVENT_RBUTTONDOWN:
        # remove_last_polyline()
        if not is_inside_polyline(x, y):
            remove_last_polyline()
        else:
            remove_polyline_at_point(x, y)

def remove_last_polyline():
    if polylines:
        del polylines[-1]
        if area_name:
            del area_name[-1]

def remove_polyline_at_point(x, y):
    global area_name, polylines
    removed_index = None

    for i, polyline in enumerate(polylines):
        result = cv2.pointPolygonTest(polyline, (x, y), False)
        if result >= 0:
            removed_index = i
            break

    if removed_index is not None:
        del polylines[removed_index]
        del area_name[removed_index]

        # Decrement area names of remaining polylines
        for i in range(removed_index, len(area_name)):
            area_name[i] = str(int(area_name[i]) - 1)

def is_inside_polyline(x, y):
    for polyline in polylines:
        result = cv2.pointPolygonTest(polyline, (x, y), False)
        if result >= 0:
            return True
    return False

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

    frame=cv2.resize(frame,(1020,500))

    for i, polyline in enumerate(polylines):
        print("testing polyline enumeratte --> ", i)
        cv2.polylines(frame,[polyline], True, (0,0,255), 2)
        ptr(frame,f'{area_name[i]}', tuple(polyline[0]),1,1)

    cv2.imshow('FRAME', frame)
    cv2.setMouseCallback('FRAME', draw)
    Key = cv2.waitKey(10) & 0xFF

    if Key == ord('s'):
        with open("polyCords","wb") as f:
            data = {
                'polylines': polylines,
                'area_name':area_name
            }
            pickle.dump(data,f)

    if Key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
