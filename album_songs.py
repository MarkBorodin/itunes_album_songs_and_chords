import csv

import requests


class AlbumAndSongFinder(object):

    """Gets:
    artist (type: str, required: true),
    song_title (type: str, required: true),
    result_file (type: str, required: false, default result file name: result_file_songs.csv)

    Finds the album of the artist to which the given song belongs.

    Output: csv file with all songs from this album"""

    required_data = [
        'artistId', 'collectionId', 'trackId', 'artistName', 'collectionName', 'trackName',
        'collectionCensoredName', 'trackCensoredName', 'artistViewUrl', 'collectionViewUrl',
        'trackViewUrl', 'previewUrl', 'collectionPrice', 'trackPrice', 'releaseDate', 'discCount',
        'discNumber', 'trackCount', 'trackNumber', 'trackTimeMillis', 'country', 'currency', 'primaryGenreName']

    all_songs = list()
    collection_name = ''


    def __init__(self, artist: str, song_title: str, result_file: str = 'result_file_songs.csv'): # noqa
        self.artist = artist
        self.song_title = song_title
        self.result_file = result_file

    def create_result_file(self):
        """the method creates a file to output the results"""

        with open(self.result_file, "w", newline="", encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerows([self.required_data])

    def get_data_from_itunes(self):
        """The method sends a request with the name of the artist and the name of the song to itunes.
        Gets the response and takes from it the id of the album to which the song belongs.
        Sends a new request and gets all songs from this album"""

        try:
            resp = requests.get(f'https://itunes.apple.com/search?term={self.artist}+{self.song_title}&limit=1').json()
            collection_id = resp['results'][0]['collectionId']
            self.collection_name = resp['results'][0]['collectionName']
            album = requests.get(f'https://itunes.apple.com/lookup?id={collection_id}&entity=song').json()
            self.all_songs = album['results'][1:]
        except Exception as e: # noqa
            print(e)

    def sort_the_required_data_and_write_to_csv(self):
        """The method iterates over the list of songs, takes the necessary data from all data and writes it to a file"""

        for song in self.all_songs:
            one_song_data_to_write = list()
            for column in self.required_data:
                try:
                    one_song_data_to_write.append(song[column])
                except Exception as e: # noqa
                    print(e)
            self.write_data_to_csv_file(one_song_data_to_write)

    def write_data_to_csv_file(self, one_song_data_to_write):
        """the method writes the sorted data to a file"""

        with open(self.result_file, "a", newline="", encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerows([one_song_data_to_write])

    def run(self):
        """starting the program"""

        print('started searching for songs from the album')
        self.create_result_file()
        print(f'file for outputting information has been created: {self.result_file}')
        self.get_data_from_itunes()
        print(f'data obtained from itunes: {len(self.all_songs)} songs in album "{self.collection_name}"')
        self.sort_the_required_data_and_write_to_csv()
        print(f'data written to file {self.result_file}')
