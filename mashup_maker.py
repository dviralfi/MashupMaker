__author__ = "Dvir Alafi"


"""
Mashup Maker - is an Automatic AI song mushap maker, supported by 'vocal-remover-5' python module and 'librosa' python music mudole.
This program is getting from the user 2 songs, and mashups them into one song that has the instruments from the one, and the vocals from the other.
The program seperates the vocals and the instruments from each song, detects the BPM and Scale, and mushaps them into onw full song.

Gets: 2 songs
Returns: 1 mashup song

"""


import argparse
from email.mime import base

from functools import reduce
from unittest.mock import DEFAULT
import inference    # Vocal Remover 5 Open Source Code
import librosa
import os
from itertools import count
import numpy as np
import soundfile as sf
from pyACA import computePitch
import keyfinder


PARSING_DESCRIPTION_TEXT = "Enter your songs for mashuping:" \
                            "-b - Path to base song.\n" \
                            "-v - Path to vocal song.\n"
CHROMATIC_KEYS = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
PITCH_TRACKERS_LIST = ['SpectralAcf', 'SpectralHps', 'TimeAcf', 'TimeAmdf', 'TimeAuditory', 'TimeZeroCrossings',]
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_SUBTYPE = 'PCM_24' # wav 24bit depth extracting


"""
def detect_pitch(y, sr, t):
  index = magnitudes[:, t].argmax()
  pitch = pitches[index, t]

  return pitch
"""


def mix_base_and_vocal(base_wf, vocal_wf, mix_file_name, sr=DEFAULT_SAMPLE_RATE):


    # because librosa is using ndarrays by NumPy, the adding of 2 ndarrays is allowed only when the length and the dimensions of them is equal.
    # here it finds if one of the arrays is bigger then the other and append to one of them if so.
    # this is because the program needs the arrays to be joind by overlay and not one after the other(because its 2 elements of music that needs to be played at the same time).
    
    if len(base_wf) < len(vocal_wf):
        new_arr = np.append(base_wf, range(len(vocal_wf) - len(base_wf)))
        base_wf = new_arr
    else:
        new_arr = np.append(vocal_wf, range(len(base_wf) - len(vocal_wf)))
        vocal_wf = new_arr

    mix_wav_form = base_wf + vocal_wf
   

    sf.write(mix_file_name, mix_wav_form, sr) # soundFile Module is writing the new file.
    
    print("Mixed the songs, mashup file name:",mix_file_name)


def get_unique_file_name(basename,file_path=str(os.getcwd()), ext='wav'):
    """
    Returns a unique file path, with a new file name:

    
    :param basename: the name of the file
    :param file_path: The path of the file
    :param ext: the extension of the file, for example '.txt', '.py', '.mid' .

    :return: a unique file path with a unique name that doesnt exists in the path of the given folder.
            for example, if it has: 'a x b Mushap' , then, it will return: 'a x b Mushap_2'
            and that in the next process: 'a x b Mushap_3', etc.

    """

    file_name = file_path + '\\' + "{basename}.{ext}".format(basename=basename, ext=ext)
    available_numbers_counter = count(2)

    while os.path.exists(file_name):
        file_name = file_path + '\\' + "{basename}_{number}.{ext}".format(basename=basename,
                                                                         number=next(available_numbers_counter),
                                                                         ext=ext)
    return file_name


def get_song_bpm(wave_form, sample_rate):

    """

    The function returns the first item, because 'beat_track' func returns a tuple, and the second item is beat frams which the program don't need. 
    Also, the value that been returned is a float and the program need it as an Integer number.

    """

    return int(librosa.beat.beat_track(y=wave_form, sr=sample_rate)[0])
    

