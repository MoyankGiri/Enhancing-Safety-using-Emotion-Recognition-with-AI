import sys
sys.path.append('C:\\Users\\moyan\\Desktop\\Capstone Project - Emotion Recognition using AI\\Enhancing-Safety-using-Emotion-Recognition-with-AI\\Speech_Emotion_Recognizer')
#sys.path.append('C:\\Users\\rames\\Desktop\\Enhancing-Safety-using-Emotion-Recognition-with-AI\Speech_Emotion_Recognizer')
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
        t2 = threading.Thread(target=realTimeAudioER.findEmotion, args=(self.AudioModelClass,))
        t1.start()
        t2.start()

        #t1.join()
        while t1.is_alive():
            self.VideoModelClass.realTimePrediction(liveVideoStream,lStart,lEnd,rStart,rEnd)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        liveVideoStream.stop()
        cv2.destroyAllWindows()
        t2.join()

        self.VideoModelClass.predictionProbs = [x / self.VideoModelClass.runs for x in self.VideoModelClass.predictionProbs]
        #print("Prediction probs from Audio:", self.AudioModelClass.emotion_array)
        #print("Prediction probs from Video:", self.VideoModelClass.predictionProbs)


        #VideoPred = self.EMScoreClass.VideoEmotionDetection([x / self.VideoModelClass.runs for x in self.VideoModelClass.predictionProbs])
        VideoPred = self.EMScoreClass.VideoEmotionDetection(self.VideoModelClass.predictionProbs)
        AudioPred = self.EMScoreClass.AudioEmotionDetection(self.AudioModelClass.emotion_array)
        #t2.join()
        print("Prediction from Video Model: ",self.EMScoreClass.VideoClassIndices[VideoPred[0]])
        print("Prediction from Audio Model: ",self.EMScoreClass.AudioClassIndices[AudioPred[0]])
        combined_emotion = self.EMScoreClass.FinalEmotionCalculation(VideoEmotion=VideoPred, AudioEmotion=AudioPred)
        if combined_emotion[0] == 'video':
            result = self.EMScoreClass.VideoClassIndices[combined_emotion[1]]
        else:
            result = self.EMScoreClass.AudioClassIndices[combined_emotion[1]]
        print("Final Prediction:", result)
        return result

        


def FinalEmotion():
    x = ERModelPredictionCombination()
    value = x.combinedPrediction()
    return value

if __name__ == "__main__":
    x = ERModelPredictionCombination()
    value = x.combinedPrediction()
    cv2.destroyAllWindows()
    print(value)
        