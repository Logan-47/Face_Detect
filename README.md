# Face_Detect
A basic Face_Detection program in Python using OpenCV.

requirements
> SQLlite database. the given database `face_database.db` is SQLlite database. it will store the data/records.

``` Install opencv by running : pip3 install -r requirements.txt```

1. Creat a Empty folder named "data". in the main Directory of repo..
2. then run ```python3 Full_Face_Detection.py``` It will scan the face and create sample images in the data folder.
3. Then run ```python3 detector.py``` it will show the Id,name,record of the detected face if it is on database.

#### it also have PushBullet API support.[used in instant notification if any face that is in the database is detected]
