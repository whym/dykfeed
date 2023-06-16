#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""

Read rss and post entries to Mastodon.

"""

import feedparser
from mastodon import Mastodon
from urllib.parse import unquote
import random
import html
import re
import os


rss_url = 'https://dykfeed.toolforge.org/rss.xml'
#hashtags = "#Wikipedia"
hashtags = ''

max_items_to_post = 3
items_to_fetch = max_items_to_post * 17


# used when posting as well as when finding already posted URLs
def normalize_url(url):
    return re.compile(r'\.$').sub('%2E', unquote(url).replace(' ', '_'))
# TODO: retrieve article HTML and extract <link rel="canonical" href="...."/>


def extract_urls_from_timeline(timeline):
    for status in timeline:
        if status['card'] is None:
            for m in re.finditer(r"href=\"(.*?)\"", status['content']):
                yield normalize_url(m.group(1))
        else:
            yield normalize_url(status['card']['url'])


if __name__ == '__main__':
    # Mastodon API credentials
    mastodon = Mastodon(
        access_token=os.environ.get('MASTODON_TOKEN', '/file_does_not_exist')
    )

    # Read your Mastdon timeline
    timeline = mastodon.account_statuses(
        mastodon.account_verify_credentials()['id'],
        limit=items_to_fetch, exclude_replies=True, exclude_reblogs=True)
    already_posted = set(extract_urls_from_timeline(timeline))

    # Read the RSS feed
    feed = feedparser.parse(rss_url)

    # Exclude feed entries already posted to your Mastodon timeline
    entries = [e for e in feed.entries if normalize_url(e.link) not in already_posted]
    random.shuffle(entries)

    print(f'feed timestamp: {feed.feed.updated}')
    print(f'{len(timeline)} timeline items and {len(feed.entries)} feed items fetched, {len(entries)} to be posted')

    for entry in entries[0:max_items_to_post]:
        # Create the toot
        title = html.unescape(entry.title)  # TODO: fix RSS so that this is uncecessary
        toot = f"{title} {normalize_url(entry.link)}\n{hashtags}".strip()
        # Post the toot to Mastodon
        res = mastodon.status_post(toot)
        print(f'posted {entry.link}')
