import os
import datetime

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import Client, TestCase
from django.utils import timezone


from pubfeeds.core.models import Feed, Edition, Section, Article, PublishingSchedule

TEST_FEED_DIR = os.path.join(os.path.dirname(__file__), "test_feeds")

FEEDS = (
    ("avclub_newswire.xml", "Newswire"),
    ("avclub_film.xml", "Film"),
    ("avclub_tvclub.xml", "TV Club"),
)


class FeedTestCase(TestCase):

    def test_onion(self):
        feed = Feed.objects.create(
            name="The Onion",
            slug="onion",
            url="http://www.theonion.com"
        )
        # I'm gonna make a feed that publishes on thursday morning (at midnight)
        PublishingSchedule.objects.create(
            feed=feed,
            weekday=3,
            time=datetime.time(hour=0, minute=0)
        )

        # This is today, a Wednesday
        target_date = datetime.datetime(year=2014, month=4, day=16, hour=21, minute=17)
        start, end = feed.get_time_period(target_date=target_date)
       
        # This should be Thursday, the 10th
        self.assertEqual(start.day, 10)
        self.assertEqual(start.month, 4)
        self.assertEqual(start.year, 2014)
        self.assertEqual(start.hour, 0)
        self.assertEqual(start.minute, 0)

    def test_schedule(self):
        feed = Feed.objects.create(
            name="The A.V. Club",
            slug="av-club",
            url="http://www.avclub.com"
        )

        # I'm gonna make a feed that publishes:
        # 1.  on sunday morning (at midnight)
        PublishingSchedule.objects.create(
            feed=feed,
            weekday=6,
            time=datetime.time(hour=0, minute=0)
        )
        # 2. On Friday, at noon
        PublishingSchedule.objects.create(
            feed=feed,
            weekday=4,
            time=datetime.time(hour=12, minute=0)
        )

        # This is today, a Tuesday
        target_date = datetime.datetime(year=2014, month=2, day=11, hour=12, minute=30)
        start, end = feed.get_time_period(target_date=target_date)

        # This should be Sunday, the 9th
        self.assertEqual(start.day, 9)
        self.assertEqual(start.month, 2)
        self.assertEqual(start.year, 2014)
        self.assertEqual(start.hour, 0)
        self.assertEqual(start.minute, 0)

        # This should be Friday, the 14th
        self.assertEqual(end.day, 14)
        self.assertEqual(end.month, 2)
        self.assertEqual(end.year, 2014)
        self.assertEqual(end.hour, 12)
        self.assertEqual(end.minute, 0)

        # This is on Friday morning
        target_date = datetime.datetime(year=2014, month=2, day=14, hour=9, minute=0)
        start, end = feed.get_time_period(target_date=target_date)
        
        # This should be Sunday, the 9th
        self.assertEqual(start.day, 9)
        self.assertEqual(start.month, 2)
        self.assertEqual(start.year, 2014)
        self.assertEqual(start.hour, 0)
        self.assertEqual(start.minute, 0)

        # This should be Friday, the 14th
        self.assertEqual(end.day, 14)
        self.assertEqual(end.month, 2)
        self.assertEqual(end.year, 2014)
        self.assertEqual(end.hour, 12)
        self.assertEqual(end.minute, 0)

        # Here's saturday afternoon
        target_date = datetime.datetime(year=2014, month=2, day=15, hour=16, minute=20)
        start, end = feed.get_time_period(target_date=target_date)

        # This should be Friday, the 14th
        self.assertEqual(start.day, 14)
        self.assertEqual(start.month, 2)
        self.assertEqual(start.year, 2014)
        self.assertEqual(start.hour, 12)
        self.assertEqual(start.minute, 0)

        # This should be Suday, the 16th
        self.assertEqual(end.day, 16)
        self.assertEqual(end.month, 2)
        self.assertEqual(end.year, 2014)
        self.assertEqual(end.hour, 0)
        self.assertEqual(end.minute, 0)


class EditionCase(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create(
            name="The A.V. Club",
            slug="av-club",
            url="http://local2.avclub.com"
        )
        PublishingSchedule.objects.create(feed=self.feed, weekday=4, time=datetime.time(hour=20))
        for url, name in FEEDS:
            Section.objects.create(
                name=name,
                url=os.path.join(TEST_FEED_DIR, url),
                slug=slugify(name),
                feed=self.feed
            )

    def test_poll(self):
        self.feed.poll()

        self.assertEqual(self.feed.editions.count(), 1)
        edition = self.feed.editions.all()[0]

        self.assertEqual(edition.articles.count(), 55)
        self.assertEqual(edition.articles.filter(section__slug="newswire").count(), 20)
        self.assertEqual(edition.articles.filter(section__slug="film").count(), 15)
        self.assertEqual(edition.articles.filter(section__slug="tv-club").count(), 20)

        c = Client()
        response = c.get("/%s/latest.xml" % self.feed.slug)
        self.assertRedirects(response, edition.get_absolute_url(), status_code=302)

        response = c.get(edition.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        for section_slug in ["newswire", "film", "tv-club"]:
            response = c.get(reverse("pubfeeds.core.views.section", args=(edition.feed.slug, edition.id, section_slug)))
            self.assertEqual(response.status_code, 200)

        for article in edition.articles.all():
            response = c.get(article.get_absolute_url())
            self.assertEqual(response.status_code, 200)
