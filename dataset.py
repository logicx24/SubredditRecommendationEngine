from multiprocessing import *
import praw
from praw.handlers import MultiprocessHandler
from mongo import *
from pymongo import *
import datetime
import sys
import requests

def getSubredditUsers(subreddit):
	"""
	Get the commentors in a subreddit. 
	"""
	client = MongoClient()
	reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation Engine", handler=MultiprocessHandler())
	subreddit = reddit.get_subreddit(subreddit)
	comments = subreddit.get_comments(limit=250)
	currentUsers = allUsers(client)
	if currentUsers:
		found = [user['username'] for user in currentUsers]
	else:
		found = []
	users = []
	for comment in comments:
		if comment.author.name not in found:
			users.append({'user':comment.author.name})
	return tempBulkInsert(users, client)

def getComments(username):
	"""
	Return the subreddits a user has commented in.
	"""
	try:
		unique_subs = []
		client = MongoClient()
		reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation Engine", handler=MultiprocessHandler())
		user = reddit.get_redditor(username)
		subs = []
		for comment in user.get_comments(limit=250):
			if comment.subreddit.display_name not in subs:
				subs.append(comment.subreddit.display_name)
			insertSub(comment.subreddit.display_name, client)
		return insertUser(username, subs, client)
	except requests.exceptions.HTTPError as e:
		print e
		pass
#def updateSubs():

def getSubreddits():
	#reddit = praw.Reddit(user_agent="kNN Subreddit Recommendation", handler=MultiprocessHandler())
	return ['all']
	#Eventually, get all subreddits with over 10,000 users and go from there.
	#return subreddits(MongoClient())

def cron(user):
	client = MongoClient()
	if abs(datetime.datetime.utcnow() - user['updated']).days >= 1:
		return getComments(username)

def main():
	try:
		pool = Pool(processes=(cpu_count()*6))
		subs = getSubreddits()
		pool.map(getSubredditUsers, subs)
		users = [user['user'] for user in tempUserList(MongoClient())]
		pool.map(getComments, users)
		pool.close()
	except KeyboardInterrupt:
		pool.terminate()
		sys.exit()

	#TEST. This will fail so hard. 

if __name__ == "__main__":
	main()






