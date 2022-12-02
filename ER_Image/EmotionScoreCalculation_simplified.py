from numpy import argmax

class EmotionScoreCalculation:

    def __init__(self):
        self.classIndices = {0: 'angry', 1: 'disgust', 2: 'fear',
                3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise', None: ''}
        self.VideoERModelAccuracy = 0.9
        self.AudioERModelAccuracy = 0.8
        
    # Returs a list of 2 values of the form [DetectedEmotion, Probability of Detected Emotion]
    def VideoEmotionDetection(self,VideoEmotionProbabilities):
        # DetectedEmotion => argmax(VideoEmotionProbabilities)
        #print("TEMP",argmax(VideoEmotionProbabilities),list(VideoEmotionProbabilities)[0][argmax(VideoEmotionProbabilities)])
        return [None,0] if len(VideoEmotionProbabilities) == 0 else [argmax(VideoEmotionProbabilities),list(VideoEmotionProbabilities)[0][argmax(VideoEmotionProbabilities)]]

    def AudioEmotionDetection(self,AudioEmotionProbabilities):
        # DetectedEmotion => argmax(VideoEmotionProbabilities) 
        return [None,0] if len(AudioEmotionProbabilities) == 0 else [argmax(AudioEmotionProbabilities),AudioEmotionProbabilities[argmax(AudioEmotionProbabilities)]]

    # returns None as output if both score is zero else returns max emotion
    def FinalEmotionCalculation(self,VideoEmotion = [None,0], AudioEmotion = [None,0]):

        VideoScore = self.VideoERModelAccuracy * VideoEmotion[1]
        AudioScore = self.AudioERModelAccuracy * AudioEmotion[1]

        return VideoEmotion[0] if VideoScore >= AudioScore else AudioEmotion[0]