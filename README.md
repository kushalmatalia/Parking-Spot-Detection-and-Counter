# Parking-Spot-Detection-and-Counter
Detection of parking spot (Occupied or Available), along with the live counter to show the availability.
The Real-Time Parking Space Detector and Counter utilize computer vision for live monitoring of parking spaces. We establish Regions of Interest (ROIs) using polylines to define parking spots. It then employs the YOLO (You Only Look Once) algorithm to identify the presence of vehicles in the vacant spots, providing details on empty spaces including their names and counts, effectively addressing parking challenges.

### Steps to install
1. Download the zip folder from the main branch
2. Unzip to the desired location
3. Upload the video feed / Find a mechanism to link the live CCTV feeds to the project
4. Navigate to the roi_train.py, add the video file and run the file - (Run Current File in interactive Window - if in VSCode)
5. Create the Region of Interests (bounding boxes polylines), which is of free-hand style to accomodate all the parking spots to monitor
   - If running the code for the first time, the polyCord file will be created, consisting of the coordinates of all the polylines and the area names of the individual regions created
   - Else no need to perform step 4 and 5, if the same video is being used, the polyCord file is generated prior already for the same
6. Navigate to detection_counter.py, add the video file and run the file (No need to change anything else)
(NOTE : Can try this if you're using a CCTV camera application on your local network, you can typically access the camera feed using an IP address and a port number. Many CCTV camera applications provide a web-based interface to access the live video feed ('http://your_ip_address:your_port_number'))

### Features offered in version 1
1. Detects all types of vehicles
2. Can work on diverse set of video feeds, provided the region of interest are marked properly (Case considered to be : India, where the video feeds come from CCTV, which is diagonally placed mostly)
3. Parking spots detection - available or occupied
4. Counter to track the current status of the entire parking space
5. Available spots with their area names are displayed (have future implementations)

### Output
https://github.com/kushalmatalia/Parking-Spot-Detection-and-Counter/assets/42527900/068900da-a1e8-470e-93eb-796ca270cdb2

### Methodology / Mechanism
1. The Polylines are created, to mark the region of interests, by storing the coordinates and the area names
2. Press 's' to save the coordinates to the polyCord file, 'q' to exit the video feed
3. Right mouse click anywhere on the video feed except the RoIs to remove the last created RoI and right mouse click anywhere within the RoI to remove that particular RoI or the bounding box
4. Reading the same video feed with the region of interests and YOLO trained model to detect the vehicles like cars, trucks, buses, motorcycles (object detection)
5. Plotting the middle point as per the coordinates of the object detected (vehicle)
6. Comparing the middle points, if falls within the region of interest i.e. the bounding box
7. Adding the counter for all the overall video feed
8. Displaying the available spots with their area names

### Impact
1. Improved parking efficiency through real-time monitoring and space utilization optimization.
2. Reduced congestion and wait times for customers, leading to a better parking experience.
3. Potential benefits for parking lot owners include increased revenue, improved customer satisfaction, and streamlined operations
4. Automated monitoring and optimization reduce the need for manual intervention, saving manpower and resources for parking lot management.

### Future Application
1. Incorporate Aerial View in the video feed, to make it more diverse. Utilizing aerial view technologies enables comprehensive coverage and better situational awareness, enhancing overall detection effectiveness.
2. Incorporate Image processing techniques like pixels manipulation, grayscale, masking to encompass the above mentioned application. Incorporating YOLO alongside core image processing techniques to significantly enhance detection accuracy, especially in diverse weather conditions
3. To verify and update for night vision, since no such data is available yet

### References
1. https://docs.ultralytics.com/
2. https://github.com/ultralytics/ultralytics
3. https://www.geeksforgeeks.org/python-opencv-cv2-polylines-method/
4. https://www.analyticsvidhya.com/blog/2018/12/practical-guide-object-detection-yolo-framewor-python/
5. Error solving and debugging - https://stackoverflow.com/ , https://www.geeksforgeeks.org/
