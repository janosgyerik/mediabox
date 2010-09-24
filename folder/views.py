from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def index(request):
    return render_to_response('folder/index.html')

# eof
