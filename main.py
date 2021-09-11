from album_songs import AlbumAndSongFinder
from song_chords import ChordsFinder

if __name__ == '__main__':

    """Enter the artist name and song title. Use "exit" to exit"""

    # get artist name and song title from input
    artist = ''
    song_title = ''

    while len(artist) < 2:
        artist = input('Enter artist name:')
        if len(artist) < 2:
            print('artist name too short')
        if artist == 'exit':
            break

    while len(song_title) < 2:
        song_title = input('Enter song title')
        if len(song_title) < 2:
            print('song title too short')
        if song_title == 'exit':
            break

    if (artist != 'exit' and song_title != 'exit') and (len(artist) > 1 and len(song_title) > 1):

        try:
            # get .csv file with information about songs from the album
            album_and_song_finder = AlbumAndSongFinder(artist, song_title)
            album_and_song_finder.run()
        except Exception as e: # noqa
            print(f'Could not get information about songs from the album due to an error: {e}')

        try:
            # get .txt file with song chords
            chords_finder = ChordsFinder(artist, song_title)
            chords_finder.run()
        except Exception as e: # noqa
            print(f'Failed to get chords due to an error: {e}')

    else:
        print('Goodbye!')

