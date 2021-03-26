# Face-Recognition-Attendance
A Raspberry Pi Face Recognition Attendance system with Pan and Tilt (using 2 Servo motors and Pan and Tilt Bracket) and OpenCV hog face recognition (using RPi camera module)
# Installation

**1. Clone the Repo by going to the command line on your Raspberry Pi (with a Camera Module) and run the command:**</br>

    git clone https://github.com/srividya-p/Face-Recognition-Attendance.git

**2. Open terminal and change the directory to Face-Recognition-Attendance** <br>

    cd Face-Recognition-Attendance

**3. Install the packages** <br>

    pip install -r requirements.txt

**4. Add images with naming format name_roll-no in the dataset folder** <br>

**5. Train the model for new images** <br>

    python3 encode_faces.py

**3. Run the face recognition app with the execute bash script** <br>

    ./execute.sh
    
# Screenshots
## Hardware Setup
![image](https://user-images.githubusercontent.com/74781344/112665078-ad563c00-8e80-11eb-8fe3-11677b06e22a.png)

## Face Recognition
![image](https://user-images.githubusercontent.com/74781344/112665206-d1b21880-8e80-11eb-8c77-43110c414d73.png)
##### Note - If you have a pan and tilt bracket set up with 2 servo motors you may use the arrow keys to move Camera Module.



  

    
