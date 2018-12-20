import os
import numpy as np
import cv2
import sqlite3
from PIL import Image

dtct=cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #cascade classifier object
webcam=cv2.VideoCapture(0) # video capture object

#function to take inputs
def data(id,name,age,record):
    connection = sqlite3.connect("face_database.db")
    command="SELECT ID,Name,Age,Record FROM Records WHERE id="+str(id)
    pointer=connection.execute(command)
    isRecord=0
    for row in pointer:
        isRecord=1
    if(isRecord==1):
        # updating the records.
        command="UPDATE Records SET Name="+str(name)+","+"age="+str(age)+","+"record="+str(record)+" WHERE ID="+str(id)
    else:
        # Inserting the new data.
        command="INSERT INTO Records(ID,Name,Age,Record) VALUES("+str(id)+","+str(name)+","+str(age)+","+str(record)+")"
    connection.execute(command)
    connection.commit()
    connection.close()
    
id=input("ID:")
name=input("Name:")
age=input("Age:")
record=input("Record:")

#function calling.
data(id,name,age,record)

sample=0
#now it is gonna take few samples of persons face[here 20] and assing a id to it and saves it in folder name "data".
while(True):
    ret, image=webcam.read()
    photo = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = dtct.detectMultiScale(photo, 1.3, 5); # general function that detects objects.
    # 1. grayscale_image
    # 2.he second is the scaleFactor.
    # Since some faces may be closer to the camera, they would appear bigger than the faces in the back.
    # The scale factor compensates for this.
    # 3. size.
    for (x,y,w,h) in faces:
        #incrementing sample no.
        sample = sample +1
        #saving the captured face in "data" folder.
        cv2.imwrite("data/User."+str(id)+"."+str(sample)+".jpg",photo[y:y+h,x:x+w])
        #imgae captured is photo[y:y+h,x:x+w] where x,y id top and left and h,w are height and width. 
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(20)
    cv2.imshow('frame',image)
    cv2.waitKey(100)
    if(sample>40):
        break
#camera released
webcam.release()

# Trainer start.
recognizer=  cv2.face.LBPHFaceRecognizer_create();
path='data'

#grab images from "data" folder
def getImages(path):
    # load the images from the "data" folder.
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    # list for faces and ids.
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        # loading image and converting it to gray scale.
        faceImg=Image.open(imagePath).convert('L'); #convert into gray scale
        # but its a PIL image[Python Imaging Library] so we need to convert it to numpy array.
        faceNp=np.array(faceImg,'uint8')
    # To get the id we split the image path and took the first from the last part (which is “-1” in python) and that is the name of the imagefile.
    # but we saved file name like "User.Id.Sample" so , if we split this using "." then we get user, id and sample , so to get id we will choose 1st index.  
        ID=int(os.path.split(imagePath)[-1].split('.')[1])          #[-1]count from backward
    # extracting the faces and appending them in faces list with id.
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("trainning",faceNp)
        cv2.waitKey(10)
    return np.array(IDs),faces

Ids,faces =getImages(path)
recognizer.train(faces,Ids)
recognizer.save('recognizer/trainning.yml')

#window closed.
cv2.destroyAllWindows()
