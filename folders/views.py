import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

MUSIC_ROOT = settings.MUSIC_ROOT

#@login_required
def index(request, relpath=None):
    if relpath is None:
	return render_to_response('folders/index.html', {
        "foldername": "Music Library",
        "folders": folders(relpath),
        }, RequestContext(request))
    else:
        return render_to_response('folders/index.html', {
            "foldername": os.path.basename(relpath),
            "folders": folders(relpath),
            "files": files(relpath),
            "locations": locations(relpath),
            }, RequestContext(request))

def locations(relpath=None):
    if relpath is None:
        return

    import django.core.urlresolvers
    href_base = django.core.urlresolvers.reverse("folders")

    locations = []
    head = relpath
    while True:
        (head, tail) = os.path.split(head)
        href = os.path.join(href_base, head, tail)

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
        "href": href_base,
        })
    locations.reverse()

    return locations

def folders(relpath=None):
    import django.core.urlresolvers
    href_base = django.core.urlresolvers.reverse("folders")

    if relpath is None:
        mediapath = MUSIC_ROOT
    else:
        mediapath = os.path.join(MUSIC_ROOT, relpath)

    if not os.path.isdir(mediapath):
        return

    folders = []
    for f in os.listdir(mediapath):
        if os.path.isdir(os.path.join(mediapath, f)):
            if relpath is None:
                href = os.path.join(href_base, f)
            else:
                href = os.path.join(href_base, relpath, f)

            folder = {
                    "name": f,
                    "href": href,
                    }

            folders.append(folder)

    return folders

def files(relpath=None):
    import django.core.urlresolvers
    href_base = "/media/mp3"

    if relpath is None:
        mediapath = MUSIC_ROOT
    else:
        mediapath = os.path.join(MUSIC_ROOT, relpath)

    if not os.path.isdir(mediapath):
        return

    files = []
    for f in os.listdir(mediapath):
        if os.path.isfile(os.path.join(mediapath, f)):
            if relpath is None:
                href = os.path.join(href_base, f)
            else:
                href = os.path.join(href_base, relpath, f)

            file = {
                    "name": f,
                    "href": href,
                    "size": os.path.getsize(os.path.join(mediapath, f)),
                    }

            files.append(file)

    return files


# eof
