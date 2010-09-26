from django.conf.urls.defaults import *
import django.contrib.auth.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'musiclibrary.views.home', name="home"),
    (r'^accounts/profile/$', 'musiclibrary.views.home'),
    (r'^accounts/password_change_done/$', 'musiclibrary.views.home'),
    (r'^accounts/$', 'musiclibrary.views.home'),
    (r'^accounts/', include('musiclibrary.accounts.urls')),
    (r'^folders/', include('musiclibrary.folders.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
	    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )

