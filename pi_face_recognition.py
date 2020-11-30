from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import os
import shutil

from database import update

path = os.getcwd()+'/screenshots'
if os.path.isdir(path):
    shutil.rmtree(path)
    os.mkdir(path)
else:
    os.mkdir(path)

u_names = set()

#setting start up serrvo positions
#positions range from (50-250)
servo1 = 100
servo2 = 100
pic=0

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "Provide path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
	help="Provide path to serialized DB of facial encodings")
args = vars(ap.parse_args())

# Load the known faces and embeddings along with OpenCV's Haar cascade for face detection
print("Loading encodings and Face Detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

# Initialize the video stream and allow the camera sensor to warm up
print("Starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Start the FPS counter
fps = FPS().start()

# Loop over frames from the video file stream
while True:
	# Grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=600)
	
	# Convert the input frame from
	#(1) BGR to grayscale (for face detection) and
	#(2) BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# Detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we reorder
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# Compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# Loop over the facial embeddings
	for encoding in encodings:
		# Attempt to match each face in the input image to our known encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# Check to see if we have found a match
		if True in matches:
			# Find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# Loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# Determine the recognized face with the largest number of votes 
			name = max(counts, key=counts.get)
		
		# Update the list of names
		names.append(name)

	# Loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# Draw the predicted face name on the image
		u_names.add(name)
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)    

	# Display the image to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKeyEx(1) & 0xFF

	# If the `q` key was pressed, break from the loop
	if key == ord("q"):
		print("Screenshots taken:",pic)
		print("Quitting...")
		break
	elif key == ord("p"):
		print("Image Captured!")
		path = 'screenshots/screenshot'+str(pic+1)+'.jpg'
		cv2.imwrite(path,frame)
		pic+=1
	elif key == 81:
		if servo1 > 50:
			servo1 = servo1 -2
		os.system("echo 6=%s > /dev/servoblaster" %servo1) 
		time.sleep(0.005)
	elif key == 82:
		if servo2 > 50:    
			servo2 = servo2 -2
		os.system("echo 5=%s > /dev/servoblaster" %servo2) 
		time.sleep(0.005)
	elif key == 83:
		if servo1 < 150:
			servo1 = servo1 +2
		os.system("echo 6=%s > /dev/servoblaster" %servo1) 
		time.sleep(0.005)
	elif key == 84:
		if servo2 < 150:
			servo2 = servo2 +2
		os.system("echo 5=%s > /dev/servoblaster" %servo2) 
		time.sleep(0.005)

	# Update the FPS counter
	fps.update()

# Stop the timer and display FPS information
fps.stop()
print("Elasped time: {:.2f}".format(fps.elapsed()))
print("Approx. FPS: {:.2f}".format(fps.fps()))

#Update Attendance
if (len(u_names)!=0):
    if(len(u_names) == 1 and 'Unknown' in u_names):
        update(None,"No recognizable students present!")
    else:
        update(u_names,"Attendance Records Updated!")
else:
    update(None,"No students present!")

# Do cleanup
cv2.destroyAllWindows()
vs.stop()