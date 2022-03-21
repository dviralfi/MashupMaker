__author__ = "Dvir Alfi"


"""
Mashup Maker - is an Automatic AI song mushap maker, supported by 'vocal-remover-5' python module and 'librosa' python music mudole.
This program is getting from the user 2 songs, and mashups them into one song that has the instruments from the one, and the vocals from the other.
The program seperates the vocals and the instruments from each song, detects the BPM and Scale, and mushaps them into onw full song.

Gets: 2 songs
Returns: 1 mashup song

"""

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
    return int(librosa.beat.beat_track(y=wave_form, sr=sample_rate)[0])
    # The function returns the first item, because 'beat_track' func returns a tuple, and the second item is beat frams which the program don't need. 
    # Also, the value that been returned is a float and the program need it as an Integer number.


def main(base_song_path,vocal_song_path):

    # Loading the songs into a computible sound files:

    base_wave_form, base_sample_rate = librosa.load(base_song_path)
    vocal_wave_form, vocal_sample_rate = librosa.load(vocal_song_path)


    # Recognize each song's BPM & Scale 

        # recognize BPM:
    base_bpm = get_song_bpm(base_wave_form,base_sample_rate)
    vocal_bpm = get_song_bpm(vocal_wave_form,vocal_sample_rate)
    
    if base_bpm > 150:                  # if the bpm is too fast, the vocals wont be heard properly, and will sound horrible and not human.
        base_bpm = int(base_bpm / 2)
    if vocal_bpm > 150:                 # on the other hand if the instruments will be too fast the song will sound bad and not recognizable by the listener.
        vocal_bpm = int(vocal_bpm / 2)

    print("Base BPM:",base_bpm,"Vocal BPM:",vocal_bpm)

        # Recognize Scale:
    pass
    pass
    pass

    base_scale = "C"
    vocal_scale = "G#"



    # Seperating the Vocals and Instruments from each song:

    #inference.main(base_song_path,is_base=True)
    #inference.main(vocal_song_path,is_base=False)

    # Reading the seperated files :

    base_wave_form, base_sample_rate = librosa.load(str(os.path.dirname(os.path.realpath(base_song_path)))+str(os.path.basename(base_song_path).split('.')[0])+'_Instruments')
    vocal_wave_form, vocal_sample_rate = librosa.load(str(os.path.dirname(os.path.realpath(vocal_song_path)))+str(os.path.basename(vocal_song_path).split('.')[0])+'_Vocals')

    # Adjusting the base Scale to the vocal Scale: 
    base_wave_form = librosa.effects.pitch_shift(y=base_wave_form, sr=base_sample_rate, n_steps=abs(CHROMATIC_KEYS.index(base_scale)-CHROMATIC_KEYS.index(vocal_scale)))

    # Adjusting the vocal BPM to the base BPM: 
    
    if base_bpm>vocal_bpm:
        stretch_rate = base_bpm/vocal_bpm
    else:
        stretch_rate = vocal_bpm/base_bpm

    vocal_wave_form = librosa.effects.time_stretch(y=vocal_wave_form, rate=stretch_rate)

    # Mixing the elements together:

        #Finding unique name for the mushap file:
    file_extension = os.path.basename(vocal_song_path).split('.')[1] 
    file_path = os.path.dirname(os.path.realpath(vocal_song_path))
    mix_file_name ='{} x {} Mashup by MashupMaker'.format(os.path.basename(vocal_song_path).split('.')[0],os.path.basename(base_song_path).split('.')[0])
    
    mix_file_name = get_unique_file_name(mix_file_name, file_path=file_path, ext=file_extension)

    inference.mix_base_and_vocal(base_wave_form, base_sample_rate, vocal_wave_form, mix_file_name)
                                

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
    


