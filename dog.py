#!/usr/bin/env python
import tweepy, json, requests, datetime, os, time, re, praw
from urlparse import urlparse
from os.path import splitext
#from our keys module (keys.py), import the keys dictionary
from keys import keys
from random import randint

date = datetime.datetime.now().strftime("%m%d%Y-%H:%M:%S")

##################### Reddit and Twitter #################################										#
# Make sure to enter your credentials are in the keys.py file                       #											#
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

########################## Read breeds.txt ###########################################
with open("breeds.txt", "r") as f:
         breed_list = f.read().splitlines()
breeds = re.compile("|".join(breed_list)) #for checking if breeds are in tweet

########################### listener #######################################
class StdOutListener(tweepy.StreamListener):
	def on_data(self, data): #upon receiving data (tweet mentions username)
		# get tweet data
		decoded = json.loads(data)
		tweet_body = decoded['text']
		user = decoded['user']['screen_name']
		tweetId = decoded['id_str']

		# remove twitter handles, just get tweet body then check if a breed is mentioned
		just_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)','', tweet_body)
		just_tweet_remove_period = just_tweet.replace(".","")
		breed_in_tweet = breeds.search(just_tweet_remove_period.lower())

		# if breed found in tweet, get random picture of breed and check size 
		# else if dog is in tweet, get random picture of dog and check size
		# else dont do anything
		
		if breed_in_tweet:
			try:
				file = get_breed_img(breed_in_tweet.group(0)) #call get breed image, returns filename
				if send_tweet(file, user, tweetId): #try to send the tweet
					return True
			except Exception as e:
				print e
		elif 'dog' in just_tweet.strip().lower():
			try:
				file = get_rand_img() #get random image, returns filename
				if send_tweet(file, user, tweetId):
					return True
			except Exception as e:
				print e
		else:
			pass
		#time.sleep(30)

	def on_error(self, status):
		print status


#################### send tweet ###############################################
def send_tweet(file, user, tweetId):
	try:
		update = '@%s' % (user)
		api.update_with_media(file, status=update, in_reply_to_status_id=tweetId) #send image @<user> (tweetId to reply to correct tweet)
		os.remove(file) 
		return True
	except Exception as e:
		print e
##################### get image from sources ###################################

# Not the best/secure way to get/check the extension
# Change in future to alternative method
def get_ext(url):
	parsed = urlparse(url)
	root, ext = splitext(parsed.path)
	return ext

# get random image from list of subreddits

def get_rand_img():
	random_num = randint(0,1000)
	if(random_num % 2 == 0): #if even use reddit, if odd use dog.ceo API (maybe change?)
	# fix to parse all options (for now just skip imgur and gfycat)
	# (https://inventwithpython.com/blog/2013/09/30/downloading-imgur-posts-linked-from-reddit-with-python/)
		while True:
				try:
					reddit_url = reddit.subreddit('dogpictures+puppies+dogswearinghats').random().url
					if "imgur.com" and "gfycat.com" and "youtube.com" not in reddit_url: #skip imgur/gfycat/youtube for now
					#if extension is not empty (poor way of checking... need to fix
						img_filename, exten = download_img(reddit_url)
						if img_filename and exten:
							return img_filename
					time.sleep(2) #only one request per 2 seconds for Reddit
				except Exception as e:
					print e
					return False 

	else: #use dog.ceo API if odd

		while True:
			try:
				url = "https://dog.ceo/api/breeds/image/random"
				resp = requests.get(url)
				if resp.ok: #check response ok
					jsondata = json.loads(resp.content)
					img_filename, exten = download_img(jsondata['message']) #download image (pass image url)
					if exten and img_filename:
						return img_filename #return filename of image
			except Exception as e:
				return False

def get_breed_img(breed):
	while True:
			try:	
				breed_nospaces = breed.replace(" ","")
				url = "https://dog.ceo/api/breed/" + breed_nospaces + "/images/random"
				resp = requests.get(url)
				if resp.ok: #check response ok
					jsondata = json.loads(resp.content)
					img_filename, exten = download_img(jsondata['message'])
					if exten and img_filename:
						return img_filename #return filename of image
			except Exception as e:
				return False

def download_img(url):
	try:
		img_data = requests.get(url).content #get data
		exten = get_ext(url)
		filename = "img-" + str(date) + exten
		with open(filename, 'wb') as handler: #write data
			handler.write(img_data)
		if os.stat(filename).st_size < 3072000: #make this into function?
			return filename, exten
		else:
			os.remove(filename)
			return False
		
	except Exception as e:
		return False

##################### start listener ###################################
def main():
	listener = StdOutListener()
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	stream = tweepy.Stream(auth, listener)
	stream.filter(track=['@ireplydogs']) #filter by twitter handle (change to reflect your own account)

if __name__ == '__main__':
	main()

