from urllib.parse import unquote
import os

#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout
from django.conf import settings

from common.models import AlbumSong
from services.handler import encode

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_WWWROOT = settings.MEDIA_WWWROOT
MEDIA_EXT = settings.MEDIA_EXT


def album_songs_to_json():
    return encode(list(AlbumSong.objects.all()))


def index(request):
    return explore_public(request)


def about(request):
    return render_to_response('explorer/about.html', {
        "foldername": "Home",
        }, RequestContext(request))


def explore_common(request, relpath, template='explorer/folders.html'):
    relpath = unquote(relpath)
    return render_to_response(template, {
        "foldername": os.path.basename(relpath),
        "folders": folders(relpath),
        "files": files(relpath),
        "images": images(relpath),
        "locations": locations(relpath),
        "albumSongs": album_songs_to_json,
        }, RequestContext(request))


def explore_public(request, relpath=''):
    if relpath is None or relpath == '':
        relpath = 'public'
    else:
        relpath = 'public/' + relpath
    return explore_common(request, relpath, template='explorer/public.html')


@login_required
def explore_private(request, relpath=None):
    if relpath is None or relpath == '':
        relpath = 'private'
    else:
        relpath = 'private/' + relpath
    return explore_common(request, relpath)


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
        "name": "Home",
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
    wwwroot = MEDIA_WWWROOT

    if relpath is None:
        mediapath = MEDIA_ROOT
    else:
        mediapath = os.path.join(MEDIA_ROOT, relpath)

    if not os.path.isdir(mediapath):
        return

    files = []
    for filename in os.listdir(mediapath):
        if os.path.isfile(os.path.join(mediapath, filename)):
            if filename.startswith('.'):
                continue

            ext = os.path.splitext(filename)[1][1:].lower()
            if not ext in MEDIA_EXT:
                continue

            if relpath is None:
                href = os.path.join(wwwroot, filename)
            else:
                href = os.path.join(wwwroot, relpath, filename)

            fileinfo = {
                    "name": filename,
                    "href": href,
                    "size": os.path.getsize(os.path.join(mediapath, filename)),
                    }

            files.append(fileinfo)

    return sorted(files, key=lambda x: x['name'])


def images(relpath=None):
    wwwroot = MEDIA_WWWROOT

    if relpath is None:
        mediapath = MEDIA_ROOT
    else:
        mediapath = os.path.join(MEDIA_ROOT, relpath)

    if not os.path.isdir(mediapath):
        return

    files = []
    for filename in os.listdir(mediapath):
        if os.path.isfile(os.path.join(mediapath, filename)):
            if filename.startswith('.'):
                continue

            ext = os.path.splitext(filename)[1][1:].lower()
            if not ext in ('jpg', 'jpeg', 'png'):
                continue

            if relpath is None:
                href = os.path.join(wwwroot, filename)
            else:
                href = os.path.join(wwwroot, relpath, filename)

            fileinfo = {
                    "name": filename,
                    "href": href,
                    }

            files.append(fileinfo)

    return sorted(files, key=lambda x: x['name'])


# eof
