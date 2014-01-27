
from django.template.defaultfilters import slugify
from django.test import Client, TestCase
from django.utils import timezone

from pubfeeds.core.models import Feed, Section, Edition, Item


FEEDS = (
    ("http://www.avclub.com/feed/rss/?feature_types=tv-club&full=true&images=true", "TV Club"),
    ("http://www.avclub.com/feed/rss/?feature_types=newswire&full=true&images=true", "Newswire")
)

class FeedTestCase(TestCase):

    def setUp(self):

        self.feed = Feed.objects.create(
            name="The A.V. Club",
            slug="av-club",
            url="http://local2.avclub.com"
        )
        for url, name in FEEDS:
            Section.objects.create(
                name=name,
                url=url,
                slug=slugify(name),
                feed=self.feed
            )

    def test_poll(self):

        edition = Edition.objects.create(feed=self.feed, published_date=timezone.now())
        edition.poll()

        c = Client()
        response = c.get("/%s/latest" % self.feed.slug)
        self.assertRedirects(response, edition.get_absolute_url(), status_code=302)

        response = c.get(edition.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        print(response.content)
