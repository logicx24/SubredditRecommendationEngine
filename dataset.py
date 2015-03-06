from multiprocessing import *
import praw
from praw.handlers import MultiprocessHandler
from mongo import *
from pymongo import *

def getSubredditUsers(subreddit):
	"""
	Get the commentors in a subreddit. 
	"""
	client = MongoClient()
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	subreddit = reddit.get_subreddit(subreddit)
	comments = subreddit.get_comments(limit=250)
	users = []
	for comment in comments:
		if comment.author.name not in users:
			users.append({'user':comment.author.name})
	return tempBulkInsert(users, client)

def getComments(username):
	"""
	Return the subreddits a user has commented in.
	"""
	client = MongoClient()
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	user = reddit.get_redditor(username['user'])
	subs = []
	for comment in user.get_comments(limit=25):
		if comment.subreddit.display_name not in subs:
			subs.append(comment.subreddit.display_name)
	return insertUser(username, subs, client)

def getSubreddits():
	#reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	return ['AskReddit']
	#Eventually, get all subreddits with over 10,000 users and go from there.

def main():
	pool = Pool(processes=cpu_count())
	subs = getSubreddits()
	pool.map(getSubredditUsers, subs)
	users = tempUserList(MongoClient())
	pool.map(getComments, users)
	#TEST. This will fail so hard. 

if __name__ == "__main__":
	main()




