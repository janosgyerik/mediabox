from django.conf.urls.defaults import patterns

urlpatterns = patterns('accounts.views',
        (r'^login$', 'login'),
        (r'^logout$', 'logout'),
)


# eof
