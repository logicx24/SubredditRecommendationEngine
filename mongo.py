from pymongo import *
import datetime

def insertUser(username, subreddits):
	user = {
		'username': username
		'subreddits' : subreddits
		'updated' : datetime.datetime.utcnow()
	}
	client = MongoCient()
	db = client.Reddit
	collection = db.users
	userID = collection.insert(user)
	return UserID

def queryUser(username):
	client = MongoCient()
	collection = client.Reddit.users
	user = collection.find_one({'username': username})
	return user

def update(username, subreddits):
	client = MongoCient()
	collection = client.Reddit.users
	collection.update({'username': username}, {$set: {'subreddits': subreddits}})

def allUsersInArray(userArray):
	client = MongoCient()
	return client.Reddit.users.find({'username': {$in: userArray}})

def tempUserList():
	return MongoCient().Reddit.temp.find()

def tempBulkInsert(users):
	return MongoCient().Reddit.temp.insert(users)
