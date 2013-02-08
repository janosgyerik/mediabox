from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('explorer.views',
    url(r'^$', 'index', name="explorer"),
    url(r'^private/(?P<relpath>.*)', 'explore_private',
        name='explore_private'),
    url(r'^public/(?P<relpath>.*)', 'explore_public',
        name='explore_public'),
)
