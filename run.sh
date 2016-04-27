#! /bin/bash
sleep $[(RANDOM % 7) * 60]m ; python /data/project/dykfeed/dykfeed.py --output /data/project/dykfeed/public_html/rss.xml
