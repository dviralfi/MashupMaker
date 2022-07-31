# MashupMaker

Automatic AI song mushap maker.

## Installation

### Install PyTorch (Build) 


[GET STARTED](https://pytorch.org/get-started/locally/)

Alternatively, you can install it locally using pip reqs.txt

### Install the other packages
```
pip install -r requirements.txt 
```

+ please read `requirements.txt` file for a complete installation. 

### For MP3 support:

`FFmpeg` module supports reading mp3 file.

`FFmpeg` is used via its command-line interface. this is the reason that pip installing `FFmpeg` doesn't work. It needs the `ffmpeg.exe` file.

download the ffmpeg installer from here - [FFMPEG Download Page](https://ffmpeg.org/)

After it is installed make sure you can start ffmpeg from the command line (type ffmpeg -h). You will probably need to add the path to the install folder (eg c:\ffmpeg\bin) to the Windows path.

+ Finally, make sure to restart your IDE. Visual Studio Code probably won't recognise the new path until after a reset.

## Usage
The following command creates a mashup file from the two songs:

```
python mashup_maker.py -b path/to/base/song -v path/to/vocal/song
```

### Description

Supported by [vocal-remover](https://github.com/tsurumeso/vocal-remover) by 'tsurumeso' python module (general usage of `PyTorch` audio) and `librosa` python music mudole.
This program is getting from the user 2 songs, and mashups them into one song that has the instruments from the one, and the vocals from the other.

The program seperates the vocals and the instruments from each song, detects the BPM and Scale, and mushaps them into onw full song.


#### Issues

- [1]  no support for stereo (only mono)

