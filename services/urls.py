from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^user/(.*)$', 'services.views.user_service', name='user_service'),
    url(r'^genre/(.*)$', 'services.views.genre_service', name='genre_service'),
    url(r'^artist/(.*)$', 'services.views.artist_service', name='artist_service'),
    url(r'^album/(.*)$', 'services.views.album_service', name='album_service'),
    url(r'^albumsong/(.*)$', 'services.views.albumsong_service', name='albumsong_service'),
    url(r'^single/(.*)$', 'services.views.single_service', name='single_service'),
)

# eof
