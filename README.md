# MashupMaker

Automatic AI song mushap maker.

## Installation

### Install PyTorch
[GET STARTED](https://pytorch.org/get-started/locally/)

### Install the other packages
```
pip install -r requirements.txt
```

## Usage
The following command creates a mashup file from the two songs:

```
python mashup_maker.py -b path/to/base/song -v path/to/vocal/song
```

### Description

supported by 'vocal-remover-5' python module (general usage of PyTorch audio) and 'librosa' python music mudole.
This program is getting from the user 2 songs, and mashups them into one song that has the instruments from the one, and the vocals from the other.

The program seperates the vocals and the instruments from each song, detects the BPM and Scale, and mushaps them into onw full song.


#### Issues

- [1] no support for mp3 files (only wav)
- [2] no support for stereo (only mono)
