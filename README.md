# Dykfeed

This is a quick hack to provide [a "Did you know?" feed](http://feeds.feedburner.com/enwp/DidYouKnow) and make [a bot](https://botsin.space/@DidYouKnowWp) work.

## How to generate an RSS

1. Clone this repository.
2. `docker build -t dykfeed . && docker run -it dykfeed`
3. `docker run dykfeed python dykfeed.py --output rss.xml`

## How to run the bot

1. See <https://mastodonpy.readthedocs.io/en/stable/> and save your authentication token.
2. `docker run dykfeed env MASTODON_TOKEN=mastodon_token.txt python rss2m.py`
