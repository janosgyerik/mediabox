from django.conf.urls.defaults import *

urlpatterns = patterns('folders.views',
    url(r'^$', 'index', name="folders"),
    (r'^(?P<relpath>.*)', 'index'),
)
