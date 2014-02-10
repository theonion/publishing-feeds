from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import utc

import feedparser
import calendar

from time import mktime
from datetime import datetime


class Feed(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class PublishingSchedule(models.Model):

    DAYS = [tup for tup in enumerate(calendar.day_name)]

    feed = models.ForeignKey(Feed)
    weekday = models.IntegerField(choices=DAYS)
    time = models.TimeField()


class Section(models.Model):

    class Meta:
        order_with_respect_to = 'feed'

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    url = models.URLField()

    feed = models.ForeignKey(Feed, related_name="sections")

    def __unicode__(self):
        return self.name


class Edition(models.Model):

    published_date = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    feed = models.ForeignKey(Feed, related_name="editions")

    class Meta:
        ordering = ["-published_date"]

    def poll(self):
        for section in self.feed.sections.all():
            data = feedparser.parse(section.url)
            for entry in data.entries:
                if entry.link:
                    try:
                        article = Article.objects.get(identifier=entry.link, edition=self)
                    except Article.DoesNotExist:
                        article = Article(identifier=entry.link, section=section, edition=self)
                    
                    if article.section != section:
                        continue # If this article has been already created in another section, skip that shit.

                    if hasattr(entry, 'author'):
                        article.byline = entry.author

                    if entry.summary:
                        article.summary

                    article.content = entry.content
                    article.publish_date = datetime.fromtimestamp(mktime(entry.published_parsed)).replace(tzinfo=utc)
                    article.save()

    def get_absolute_url(self):
        return reverse("pubfeeds.core.views.edition", args=(self.feed.slug, self.id))

    def __unicode__(self):
        return "%s: %s" % (self.feed.name, self. publish_date)


class Article(models.Model):
    section = models.ForeignKey(Section, related_name="articles")
    edition = models.ForeignKey(Edition, related_name="articles")

    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    identifier = models.CharField(unique=True, max_length=255)
    byline = models.CharField(null=True, blank=True, max_length=255)
    summary = models.TextField(null=True, blank=True)
    kicker = models.CharField(null=True, blank=True, max_length=255)
    content = models.TextField()

    class Meta:
        ordering = ["-publish_date"]
        unique_together = ("edition", "identifier")

    def get_absolute_url(self):
        return reverse("pubfeeds.core.views.article", args=(self.edition.feed.slug, self.edition.id, self.section.slug, self.id))
