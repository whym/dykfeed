# Dykfeed

Small scripts to provide [a "Did you know?" feed](http://feeds.feedburner.com/enwp/DidYouKnow) and [a bot](https://botsin.space/@DidYouKnowWp).

## How to generate an RSS

1. Clone this repository.
2. `docker build -t dykfeed . && docker run -it dykfeed`
3. `docker run dykfeed python dykfeed.py --output rss.xml`

## How to run the bot

1. Visit <https://mastodonpy.readthedocs.io/en/stable/> to find how to save your authentication token.
2. `docker run dykfeed python rss2m.py --token mastodon_token.txt`

## How to run tests

`docker build -t dykfeed . && docker run -it dykfeed`

## Notes on running it at Toolforge

- Run `toolforge-jobs run bootstrap-venv --command "./bootstrap_venv.sh" --image tf-python39 --wait` when dependencies (`requirements.txt`) change.
- `chmod 600 $MASTODON_TOKEN`
