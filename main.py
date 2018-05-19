"""
Script transferring audio files from one folder to another and converting them
in the process.
Uses FFmpeg for conversion.

To know the path of the destination folder in a smartphone, please check:
ls /run/user/1000/gvfs/mtp:host=%5Busb%3A003%2C004%5D/Mémoire\ de\ stockage\ interne/Music

Usage:
    main.py <source_folder_path> <destination_folder_path> <artist_list_file>

Options:
    -h --help    Show this help
"""

from docopt import docopt
from subprocess import call
import os

if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    print(args)
    SRC_ROOT_FOLDER_PATH = args['<source_folder_path>']
    DEST_ROOT_FOLDER_PATH = args['<destination_folder_path>']
    ARTISTS_FILE_PATH = args['<artist_list_file>']

    with open(ARTISTS_FILE_PATH, 'r') as artists_file:
        artists = artists_file.read().splitlines()
    print(artists)

    # command to call
    # ffmpeg -i "/test/file.flac" -y -acodec libvorbis -aq 7 -vn -ac 2 "/test/result.mp3"
    for dirpath, dirnames, filenames in os.walk(SRC_ROOT_FOLDER_PATH):
        for artist in artists:
            # print(dirpath, artist)
            if artist in dirpath:
                print("XXXXX", artist, dirpath, dirnames, filenames)
                if os.path.exists(os.path.join(DEST_ROOT_FOLDER_PATH, artist)):
                    print("EXISTING FOLDER")
                    print(os.path.join(DEST_ROOT_FOLDER_PATH, artist))
                    for filename in filenames:
                        new_filename = os.path.splitext(filename)[0] + ".ogg"
                        call([
                            "ffmpeg",
                            "-i",
                            os.path.join(dirpath, filename),
                            "-y",
                            "-acodec",
                            "libvorbis",
                            "-aq",
                            "7",
                            "-vn",
                            "-ac",
                            "2",
                            os.path.join(DEST_ROOT_FOLDER_PATH, artist, new_filename)
                        ])
                else:
                    print("NEW FOLDER")
                    os.mkdir(os.path.join(DEST_ROOT_FOLDER_PATH, artist))
                    for filename in filenames:
                        new_filename = os.path.splitext(filename)[0] + ".ogg"
                        call([
                            "ffmpeg",
                            "-i",
                            os.path.join(dirpath, filename),
                            "-y",
                            "-acodec",
                            "libvorbis",
                            "-aq",
                            "7",
                            "-vn",
                            "-ac",
                            "2",
                            os.path.join(DEST_ROOT_FOLDER_PATH, artist, new_filename)
                        ])
