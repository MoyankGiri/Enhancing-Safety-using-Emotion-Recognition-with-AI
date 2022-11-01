
"""
This file can be used to try a live prediction while getting input audio stream. 
"""
import threading
import time
import keras
import librosa
import numpy as np
from playsound import playsound
import speech_text_translation as stt
import sounddevice as sd
import wavio as wv

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


def findEmotion():
    number_of_times = 1
    time.sleep(3)
    #live_prediction.loaded_model.summary() -> to get summary of the model
    for i in range(number_of_times):
        time.sleep(5)
        AUDIO_FILE = "recording0.wav" #must be present in examples folder and must be .wav
        if stt.convert(EXAMPLES_PATH + AUDIO_FILE) != -1:   
            live_prediction = LivePredictions(file=EXAMPLES_PATH + AUDIO_FILE)
            live_prediction.make_predictions()

    #AUDIO_FILE = '03-01-05-02-01-01-10.wav' #must be present in examples folder and must be .wav   
    #live_prediction = LivePredictions(file=EXAMPLES_PATH + AUDIO_FILE)
    #live_prediction.make_predictions()

def takeAudio():
    # Sampling frequency
    freq = 48000
    
    # Recording duration
    duration = 5

    number_of_times = 1 #number of times you want to record audio and get prediction
    
    # Start recorder with the given values 
    # of duration and sample frequency
    for i in range(number_of_times):
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

        print("Please Speak")  

        # Record audio for the given number of seconds
        sd.wait()

        print("Done Recording")
    
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        wv.write("C:\\Users\\rames\\Desktop\\Emotion-Classification-Ravdess\\examples\\recording0.wav", recording, freq, sampwidth=2)

if __name__ == "__main__":
    t1 = threading.Thread(target=takeAudio)
    t2 = threading.Thread(target=findEmotion)
    t1.start()
    t2.start()
    