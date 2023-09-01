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
        self.assertEqual(
            ['https://en.wikipedia.org/wiki/Jr%2E'],
            list(rss2m.extract_urls_from_timeline(timeline)))

    def testExtractUrlWithPeriodFromTimelineEscaped(self):
        card = {
            'card': None,
            'content': 'link is <a href="https://en.wikipedia.org/wiki/Jr%2E">here</a>'}
        timeline = [card]
        self.assertEqual(['https://en.wikipedia.org/wiki/Jr%2E'],
                         list(rss2m.extract_urls_from_timeline(timeline)))

    def testNormalizeUrlWithPeriod(self):
        self.assertEqual('https://enwp.org/Jr%2E',
                         rss2m.normalize_url('https://enwp.org/Jr.'))

    def testNormalizeUrlWithExclamation(self):
        self.assertEqual('https://enwp.org/Compute%21',
                         rss2m.normalize_url('https://enwp.org/Compute!'))

    def testNormalizeUrlWithPercent(self):
        self.assertEqual('https://enwp.org/100%25',
                         rss2m.normalize_url('https://enwp.org/100%'))

    def testNormalizeUrlWithHyphen(self):
        self.assertEqual('https://enwp.org/100%25',
                         rss2m.normalize_url('https://enwp.org/100%'))

    def testNormalizeUrlWithQuoteAndQuestion(self):
        self.assertEqual(
            "https://enwp.org/Where's_Wally%3F",
            rss2m.normalize_url('https://enwp.org/Where%27s_Wally%3F'))
        self.assertEqual(
            "https://enwp.org/Where's_Wally%3F",
            rss2m.normalize_url("https://enwp.org/Where's_Wally?"))

    def testNormalizeUrlWithAccent(self):
        self.assertEqual(
            'https://enwp.org/Le_Vin_herb%C3%A9',
            rss2m.normalize_url('https://enwp.org/Le_Vin_herb%C3%A9'))
        self.assertEqual(
            'https://enwp.org/Le_Vin_herb%C3%A9',
            rss2m.normalize_url('https://enwp.org/Le_Vin_herbé'))

    def testNormalizeUrlWithParens(self):
        self.assertEqual(
            'https://enwp.org/Apple_%28disambiguation%29',
            rss2m.normalize_url('https://enwp.org/Apple_(disambiguation)'))

    def testNormalizeUrlWithSpace(self):
        self.assertEqual(
            'https://enwp.org/United_States',
            rss2m.normalize_url('https://enwp.org/United States'))

    def testNormalizeUrlWithSpaceEscaped(self):
        self.assertEqual(
            'https://enwp.org/United_States',
            rss2m.normalize_url('https://enwp.org/United%20States'))
