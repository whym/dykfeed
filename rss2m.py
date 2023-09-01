#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""

Read rss and post entries to Mastodon.

"""

import feedparser
from mastodon import Mastodon
from bs4 import BeautifulSoup
from urllib.parse import unquote, quote
import hashlib
import random
import html
import re
import os
import argparse


rss_url = 'https://dykfeed.toolforge.org/rss.xml'
hashtags = "#Wikipedia"
max_items_to_post = 3
items_to_fetch = 20
url_ending_characters = re.compile(r'[^a-zA-Z0-9_]$')  # https://github.com/mastodon/mastodon/blob/00084581289b4b7afd120845363b16247c5fa93b/config/initializers/twitter_regex.rb#L12
to_be_escaped_in_url = re.compile(r'[!\(\)\[\]]')
quote_safe = re.compile(r'[_\.\-~]')


def hash_post(post):
    return hashlib.sha256(post.encode('utf-8')).hexdigest()


def percent_encode_match(match):
    char = match.group(0)
    if quote_safe.match(char):
        return f'%{ord(char):X}'
    return quote(char.encode('utf-8'))


# used when posting as well as when finding already posted URLs
def normalize_url(url):
    return to_be_escaped_in_url.sub(
        percent_encode_match,
        url_ending_characters.sub(
            percent_encode_match,
            unquote(url).replace(' ', '_')))
# TODO: retrieve article HTML and extract <link rel="canonical" href="...."/>


def extract_urls_from_timeline(timeline):
    for status in timeline:
        bs = BeautifulSoup(status['content'], features='html.parser')
        for a in bs.findAll('a'):
            url = a.attrs.get('href')
            if url is not None:
                yield normalize_url(url)
        if status.get('card') is not None:
            yield normalize_url(status['card']['url'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', dest='token', type=str,
                        help='mastodon token file')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    # Mastodon API credentials
    mastodon = Mastodon(access_token=args.token)

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
        if args.dry_run:
            print(f'posted {entry.link} ({normalize_url(entry.link)}) (simulated)')
        else:
            res = mastodon.status_post(toot, idempotency_key=(hash_post(toot)))
            print(f'posted {entry.link} ({normalize_url(entry.link)})')
