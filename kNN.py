import math
from mongo import *
from pymongo import *
import dataset
import operator

def createUserVector(username):
	client = MongoClient()
	vector = [0]*len(dataset.unique_subs)
	user = queryUser(username, client)
	unique_subs = subreddits(client)
	for i in range(len(unique_subs)):
		if unique_subs[i]['name'] in user['subreddits']:
			vector[i] = 1
	return vector

def vectorDistance(user1, user2):
	vector1 = createUserVector(user1)
	vector2 = createUserVector(user2)
	dist = 0
	for i in range(len(vector1)):
		dist += pow(vector1[i] - vector2[i], 2)
	return math.sqrt(dist)

def getNeighbors(username, k):
	distances = []
	for user in allUsers(MongoClient()):
		dist = vectorDistance(username, user['username'])
		distances.append((user['username'], dist))
	distances.sort(key=operator.itemgetter(1))
	return distances[:k]

def getRecommendedSubreddit(neighbors):
	client = MongoClient()
	users = allUsersInArray([neighbor[0] for neighbor in neighbors], client)
	subredditFrequency = {}
	totalsubs = []
	for user in users:
		totalsubs += user['subreddits']
	subredditFrequency = {word : totalsubs.count(word) for word in set(totalsubs)}
	return max(totalsubs, key=totalsubs.get)

def main(username):
	return getRecommendedSubreddit(getNeighbors(username, 100))







