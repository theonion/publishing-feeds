from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import utc

import feedparser

from time import mktime
from datetime import datetime


class Feed(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    url = models.URLField()


class Section(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    url = models.URLField()

    feed = models.ForeignKey(Feed, related_name="sections")


class Edition(models.Model):

    published_date = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    feed = models.ForeignKey(Feed, related_name="editions")

    def poll(self):
        for section in self.feed.sections.all():
            data = feedparser.parse(section.url)
            for entry in data.entries:
                if entry.link:
                    try:
                        item = Item.objects.get(article_id=entry.link, section=section, edition=self)
                    except Item.DoesNotExist:
                        item = Item(article_id=entry.link, section=section, edition=self)

                    if hasattr(entry, 'author'):
                        item.byline = entry.author

                    if entry.summary:
                        item.summary

                    item.content = entry.content
                    item.publish_date = datetime.fromtimestamp(mktime(entry.published_parsed)).replace(tzinfo=utc)
                    item.save()

    def get_absolute_url(self):
        return reverse("pubfeeds.core.views.edition", args=(self.feed.slug, self.id))


class Item(models.Model):
    section = models.ForeignKey(Section, related_name="items")
    edition = models.ForeignKey(Edition, related_name="items")

    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    article_id = models.CharField(unique=True, max_length=255)
    byline = models.CharField(null=True, blank=True, max_length=255)
    summary = models.TextField(null=True, blank=True)
    kicker = models.CharField(null=True, blank=True, max_length=255)
    content = models.TextField()
