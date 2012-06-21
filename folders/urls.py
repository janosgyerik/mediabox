from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('folders.views',
    url(r'^$', 'index', name="folders"),
    (r'^(?P<relpath>.*)', 'index'),
)
