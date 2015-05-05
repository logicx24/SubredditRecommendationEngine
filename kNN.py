#! /usr/bin/env python

import math
from mongo import *
from pymongo import *
import dataset
import operator
import numpy as np

def createUserVector(username):
	client = MongoClient()
	user = queryUser(username, client)
	unique_subs = list(subreddits(client))
	vector = [0]*len(unique_subs)
	for i in range(len(unique_subs)):
		if unique_subs[i]['name'] in user['subreddits']:
			vector[i] = 10
	return vector

def vectorDistance(user1, user2):
	vector1 = createUserVector(user1)
	vector2 = createUserVector(user2)
	# dist = 0
	# for i in range(len(vector1)):
	# 	dist += pow(vector1[i] - vector2[i], 2)
	# return math.sqrt(dist)
	return np.linalg.norm(np.array(vector1) - np.array(vector2))

def getNeighbors(username, k):
	client = MongoClient()
	distances = []
	for user in allUsers(client):
		if len(distances) > k:
			break
		dist = vectorDistance(username, user['username'])
		distances.append((user['username'], dist))
	distances.sort(key=operator.itemgetter(1))
	return distances

def getRecommendedSubreddit(username):
	client = MongoClient()
	neighbors = getNeighbors(username, 70)
	users = allUsersInArray([neighbor[0] for neighbor in neighbors], client)
	banned = queryUser(username, client)['subreddits']
	subredditFrequency = {}
	totalsubs = [sub for user in users for sub in user['subreddits']]
	subredditFrequency = {word : totalsubs.count(word) for word in set(totalsubs) if word not in banned}
	return max(subredditFrequency, key=subredditFrequency.get)


def main(username):
	dataset.getComments(username)
	return getRecommendedSubreddit(username)

if __name__ == "__main__":
	username = raw_input()
	print(main(username))



