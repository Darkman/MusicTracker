import json
import argparse
from pathlib import Path
from stagger import read_tag
from collections import namedtuple, Mapping

Song = namedtuple('Song', 'artist album title path')
foobar_file = r"E:\Users\Darkman\My Music\Foobar_Currently_Playing.txt"


def read_foobar_file():
    """
    This function reads the foobar output file located
    at `foobar_file` and returns a namedtuple with the
    artist, album, title, and path.

    For this function to work, the foobar output formatting
    string must be as follows:

    %artist%
    $crlf()
    %album%
    $crlf()
    %title%
    $crlf()
    %path%

    This outputs the following items on separate lines: ARTIST, ALBUM, TITLE, PATH
    $crlf() is the linebreak
    """

    with open(foobar_file, mode='r', encoding='utf-8') as infile:
        data = infile.read()

    lines = data.splitlines()

    if len(lines) != 4:
        raise ValueError('Incorrect number of items in list.')

    path = Path(lines.pop())
    return Song(*lines, path=path.as_posix())


def enumerate_album(song):
    path = Path(song.path)
    songs = []
    for path in sorted(path.parent.glob('*.mp3')):
        tag = read_tag(path.as_posix())
        if tag.album == song.album:
            song = Song(song.artist, song.album, tag.title, path.as_posix())
            songs.append(song)
        else:
            print("tag.album does not match song.album")
    return songs


class MusicJSON:
    def __init__(self, filepath):
        self.filepath = filepath
        self.music = self._read_json()

    def save(self):
        with open(self.filepath, mode='w', encoding='utf-8') as outfile:
            json.dump(self.music, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    def update(self, song):
        song_dict = {'Artist': {song.artist: {song.album: {song.title: song.path}}}}
        self.music = self._dict_update(self.music, song_dict)

    def _dict_update(self, dict1, dict2):
        for key, value in dict2.items():
            if isinstance(value, Mapping):
                r = self._dict_update(dict1.get(key, {}), value)
                dict1[key] = r
            else:
                dict1[key] = dict2[key]
        return dict1

    def _read_json(self):
        """
        Read existing favorited or deleted music,
        otherwise return an empty dict.
        """
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as infile:
                try:
                    return json.load(infile)
                except ValueError:
                    return dict()
        except FileNotFoundError:
            return dict()


class Controls:
    def __init__(self):
        self.favorited_music = MusicJSON('favorited_music.json')
        self.deleted_music = MusicJSON('deleted_music.json')
        self.song = read_foobar_file()

    def favorite_song(self):
        self.favorited_music.update(self.song)
        self.favorited_music.save()

    def favorite_album(self):
        for song in enumerate_album(self.song):
            self.favorited_music.update(song)
        self.favorited_music.save()

    def delete_song(self):
        self.deleted_music.update(self.song)
        self.deleted_music.save()

    def delete_album(self):
        for song in enumerate_album(self.song):
            self.deleted_music.update(song)
        self.deleted_music.save()


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--fav-song', help='Favorite the currently playing song.', action='store_true')
    group.add_argument('-fa', '--fav-album', help='Favorite the entire album.', action='store_true')
    group.add_argument('-d', '--delete-song', help='Delete the currently playing song.', action='store_true')
    group.add_argument('-da', '--delete-album', help='Delete the entire album.', action='store_true')

    args = parser.parse_args()

    controls = Controls()

    if args.fav_song:
        controls.favorite_song()
    elif args.fav_album:
        controls.favorite_album()
    elif args.delete_song:
        controls.delete_song()
    elif args.delete_album:
        controls.delete_album()

if __name__ == '__main__':
    main()
