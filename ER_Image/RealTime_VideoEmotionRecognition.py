from ast import arg
from scipy.spatial import distance as dist
import numpy as np
import cv2
from imutils import face_utils
from imutils.video import VideoStream
import imutils
import argparse
import time
import dlib
import os
import tensorflow as tf
import pandas as pd
from fastai.vision import *

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
working_dir_path = str(parent_dir) + '\\ER_Image'

ap = argparse.ArgumentParser()
ap.add_argument("--save", dest="save", action="store_true")
ap.add_argument("--no-save", dest="save", action="store_false")
ap.set_defaults(save=False)
ap.add_argument("--savedata", dest="savedata", action="store_true")
ap.add_argument("--no-savedata", dest="savedata", action="store_false")
ap.set_defaults(savedata=False)
ap.add_argument("--savepath", dest="savepath")
ap.set_defaults(savepath="./")
args = vars(ap.parse_args())

class RealTime_VideoEmotionRecognition:

    def __init__(self):

        self.VideoERModel = tf.keras.models.load_model(working_dir_path + "\\FER_ModifiedModel_balanced.h5")
        self.FaceCascadeClassifier = cv2.CascadeClassifier(working_dir_path + "\\haarcascade_frontalface_default.xml")
        self.predictor = None
        self.prediction = None
        self.predictionProbs = []
        self.classIndices = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise', None: ''}
        self.out = None
        self.EYE_AR_THRESH = 0.20
        self.EYE_AR_CONSEC_FRAMES = 10
        self.COUNTER = 0
        self.FRAMES = -1
    
    def eye_aspect_ratio(self,eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def data_time(self,time_value, prediction, probability, ear):
        current_time = int(time.perf_counter()-start)
        if current_time != time_value:
            data.append([current_time, prediction, probability, ear])
            time_value = current_time
        return time_value
    
    def loadFaceDetector(self,faceLandmarksPath = working_dir_path + "\\shape_predictor_68_face_landmarks.dat", saveOutput = args["save"], savePath = args["savepath"]):

        self.predictor = dlib.shape_predictor(faceLandmarksPath)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        if saveOutput:
            self.out = cv2.VideoWriter(savePath + "liveoutput.avi",
                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (450, 253))
        return lStart, lEnd, rStart, rEnd

    def realTimePrediction(self,liveVideoStream, lStart, lEnd, rStart, rEnd):

        frame = liveVideoStream.read()
        self.FRAMES += 1
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        face_coord = self.FaceCascadeClassifier.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        for coords in face_coord:
            X, Y, w, h = coords
            H, W, _ = frame.shape
            X_1, X_2 = (max(0, X - int(w * 0.3)), min(X + int(1.3 * w), W))
            Y_1, Y_2 = (max(0, Y - int(0.3 * h)), min(Y + int(1.3 * h), H))
            img_cp = gray[Y_1:Y_2, X_1:X_2].copy()
            #prediction, idx, probability = learn.predict(Image(pil2tensor(img_cp, np.float32).div_(225)))
            if self.FRAMES % 100 == 0:
                self.prediction = np.argmax(self.VideoERModel.predict(np.expand_dims(np.expand_dims(cv2.resize(img_cp, (48, 48)), -1), 0)))
                self.predictionProbs = list(self.VideoERModel.predict(np.expand_dims(np.expand_dims(cv2.resize(img_cp, (48, 48)), -1), 0)))
            cv2.rectangle(
                img=frame,
                pt1=(X_1, Y_1),
                pt2=(X_2, Y_2),
                color=(128, 128, 0),
                thickness=2,
            )
            rect = dlib.rectangle(X, Y, X+w, Y+h)
            if self.FRAMES % 100 == 0:
                print(self.prediction)
            cv2.putText(frame, str(self.classIndices[self.prediction]), (
                10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 0), 2)
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < self.EYE_AR_THRESH:
                self.COUNTER += 1
                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                    cv2.putText(frame, "Distracted", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                self.COUNTER = 0
            cv2.putText(frame, "Eye Ratio: {:.2f}".format(
                ear), (250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #time_value = data_time(time_value, prediction, probability, ear)
        if self.FRAMES % 100 == 0:
            if len(face_coord) == 0:
                self.prediction = None
        cv2.imshow("frame", frame)
        if self.out is not None:
            self.out.write(frame)


if __name__ == "__main__":

    liveVideoStream = VideoStream(src=0).start()
    start = time.perf_counter()
    data = []
    time_value = 0
    VideoERPredictionModelClass = RealTime_VideoEmotionRecognition()
    lStart, lEnd, rStart, rEnd = VideoERPredictionModelClass.loadFaceDetector()

    while True:
        VideoERPredictionModelClass.realTimePrediction(liveVideoStream,lStart,lEnd,rStart,rEnd)
        #realTimePrediction(liveVideoStream, VideoERModel, FaceCascadeClassifier, predictor, lStart, lEnd, rStart, rEnd, out)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if args["savedata"]:
        df = pd.DataFrame(data, columns=['Time (seconds)', 'Expression', 'Probability', 'EAR'])
        df.to_csv(args["savepath"]+'/exportlive.csv')
        print("data saved to exportlive.csv")

    liveVideoStream.stop()

    if args["save"]:
        print("done saving video")
        VideoERPredictionModelClass.out.release()

    cv2.destroyAllWindows()
