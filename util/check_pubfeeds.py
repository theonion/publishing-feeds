#!/usr/bin/env python3
#
# Validate existing pubfeed.
#

import argparse
import re
import sys
import xml.dom.minidom
import xml.parsers.expat

import feedparser
import requests
from bs4 import BeautifulSoup

CHECKED_IMAGES = set()

IMAGE_TYPES = ['^image/*',
               ]

class Error(Exception):
    pass


class ImageError(Error):
    pass


def check_image(url):
    if url not in CHECKED_IMAGES:
        resp = requests.get(url)
        if resp.ok:
            content_type = resp.headers.get('content-type')
            if not any(re.search(p, content_type) for p in IMAGE_TYPES):
                raise ImageError(url, 'Invalid content type: {}'.format(content_type))

            print('\tImage OK: ', url)
            CHECKED_IMAGES.add(url)
        else:
            raise ImageError(url, 'Failed GET')


def check_xml(url, content=None):
    if content is None:
        content = requests.get(url).content

    try:
        xml.dom.minidom.parseString(content)
    except xml.parsers.expat.ExpatError as exc:
        raise Error(url, content, exc)

def check_content(url):

    content = requests.get(url).content

    soup = BeautifulSoup(content, "html.parser")
    print('Article: ', soup.title.text)

    check_xml(url, content)

    for img in soup.findAll("img"):
        check_image(img["src"])


def main():
    parser = argparse.ArgumentParser(description='Initialize ship database')
    parser.add_argument('root', metavar='root',
                        help='Root pubfeed XML file (http://pubfeeds.theonion.com/onion/latest.xml')
    parser.add_argument('--whitelist', nargs='*',
                        help='Optional whiteliest')
    parser.add_argument('--min-articles', type=int, help='Optional whiteliest')
    args = parser.parse_args()

    items = []
    errors = []
    # Overview
    check_xml(args.root)
    overview = feedparser.parse(args.root)
    for entry in overview.entries:
        # Specific feeds
        check_xml(entry.link)
        feed = feedparser.parse(entry.link)
        title = feed.feed.title
        if not args.whitelist or any(re.search(p, title) for p in  args.whitelist):
            print('******* {} *******'.format(title))
            for item in feed.entries:
                items.append(item)
                try:
                    check_content(item.link)
                except Error as exc:
                    print('\tError: ', exc)
                    errors.append(exc)
    if errors:
        print('\nERRORS:')
        for error in errors:
            print(error)
        sys.exit(1)

    if args.min_articles and len(items) < args.min_articles:
        print('Error: Article count ({}) less than MIN_ARTICLES ({})'.format(
            len(items),
            args.min_articles))
        sys.exit(1)


if __name__ == '__main__':
    main()
