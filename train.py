import cv2
import numpy as np
import os

# 1. Initialize the LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# 2. Prepare dummy training data (In reality, load images from a directory)
# For this script to work, you need grayscale images of faces cropped to the face bounds.
faces = []
ids = []

def train_pfp(path):
    global faces, ids
    if os.path.exists(path): 
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        ids.append(1)

train_pfp('rahul.png')
train_pfp('photo2.png')
train_pfp('photo3.png')


# Example: Assuming you have a folder of your face named 'dataset/user_1/'
# You would loop through it, convert to grayscale, and append to the lists:
# img = cv2.imread('face_1.jpg', cv2.IMREAD_GRAYSCALE)
# faces.append(img)
# ids.append(1)  # 1 represents "User 1"

if len(faces) > 0:
    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer.yml')
    print("Model trained and saved as trainer.yml!")
else:
    print("Please add grayscale numpy arrays to 'faces' and integer IDs to 'ids' to train.")