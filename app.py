# import base64
# from flask import Flask,request,render_template,jsonify

# app=Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/_api",methods=["GET","POST"])
# def api():
#     return jsonify(result=time.time())
#     print("JJJJJ\n")
#     if request.method=="GET":
#         return "No picture"
#     elif request.method=="POST":
#         print("hello")
#         image_data=request.form.get("content").split(",")[1]
#         with open("clientimage.png","wb") as f:
#             f.write(base64.b64decode(image_data))
#         # mess="got picture"
#         return render_template("index.html",mes="gotit")

# if __name__=="__main__":
#     app.run(debug=True)



from flask import Flask, jsonify, render_template, request
import webbrowser
import time
import cv2
# Numpy for array related functions
import numpy as np
import os
# Dlib for deep learning based Modules and face landmark detection
import dlib
#face_utils for basic operations of conversion
from imutils import face_utils
import vlc
from PIL import Image

app = Flask(__name__)

cap = cv2.VideoCapture(0)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")




def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)

	#Checking if it is blinked
	if(ratio>0.25):
		return 2
	elif(ratio>0.21 and ratio<=0.25):
		return 1
	else:
		return 0



t=0
@app.route('/_stuff', methods = ['GET','POST'])
def stuff():
    global sleep
    global active
    global drowsy
    global status
    # print("ENTER")
    # print(status)
    if request.method == 'POST':
        # Get the file from post request
        # print("SEC")
        # print(request.form)
        f = request.form['hello']
        l=f.split(',')
        g=[]
        for i in l:
            g.append(int(i))
        # print(type(g[0]))
        arr=np.array(g)
        # print(arr.shape)
        arr=arr.reshape((10,10,4))
        # print(arr.shape)
        # arr2=arr[1:,:,:]
        arr=arr[:,:,:]
        # print(arr2.shape)
        # pixcels=[[(0,0,0)]*480 for _ in range(640)]
        # print(len(pixcels),len(pixcels[0]))
        # for i in range(640):
            # for j in range(480):
                # pixcels[i][j]=(arr2[2][i][j],arr2[1][i][j],arr2[0][i][j])
        array = np.array(arr, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array)
        new_image.save('new.png')
        frame=cv2.imread("new.png", cv2.IMREAD_COLOR)
        face_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            
            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            #The numbers are actually the landmarks which will show eye
            left_blink = blinked(landmarks[36],landmarks[37], 
                landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42],landmarks[43], 
                landmarks[44], landmarks[47], landmarks[46], landmarks[45])
            
            #Now judge what to do for the eye blinks
            if(left_blink==0 or right_blink==0):
                sleep+=1
                drowsy=0
                active=0
                if(sleep>=1):
                    status="SLEEPING !!!"
                    color = (255,0,0)

            elif(left_blink==1 or right_blink==1):
                sleep=0
                active=0
                drowsy+=1
                if(drowsy>=1):
                    status="Drowsy !"
                    color = (0,0,255)

            else:
                drowsy=0
                sleep=0
                active+=1
                if(active>=1):
                    status="Active :)"
                    color = (0,255,0)
            
            # if(status=="Drowsy !"):
            #     p = vlc.MediaPlayer("mixkit-facility-alarm-908.wav")
            #     p.play()
            # elif(status=="SLEEPING !!!"):
            #     p = vlc.MediaPlayer("mixkit-facility-alarm-908.wav")
            #     p.play()

            # cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

            for n in range(0, 68):
                (x,y) = landmarks[n]
        # ret,buffer=cv2.imencode('.jpg',frame)
        # frame=buffer.tobytes()
        # os.remove("new.png")
        result=status
        return result
    return "FLASK"


@app.route('/')
def index():
   
    return render_template('index.html')


# if __name__ == '__main__':
if 1:
    sleep=0
    active=0
    drowsy=0
    # if(drowsy>6):
    status="NO FACE DETECTED,PLEASE COME IN FRONT OF LIGHT!"
    app.run(debug=True)
