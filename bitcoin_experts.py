#!/usr/bin/env python

import praw
import requests
import time
import tweepy
import os
import sys
from os.path import getmtime

WATCHED_FILES = [__file__]
WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]

CONSUMER_KEY = '**************'
CONSUMER_SECRET = '**************'
ACCESS_TOKEN = '**************'
ACCESS_TOKEN_SECRET = '**************'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

r = praw.Reddit(user_agent = "Twitter:@bitcoin_experts:v0.2 by /u/kyletorpey")
r.login("**************","**************")

comments_cache = []
posts_cache = []
btcsubreddits = ['t5_32s8k','t5_2s3qj','t5_2yt0h','t5_2wwh3','t5_2si5v','t5_35ity','t5_31kw5','t5_3fpq3','t5_2r36m']
launchtime = time.time()

def comments_bot():
		comments = r.get_content(url="https://www.reddit.com/r/friends/comments/",limit=20)
		for comment in comments:
			tweet_body = str(comment.author) + ": " + comment.body
			tweet_body = tweet_body[:115]
			tweet = tweet_body + " " + comment.permalink
			if (comment.subreddit_id in btcsubreddits) and (comment.created_utc > launchtime) and (comment.id not in comments_cache):
				print "New tweet: " + tweet
				api.update_status(tweet)
				comments_cache.append(comment.id)

def posts_bot():
		posts = r.get_content(url="https://www.reddit.com/r/friends/",limit=20)
		for post in posts:
			tweet_body = str(post.author) + ": " + post.title
			tweet_body = tweet_body[:115]
			tweet = tweet_body + " " + post.permalink
			if (post.subreddit_id in btcsubreddits) and (post.created_utc > launchtime) and (post.id not in posts_cache):
				print "New tweet: " + tweet
				api.update_status(tweet)
				posts_cache.append(post.id)

def restart():
    print('--> restarting')
    os.execv("./bitcoin_experts2.py", sys.argv)

while True:
	for f, mtime in WATCHED_FILES_MTIMES:
		if getmtime(f) != mtime:
			restart()
		else:
			try:
			    posts_bot()
			    comments_bot()
			    time.sleep(60)
			except requests.ConnectionError as e:
			    restart()

###TO DO LIST###
#add posts to the mailing list by bitcoin experts?
#replace reddit names with twitter names in tweets
#fix tweets being too long sometimes
#post github link on the twitter
#remove quoted text from tweets
#add context to reddit links
