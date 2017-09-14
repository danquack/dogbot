#!/usr/bin/env python
import tweepy, json, requests, datetime, os, time, re
from urlparse import urlparse
from os.path import splitext
#from our keys module (keys.py), import the keys dictionary
from keys import keys
import praw

date = datetime.datetime.now().strftime("%m%d%Y-%H:%M:%S")

##################### Connect to reddit and twitter #################################
#																					#
# Make sure to enter your credentials in the keys.py file                           #
#																					#
#																					#
#####################################################################################
reddit = praw.Reddit(client_id=keys['reddit_clientID'], client_secret=keys['reddit_clientsec'],
                     password=keys['reddit_pass'], user_agent='dog bot',
                     username=keys['reddit_user'])

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

########################### Twitter listener #######################################
class StdOutListener(tweepy.StreamListener):
	def on_data(self, data):
		decoded = json.loads(data)
		tweet_body = decoded['text']
		# remove twitter handles and just check tweet for 'dog'
		just_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)','', tweet_body)
		#if "dog" is found in the tweet, call get_img until less than 3072 kb (limit for tweepy?)
		if 'dog' in just_tweet.strip().lower():
			try:
				while True:
					file = get_img()
					if os.stat(file).st_size < 3072000:
						break
			except OSError as e:
				print e

			update = '@%s' % (decoded['user']['screen_name'])
			tweetId = decoded['id_str']
			api.update_with_media(file, status=update, in_reply_to_status_id=tweetId)
			os.remove(file)
			#time.sleep(36)
			return True

	def on_error(self, status):
		print status

##################### reddit get image from dog subreddits ###################################
# Not the best/secure way to get the extension
# Change in future to alternative method
def get_ext(url):
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext

# get random image from list of subreddits

def get_img():
	subreddit = reddit.subreddit('dogpictures+dogswearinghats+puppies+dogswitheyebrows')
	
	# fix to parse all imgur options (for now just skip imgur)
	# (https://inventwithpython.com/blog/2013/09/30/downloading-imgur-posts-linked-from-reddit-with-python/)
	try:
		while True:
			rand = subreddit.random().url
			if "imgur.com" not in rand:
				break
		
		img_data = requests.get(rand).content
		ext = get_ext(rand)
		filename = "img-" +str(date) + ext
		with open(filename, 'wb') as handler:
			handler.write(img_data)
		return filename
	except Exception as e:
		print e

##################### start listener ###################################
if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['@ireplydogs'])

