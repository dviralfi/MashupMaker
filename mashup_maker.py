__author__ = "Dvir Alafi"


import os
from math import log, sqrt, ceil
from statistics import mean
import argparse
from itertools import count
import numpy as np

import librosa
import soundfile as sf
import keyfinder
import inference    # Vocal Remover 5 Code


"""
Mashup Maker - is an Automatic AI song mushap maker, supported by 'vocal-remover-5' python module and 'librosa' python music mudole.
This program is getting from the user 2 songs, and mashups them into one song that has the instruments from the one, and the vocals from the other.
The program seperates the vocals and the instruments from each song, detects the BPM and Scale, and mushaps them into onw full song.

Gets: 2 songs
Returns: 1 mashup song

NOTES:
- sr = sample rate
- wf = wave form

"""


PARSING_DESCRIPTION_TEXT = "Enter your songs for mashuping:\n" \
                            "-b - Path to base song.\n" \
                            "-v - Path to vocal song.\n"
CHROMATIC_KEYS = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

DEFAULT_SAMPLE_RATE = 44100

PARTS_OF_SECONDS_TO_DIVIDE_DBS = 1000

SILENCE_SECONDS_TO_IGNORE = PARTS_OF_SECONDS_TO_DIVIDE_DBS * 1 
CONTINUITY_SECONDS = PARTS_OF_SECONDS_TO_DIVIDE_DBS * 2

DEFAULT_VOCAL_START_SECOND = 10


def get_unique_file_name(basename,file_path=str(os.getcwd()), ext='wav'):

    """
    Returns a unique file path, with a new file name:

    :param basename: the name of the file
    :param file_path: The path of the file
    :param ext: the extension of the file, for example '.txt', '.py', '.mid' .

    :return: a unique file path with a unique name that doesnt exists in the path of the given folder.

    """

    file_name = file_path + '\\' + "{basename}.{ext}".format(basename=basename, ext=ext)
    available_numbers_counter = count(2)

    while os.path.exists(file_name):
        file_name = file_path + '\\' + "{basename}_{number}.{ext}".format(basename=basename,
                                                                         number=next(available_numbers_counter),
                                                                         ext=ext)
    return file_name


class Song():
    """
    Song class for simplification.
    because there is a use of 2 songs and methods duplicates .

    """
    pass
    # attributes - self.wf, self.sr
    # methods - self.get_dbs, self.get_length, self.plot_wf ..

def clean_excess_end_of_song(wf, sr=DEFAULT_SAMPLE_RATE):
    pass


