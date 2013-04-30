from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth import logout as django_logout
from django.http import HttpResponse

from accounts.auth import NonListedException


def login(request):
    return render_to_response(
            'login.html', context_instance=RequestContext(request))


def logout(request):
    django_logout(request)
    return redirect('home')


def render_failure(request, message, status=403,
        template_name='login.html',
        exception=None):
    if type(exception) is NonListedException:
        message = 'nonlisted'
    data = render_to_string(
            template_name, dict(message=message, exception=exception),
            context_instance=RequestContext(request))
    return HttpResponse(data, status=status)


# eof
