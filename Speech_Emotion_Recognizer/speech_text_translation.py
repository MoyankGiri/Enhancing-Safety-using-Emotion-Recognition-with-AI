import speech_recognition as sr
import pyttsx3

def convert(sourceFile):
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile(sourceFile) as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio_text = r.listen(source)
        
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            
            # using google speech recognition
            text = r.recognize_google(audio_text)
            return text
        
        except:
            print('No input speech detected!')
            return -1