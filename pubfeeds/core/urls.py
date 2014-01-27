from django.conf.urls import patterns, url

urlpatterns = patterns('pubfeeds.core.views',
    url(r'(?P<feed_slug>[\w\d-]+)/latest$', 'latest'),
    url(r'(?P<feed_slug>[\w\d-]+)/(?P<edition_id>\d+)/manifest\.xml', 'edition'),
)