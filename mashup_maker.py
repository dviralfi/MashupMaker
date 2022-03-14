import argparse
import 




PARSING_DESCRIPTION_TEXT = "Enter your songs for mashuping:" \
                            "-b - Path to base song.\n" \
                            "-v - Path to vocal song.\n"

def main(base_song,vocal_song):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=PARSING_DESCRIPTION_TEXT)
    parser.add_argument('-b', "--base_song", help="Path to base song")
    parser.add_argument('v','--vocal_song', help="Path to vocal song")

    args = parser.parse_args()

    base_song = args.base_song
    vocal_song = args.vocal_song
   

    main(base_song,vocal_song)
