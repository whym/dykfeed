#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""

Parse https://en.wikipedia.org/wiki/Template:Did_you_know and generate a fed.

"""

import sys
import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import PyRSS2Gen
import datetime
import cgi


def detag(s):
    s = re.sub(r'<.*?>', ' ', s)
    s = re.sub(r' +', ' ', s)
    s = re.sub(r' ([\?\.,])', lambda m: m.group(1), s)
    return s


def cdata(s):
    return "\n<![CDATA[\n%s\n]]>\n" % cgi.escape(s)


def absolutelink(url):
    return re.sub(r'^.', 'https://en.wikipedia.org/wiki', url)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str,
                        default='public_html/rss.xml')
    parser.add_argument('--bs4features', type=str,
                        default='lxml')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False,
                        help='turn on verbose message output')
    options = parser.parse_args()
    if options.verbose:
        print(f'{options}', file=sys.stderr)

    source = urlopen('https://en.wikipedia.org/api/rest_v1/page/html/Template%3ADid_you_know').read().decode('utf-8')
    html = BeautifulSoup(source, options.bs4features)
    date = html.find('meta', attrs={'property': 'dc:modified'}).get('content')
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

    source = re.sub(r'.*<!--Hooks-->', '', source, flags=re.DOTALL)
    source = re.sub(r'<!--HooksEnd-->.*', '', source, flags=re.DOTALL)
    source = re.sub(r' ?<i.*?>\(pictured\)</i>', '', source)
    ul = BeautifulSoup(source, options.bs4features)

    feed = PyRSS2Gen.RSS2(
        title=u'Wikipedia\'s latest "Did you know?" entries',
        link=u'https://en.wikipedia.org/wiki/Wikipedia:Did_you_know',
        description=u'Latest "Did you know?" entries from English Wikipedia contributors',
        lastBuildDate=datetime.datetime.utcnow())

    for e in ul.findAll('li'):
        anc = e.find('b')
        if anc is None:
            continue
        anc = anc.find('a')
        url = absolutelink(anc['href'])
        for a in e.findAll('a'):
            a['href'] = absolutelink(a['href'])
        feed.items.append(PyRSS2Gen.RSSItem(
            title=detag(str(e)).replace('...', '#DidYouKnow'),
            link=url,
            description=u''.join(str(x) for x in e.contents).replace('...', 'Did you know'),
            pubDate=date))

    with open(options.output, 'w') as f:
        feed.write_xml(f, encoding='utf-8')
