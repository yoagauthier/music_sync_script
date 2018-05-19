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
from multiprocessing.pool import Pool
import os


# command to call
# ffmpeg -i "/test/file.flac" -y -acodec libvorbis -aq 7 -vn -ac 2 "/test/result.mp3"
def convert(tuple):
    input_filepath, output_filepath = tuple
    call([
        "ffmpeg",
        "-i",
        input_filepath,
        "-y",
        "-loglevel",
        "panic",
        "-acodec",
        "libvorbis",
        "-aq",
        "7",
        "-vn",
        "-ac",
        "2",
        output_filepath
    ])
    print(output_filepath)



if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    print(args)
    SRC_ROOT_FOLDER_PATH = args['<source_folder_path>']
    DEST_ROOT_FOLDER_PATH = args['<destination_folder_path>']
    ARTISTS_FILE_PATH = args['<artist_list_file>']

    with open(ARTISTS_FILE_PATH, 'r') as artists_file:
        temp = artists_file.read().splitlines()
        artists = [i for i in temp if not i.startswith('#')]
    print(artists)

    to_convert = []
    for dirpath, dirnames, filenames in os.walk(SRC_ROOT_FOLDER_PATH):
        for artist in artists:
            # print(dirpath, artist)
            if artist in dirpath:
                # print("XXXXX", artist, dirpath, dirnames, filenames)
                if not os.path.exists(os.path.join(DEST_ROOT_FOLDER_PATH, artist)):
                    os.mkdir(os.path.join(DEST_ROOT_FOLDER_PATH, artist))
                    # print("NEW FOLDER")
                else:
                    # print("EXISTING FOLDER")
                    print(os.path.join(DEST_ROOT_FOLDER_PATH, artist))

                for filename in filenames:
                    if filename.lower().endswith(('flac', 'ogg', 'mp3', 'wma')):
                        new_filename = os.path.splitext(filename)[0] + ".ogg"
                        to_convert.append(
                            (
                                os.path.join(dirpath, filename),
                                os.path.join(DEST_ROOT_FOLDER_PATH, artist, new_filename)
                            )
                        )

    with Pool() as sp:
        sp.map(convert, to_convert)
