# return np.linalg.norm(face_encodings - face_to_compare, axis=1)
# TypeError: ufunc 'subtract' did not contain a loop with signature matching types dtype('<U2080') dtype('<U2080') dtype('<U2080')
# File "C:/Users/py/Documents/GitHub/lab1zakh/recognition.py", line 56, in <module>
# matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
# <class 'numpy.ndarray'>
# <class 'numpy.ndarray'>