# dogbot
A bot that responds to users with picture of dogs. If a user calls at the api, it will respond with a random dog picture (from a few dog subreddits and dog.ceo API). Also, if a user requests a specific dog breed the bot it will respond with an image of that breed (sub-breeds coming soon?).


There are a few things you will need before deploying this bot
* Reddit API access (https://www.reddit.com/prefs/apps/)
* Environment variables are set with all your creds

```bash
	# reddit specific (optional)
	TF_VAR_use_reddit = "true/false"
	TF_VAR_access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	TF_VAR_reddit_clientID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	TF_VAR_reddit_clientsec = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	TF_VAR_reddit_pass = '<password>',
	TF_VAR_reddit_user = '<username>',

	# required
	TF_VAR_domain_name = '<domain name>'
	TF_VAR_certificate_id = '<certificate id from arn>'
	TF_VAR_zone_id = '<route 53 zone>'
```

## Usage
Endpoint|Purpose|Query params avail
--- | --- | ---
/random|get a random dog image|image=<true/false> (302 edirect to image)
/breed|get a list of avail breeds|
/breed/{breed}|gets a random dog of breed|image=<true/false> (302 redirect to image)