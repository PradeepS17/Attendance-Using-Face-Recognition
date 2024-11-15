import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = "Attendance image"
images = []
className = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])
print(className)

def findEncodings(images):
    encodeList =[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
kList=[]
def markAttendance(name):
    with open('testing.csv', "a+")as f:
        myDataList = f.readlines()
        nameList = set(kList)
        print(name)
        #for line in myDataList:
            #entry = line.split(',')
           # print(entry)
           # nameList.append(name)
        if name not in nameList:
            kList.append(name)
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            roll = "22CB"+name[-3:]
            name1 = name[:-4]
            f.writelines(f'\n{roll},{name1},{tString},{dString}')
        
            
encodeListKnown = findEncodings(images)
print('ENCODE DETECTED')

cap = cv2.VideoCapture(0)
    
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = className[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    cv2.imshow('webcam', img)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destroyAllWindow()
