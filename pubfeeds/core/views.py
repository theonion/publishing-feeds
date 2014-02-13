
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from .models import Feed, Edition, Section, Article


def latest(request, feed_slug):
    feed = get_object_or_404(Feed, slug=feed_slug)
    try:
        latest_edition = feed.editions.all()[0]
    except IndexError:
        raise Http404
    return HttpResponseRedirect("%s" % latest_edition.get_absolute_url())


def edition(request, feed_slug, edition_id):
    edition = get_object_or_404(Edition, id=edition_id)
    context = {
        "edition": edition,
        "sections": [],
    }
    for item in edition.articles.iterator():
        if item.section not in context["sections"]:
            context["sections"].append(item.section)

    format = "xml"

    return render(request, "manifest.%s" % format, context, content_type="text/xml")


def section(request, feed_slug, edition_id, section_slug):

    edition = get_object_or_404(Edition, id=edition_id)
    section = get_object_or_404(Section, slug=section_slug)

    context = {
        "edition": edition,
        "section": section,
        "articles": edition.articles.filter(section=section)
    }

    format = "xml"

    return render(request, "section.%s" % format, context, content_type="text/xml")



def article(request, feed_slug, edition_id, section_slug, article_id):
    
    article = get_object_or_404(Article, id=article_id)

    format = "xml"

    context = {
        "article": article
    }

    return render(request, "article.%s" % format, context, content_type="text/xml")
