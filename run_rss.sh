#! /bin/bash -x
date
sleep $(((RANDOM % 3) * 60))m ; ~/pyvenv/bin/python ~/dykfeed.py --output ~/public_html/rss.xml