def get_song_length_in_seconds(wave_form, sr=DEFAULT_SAMPLE_RATE):
    seconds = len(wave_form)//sr
    return str(seconds//60)+":"+str(seconds%60)


def add_silence_seconds_at_start(seconds, wave_form, sr=DEFAULT_SAMPLE_RATE):
    zeros_array = [0.00001] * int(seconds * sr)
    # int() because the seconds might be 5.25 - 5sec and quarter of a second, and cant make half of item in array..
    # 0.00001 because when it converted to db it becomes -100dB which is very low in volume.
    # Example: (int(20*log( sqrt(mean(chunk**2)),10 ))) - mean(chunk) will be 0.00001 at the first seconds that we added.
    return np.concatenate((zeros_array, wave_form), axis=None)


def get_dbs(wave_form,sr=DEFAULT_SAMPLE_RATE):

    """
    Returns list of dBs values of every in the given wave_form 

    seconds are divided by PARTS_OF_SECONDS_TO_DIVIDE_DBS const, that you can alter. (e.g. half a second)
    """

    # Basically taking a reading every half a second (sr/2) - the size of the data 
    # divided by the sample rate gives us 1 second chunks so if for example I chop 
    # sample rate in half for half a second chunks 
    # `chunks = np.array_split(wave_form, wave_form.size/(sr/2))`
    
    # (due to a large dataset, its vital to make a generator)
    # Creating a generator, because there is no need for loading the whole dBs waveform list.

    chunks = np.array_split(wave_form, wave_form.size/(sr / PARTS_OF_SECONDS_TO_DIVIDE_DBS)) # check the db in every part of second
    for chunk in chunks:
        if sqrt(mean(chunk ** 2)) > 0:
            yield int(20*log(sqrt(mean(chunk**2)), 10)) 
            # Algorithm that converts Amplitude to a decible value
            # if the sqrt(mean(chunk**2)) value is negative it means that the song is silent.

    # list-return type of func:
    #dbs = [int(20*log(sqrt(mean(chunk**2)), 10)) for chunk in chunks if sqrt(mean(chunk ** 2)) > 0]
    #return dbs
    

def get_song_bpm(wave_form, sr=DEFAULT_SAMPLE_RATE):

    """
    Returns the bpm for a given waveform

    """ 

    # 'beat_track' func returns a tuple, and the second item is beat frames which the program don't need. 
    # Also, the value that been returned is a float and the program need it as an Integer number.

    return int(librosa.beat.beat_track(y=wave_form, sr=sr)[0])
    

def get_vocal_start_second(wf, sr=DEFAULT_SAMPLE_RATE):
    """
    Returns the second the vocal starts
    """

    # Issues:
    # Vocal FX - not the actual singing start

    # Checking if the dBs are below -30dB for 3 sec continuously
    
    continuity_counter = 0
    silence_counter = 0

    for index, db in enumerate(get_dbs(wf, sr)): # iterate through a generator that the get_dbs func yeilds.

        if db > -30 : # reasonable amount of dBs that the vocal would be
            #print(index/PARTS_OF_SECONDS_TO_DIVIDE_DBS,":", db, end='\n')
            continuity_counter += 1
            #print("continuty counter: ",continuity_counter)
        else:
            
            if continuity_counter > CONTINUITY_SECONDS / (PARTS_OF_SECONDS_TO_DIVIDE_DBS/10)  and silence_counter+1 < SILENCE_SECONDS_TO_IGNORE: 
                # 10th of the continuity time has passed, its likely that the vocal will continue to rise above -30 dB.
                # Maybe there is a slight chance that the singer stopped sing for just a moment, I dont want to reset the counter
                # and for that we have the silence_counter that check if the silence is too much
                
                    continuity_counter += 1
                    silence_counter += 1

            else:            

                silence_counter = 0
                continuity_counter = 0
                
        if continuity_counter == CONTINUITY_SECONDS: #if analized 1/2 of a second than it needs to be 6 indexes continuity

            return (index - CONTINUITY_SECONDS) / PARTS_OF_SECONDS_TO_DIVIDE_DBS
            
            # if the index is 6 then the vocal start in 4 than 5 than 6, and now continuity_counter==3. 
            # /PARTS_OF_SECONDS_TO_DIVIDE_DBS - to get the actual second value not the parts of seconds (not 7 - but 7/3 - means in 2.33 seconds..)
    
    return DEFAULT_VOCAL_START_SECOND # Default second vocal start


def adjust_start_of_vocal(vocal_wf, base_vocal_wf, sr=DEFAULT_SAMPLE_RATE):

    """
    Adjust the vocal wave form in case the vocal starts not when the original base song vocal starts.
    Returns the adjusted vocal wf
    """

    # Check in which seconds the vocal of `vocal_wf` begins
    # Check in which seconds the vocal of `base_vocal_wf` begins
    #
    # if vocal_wf starts before base_vocal :
    #      add_silence_seconds_at_start()
    # else:
    #      seconds_to_cut = seconds_vocal_wf_begins
    #      (e.g. starts after 3s) - seconds_base_vocal_begins(e.g. starts after 1s) = 2s
    #
    #      vocal_wf = vocal_wf[seconds_to_cut:]
    #      return vocal_wf     

    start_second_vocal = get_vocal_start_second(vocal_wf, sr)
    start_second_vocal_base = get_vocal_start_second(base_vocal_wf, sr)
    
    print('Vocal Start at:',start_second_vocal) 
    print('Base Vocal Start at:',start_second_vocal_base)


    if start_second_vocal == start_second_vocal_base: # no need to adjust
        return vocal_wf

    if start_second_vocal < start_second_vocal_base:
        seconds_to_add_silence = start_second_vocal_base-start_second_vocal
        new_vocal_wf = add_silence_seconds_at_start(seconds_to_add_silence,vocal_wf,sr)
        return new_vocal_wf

    else:
        seconds_to_start_with = start_second_vocal - start_second_vocal_base 
        # if the vocal starts in 4s and the base vocal starts in 2s you need to cut the excess of the vocal wf:
        #               1  2  3  4  5
        # VOCAL         .  .  .  -  -  start_second_vocal=4
        # BASE VOCAL    .  -  -  -  -  start_second_vocal_base=2
        

        return vocal_wf[int(seconds_to_start_with * sr):] 
        # int() because the seconds might be 5.25 - 5sec and quarter of a second, and cant make half of item in array..
        # *sr because each second is divided by sample rate, to start from 
        # some second you need to multiply the second by the sample rate. 
        # e.g. 3sec = 66,150, 5sec = 110,250      

def mashup_base_and_vocal(base_wf, vocal_wf, mix_file_name, sr=DEFAULT_SAMPLE_RATE):


    # because librosa is using ndarrays by NumPy, the adding of 2 ndarrays is allowed only
    # when the length and the dimensions of them is equal.
    # here it finds if one of the arrays is bigger then the other and append to one of them if so.
    # this is because the program needs the arrays to be joind by overlay and not one
    # after the other(because its 2 elements of music that needs to be played at the same time).


    if len(base_wf) < len(vocal_wf):
        new_arr = np.append(base_wf, range(len(vocal_wf) - len(base_wf)))
        base_wf = new_arr
    else:
        new_arr = np.append(vocal_wf, range(len(base_wf) - len(vocal_wf)))
        vocal_wf = new_arr

    mix_wav_form = base_wf + vocal_wf
   
    sf.write(mix_file_name, mix_wav_form, sr) 
    
    print("Mixed the songs, mashup file name:",mix_file_name)


def plot_wf(wf, sr=DEFAULT_SAMPLE_RATE):
    """
    Plot Audio WaveForm
    """

    dbs = [db for db in get_dbs(wf,sr)]
    x_axis = np.arange(0, len(dbs))
    np_array_dbs = np.array(dbs)

    import matplotlib.pyplot as plt
    plt.title("dBs of waveform")
    plt.xlabel("Seconds")
    plt.ylabel("dB")
    plt.plot(x_axis, np_array_dbs, color ="black")
    plt.show()


def main(base_song_path, vocal_song_path, **args):

    """
    Main Function

    Steps:

    1. Loading the songs into a computible sound files
    2. Recognize each song's BPM & Scale 
    3. Seperating the Vocals and Instruments from each song

    4. Loading the seperated files 
    5. Adjusting the base Scale&BPM to the vocal Scale&BPM
    6. Mixing the seperated elements together
    
    """

    ### Loading the songs into a computible sound files:   
    
    base_wf, base_sr = librosa.load(base_song_path)
    vocal_wf, vocal_sr = librosa.load(vocal_song_path)

    vocal_song_name = os.path.splitext(os.path.basename(vocal_song_path))[0]
    base_song_name = os.path.splitext(os.path.basename(base_song_path))[0]
    

    ### Recognize each song's BPM & Scale 
         
    # Recognize BPM:
    
    base_bpm = get_song_bpm(base_wf,base_sr)
    vocal_bpm = get_song_bpm(vocal_wf,vocal_sr)
    
    # if vocal bpm is too fast, the vocals wont be heard properly, and will sound horrible and not human.
    if base_bpm > 165:                  
        base_bpm = int(base_bpm / 2)
    elif base_bpm < 65:
        base_bpm = int(base_bpm * 2)

    # if instruments bpm too fast the song will sound bad and not recognizable by the listener.
    if vocal_bpm > 165:                
        vocal_bpm = int(vocal_bpm / 2)
    elif vocal_bpm < 65:
        vocal_bpm = int(vocal_bpm * 2)

    # Recognize Scale:

    base_obj = keyfinder.Tonal_Fragment(base_wf,base_sr)
    base_f0 = base_obj.get_key()[0].split(' ')[0]
    base_scale = base_obj.get_key()[0].split(' ')[1]


    vocal_obj = keyfinder.Tonal_Fragment(vocal_wf,vocal_sr)
    vocal_f0 = vocal_obj.get_key()[0].split(' ')[0]
    vocal_scale = vocal_obj.get_key()[0].split(' ')[1]

    if vocal_scale != base_scale: 
        print(f'Might not sound well... because:\nVocal Scale Type: {vocal_scale}\nBase Scale Type: {base_scale}')
        

    print("Base BPM:",base_bpm)
    print("Vocal BPM:",vocal_bpm,'\n')

    print("Base Key:",base_f0)
    print("Vocal Key:",vocal_f0,'\n')


    ### Seperating the Vocals and Instruments from each song:

    inference.main(base_song_path, is_base=True, is_vocal=True, **args) 
    inference.main(vocal_song_path, is_base=False,is_vocal=True, **args)


    sep_vocal_file_name = '{}_Vocals.wav'.format(vocal_song_name)

    sep_base_file_name =  '{}_Instruments.wav'.format(base_song_name)
    sep_base_vocal_file_name = '{}_Vocals.wav'.format(base_song_name)
    
    
    ### Loading the seperated files :
    
    sep_base_wf, sep_base_sr = librosa.load(os.getcwd()+'\\'+sep_base_file_name,sr=DEFAULT_SAMPLE_RATE)
    sep_vocal_wf, sr = librosa.load(os.getcwd()+'\\'+sep_vocal_file_name,sr=DEFAULT_SAMPLE_RATE)
    sep_base_vocal_wf, sr = librosa.load(os.getcwd()+'\\'+sep_base_vocal_file_name,sr=DEFAULT_SAMPLE_RATE)

    ### Adjusting the base Scale & BPM to the vocal Scale & BPM: 


    tone_steps = CHROMATIC_KEYS.index(vocal_f0)-CHROMATIC_KEYS.index(base_f0)

    shifted_base_wf = librosa.effects.pitch_shift(y=sep_base_wf, sr=sep_base_sr, n_steps=tone_steps)
    
    # Adjusting the vocal BPM to the base BPM: 

    # and not the opposite, because I want the vocal to sound natural and not robotic..
    
    if base_bpm < vocal_bpm:
        stretch_rate = base_bpm / vocal_bpm
    else:       
        stretch_rate = vocal_bpm / base_bpm

    if stretch_rate < 0.65: stretch_rate*=2
    print("BPM stretch rate: ", stretch_rate)

    stretched_vocal_wf = librosa.effects.time_stretch(y=sep_vocal_wf, rate=stretch_rate)

    # Finding unique name for the mashup file:

    file_path = os.path.dirname(os.path.realpath(vocal_song_path))
    mashup_file_name ='{}_x_{}_by_MashupMaker'.format(
        os.path.basename(vocal_song_path).split('.')[0],os.path.basename(base_song_path).split('.')[0])
    
    mashup_file_name = get_unique_file_name(mashup_file_name, file_path=file_path, ext='wav')

    
    # Adjusting vocal wave-form

    print("Adjusting vocal wave-form to fit base wave-form")
    vocal_adjusted_vocal_wf = adjust_start_of_vocal(stretched_vocal_wf,sep_base_vocal_wf)

    # Mixing the seperated elements together:
    mashup_base_and_vocal(shifted_base_wf, vocal_adjusted_vocal_wf, mashup_file_name)

    print("Done! ")                            

def get_args():
    p = argparse.ArgumentParser(description=PARSING_DESCRIPTION_TEXT)
    p.add_argument("--base_song_path",'-b', help="File path to base song",dest='b')
    p.add_argument('--vocal_song_path','-v', help="File path to vocal song",dest='v')

    p.add_argument('--gpu', '-g', type=int, default=-1)
    p.add_argument('--pretrained_model', '-P', type=str, default='models/baseline.pth')
    p.add_argument('--sr', '-r', type=int, default=44100)
    p.add_argument('--n_fft', '-f', type=int, default=2048)
    p.add_argument('--hop_length', '-H', type=int, default=1024)
    p.add_argument('--batchsize', '-B', type=int, default=4)
    p.add_argument('--cropsize', '-c', type=int, default=256)
    p.add_argument('--output_image', '-I', action='store_true')
    p.add_argument('--postprocess', '-p', action='store_true')
    p.add_argument('--tta', '-t', action='store_true')

    args = p.parse_args()

    return args

if __name__ == '__main__':
    args = get_args()

    main(base_song_path=args.b, vocal_song_path=args.v, args=args)
