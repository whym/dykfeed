#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import rss2m

class TestRss2m(unittest.TestCase):

    def testExtractUrlWithPeriodFromTimeline(self):
        card = {
            'card': None,
            'content': 'link is <a href="https://en.wikipedia.org/wiki/Jr.">here</a>'}
        timeline = [card]
        self.assertEqual(['https://en.wikipedia.org/wiki/Jr%2E'],
                         list(rss2m.extract_urls_from_timeline(timeline)))

    def testExtractUrlWithPeriodFromTimelineEscaped(self):
        card = {
            'card': None,
            'content': 'link is <a href="https://en.wikipedia.org/wiki/Jr%2E">here</a>'}
        timeline = [card]
        self.assertEqual(['https://en.wikipedia.org/wiki/Jr%2E'],
                         list(rss2m.extract_urls_from_timeline(timeline)))

    def testNormalizeUrlWithPeriod(self):
        self.assertEqual('https://en.wikipedia.org/wiki/Jr%2E',
                         rss2m.normalize_url('https://en.wikipedia.org/wiki/Jr.'))

    def testNormalizeUrlWithSpace(self):
        self.assertEqual('https://en.wikipedia.org/wiki/United_States',
                         rss2m.normalize_url('https://en.wikipedia.org/wiki/United States'))

    def testNormalizeUrlWithSpaceEscaped(self):
        self.assertEqual('https://en.wikipedia.org/wiki/United_States',
                         rss2m.normalize_url('https://en.wikipedia.org/wiki/United%20States'))

