#!/usr/bin/env python
import tweepy, json, requests, datetime, os, time, re, praw
from urlparse import urlparse
from os.path import splitext
#from our keys module (keys.py), import the keys dictionary
from keys import keys
from random import randint

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

########################## Read breeds ###########################################
with open("breeds.txt", "r") as f:
         breed_list = f.read().splitlines()
breeds = re.compile("|".join(breed_list))

########################### Twitter listener #######################################
class StdOutListener(tweepy.StreamListener):
	def on_data(self, data):
		# get tweet data
		decoded = json.loads(data)
		tweet_body = decoded['text']
		user = decoded['user']['screen_name']
		tweetId = decoded['id_str']

		# remove twitter handles, just get tweet body then check if a breed is mentioned
		just_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)','', tweet_body)
		breed_in_tweet = breeds.search(just_tweet.lower())

		# if breed found in tweet, get random picture of breed and check size 
		# else if dog is in tweet, get random picture of dog and check size
		# else pass
		
		if breed_in_tweet:
			while True:
                                try:
					file = get_breed_img(breed_in_tweet.group(0))
					if os.stat(file).st_size < 3072000: #make this into function?
						break
					else:
						os.remove(file)
				except Exception as e:
					continue
			try: #need to test with send_tweet()
				update = '@%s' % (user)
				api.update_with_media(file, status=update, in_reply_to_status_id=tweetId)
				os.remove(file)
			except Exception as e:
				return False
	
			return True
		elif 'dog' in just_tweet.strip().lower():
			while True:
				try:
					file = get_rand_img()
					if os.stat(file).st_size < 3072000:
						break
					else:
						os.remove(file)
				except Exception as e:
					continue
			try:
				update = '@%s' % (user)
				api.update_with_media(file, status=update, in_reply_to_status_id=tweetId)	
				os.remove(file)
				#send_tweet(file, user, tweetId)
			except Exception as e:
				print e

			return True
		else:
			pass
		#time.sleep(30)

	def on_error(self, status):
		print status


#################### send tweet ###############################################
def send_tweet(file, user, tweetId):
	update = '@%s' % (user)
	api.update_with_media(file, status=update, in_reply_to_status_id=tweetId)
	os.remove(file)
##################### get image from sources ###################################

# Not the best/secure way to get the extension
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
		try:
			rand = reddit.subreddit('dogpictures+puppies+dogswearinghats+lookatmydog').random().url
			ext = get_ext(rand)
			print(ext)
			if "imgur.com" and "gfycat.com" and "youtube.com" not in rand: #skip imgur and gfycat for now
			#if extension is not empty (poor way of checking... need to fix
				jsondata = json.loads(resp.content)
				img_filename = download_img(jsondata['message'])
				if ext:
					return img_filename
			time.sleep(2) #only one request per 2 seconds for Reddit
		except Exception as e:
			return False 
	else: #use dog.ceo API if odd
		try:
			url = "https://dog.ceo/api/breeds/image/random"
			resp = requests.get(url)
			if resp.ok: #check response ok
				jsondata = json.loads(resp.content)
				img_filename = download_img(jsondata['message'])
		except Exception as e:
			return False
		return img_filename #return filename of image
		

def get_breed_img(breed):
	try:
		url = "https://dog.ceo/api/breed/" + breed + "/images/random"
		resp = requests.get(url)
		if resp.ok: #check response ok
			jsondata = json.loads(resp.content)
			img_filename = download_img(jsondata['message'])

	except Exception as e:
		print e

	return img_filename #return filename of image

def download_img(url):
	try:
		img_data = requests.get(url).content #get data
		exten = get_ext(url)
		filename = "img-" + str(date) + exten
		with open(filename, 'wb') as handler: #write data
			handler.write(img_data)
		return filename
	except Exception as e:
		return

##################### start listener ###################################
def main():
	listener = StdOutListener()
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	stream = tweepy.Stream(auth, listener)
	stream.filter(track=['@ireplydogs']) #filter by twitter handle (change to reflect your own account)

if __name__ == '__main__':
	main()

