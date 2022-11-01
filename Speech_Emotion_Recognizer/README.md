# Speech Emotion Recognizer using CNNs

**Description**

This project presents a deep learning classifier able to predict the emotions of a human speaker encoded in an audio file. The classifier is trained using 2 different datasets, RAVDESS and TESS, and has an overall F1 score of 80% on 8 classes (neutral, calm, happy, sad, angry, fearful, disgust and surprised).

**Steps to Run**

- First, ensure keras, librosa, numpy, pyaudio, playsound, sounddevice, wavio, speechrecognition, pyttsx3 packages are installed on your system.
- The data files are available in the RAVDESS+TESS_Dataset folder. To interpret the file names, look at the section below.
- The features have been extracted and saved in the joblib_features folder. Features can be extracted through create_features.py file (Optional)
- The trained model has been saved in the model folder. Training can be done through the neural_network.py file, in this case all requirements from requirements.txt must be installed (Optional)
- You can record audio for any duration using the recordaudio.py file, the frequency is kept at 48kHz
- No speech in the audio signal is detected using the speech_text_translation.py file
- MP4 files can be converted to .wav file through Mp4ToWav.py 
- Model summary, confusion matrix and other metrics are saved in the media folder
- Either choose an audio file from the dataset folder, or any audio file of your choice, or record audio yourself and place it in the examples folder.
- Change AUDIO_FILE in the live_predictions.py folder to the name of your audio file and simply execute live_predictions.py
- The output displayed is the predicted emotion / probability of each emotion
- Alternatively, you can use the streaming.py file to simultaneously record audio and give live predictions by changing the number_of_times variable inside the file

**RAVDESS File Naming Convention**

The dataset (present in RAVDESS+TESS_Dataset folder) contains the complete set of 7356 RAVDESS files (total size: 24.8 GB). Each of the 24 actors consists of three modality formats: Audio-only (16bit, 48kHz .wav), Audio-Video (720p H.264, AAC 48kHz, .mp4), and Video-only (no sound).  Note, there are no song files for Actor_18.

Each of the 7356 RAVDESS files has a unique filename. The filename consists of a 7-part numerical identifier (e.g., 02-01-06-01-02-01-12.mp4). These identifiers define the stimulus characteristics:

Filename identifiers 

- Modality (01 = full-AV, 02 = video-only, 03 = audio-only).
- Vocal channel (01 = speech, 02 = song).
- Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
- Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the ‘neutral’ emotion.
- Statement (01 = “Kids are talking by the door”, 02 = “Dogs are sitting by the door”).
- Repetition (01 = 1st repetition, 02 = 2nd repetition).
- Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).

*Filename example: 02-01-06-01-02-01-12.mp4*

- Video-only (02)
- Speech (01)
- Fearful (06)
- Normal intensity (01)
- Statement “dogs” (02)
- 1st Repetition (01)
- 12th Actor (12)
- Female, as the actor ID number is even.
```
