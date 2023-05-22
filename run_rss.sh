#! /bin/bash -x
sleep $(((RANDOM % 7) * 60))m ; ~/pyvenv/bin/python ~/dykfeed.py --output ~/public_html/rss.xml
