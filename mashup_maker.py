__author__ = "Dvir Alfi"

import argparse
import inference    # Vocal Remover 5 Open Source Code
import librosa
import os
from itertools import count

PARSING_DESCRIPTION_TEXT = "Enter your songs for mashuping:" \
                            "-b - Path to base song.\n" \
                            "-v - Path to vocal song.\n"
CHROMATIC_KEYS = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

"""
def detect_pitch(y, sr, t):
  index = magnitudes[:, t].argmax()
  pitch = pitches[index, t]

  return pitch
"""


def get_unique_file_name(basename,file_path=str(os.getcwd()), ext='wav'):
    """
    Returns a unique file path, with a new file name:

    
    :param basename: the name of the file
    :param file_path: The path of the file
    :param ext: the extension of the file, for example '.txt', '.py', '.mid' .

    :return: a unique file path with a unique name that doesnt exists in the path of the given folder.
             for example, if it has: Midis/RandoMMelody, then, it will return: Midis/RandoMMelody_2,
              and that in the next process: Midis/RandoMMelody_3, etc.

    """

    file_name = file_path + '\\' + "{basename}.{ext}".format(basename=basename, ext=ext)
    available_numbers_counter = count(2)

    while os.path.exists(file_name):
        file_name = file_path + '\\' + "{basename}_{number}.{ext}".format(basename=basename,
                                                                         number=next(available_numbers_counter),
                                                                         ext=ext)
    return file_name

def get_song_bpm(wave_form, sample_rate):
    return int(librosa.beat.beat_track(y=wave_form, sr=sample_rate)[0])
    # The function returns the first item, because 'beat_track' func returns a tuple, and the second item is beat frams which the program don't need. 
    # Also, the value that been returned is a float and the program need it as an Integer number.


def main(base_song_path,vocal_song_path):

    # Loading the songs into a computible sound files:

    base_wave_form, base_sample_rate = librosa.load(base_song_path)
    vocal_wave_form, vocal_sample_rate = librosa.load(vocal_song_path)


    # Recognize each song's BPM & Scale 

    base_bpm = get_song_bpm(base_wave_form,base_sample_rate)
    vocal_bpm = get_song_bpm(vocal_wave_form,vocal_sample_rate)
    
    if base_bpm > 150:
        base_bpm = int(base_bpm / 2)
    if vocal_bpm > 150:
        vocal_bpm = int(vocal_bpm / 2)
        

    print("Base BPM:",base_bpm,"Vocal BPM:",vocal_bpm)

    # Recognize the Scale of each song:
    pass
    pass
    pass

    base_scale = "C"
    vocal_scale = "G#"

    # Adjusting the base Scale to the vocal Scale: 
    base_wave_form = librosa.effects.pitch_shift(y=base_wave_form, sr=base_sample_rate, n_steps=abs(CHROMATIC_KEYS.index(base_scale)-CHROMATIC_KEYS.index(vocal_scale)))

    # Adjusting the vocal BPM to the base BPM: 
    
    if base_bpm>vocal_bpm:
        stretch_rate = base_bpm/vocal_bpm
    else:
        stretch_rate = vocal_bpm/base_bpm

    vocal_wave_form = librosa.effects.time_stretch(y=vocal_wave_form, rate=stretch_rate)

    # Mixing the elements together:

    mix_file_name ='{} x {} Mashup by MashupMaker'.format(os.path.basename(vocal_song_path).split('.')[0],os.path.basename(base_song_path).split('.')[0])
    
    mix_file_name = get_unique_file_name(mix_file_name)
    
    inference.mix_base_and_vocal(base_wave_form, base_sample_rate, vocal_wave_form, mix_file_name)
                                
   
    exit()



    # Seperating the Vocals and Instruments from each song:
    inference.main(base_song_path,is_base=True)
    inference.main(vocal_song_path,is_base=False)



if __name__ == '__main__':

    
    base_song_path = 'C:/Users/refae/Desktop/melody.wav'
    vocal_song_path = 'C:/Users/refae/Desktop/chords.wav'

    main(base_song_path,vocal_song_path)

    exit()

    parser = argparse.ArgumentParser(description=PARSING_DESCRIPTION_TEXT)
    parser.add_argument('-b', "--base_song_path", help="Path to base song")
    parser.add_argument('v','--vocal_song_path', help="Path to vocal song")

    args = parser.parse_args()

    base_song_path = args.base_song_path
    vocal_song_path = args.vocal_song_path
    


