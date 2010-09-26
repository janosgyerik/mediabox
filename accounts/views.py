from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse as reverse_url
from django.http import HttpResponseRedirect

def create_user(request, template_name="registration/create_user_form.html"):
    if request.method == 'POST':
	form = UserCreationForm(request.POST)
	if form.is_valid():
	    user = User.objects.create_user(form.cleaned_data["username"], "", form.cleaned_data["password1"])
	    return HttpResponseRedirect(reverse_url("home"))
    else:
	form = UserCreationForm()

    return render_to_response(template_name, {
	"form": form,
	}, context_instance=RequestContext(request))

# eof
