from tensorflow.keras.models import model_from_json
from tensorflow.python.keras.backend import set_session
import numpy as np

import tensorflow as tf

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.15
session = tf.compat.v1.Session(config=config)
set_session(session)


class FacialExpressionModel(object):

    EMOTIONS_LIST = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    def __init__(self, model_weights_file):
        # load model from JSON file
       # with open(model_json_file, "r") as json_file:
        #    loaded_model_json = json_file.read()
         #   self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        #self.loaded_model.compile()
        #self.loaded_model._make_predict_function()

    def predict_emotion(self, img):
        global session
        set_session(session)
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]









#import cv2

#video=cv2.VideoCapture(0)

#faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#while True:
    #ret,frame=video.read()
    #faces=faceDetect.detectMultiScale(frame, 1.3, 5)
    #for x,y,w,h in faces:
        #x1,y1=x+w, y+h
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 1)
        #cv2.line(frame, (x,y), (x+30, y),(255,0,255), 6) #Top Left
        #cv2.line(frame, (x,y), (x, y+30),(255,0,255), 6)

        #cv2.line(frame, (x1,y), (x1-30, y),(255,0,255), 6) #Top Right
        #cv2.line(frame, (x1,y), (x1, y+30),(255,0,255), 6)

        #cv2.line(frame, (x,y1), (x+30, y1),(255,0,255), 6) #Bottom Left
        #cv2.line(frame, (x,y1), (x, y1-30),(255,0,255), 6)

        #cv2.line(frame, (x1,y1), (x1-30, y1),(255,0,255), 6) #Bottom right
        #cv2.line(frame, (x1,y1), (x1, y1-30),(255,0,255), 6)

    #cv2.imshow("Frame", frame)
    #k=cv2.waitKey(1)
    #if k==ord('q'):
     #   break
#video.release()
#cv2.destroyAllWindows()
