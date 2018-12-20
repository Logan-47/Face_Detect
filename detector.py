import numpy as np
import cv2
import sqlite3
#from pushbullet import PushBullet

dtct= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
webcam = cv2.VideoCapture(0)
rec=cv2.face.LBPHFaceRecognizer_create() #Recognizer Object using Opencv library.
try:
    rec.read('./recognizer/trainning.yml') # load data from database.
except:
    rec.read('recognizer\\trainning.yml') # load data from database.



id=0
mssg=0
previd=0
def record_data(id):
    connection=sqlite3.connect("face_database.db")
    command="SELECT * FROM Records WHERE id="+str(id)
    pointer=connection.execute(command)
    record=None
    for row in pointer:
        record=row
    connection.close()
    return record
    

font = cv2.FONT_HERSHEY_SIMPLEX #font
fontscale = 1                   # font size.
fontcolor = (255, 255, 0)       # font colour.
while(True):
    ret, img = webcam.read()    #started capturing frames.       
    photo = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # Converting it to gray scale.
    faces = dtct.detectMultiScale(photo, 1.3, 5)    #detect and extract faces from images.
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(photo[y:y+h,x:x+w]) #to recognize the id. [Confidence level]
        
        record = record_data(id)
        if(conf<40):
            mssg=1
            if(record!=None):
                 if(previd != id):
                     key=1
                 else:
                     key=0
                 name_S = str(record[1])
                 age_S = str(record[2])
                 record_S = str(record[3])
                 Id_S = str(record[0]) 
                 cv2.putText(img,"ID:"+str(record[0]),(x,y+h+20),font,fontscale,fontcolor)
                 cv2.putText(img,"Name:"+str(record[1]),(x,y+h+50),font,fontscale,fontcolor)
                 cv2.putText(img,"Age:"+str(record[2]),(x,y+h+90),font,fontscale,fontcolor)
                 cv2.putText(img,"Record:"+str(record[3]),(x,y+h+130),font,fontscale,fontcolor)
                 previd = record[0]
                 # Push Bullet API to send instant messages..
                 #if(mssg==1 and key==1):
                  #   mssg=0
                   #  key=0
                    # pb = PushBullet("API key")
                     #pb.push_note("Face Recognized","ID"+Id_S+"\n Name:"+name_S+"\n Age:"+age_S+"\n record:"+record_S)
                     #"""with open("photo.jpg", "rb") as pic:
                     #file_data = pb.upload_file(pic, "photo.jpg")
                     #push = pb.push_file(**file_data)
                     #pb.push_note("Facerecognization","Hello")"""
            
        else:
            cv2.putText(img,"Unknown",(x,y+h+30),font,fontscale,fontcolor)                    
    cv2.imshow('frame',img)
    cv2.waitKey(10)
    if cv2.waitKey(1) == ord('e'):
        break
    
webcam.release()
cv2.destroyAllWindows()
