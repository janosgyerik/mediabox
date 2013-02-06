from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('explorer.views',
    url(r'^$', 'index', name="explorer"),
    (r'^(?P<relpath>.*)', 'index'),
)
