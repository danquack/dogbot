#!/usr/bin/env python
import tweepy, json, requests, datetime, os, time
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
		result = decoded['text'].split()
		if 'dog' in result[1]:
			try:
				while True:
					file = get_img()
					if os.stat(file).st_size < 5000000:
						break
			except OSError as e:
				print e

			update = '@%s' % (decoded['user']['screen_name'])
			tweetId = decoded['id_str']
			api.update_with_media(file, status=update, in_reply_to_status_id=tweetId)
			os.remove(file)
			time.sleep(60)
			return True

	def on_error(self, status):
		print status

##################### reddit get image from dogpictures subreddit ###################################
def get_img():
	subreddit = reddit.subreddit('dogpictures+dogswearinghats+puppies+Happydogs+blop')
	
	# fix to parse all imgur options (for now just skip imgur)
	# (https://inventwithpython.com/blog/2013/09/30/downloading-imgur-posts-linked-from-reddit-with-python/)
	while True:
		rand = subreddit.random().url
		if "imgur.com" not in rand:
			break
	img_data = requests.get(rand).content
	filename = "img-" +str(date) + '.jpg'
	with open(filename, 'wb') as handler:
		handler.write(img_data)
	return filename

##################### start listener ###################################
if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['@ireplydogs'])

