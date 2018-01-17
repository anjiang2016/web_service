# web_service
a small web service use mtcnn for facedetected
# useage:
### show the image on server:
http://192.168.7.37:8393/show/
http://192.168.7.37:8393/show/?start_num=1&length=47&dirname=video%2Fstudent_images%2F


### do face detec:
http://192.168.7.37:8393/facedetec/

### use the face detec api:
http://192.168.7.37:8393:/apis/
#### for example:
http://192.168.7.37:8393/apis/?url=https%3A%2F%2Fss1.bdstatic.com%2F70cFuXSh_Q1YnxGkpoWK1HF6hhy%2Fit%2Fu%3D2762678811%2C2154977094%26fm%3D27%26gp%3D0.jpg
#### this will return:
{"img_result": "http://192.168.7.37:8393/static/face_detect_u=2762678811,2154977094&fm=27&gp=0.jpg.jpg", "boxstr": "face[1]:[219.337334,286.127627,311.318285,415.273748]<br/>face[2]:[119.448813,277.364546,212.329136,403.095747]<br/>face[3]:[320.877833,271.137433,423.030022,405.554612]<br/>face[4]:[323.902125,11.838839,425.545304,138.334798]<br/>face[5]:[74.449405,76.125240,158.835411,182.345312]<br/>face[6]:[189.457448,52.252446,280.120322,182.184828]<br/>", "face_num": 6}
#### open your python script in your server:
http://192.168.7.37:8393/run/?filepath=%2Fdata1%2Fmingmingzhao%2Fdlib%2Fpython_examples%2Fcv2drawlib.py&content=input+the+file+content&activity=open&text_style=vim

#### run your python script in your server:
http://192.168.7.37:8393/run/?filepath=%2Fdata1%2Fmingmingzhao%2Fdlib%2Fpython_examples%2Fcv2drawlib.py&content=input+the+file+content&activity=run&text_style=vim
