import os

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import Client, TestCase
from django.utils import timezone


from pubfeeds.core.models import Feed, Section, Edition, Article

TEST_FEED_DIR = os.path.join(os.path.dirname(__file__), "test_feeds")

FEEDS = (
    ("avclub_newswire.xml", "Newswire"),
    ("avclub_film.xml", "Film"),
    ("avclub_tvclub.xml", "TV Club"),
)

class EditionCase(TestCase):

    def setUp(self):
        self.feed = Feed.objects.create(
            name="The A.V. Club",
            slug="av-club",
            url="http://local2.avclub.com"
        )
        for url, name in FEEDS:
            Section.objects.create(
                name=name,
                url=os.path.join(TEST_FEED_DIR, url),
                slug=slugify(name),
                feed=self.feed
            )

    def test_poll(self):
        edition = Edition.objects.create(feed=self.feed, published_date=timezone.now())
        edition.poll()
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
            print(response.content)
            self.assertEqual(response.status_code, 200)
