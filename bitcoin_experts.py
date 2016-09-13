import praw
import time
import tweepy

CONSUMER_KEY = '*************'
CONSUMER_SECRET = '*************'
ACCESS_TOKEN = '*************'
ACCESS_TOKEN_SECRET = '*************'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

r = praw.Reddit(user_agent = "Twitter:@bitcoin_experts:v0.2 by /u/kyletorpey")
r.login("*************","*************")

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
			if ((comment.subreddit_id not in btcsubreddits) or (comment.created_utc < launchtime)) or (comment.id in comments_cache):
				print "New comment by " + str(comment.author) + ", but it's not in a Bitcoin subreddit or old."
			else:
				print "New tweet: " + tweet
				api.update_status(tweet)
				comments_cache.append(comment.id)

def posts_bot():
		posts = r.get_content(url="https://www.reddit.com/r/friends/",limit=20)
		for post in posts:
			tweet_body = str(post.author) + ": " + post.title
			tweet_body = tweet_body[:115]
			tweet = tweet_body + " " + post.url
			if ((post.subreddit_id not in btcsubreddits) or (post.created_utc < launchtime)) or (post.id in posts_cache):
				print "New submission by " + str(post.author) + ", but it's not in a Bitcoin subreddit or old."
			else:
				print "New tweet: " + tweet
				api.update_status(tweet)
				posts_cache.append(post.id)

while True:
	posts_bot()
	comments_bot()
	time.sleep(60)

###TO DO LIST###
#add posts to the mailing list by bitcoin experts?
#replace reddit names with twitter names in tweets
