#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""

Parse https://en.wikipedia.org/wiki/Template:Did_you_know and generate a feed.

"""

import sys
import argparse
from urllib.request import urlopen
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup
import re
import copy
import PyRSS2Gen
import datetime
from collections import namedtuple

FeedEntry = namedtuple('FeedEntry', ('title', 'link', 'desc'))


def reencode_url(url):
    parsed_url = urlparse(url)
    encoded_path = quote(parsed_url.path)

    if parsed_url.query:
        encoded_query = quote(parsed_url.query)
        encoded_url = f"{parsed_url.scheme}://{parsed_url.netloc}{encoded_path}?{encoded_query}"
    else:
        encoded_url = f"{parsed_url.scheme}://{parsed_url.netloc}{encoded_path}"

    return encoded_url


def detag(node):
    s = node.get_text()
    s = re.sub(r' +', ' ', s)
    return s


def replace_dyk(s, rep):
    return re.sub(r'^\.\.\.', rep, s)


def absolutelink(url):
    return re.sub(r'^.', 'https://en.wikipedia.org/wiki', url)
# TODO: read <base href=


def clean_html_in_hooks(source):
    source = re.sub(r'.*<!--Hooks-->', '', source, flags=re.DOTALL)
    source = re.sub(r'<!--HooksEnd-->.*', '', source, flags=re.DOTALL)
    source = re.sub(r' ?<i[^<>]*>\((pictured|example pictured)\)</i>', '', source)
    return source


def extractEntry(htmlNode):
    htmlNode = copy.copy(htmlNode)

    # extract link from <b><a href="...">...
    anc = htmlNode.find('b')
    if anc is None:
        return None
    anc = anc.find('a')
    url = reencode_url(absolutelink(anc['href']))

    for a in htmlNode.findAll('a'):
        a['href'] = reencode_url(absolutelink(a['href']))

    title = replace_dyk(detag(htmlNode), '#DidYouKnow')
    desc = htmlNode.encode_contents(formatter='html5').decode('utf-8')
    desc = replace_dyk(desc, 'Did you know')
    return FeedEntry(title.strip(), url, desc.strip())


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str,
                        default='public_html/rss.xml')
    parser.add_argument('-u', '--url', type=str,
                        default='https://en.wikipedia.org/api/rest_v1/page/html/Template%3ADid_you_know')
    parser.add_argument('--bs4features', type=str,
                        default='html.parser')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False,
                        help='turn on verbose message output')
    options = parser.parse_args()
    if options.verbose:
        print(f'{options}', file=sys.stderr)

    source = urlopen(options.url).read().decode('utf-8')
    html = BeautifulSoup(source, options.bs4features)
    date = html.find('meta', attrs={'property': 'dc:modified'}).get('content')
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

    ul = BeautifulSoup(clean_html_in_hooks(source), options.bs4features)

    feed = PyRSS2Gen.RSS2(
        title=u'Wikipedia\'s latest "Did you know?" entries',
        link=u'https://en.wikipedia.org/wiki/Wikipedia:Did_you_know',
        description=u'Latest "Did you know?" entries written by English Wikipedia contributors',
        lastBuildDate=datetime.datetime.utcnow())

    for e in ul.findAll('li'):
        entry = extractEntry(e)
        if entry is None:
            if options.verbose:
                print(f'entry: failed: {e}')
            continue
        feed.items.append(PyRSS2Gen.RSSItem(
            title=entry.title,
            link=entry.link,
            description=entry.desc,
            pubDate=date))
        if options.verbose:
            print(f'entry: {entry.link}')

    with open(options.output, 'w') as f:
        feed.write_xml(f, encoding='utf-8')
        if options.verbose:
            print(f'output: {options.output}')
