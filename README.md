# dogbot

A Twitter bot that responds to users with picture of dogs. If a user tweets at the bot account with the word dog in the tweet, it will respond with a random dog picture (from a few dog subreddits).

There are a few things you will need before deploying this bot
* Twitter API access (https://apps.twitter.com/)
  * And most likely a separate account for the bot to use
* Reddit API access (https://www.reddit.com/prefs/apps/)
* Python installed with tweepy and praw
  ```bash
  pip install tweepy
  pip install praw
  ````
* A keys.py file with all your creds

```python
keys = dict(
	consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	reddit_clientID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	reddit_clientsec = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	reddit_pass = '<password>',
	reddit_user = '<username>'
)
```

Finally, just run ``` python dog.py ``` and start tweeting at it!!!
