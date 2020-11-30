#workon cv

#cd Desktop/FaceRec

# python3 encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

python3 pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# python3 pantilt.py