#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""Parse https://en.wikipedia.org/wiki/Template:Did_you_know and generate a feed."""

import sys
import argparse
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import PyRSS2Gen
import datetime
import cgi
import codecs

def detag(s):
    s = re.sub(r'<.*?>', ' ', s)
    s = re.sub(r' +', ' ', s)
    s = re.sub(r' ([\?\.,])', lambda m: m.group(1), s)
    return s

def cdata(s):
    return "\n<![CDATA[\n%s\n]]>\n" % cgi.escape(s)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, default='public_html/rss.xml')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='turn on verbose message output')
    options = parser.parse_args()
    if options.verbose:
        print >>sys.stderr, options

    source = urllib2.urlopen('http://parsoid-lb.eqiad.wikimedia.org/v2/en.wikipedia.org/html/Template%3ADid_you_know').read()
    html = BeautifulSoup(source)
    date = html.find('meta', attrs={'property': 'dc:modified'}).get('content')
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    source = re.sub(r'.*<!--Hooks-->', '', source, flags=re.DOTALL)
    source = re.sub(r'<!--HooksEnd-->.*', '', source, flags=re.DOTALL)
    source = re.sub(r' ?<i.*?>\(pictured\)</i>', '', source)
    ul = BeautifulSoup(source)

    feed = PyRSS2Gen.RSS2(
        title=u'Wikipedia\'s latest "Did you know?" entries',
        link=u'https://en.wikipedia.org/wiki/Wikipedia:Did_you_know',
        description=u'Latest "Did you know?" entries from English Wikipedia contributors',
        lastBuildDate=datetime.datetime.utcnow())

    for e in ul.findAll('li'):
        anc = e.find('b').find('a')
        url = anc['href']
        url = re.sub(r'^.', 'https://en.wikipedia.org/wiki', url)
        q = detag(unicode(e))
        feed.items.append(PyRSS2Gen.RSSItem(
            title=q.replace('...', '#DidYouKnow'),
            link=url,
            description=u''.join(unicode(x) for x in e.contents).replace('...', 'Did you know'),
            pubDate=date))
            

    feed.write_xml(codecs.open(options.output, 'w', encoding='utf-8'))
