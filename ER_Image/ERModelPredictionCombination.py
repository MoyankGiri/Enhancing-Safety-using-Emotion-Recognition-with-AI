import sys
sys.path.append('C:\\Users\\moyan\\Desktop\\Capstone Project - Emotion Recognition using AI\\Enhancing-Safety-using-Emotion-Recognition-with-AI\\Speech_Emotion_Recognizer')

import RealTime_VideoEmotionRecognition as realTimeVideoER
import streaming as realTimeAudioER
import EmotionScoreCalculation_simplified as EMScore
from imutils.video import VideoStream
import cv2
import threading

class ERModelPredictionCombination:

    def __init__(self):
        self.VideoModelClass = realTimeVideoER.RealTime_VideoEmotionRecognition()
        self.AudioModelClass = realTimeAudioER.LivePredictions(file=None)
        self.EMScoreClass = EMScore.EmotionScoreCalculation()
    
    def combinedPrediction(self):
        liveVideoStream = VideoStream(src=0).start()
        #start = time.perf_counter()
        data = []
        time_value = 0
        lStart, lEnd, rStart, rEnd = self.VideoModelClass.loadFaceDetector()
        t1 = threading.Thread(target=realTimeAudioER.takeAudio)
        t2 = threading.Thread(target=realTimeAudioER.findEmotion)
        t1.start()
        t2.start()

        t1.join()

        while (self.VideoModelClass.predictionProbs is None) or (len(self.VideoModelClass.predictionProbs) == 0):
            self.VideoModelClass.realTimePrediction(liveVideoStream,lStart,lEnd,rStart,rEnd)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        liveVideoStream.stop()
        cv2.destroyAllWindows()
        print("Prediction probs from Video:", self.VideoModelClass.predictionProbs)

        VideoPred = self.EMScoreClass.VideoEmotionDetection(self.VideoModelClass.predictionProbs)
        t2.join()
        print("Final Prediction:", self.EMScoreClass.classIndices[self.EMScoreClass.FinalEmotionCalculation(VideoEmotion=VideoPred)])

        


if __name__ == "__main__":
    x = ERModelPredictionCombination()
    x.combinedPrediction()
