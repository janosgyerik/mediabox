from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'explorer.views.index', name='home'),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^api/', include('services.urls')),

    url(r'accounts/', include('accounts.urls')),
    url(r'openid/', include('django_openid_auth.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
