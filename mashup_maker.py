__author__ = "Dvir Alfi"

import argparse
import inference    # Vocal Remover 5 Open Source Code



PARSING_DESCRIPTION_TEXT = "Enter your songs for mashuping:" \
                            "-b - Path to base song.\n" \
                            "-v - Path to vocal song.\n"

#def main(base_song_path,vocal_song_path):
def main(base_song_path,vocal_song_path):

    inference.main(base_song_path,is_base=True)
    inference.main(vocal_song_path,is_base=False)



if __name__ == '__main__':

    
    base_song_path = 'C:/Users/refae/Desktop/son.wav'
    vocal_song_path = 'C:/Users/refae/Desktop/song2.wav'

    main(base_song_path,vocal_song_path)

    exit()

    parser = argparse.ArgumentParser(description=PARSING_DESCRIPTION_TEXT)
    parser.add_argument('-b', "--base_song_path", help="Path to base song")
    parser.add_argument('v','--vocal_song_path', help="Path to vocal song")

    args = parser.parse_args()

    base_song_path = args.base_song_path
    vocal_song_path = args.vocal_song_path
    


