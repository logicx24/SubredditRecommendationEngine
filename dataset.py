from comments import getComments
from multiprocessing import *
import praw
from praw.handlers import MultiprocessHandler
from mongo import *

def getSubredditUsers(subreddit):
	"""
	Get the commentors in a subreddit. 
	"""
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	subreddit = reddit.get_subreddit(subreddit)
	comments = subreddit.get_comments(limit=25)
	users = []
	for comment in comments:
		if comment.author not in users:
			users.append({'user':comment.author})
	return tempBulkInsert(users)

def getComments(username):
	"""
	Return the subreddits a user has commented in.
	"""
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	user = reddit.get_redditor(username)
	subs = []
	for comment in user.get_comments(limit=None):
		if comment.subreddit not in subs:
			subs.append(comment.subreddit)
	insertUser(username, subs)

def getSubreddits():
	#reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	return ['AskReddit']
	#Eventually, get all subreddits with over 10,000 users and go from there.

def main():
	pool = Pool(processes=cpu_count())
	pool.map(getSubredditUsers, getSubreddits())
	users = tempUserList()
	pool.map(getComments, users)
	#TEST. This will fail so hard. 

