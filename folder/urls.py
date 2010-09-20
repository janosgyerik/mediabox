from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^login/(?P<username>[^/]+)/(?P<sensor_id>[^/]+)/(?P<formatstr>[^/]+)$', 'sensormap.api.views.login'),
    #(r'^login/.*$', 'sensormap.api.views.login_bad'),
    #(r'^store/(?P<session_id>\d+)/(?P<data>.+)$', 'sensormap.api.views.store'),
    #(r'^store/.*$', 'sensormap.api.views.store_bad'),
    (r'^.*', 'musiclibrary.folder.views.index'),
)
