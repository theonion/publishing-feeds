from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


import feedparser
import calendar

from time import mktime
import datetime


class Feed(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    url = models.URLField(max_length=1024)

    def __unicode__(self):
        return self.name

    def get_time_period(self, target_date=None):
        if target_date is None:
            target_date = timezone.now()

        start = None
        end = None
        for schedule in self.schedule.all():

            delta = (target_date.weekday() - schedule.weekday) % 7
            deltas = (
                datetime.timedelta(days=delta),
                datetime.timedelta(days=delta - 7),
            )

            for delta in deltas:
                schedule_date = target_date - delta
                schedule_date = schedule_date.replace(hour=schedule.time.hour, minute=schedule.time.minute, second=0, microsecond=0)

                if schedule_date < target_date:
                    if start is None or start < schedule_date:
                        start = schedule_date

                if schedule_date > target_date:
                    if end is None or end > schedule_date:
                        end = schedule_date
        return (start, end)

    def poll(self):
        start, end = self.get_time_period()
        edition, created = Edition.objects.get_or_create(feed=self, published_date=end)
        edition.poll(start, end)


class PublishingSchedule(models.Model):

    DAYS = [day_pair for day_pair in enumerate(calendar.day_name)]

    feed = models.ForeignKey(Feed, related_name="schedule")
    weekday = models.IntegerField(choices=DAYS)
    time = models.TimeField()

    class Meta:
        ordering = ["weekday", "time"]


class Section(models.Model):

    class Meta:
        order_with_respect_to = 'feed'

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    url = models.URLField(max_length=1024)

    feed = models.ForeignKey(Feed, related_name="sections")

    def __unicode__(self):
        return self.name


class Edition(models.Model):

    published_date = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    feed = models.ForeignKey(Feed, related_name="editions")

    class Meta:
        ordering = ["-published_date"]

    def poll(self, start, end):
        for section in self.feed.sections.all():
            data = feedparser.parse(section.url)
            for entry in data.entries:
                if entry.link:
                    publish_date = datetime.datetime.fromtimestamp(mktime(entry.published_parsed)).replace(tzinfo=timezone.utc)
                    if publish_date < start or publish_date > end:
                        continue

                    try:
                        article = Article.objects.get(identifier=entry.link, edition=self)
                    except Article.DoesNotExist:
                        article = Article(identifier=entry.link, section=section, edition=self)
                    
                    if article.section != section:
                        continue  # If this article has been already created in another section, skip that shit.

                    article.title = entry.title

                    if getattr(entry, 'author', None):
                        article.byline = entry.author

                    if entry.summary:
                        article.summary

                    article.content = entry.content[0].get("value")
                    article.publish_date = publish_date

                    article.save()

    def get_absolute_url(self):
        return reverse("pubfeeds.core.views.edition", args=(self.feed.slug, self.id))

    def __unicode__(self):
        return "%s: %s" % (self.feed.name, self.published_date)


class Article(models.Model):

    edition = models.ForeignKey(Edition, related_name="articles")
    section = models.ForeignKey(Section, related_name="articles")

    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    identifier = models.CharField(max_length=255)
    byline = models.CharField(null=True, blank=True, max_length=255)
    summary = models.TextField(null=True, blank=True)
    kicker = models.CharField(null=True, blank=True, max_length=255)
    content = models.TextField()

    class Meta:
        ordering = ["-publish_date"]

    def get_absolute_url(self):
        return reverse("pubfeeds.core.views.article", args=(self.edition.feed.slug, self.edition.id, self.section.slug, self.id))
