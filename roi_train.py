import cv2
import numpy as np
from utils import putTextRect as ptr
import pickle

# Loading the video feed - Plaksha_Parking2 to be used for Plaksha
cap = cv2.VideoCapture('')

# drawing - boolean to be true/false to decide wheather the current mouse event is eligible for drawing or stop drawing
# area_name - the list to store all the area names for all the polygons drawn i.e. the RoIs
# paused - booelan to be used to pause the video feed as soon as the mouse event is triggered
drawing = False
area_name = []
paused = False

# Try-Except block to read the polyCord file to read the coordinates for all the polygons drawn : If Exists
# or else, set the polylines list to be empty
# polylines - list to store arrays of polygon coordinates 
try:
    with open("polyCords","rb") as f:
                data = pickle.load(f)
                polylines, area_name = data['polylines'], data['area_name']
except:
    polylines = []

# points - list to store all the individual points
# current_name - the current name of the area under consideration
points = []
current_name = " "

# Code block to draw the polylines and create the RoIs i.e. the bounding boxes for each parking spots
# Hardware inputs - mouse left and right buttons
def draw(event, x, y, flags, param):
    global points, drawing, paused
    drawing = True

    # Left Mouse Button event
    # Drawing polygons and creating the RoIs
    # Storing the initial coordinates of the mouse click to start the polyline
    if event == cv2.EVENT_LBUTTONDOWN:
        points = [(x,y)]
        paused = not paused

    # Storing all the points while the mouse is dragged to draw the polygon
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x,y))

    # Storing all the polygon coordinates along with the area name (which is generated automatically - 1,2,...) while the mouse button is released
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        current_name = str(len(area_name) + 1)
        area_name.append(current_name)
        polylines.append(np.array(points,np.int32))
        paused = not paused

    # Right Mouse Button event
    # Removing the polygons and the RoIs
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Based on the True/False value the respective methods are called to remove the polygon
        if not is_inside_polyline(x, y):
            remove_last_polyline()
        else:
            remove_polyline_at_point(x, y)

# When the right button is clicked anywhere else other than the RoIs:
# Removing the last created polygon
def remove_last_polyline():
    if polylines:
        del polylines[-1]
        if area_name:
            del area_name[-1]

# When the right button is clicked anywhere within the RoIs:
# Removing that particular polygon, and accordingly update the area names
def remove_polyline_at_point(x, y):
    global area_name, polylines
    removed_index = None

    # Testing whether the coordinates of the point clicked is within the polygon - using pointPolygonTest
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

# Method to return True/False if the coordinate of the point of the button clicked is within any RoIs
def is_inside_polyline(x, y):
    for polyline in polylines:
        result = cv2.pointPolygonTest(polyline, (x, y), False)
        if result >= 0:
            return True
    return False

# Reading the video feed frame by frame, and when completed, set to the beginning to again start the loop
while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

    # Setting frame size to 1020x500
    frame = cv2.resize(frame,(1020,500))

    # Drawing the polygons i.e. the RoIs, which are red in color
    # Appending the area names by default as numbers
    for i, polyline in enumerate(polylines):
        print("testing polyline enumeratte --> ", i)
        cv2.polylines(frame, [polyline], True, (0,0,255), 2)
        ptr(frame, f'{area_name[i]}', tuple(polyline[0]),1,1)

    cv2.imshow('FRAME', frame)
    cv2.setMouseCallback('FRAME', draw)
    Key = cv2.waitKey(10) & 0xFF

    # Keyboard event, where:
    # key 's' -> to save all the polylines drawn i.e. the polygons i.e. the RoIs at any moment in time
    # key 'q' -> to stop the video feed and exit
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
