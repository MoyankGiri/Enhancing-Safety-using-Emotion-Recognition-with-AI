"""
Configuration file: using this one to keep all the paths in one place for various imports.

TRAINING_FILES_PATH = Path of the training files. Here there are

- the RAVDESS dataset files (Folders Actor_01 to Actor_24
- the TESS dataset renamed files (Folders Actor_25 and Actor_26)

SAVE_DIR_PATH = Path of the joblib features created with create_features.py

MODEL_DIR_PATH = Path for the keras model created with neural_network.py

TESS_ORIGINAL_FOLDER_PATH = Path for the TESS dataset original folder (used by tess_pipeline.py)

"""
import sys
import pathlib
import os

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
working_dir_path = str(parent_dir) + '\\Speech_Emotion_Recognizer'

if sys.platform.startswith('win32'):
    TRAINING_FILES_PATH = str(working_dir_path) + '\\RAVDESS+TESS_Dataset\\'
    SAVE_DIR_PATH = str(working_dir_path) + '\\joblib_features\\'
    MODEL_DIR_PATH = str(working_dir_path) + '\\model\\'
    TESS_ORIGINAL_FOLDER_PATH = str(working_dir_path) + '\\TESS_Speech_Data\\'
    EXAMPLES_PATH = str(working_dir_path) + '\\examples\\'
    ALERTS_PATH = str(working_dir_path) + '\\alerts\\'
else:
    TRAINING_FILES_PATH = str(working_dir_path) + '/RAVDESS+TESS_Dataset/'
    SAVE_DIR_PATH = str(working_dir_path) + '/joblib_features/'
    MODEL_DIR_PATH = str(working_dir_path) + '/model/'
    TESS_ORIGINAL_FOLDER_PATH = str(working_dir_path) + '/TESS_Speech_Data/'
    EXAMPLES_PATH = str(working_dir_path) + '/examples/'
    ALERTS_PATH = str(working_dir_path) + '/alerts/'
