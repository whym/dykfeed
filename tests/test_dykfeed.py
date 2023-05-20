#! /usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import dykfeed
from bs4 import BeautifulSoup


def parse(html):
    return BeautifulSoup(html, 'html.parser')


class TestDYKFeed(unittest.TestCase):

    def setup(self):
        None

    def testDetagSpace(self):
        self.assertEqual('... that although several buildings surrounding Pimlico tube station are Grade II listed, the tube station itself is not?',
                         dykfeed.detag(parse('<li>... that although several buildings surrounding <b><a href="/wiki/Pimlico_tube_station" title="Pimlico tube station">Pimlico tube station</a></b> are <a href="/wiki/Listed_building#Categories_of_listed_building" title="Listed building">Grade&nbsp;II listed</a>, the tube station itself is not?</li>')))

    def testExtractTitleNormal(self):
        node = parse('<li id="mwIg">... that the Soviet submarine <i id="mwIw"><b id="mwJA"><a rel="mw:WikiLink" href="./Soviet_submarine_K-222" title="Soviet submarine K-222" id="mwJQ"><span class="nowrap" about="#mwt35" typeof="mw:Transclusion" id="mwJg">K-222</span></a></b></i> was the fastest submarine ever built?</li>').li
        self.assertEqual('#DidYouKnow that the Soviet submarine K-222 was the fastest submarine ever built?',
                         dykfeed.extractEntry(node).title)

    def testExtractUrlNormal(self):
        node = parse('<li id="mwIg">... that the Soviet submarine <i id="mwIw"><b id="mwJA"><a rel="mw:WikiLink" href="./Soviet_submarine_K-222" title="Soviet submarine K-222" id="mwJQ"><span class="nowrap" about="#mwt35" typeof="mw:Transclusion" id="mwJg">K-222</span></a></b></i> was the fastest submarine ever built?</li>').li
        self.assertEqual('https://en.wikipedia.org/wiki/Soviet_submarine_K-222',
                         dykfeed.extractEntry(node).link)

    def testExtractTitleAmpersand(self):
        node = parse('<li>... that the <b><a href="/wiki/Huanaki_Cultural_Centre_%26_Museum" title="Huanaki Cultural Centre &amp; Museum">Huanaki Cultural Centre &amp; Museum</a></b> was destroyed by <a href="/wiki/Cyclone_Heta" title="Cyclone Heta">a cyclone</a>?</li>').li
        self.assertEqual('#DidYouKnow that the Huanaki Cultural Centre & Museum was destroyed by a cyclone?',
                         dykfeed.extractEntry(node).title)

    def testExtractDescAmpersand(self):
        node = parse('<li>... that the <b><a href="/wiki/Huanaki_Cultural_Centre_%26_Museum" title="Huanaki Cultural Centre &amp; Museum">Huanaki Cultural Centre &amp; Museum</a></b> was destroyed by <a href="/wiki/Cyclone_Heta" title="Cyclone Heta">a cyclone</a>?</li>').li
        self.assertEqual('Did you know that the <b><a href="https://en.wikipedia.org/wikiwiki/Huanaki_Cultural_Centre_%26_Museum" title="Huanaki Cultural Centre &amp; Museum">Huanaki Cultural Centre &amp; Museum</a></b> was destroyed by <a href="https://en.wikipedia.org/wikiwiki/Cyclone_Heta" title="Cyclone Heta">a cyclone</a>?',
                         dykfeed.extractEntry(node).desc)
