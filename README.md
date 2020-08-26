# Face_Detect

A Face Detection System built using Python, OpenCV, and SQL.

`Install all the dependencies by running : pip install -r requirements.txt`

> `face_database.db` is provided You can clear that DB first and can use it.

1. First run `python Full_Face_Detection.py` It will scan the face and create sample images inside the data directory.
1. Then run `python3 detector.py` it will show the Id,name,record of the detected face if it is present in the database.

#### it also have PushBullet API support.[used for instant notification if any face that is in the database is detected]

> to use the pushbullet API go in `detector.py` and uncomment the pushbullet API code and put you API key in place of "API KEY"
