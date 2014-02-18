from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pubfeeds.core.models import Feed

class Command(BaseCommand):
    help = 'Polls for new feed entries'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            feed.poll()