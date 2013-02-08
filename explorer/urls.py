from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('explorer.views',
    url(r'^$', 'explore_private', name="explorer"),
    (r'^(?P<relpath>.*)', 'explore_private'),
)
