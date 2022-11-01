import sounddevice as sd
#from scipy.io.wavfile import write
from config import EXAMPLES_PATH
import wavio as wv
  
# Sampling frequency
freq = 48000
  
# Recording duration
duration = 5

counter = 0
  
# Start recorder with the given values 
# of duration and sample frequency
for counter in range(1):

    AUDIO_FILE = "no_speech_test.wav"

    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    print("Please Speak")  

    # Record audio for the given number of seconds
    sd.wait()

    print("Done Recording")
  
    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    #write("C:\\Users\\rames\\Desktop\\Emotion-Classification-Ravdess\\examples\\recording" + str(counter) + ".wav", freq, recording)
    wv.write(EXAMPLES_PATH + AUDIO_FILE, recording, freq, sampwidth=2)
