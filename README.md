Setup
-----
1. Install required python modules

        pip install -r pip.txt

2. Create settings.py from sample

        cp musiclibrary/settings.py.sample musiclibrary/settings.py

3. Create database (sqlite3), and admin account

        ./manage.py syncdb

4. Create a symbolic link to your mp3 collection inside static/

        ln -s /path/to/mp3/collection static/mp3

5. Import music meta data

        ./manage.py import_id3_genres
        ./manage.py sync_music

6. Start local website on localhost:8000

        ./manage.py runserver

7. Visit http://localhost:8000/folders/