def main(base_song_path,vocal_song_path):

    """

    Steps:

    1. Loading the songs into a computible sound files
    2. Recognize each song's BPM & Scale 
    3. Seperating the Vocals and Instruments from each song

    4. Loading the seperated files 
    5. Adjusting the base Scale&BPM to the vocal Scale&BPM
    6. Mixing the seperated elements together
    
    """

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Loading the songs into a computible sound files:      
    base_wave_form, base_sample_rate = librosa.load(base_song_path,sr=DEFAULT_SAMPLE_RATE)
    vocal_wave_form, vocal_sample_rate = librosa.load(vocal_song_path,sr=DEFAULT_SAMPLE_RATE)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Recognize each song's BPM & Scale 
                     
        # Recognize BPM:
    base_bpm = get_song_bpm(base_wave_form,base_sample_rate)
    vocal_bpm = get_song_bpm(vocal_wave_form,vocal_sample_rate)
    
    if base_bpm > 160:                  # if the bpm is too fast, the vocals wont be heard properly, and will sound horrible and not human.
        base_bpm = int(base_bpm / 2)
    if vocal_bpm > 160:                 # on the other hand if the instruments will be too fast the song will sound bad and not recognizable by the listener.
        vocal_bpm = int(vocal_bpm / 2)

    print("Base BPM:",base_bpm)
    print("Vocal BPM:",vocal_bpm,'\n')

        # Recognize Scale:

    """
    pitch_tracker = PITCH_TRACKERS_LIST[2]      # TimeZeroCrossings

    base_f0, base_time_stamp = computePitch(pitch_tracker,base_wave_form,base_sample_rate)
    vocal_f0, vocal_time_stamp = computePitch(pitch_tracker,vocal_wave_form,vocal_sample_rate)

    print('base freq:\n',base_f0)
    
    print('vocal freq:\n',vocal_f0)
    """

    base_obj = keyfinder.Tonal_Fragment(base_wave_form,base_sample_rate)
    base_f0 = base_obj.get_key()[0].split(' ')[0]

    vocal_obj = keyfinder.Tonal_Fragment(vocal_wave_form,vocal_sample_rate)
    vocal_f0 = vocal_obj.get_key()[0].split(' ')[0]


    print("Base Scale:", base_f0)
    print("Vocal Scale:", vocal_f0)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Seperating the Vocals and Instruments from each song:

    seperated_base_file_name = inference.main(base_song_path,is_base=True)
    seperated_vocal_file_name = inference.main(vocal_song_path,is_base=False)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Loading the seperated files :

    # just for testing:
    #seperated_base_file_name = "pardes_Instruments.wav"
    #seperated_vocal_file_name = "leva_Vocals.wav"

    sep_base_wave_form, sep_base_sample_rate = librosa.load(os.getcwd()+'\\'+seperated_base_file_name,sr=DEFAULT_SAMPLE_RATE)

    sep_vocal_wave_form, sep_vocal_sample_rate = librosa.load(os.getcwd()+'\\'+seperated_vocal_file_name,sr=DEFAULT_SAMPLE_RATE)
    

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Adjusting the base Scale & BPM to the vocal Scale & BPM: 
    n_steps = CHROMATIC_KEYS.index(vocal_f0)-CHROMATIC_KEYS.index(base_f0)
    print("steps between vocal and base keys:",base_f0,'-',vocal_f0,':',n_steps)

    new_base_wave_form = librosa.effects.pitch_shift(y=sep_base_wave_form, sr=base_sample_rate, n_steps=n_steps)
    
    # Adjusting the vocal BPM to the base BPM: 
    
    if base_bpm>vocal_bpm:
        stretch_rate = base_bpm/vocal_bpm
    else:
        stretch_rate = vocal_bpm/base_bpm

    new_vocal_wave_form = librosa.effects.time_stretch(y=sep_vocal_wave_form, rate=stretch_rate)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Finding unique name for the mashup file:
    file_extension = os.path.basename(vocal_song_path).split('.')[1] 
    file_path = os.path.dirname(os.path.realpath(vocal_song_path))
    mix_file_name ='{} x {} by MashupMaker'.format(os.path.basename(vocal_song_path).split('.')[0],os.path.basename(base_song_path).split('.')[0])
    
    mix_file_name = get_unique_file_name(mix_file_name, file_path=file_path, ext=file_extension)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Mixing the seperated elements together:
    mix_base_and_vocal(new_base_wave_form, new_vocal_wave_form, mix_file_name)
                                
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    
    base_song_path = 'C:/Users/refae/Desktop/pardes.wav'
    vocal_song_path = 'C:/Users/refae/Desktop/leva.wav'

    main(base_song_path,vocal_song_path)

    exit()

    parser = argparse.ArgumentParser(description=PARSING_DESCRIPTION_TEXT)
    parser.add_argument('-b', "--base_song_path", help="Path to base song")
    parser.add_argument('v','--vocal_song_path', help="Path to vocal song")

    args = parser.parse_args()

    base_song_path = args.base_song_path
    vocal_song_path = args.vocal_song_path
    


