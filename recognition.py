import face_recognition
import cv2
import numpy as np
import os
import pickle
from datetime import datetime

from pymongo import MongoClient as mc
myclient = mc("mongodb://localhost:27017/")
db = myclient["faceszakh"]
col = db["faces"]

# get names and faces from mongo

dirname = os.path.dirname(__file__) + '/known_people'

known_face_encodings = []
known_face_names = []
known_face_uids = []

cursor = col.find()
len = col.find().count()

for i in range(len):
    a = pickle.loads(cursor[i]['photo'])
    known_face_encodings.append(a)
    known_face_names.append(cursor[i]['name'])
    known_face_uids.append(cursor[i]['uid'])

    # known_face_names.append(cursor[i]['name'].replace(dirname,'')[1:-4])

# Initialize some variables
# face_locations = []
# face_encodings = []
face_names = []
process_this_frame = True

video_capture = cv2.VideoCapture(0)
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                uid = known_face_uids[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        dirname = os.path.dirname(__file__) + '/known_people'
        
        if name != 'Unknown':
            name = name[:-4].replace(dirname, '')[1:]
            cursor = col.find({'uid': f"""{uid}"""})
            time = str(datetime.now())[:-7]
            if time not in cursor[0]['time']:
                col.update_one({'uid': uid}, {'$push': {'time': time}})
                print(name +' появился в: '+ time)



        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (133, 133, 133), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (133, 133, 133), cv2.FILLED)
        font = cv2.FONT_ITALIC
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()