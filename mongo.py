from pymongo import *
import datetime

def insertUser(username, subreddits, client):
	user = {
		'username': username,
		'subreddits' : subreddits,
		'updated' : datetime.datetime.utcnow()
	}
	#client = MongoCient()
	db = client.Reddit
	collection = db.users
	userID = collection.insert(user)
	return userID

def queryUser(username, client):
	#client = MongoCient()
	collection = client.Reddit.users
	user = collection.find_one({'username': username})
	return user

def update(username, subreddits, client):
	#client = MongoCient()
	collection = client.Reddit.users
	collection.update({'username': username}, {"$set": {'subreddits': subreddits}})

def subreddits(client):
	return client.Reddit.subreddits.find()

def allUsersInArray(userArray, client):
	#client = MongoCient()
	return client.Reddit.users.find({'username': {"$in": userArray}})

def tempUserList(client):
	return client.Reddit.temp.find()

def allUsers(client):
	return client.Reddit.users.find()

def tempBulkInsert(users, client):
	return client.Reddit.temp.insert(users)
