from numpy import argmax
from warnings import warn

VideoERModelAccuracy, AudioERModelAccuracy = 0.9, 0.8

classIndices = {0: 'angry', 1: 'disgust', 2: 'fear',
                3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise', None: ''}

# Code to get emotion probabilities from Video And Audio ER Models

# Code to get ER Model Accuracies 


def EmotionDetectionCombined(VideoEmotionProbabilities=None, AudioEmotionProbabilities=None):
    if VideoEmotionProbabilities is None and AudioEmotionProbabilities is None:
        warn("No Input.... No Emotion Detected")

    elif VideoEmotionProbabilities is None:
        print("Only Audio Input....Audio Detected Emotion\n")
        return classIndices[argmax(AudioEmotionProbabilities)]

    elif AudioEmotionProbabilities is None:
        print("Only Video Input....Video Detected Emotion\n")
        return classIndices[argmax(VideoEmotionProbabilities)]

    else:
        VideoEmotion = argmax(VideoEmotionProbabilities)
        AudioEmotion = argmax(AudioEmotionProbabilities)

        if VideoEmotion == AudioEmotion:
            return classIndices[VideoEmotion]
        else:
            return VideoEmotion if VideoERModelAccuracy * VideoEmotionProbabilities[VideoEmotion] > AudioERModelAccuracy * AudioEmotionProbabilities[AudioEmotion] else AudioEmotion

EmotionDetectionCombined()