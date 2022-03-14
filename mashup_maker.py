import argparse
import inference



PARSING_DESCRIPTION_TEXT = "Enter your songs for mashuping:" \
                            "-b - Path to base song.\n" \
                            "-v - Path to vocal song.\n"

#def main(base_song_path,vocal_song_path):
def main():
    vocal_song_path = 'C:/Users/refae/Desktop/song2.wav'
    inference.main(vocal_song_path)


if __name__ == '__main__':
    main()

    exit()

    parser = argparse.ArgumentParser(description=PARSING_DESCRIPTION_TEXT)
    parser.add_argument('-b', "--base_song_path", help="Path to base song")
    parser.add_argument('v','--vocal_song_path', help="Path to vocal song")

    args = parser.parse_args()

    base_song_path = args.base_song_path
    vocal_song_path = args.vocal_song_path
    
    main(base_song_path,vocal_song_path)

