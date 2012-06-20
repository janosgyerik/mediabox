from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from django.contrib.auth.decorators import login_required

from folders.views import folders, latest_x

#@login_required
def home(request):
    return render_to_response('home.html', 
            { 
                "folders": folders(), 
                "latest": latest_x(10),
                }, RequestContext(request))

# eof
