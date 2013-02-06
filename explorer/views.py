from urllib import unquote
import os

#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout
from django.conf import settings

from explorer.models import AlbumSong
from services.handler import encode

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_WWWROOT = settings.MEDIA_WWWROOT


def album_songs_to_json():
    return encode(list(AlbumSong.objects.all()))


#@login_required
def index(request, relpath=None):
    if relpath is None:
        return render_to_response('folders/index.html', {
            "foldername": "Media Box",
            "folders": folders(relpath),
            "albumSongs": album_songs_to_json,
            }, RequestContext(request))
    else:
        relpath = unquote(relpath)
        return render_to_response('folders/index.html', {
            "foldername": os.path.basename(relpath),
            "folders": folders(relpath),
            "files": files(relpath),
            "locations": locations(relpath),
            "albumSongs": album_songs_to_json,
            }, RequestContext(request))


def locations(relpath=None):
    if relpath is None:
        return

    import django.core.urlresolvers
    wwwroot = django.core.urlresolvers.reverse("explorer")

    locations = []
    head = relpath
    while True:
        (head, tail) = os.path.split(head)
        href = os.path.join(wwwroot, head, tail)

        item = {
                "name": tail,
                "href": href,
                }

        locations.append(item)

        if head == "":
            break

    locations[0]["last"] = True
    locations.append({
        "name": "Top",
        "href": wwwroot,
        })
    locations.reverse()

    return locations


def folders(relpath=None):
    import django.core.urlresolvers
    wwwroot = django.core.urlresolvers.reverse("explorer")

    if relpath is None:
        mediapath = MEDIA_ROOT
    else:
        mediapath = os.path.join(MEDIA_ROOT, relpath)

    folders = []
    if os.path.isdir(mediapath):
        for f in os.listdir(mediapath):
            if os.path.isdir(os.path.join(mediapath, f)):
                if relpath is None:
                    href = os.path.join(wwwroot, f)
                else:
                    href = os.path.join(wwwroot, relpath, f)

                folder = {
                        "name": f,
                        "href": href,
                        }

                folders.append(folder)

    return sorted(folders, key=lambda x: x['name'])


def files(relpath=None):
    #import django.core.urlresolvers
    wwwroot = MEDIA_WWWROOT

    if relpath is None:
        mediapath = MEDIA_ROOT
    else:
        mediapath = os.path.join(MEDIA_ROOT, relpath)

    if not os.path.isdir(mediapath):
        return

    files = []
    for f in os.listdir(mediapath):
        if os.path.isfile(os.path.join(mediapath, f)):
            if relpath is None:
                href = os.path.join(wwwroot, f)
            else:
                href = os.path.join(wwwroot, relpath, f)

            file = {
                    "name": f,
                    "href": href,
                    "size": os.path.getsize(os.path.join(mediapath, f)),
                    }

            files.append(file)

    return sorted(files, key=lambda x: x['name'])


# eof
