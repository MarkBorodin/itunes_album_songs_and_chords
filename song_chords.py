import requests
from bs4 import BeautifulSoup
from googlesearch import search


class ChordsFinder(object):

    """Gets:
    artist (type: str, required: true),
    song_title (type: str, required: true),
    result_file (type: str, required: false, default result file name: result_file_chords.txt)

    Searches for chords for the specified song

    Output: txt file with chords"""

    urls = list()
    chords = ''

    def __init__(self, artist: str, song_title: str, result_file: str = 'result_file_chords.txt'): # noqa
        self.artist = artist
        self.song_title = song_title
        self.result_file = result_file
        self.query = artist + song_title + 'chords'

    def get_site_url(self):
        """the method generates a query to google and receives a URL with a search result"""

        for url in search(self.query, tld="co.in", num=5, stop=5):
            if 'ultimate' in url:
                continue
            else:
                self.urls.append(url)

    def get_chords(self):
        """the method searches for a tag "pre" on the page (most often it contains chords) and gets chords from it"""

        for url in self.urls:
            try:
                response = requests.get(url).text
                soup = BeautifulSoup(response, "lxml")
                self.chords = soup.find('pre').text
            except AttributeError:
                continue
            if self.chords:
                break

    def write_data_to_txt_file(self):
        """the method writes the sorted data to a file"""

        with open(self.result_file, 'w') as f:
            f.write(self.chords)

    def run(self):
        """starting the program"""

        print('chords search started')
        self.get_site_url()
        self.get_chords()
        print(f'chords are taken')
        self.write_data_to_txt_file()
        print(f'results are written to a file: {self.result_file}')
