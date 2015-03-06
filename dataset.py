from multiprocessing import *
import praw
from praw.handlers import MultiprocessHandler
from mongo import *
from pymongo import *
import datetime

unique_subs = []

def getSubredditUsers(subreddit):
	"""
	Get the commentors in a subreddit. 
	"""
	client = MongoClient()
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	subreddit = reddit.get_subreddit(subreddit)
	comments = subreddit.get_comments(limit=None)
	users = []
	for comment in comments:
		if comment.author.name not in users:
			users.append({'user':comment.author.name})
	return tempBulkInsert(users, client)

def getComments(username):
	"""
	Return the subreddits a user has commented in.
	"""
	global unique_subs
	client = MongoClient()
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	user = reddit.get_redditor(username['user'])
	subs = []
	for comment in user.get_comments(limit=250):
		if comment.subreddit.display_name not in subs:
			subs.append(comment.subreddit.display_name)
		if comment.subreddit.display_name not in unique_subs:
			unique_subs.append(comment.subreddit.display_name)
	return insertUser(username, subs, client)

#def updateSubs():

def getSubreddits():
	#reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	return ['all']
	#Eventually, get all subreddits with over 10,000 users and go from there.
	#return subreddits(MongoClient())

def cron(user):
	client = MongoClient()
	if abs(datetime.datetime.utcnow() - user['updated']).days >= 1:
		reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
		user = reddit.get_redditor(username['user'])
		subs = []
		for comment in user.get_comments(limit=250):
			if comment.subreddit.display_name not in subs:
				subs.append(comment.subreddit.display_name)
	return update(user, subs, client)

def main():
	try:
		pool = Pool(processes=cpu_count())
		subs = getSubreddits()
		pool.map(getSubredditUsers, subs)
		users = tempUserList(MongoClient())
		pool.map(getComments, users)
		pool.close()
	except KeyboardInterrupt:
		pool.terminate()
	#TEST. This will fail so hard. 

if __name__ == "__main__":
	main()






