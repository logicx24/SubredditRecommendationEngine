import math
from mongo import *
from pymongo import *
import dataset
import operator

def createUserVector(username):
	vector = [0]*len(dataset.unique_subs)
	user = queryUser(username, MongoClient())
	for i in range(len(dataset.unique_subs)):
		if unique_subs[i] in user['subreddits']:
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
	




