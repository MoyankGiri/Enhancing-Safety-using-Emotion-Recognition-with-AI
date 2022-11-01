"""
This file can be used to try a live prediction. 
"""

import keras
import librosa
import numpy as np
from playsound import playsound

import speech_text_translation as stt
from config import EXAMPLES_PATH
from config import MODEL_DIR_PATH
from config import ALERTS_PATH

                
class LivePredictions:
    """
    Main class of the application.
    """

    def __init__(self, file):
        """
        Init method is used to initialize the main parameters.
        """
        self.file = file
        self.path = MODEL_DIR_PATH + 'Emotion_Voice_Detection_Model.h5'
        self.loaded_model = keras.models.load_model(self.path)

    def make_predictions(self):
        """
        Method to process the files and create your features.
        """
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predict = self.loaded_model.predict(x)
        print(predict) #to get probability for each class
        #predictions = np.argmax(predict, axis=1)
        #emotion = self.convert_class_to_emotion(predictions)
        #print( "Prediction is", " ", emotion)
        #if emotion=='angry' or emotion=='fearful':
            #playsound(ALERTS_PATH + 'peaceful-ambiance-theme-6350.mp3')
        #elif emotion=='sad':
            #playsound(ALERTS_PATH + 'lifting-12548.mp3')

    @staticmethod
    def convert_class_to_emotion(pred):
        """
        Method to convert the predictions (int) into human readable strings.
        """
        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label


if __name__ == '__main__':
    #live_prediction.loaded_model.summary() -> to get summary of the model
    AUDIO_FILE = 'angry2.wav' #must be present in examples folder and must be .wav   -> won't work for this audio file as it was recorded with scipy, not wavio
    #if stt.convert(EXAMPLES_PATH + AUDIO_FILE) != -1: 
    live_prediction = LivePredictions(file=EXAMPLES_PATH + AUDIO_FILE)
    live_prediction.make_predictions()
    AUDIO_FILE = 'surprised.wav' #must be present in examples folder and must be .wav
    #if stt.convert(EXAMPLES_PATH + AUDIO_FILE) != -1:    -> won't work for this audio file as it was recorded with scipy, not wavio
    live_prediction = LivePredictions(file=EXAMPLES_PATH + AUDIO_FILE)
    live_prediction.make_predictions()
    AUDIO_FILE = 'no_speech_test.wav' #must be present in examples folder and must be .wav    -> will work as this was recorded with updated record_audio.py with wavio
    if stt.convert(EXAMPLES_PATH + AUDIO_FILE) != -1:
        live_prediction = LivePredictions(file=EXAMPLES_PATH + AUDIO_FILE)
        live_prediction.make_predictions()
    #AUDIO_FILE = '03-01-05-02-01-01-10.wav' #must be present in examples folder and must be .wav   
    #live_prediction = LivePredictions(file=EXAMPLES_PATH + AUDIO_FILE)
    #live_prediction.make_predictions()
