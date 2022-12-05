from numpy import argmax

class EmotionScoreCalculation:

    def __init__(self):
        self.VideoClassIndices = {0: 'angry', 1: 'disgust', 2: 'fear',
                3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise', None: ''}
        self.AudioClassIndices = {0: 'neutral',
                            1: 'calm',
                            2: 'happy',
                            3: 'sad',
                            4: 'angry',
                            5: 'fearful',
                            6: 'disgust',
                            7: 'surprised',
                            None: ''}
        self.VideoERModelAccuracy = 0.9
        self.AudioERModelAccuracy = 0.8
        
    # Returs a list of 2 values of the form [DetectedEmotion, Probability of Detected Emotion]
    def VideoEmotionDetection(self,VideoEmotionProbabilities):
        # DetectedEmotion => argmax(VideoEmotionProbabilities)
        #print("TEMP",argmax(VideoEmotionProbabilities),list(VideoEmotionProbabilities)[0][argmax(VideoEmotionProbabilities)])
        #print("1", VideoEmotionProbabilities)
        #print("2", argmax(VideoEmotionProbabilities))
        #print("3", list(VideoEmotionProbabilities)[0][argmax(VideoEmotionProbabilities)])
        return [None,0] if len(VideoEmotionProbabilities) == 0 else [argmax(VideoEmotionProbabilities),list(VideoEmotionProbabilities)[0][argmax(VideoEmotionProbabilities)]]

    def AudioEmotionDetection(self,AudioEmotionProbabilities):
        # DetectedEmotion => argmax(VideoEmotionProbabilities)
        #print("1", AudioEmotionProbabilities)
        #print("2", argmax(AudioEmotionProbabilities))
        #print("3", AudioEmotionProbabilities[0][argmax(AudioEmotionProbabilities)]) 
        return [None,0] if AudioEmotionProbabilities is None else [argmax(AudioEmotionProbabilities),AudioEmotionProbabilities[0][argmax(AudioEmotionProbabilities)]]

    # returns None as output if both score is zero else returns max emotion
    def FinalEmotionCalculation(self,VideoEmotion = [None,0], AudioEmotion = [None,0]):

        VideoScore = self.VideoERModelAccuracy * VideoEmotion[1]
        AudioScore = self.AudioERModelAccuracy * AudioEmotion[1]

        return ['video', VideoEmotion[0]] if VideoScore >= AudioScore else ['audio', AudioEmotion[0]]