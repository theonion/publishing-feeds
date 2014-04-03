
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .models import Feed, Edition, Section, Article


def feed_overview(request, feed_slug):

    feed = get_object_or_404(Feed, slug=feed_slug)
    context = {
        "feed": feed
    }

    return render(request, "feed_overview.html", context)


def edition_overview(request, feed_slug, edition_id):
    edition = get_object_or_404(Edition, id=edition_id)
    feed = get_object_or_404(Feed, slug=feed_slug)
    context = {
        "feed": feed,
        "edition": edition,
        "sections": [],
    }

    for section_id in feed.get_section_order():
        section = Section.objects.get(id=section_id)
        if section.articles.filter(edition=edition).exists():
            section_data = {
                "articles": edition.articles.filter(section=section).order_by("-publish_date"),
                "name": section.name,
                "url": section.url
            }
            context["sections"].append(section_data)

    return render(request, "edition_overview.html", context)


def latest(request, feed_slug):
    feed = get_object_or_404(Feed, slug=feed_slug)
    try:
        latest_edition = feed.editions.filter(published_date__lte=timezone.now())[0]
    except IndexError:
        raise Http404
    return HttpResponseRedirect("%s" % latest_edition.get_absolute_url())


def edition(request, feed_slug, edition_id):
    edition = get_object_or_404(Edition, id=edition_id)
    feed = get_object_or_404(Feed, slug=feed_slug)
    context = {
        "feed": feed,
        "edition": edition,
        "sections": [],
    }

    for section_id in feed.get_section_order():
        section = Section.objects.get(id=section_id)
        if section.articles.filter(edition=edition).exists():
            context["sections"].append(section)

    format = request.GET.get("format", "nitf")

    return render(request, "{}/manifest.xml".format(format), context, content_type="text/xml")


def section(request, feed_slug, edition_id, section_slug):

    edition = get_object_or_404(Edition, id=edition_id)
    section = get_object_or_404(Section, slug=section_slug)

    context = {
        "edition": edition,
        "section": section,
        "articles": edition.articles.filter(section=section).order_by("-publish_date")
    }

    format = request.GET.get("format", "nitf")

    return render(request, "{}/section.xml".format(format), context, content_type="text/xml")


def article(request, feed_slug, edition_id, section_slug, article_id):
    
    article = get_object_or_404(Article, id=article_id)

    format = "xml"

    context = {
        "article": article
    }

    format = request.GET.get("format", "nitf")

    return render(request, "{}/article.xml".format(format), context, content_type="text/xml")
