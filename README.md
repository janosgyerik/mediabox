MediaBox
========
A simple web interface to access to your media from anywhere.  Open ID
login with whitelisting. Open-source project, using Django, Python,
Backbone.js, HTML5, Bootstrap from Twitter.


Setup
-----
1. Install required python modules

        pip install -r pip.txt

2. Create database (sqlite3), and admin account

        ./manage.py syncdb

3. Create a symbolic link to your media collection inside static/

        ln -s /path/to/media/collection static/media

4. Import ID3 genre data to use as canonical genre meta data

        ./manage.py import_id3_genres

5. Synchronize meta data of media files from the filesystem into the database

        ./manage.py sync_media

6. Start local website on localhost:8000

        ./manage.py runserver

7. Visit http://localhost:8000/


Local settings
--------------
The default settings.py is suitable for development. To override some
settings, especially DATABASES and SECRET_KEY, create a custom
local_settings.py file, based on the included local_settings.py.sample
and call manage.py like this:

    ./manage cmd --settings=local_settings


Live demos
----------
- http://dev.mediabox.titan2x.com/


Screenshots
-----------
![Folders](https://github.com/websitedevops/mediabox/raw/master/static/screenshots/folders.png)
![Albums](https://github.com/websitedevops/mediabox/raw/master/static/screenshots/album.png)


Features
--------
- Traverse directory of music files
- mp3 files are playable in the browser using the Yahoo! WebPlayer

Well that's pretty much it for now. And it's working fine like that. But that's not great.

Work in progress: (stuff that's working but not really used yet) 
- Import meta data from mp3 files and store in a local database cache for fast access
- Supported audio formats:

    - mp3
    - (more are coming soon, can be added easily using `mutagen`)


Technologies used or planned (for aspiring contributors)
--------------------------------------------------------
- django/python: database not used yet, but will be used to replace folder traversal
- a versioned and defined and stable ReST server as well to allow add-on's and alternate front-ends in the future, while not in code now it is thought about as features are added
- \_, Backbone, jQ.tpl all powerhousing the new responsive Bootstrap Framework based set of theme(s)
- multiple views per artist, album, playlist, etc all graceful as one would expect
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

