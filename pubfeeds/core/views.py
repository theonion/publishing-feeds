
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .models import Feed, Edition


def latest(request, feed_slug):
    feed = get_object_or_404(Feed, slug=feed_slug)
    try:
        latest_edition = feed.editions.all()[0]
    except IndexError:
        raise Http404
    return HttpResponseRedirect(latest_edition.get_absolute_url())


def edition(request, feed_slug, edition_id):
    edition = get_object_or_404(Edition, id=edition_id)
    context = {
        "edition": edition,
        "sections": [],
    }
    for item in edition.items.iterator():
        if item.section not in context["sections"]:
            context["sections"].append(item.section)

    return render(request, "manifest.xml", context)


def section(request, slug):
    pass


def item(request, pk):
    pass

