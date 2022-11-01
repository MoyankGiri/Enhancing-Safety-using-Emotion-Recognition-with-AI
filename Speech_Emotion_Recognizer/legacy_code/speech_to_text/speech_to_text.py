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
            happy = ['happy', 'delighted', 'great', 'fun', 'amazing', 'exciting']
            angry = ['angry', 'threatening', 'annoyed', 'terrible']
            surprised = ['wow', 'surprised', 'shocked', 'unbelievable']
            sad = ['sad', 'bad', 'sorry']
            fear = ['disappointed', 'scared', 'fearful', 'nervous']

            for i in happy:
                if i in text:
                    return 'happy'
            for i in angry:
                if i in text:
                    return 'angry'
            for i in surprised:
                if i in text:
                    return 'surprised'
            for i in sad:
                if i in text:
                    return 'sad'
            for i in fear:
                if i in text:
                    return 'fear'
            return 'calm'
        
        except:
            print('Sorry.. run again...')