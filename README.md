# Parking-Spot-Detection-and-Counter
Detection of parking spot (Occupied or Available), along with the live counter to show the availability.

### Steps to install
1. Download the zip folder from the main branch
2. Unzip to the desired location
3. Upload the video feed / Find a mechanism to link the live CCTV recordings to the project
4. Navigate to the roi_train.py, add the video file and run the file - (Run Current File in interactive Window - if in VSCode)
5. Create the Region of Interests (bounding boxes polylines), which is of free-hand style to accomodate all the parking spots to monitor
   - If running the code for the first time, the polyCords file will be created, consisting of the coordinates of all the polylines and the area names to individual regions created
   - Else no need to perform step 4 and 5, if the same video is being used and the polyCord file is generated prior already for the same
6. Navigate to detection_counter.py, add the video file and run the file

### Features offered in version 1
1. Detects all types of vehicles
2. Can work on diverse set of video feeds, provided the region of interest are marked properly (Case considered to be : India, where the video feeds come from CCTV, which is diagonally placed mostly)
3. Parking spots detection - available or occupied
4. Counter to track the current status of the entire parking space

### Output
https://github.com/kushalmatalia/Parking-Spot-Detection-and-Counter/assets/42527900/068900da-a1e8-470e-93eb-796ca270cdb2

### Methodology / Mechanism
1. The Polylines are created, to mark the region of interests, by storing the coordinates and the area names
2. Press 's' to save the coordinates to the polyCord file, 'q' to exit the video feed
3. Reading the same video feed with the region of interests and YOLO trained model to detect the vehicles like cars, trucks, buses, motorcycles (object detection)
4. Plotting the middle point as per the coordinates of the object detected (vehicle)
5. Comparing the points, if falls within the region of interest i.e. the bounding box
6. Adding the counter for all the overall video feed and do the detection and counter to be detected

### Future Application
1. Incorporate Aerial View in the video feed, to make it more diverse
2. Incorporate Image processing techniques like pixels manipulation, grayscale, masking to encompass the above mentioned application
3. To verify and update for night vision, since no such data is available yet
