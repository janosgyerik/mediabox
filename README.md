Music Library
=============
A simple web interface to listen to your music anywhere.


Setup
-----
1. Install required python modules

        pip install -r pip.txt

2. Create settings.py from sample

        cp musiclibrary/settings.py.sample musiclibrary/settings.py

3. Create database (sqlite3), and admin account

        ./manage.py syncdb

4. Create a symbolic link to your music collection inside static/

        ln -s /path/to/music/collection static/music

5. Import ID3 genre data to use as canonical genre meta data

        ./manage.py import_id3_genres

6. Synchronize meta data of music files from the filesystem into the database

        ./manage.py sync_music

7. Start local website on localhost:8000

        ./manage.py runserver

8. Visit http://localhost:8000/folders/


Live demos
----------
- http://dev.musiclibrary.titan2x.com/folders/


Screenshots
-----------
![Folders](https://github.com/websitedevops/musiclibrary/raw/master/static/screenshots/folders.png)
![Albums](https://github.com/websitedevops/musiclibrary/raw/master/static/screenshots/album.png)


Features
--------
- Traverse directory of music files
- Music files are playable in the browser using the Yahoo! WebPlayer

Well that's pretty much it for now. And it's working fine like that. But that's not great.

Work in progress: (stuff that's working but not really used yet) 
- Import meta data from music files and store in a local database cache for fast access
- Supported audio formats:

    - mp3
    - (more are coming soon, can be added easily using `mutagen`)


Technologies used or planned (for aspiring contributors)
--------------------------------------------------------
- django/python: database not used yet, but will be used to replace folder traversal
- backbone: not used yet, but will be used to have multiple views per artist, album, playlist, etc
- mutagen: used to get music file meta data, supports many audio formats
- webplayer by Yahoo!: the current media player, but it would be great to change this
  to a pure html5 implementation without Flash
- openid + whitelisting + invites: only invited ppl can login, via openid


Planned features (most important at the top)
--------------------------------------------
- openid + whitelisting + invites: only invited ppl can login, via openid
- Change the navigation: instead of page reloads folder by folder, load the entire
  collection on the client side into backbone objects and use js to navigate artists and albums.
- Search!
- Recently listened to
- Count how many times I listen to the same stuff
- Favoriting: albums, artists, songs
- Playlists!
- Add support for more audio formats: ogg, flac
  Note: the webplayer probably cannot play anything but mp3.
  A pure HTML5 player should have no problem with that.

