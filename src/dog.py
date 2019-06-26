#!/usr/bin/env python
import datetime, os, time, re, base64
from pathlib import Path
from os.path import splitext
from random import randint

from praw import Reddit
import requests

date = datetime.datetime.now().strftime("%m%d%Y-%H:%M:%S")


########################## Read breeds.txt ###########################################
with open("breeds.txt", "r") as f:
    breed_list = f.read().splitlines()


##################### get image from sources ###################################
# Not the best/secure way to get/check the extension
# Change in future to alternative method
def get_ext(url):
	return Path(url).suffix[1:]

# get random image from list of subreddits

def get_rand_img():
	random_num = randint(0,1000)
	if random_num % 2 == 0 and os.environ.get('use_reddit', False): #if even use reddit, if odd use dog.ceo API (maybe change?)
	# fix to parse all options (for now just skip imgur and gfycat)
	# (https://inventwithpython.com/blog/2013/09/30/downloading-imgur-posts-linked-from-reddit-with-python/)

		##################### Reddit #################################										#
		# Make sure to enter your credentials are in the environ vars                       #											#
		#####################################################################################
		reddit = Reddit(client_id=os.environ['reddit_clientID'], client_secret=os.environ['reddit_clientsec'],
							password=os.environ['reddit_pass'], user_agent='dog bot',
							username=os.environ['reddit_user'])
		while True:
				try:
					reddit_url = reddit.subreddit('dogpictures+puppies+dogswearinghats').random().url
					if "imgur.com" and "gfycat.com" and "youtube.com" not in reddit_url: #skip imgur/gfycat/youtube for now
						return reddit_url
					time.sleep(2) #only one request per 2 seconds for Reddit
				except Exception as e:
					print(e)
					return False

	else: #use dog.ceo API if odd
		while True:
			try:
				url = "https://dog.ceo/api/breeds/image/random"
				resp = requests.get(url)
				if resp.ok: #check response ok
					jsondata = resp.json()
					return jsondata['message']
			except Exception as e:
				print(e)
				return False

def get_breed_img(breed):
	try:
		if breed not in breed_list:
			raise Exception("Not a valid breed %s", breed)
		breed_nospaces = breed.replace(" ","")
		url = "https://dog.ceo/api/breed/" + breed_nospaces + "/images/random"
		resp = requests.get(url)
		if resp.ok: #check response ok
			jsondata = resp.json()
			return jsondata['message']
	except Exception as e:
		return False

def download_img(url):
	try:
		img_data = requests.get(url).content #get data
		exten = get_ext(url)
		filename = "/tmp/img-" + str(date) + "." + exten
		with open(filename, 'wb') as handler: #write data
			handler.write(img_data)
		return filename
	except Exception as e:
		return False