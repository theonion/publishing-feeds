from django.conf.urls import patterns, url

urlpatterns = patterns('pubfeeds.core.views',
    url(r'(?P<feed_slug>[a-z0-9-]+)/overview$', "feed_overview"),  # noqa
    url(r'(?P<feed_slug>[\w\d-]+)/latest\.xml$', "latest"),
    url(r'(?P<feed_slug>[\w\d-]+)/(?P<edition_id>\d+)/manifest\.xml', "edition"),
    url(r'(?P<feed_slug>[a-z0-9-]+)/(?P<edition_id>\d+)/overview$', "edition_overview"),
    url(r'(?P<feed_slug>[\w\d-]+)/(?P<edition_id>\d+)/(?P<section_slug>[\w\d-]+)\.xml', "section"),
    url(r'(?P<feed_slug>[\w\d-]+)/(?P<edition_id>\d+)/(?P<section_slug>[\w\d-]+)/(?P<article_id>\d+)\.xml', "article"),
)
