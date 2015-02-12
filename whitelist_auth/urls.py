from django.conf.urls import patterns, url

urlpatterns = patterns(
    'whitelist_auth.views',
    url(r'^$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^status$', 'status', name='status'),
)
