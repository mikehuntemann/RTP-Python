#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient, TEXT, ASCENDING
from random import randint

conn = None
videos = None
subtitles = None
fields = { 'snippet': ['publishedAt', 'channelId', 'title', 'description', 'thumbnails', 'channelTitle', 'tags',
                           'categoryId', 'defaultAudioLanguage', 'duration', 'aspectRatio', 'viewCount', 'likeCount',
                           'dislikeCount', 'commentCount']}

SKIP_AMOUNT = 1000


# MONGO INITIALISATION SECTION:

def init():
	global conn, videos, subtitles, db

	conn = MongoClient()	
	db = conn['youtube']
	subtitles = db.subtitles
	videos = db.videos
	makeIndex()

def dropAndReconnect():
	global subtitles, videos

	db = conn['youtube']
	db.videos.drop()	
	db.subtitles.drop()
	subtitles = db.subtitles
	videos = db.videos
	makeIndex()

def makeIndex():
	db.subtitles.ensure_index([("content", TEXT)])
	db.subtitles.ensure_index(("youtubeid"), ASCENDING)
	db.videos.ensure_index(("youtubeid"), unique = True)


# CRAWLER PICK SECTION:	

def pickUpdate(tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'randompicked': 1}})


def getNotPicked():
	count = videos.find({'randompicked': 0}).count()
	print count
	return count

def getRandomID(skip=True):
	skipAmount = 0
	
	if skip:
		skipAmount = randint(0, SKIP_AMOUNT)

	cursor = videos.find_one({'randompicked': 0},{"youtubeid": 1}, skip = skipAmount) # $skip: XXX
	
	if not cursor:
		return getRandomID(False)

	return cursor['youtubeid']


# SAVE URL FROM VIDEO:

def saveUrl(tinyurl):
	try:
		videos.insert_one({'youtubeid': tinyurl, 'randompicked': 0})
		return True
	except:
		return False


# UPDATE SECTION:

def titleUpdate(title, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'title': title}})

def descriptionUpdate(description, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"set": {'description': description}})

def publishedAtUpdate(publishedAt, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'publishedAt': publishedAt}})

def channelIdUpdate(channelId, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'channelId': channelId}})

def channelTitle(channelTitle, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'channelTitle': channelTitle}})

def tagsUpdate(tags, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'tags': tags}})

def categoryIdUpdate(categoryId, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'categoryId': categoryId}})

def defaultAudioLanguageUpdate(defaultAudioLanguage, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'defaultAudioLanguage': defaultAudioLanguage}})

def durationUpdate(duration, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'duration': duration}})

def aspectRatioUpdate(aspectRatio, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'aspectRatio': aspectRatio}})

def viewCountUpdate(viewCount, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'viewCount': viewCount}})

def likeCountUpdate(likeCount, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'likeCount': likeCount}})

def dislikeCountUpdate(dislikeCount, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'dislikeCount': dislikeCount}})

def favortiveCountUpdate(favortiveCount, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'favortiveCount': favortiveCount}})

def commentCountUpdate(commentCount, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'commentCount': commentCount}})

def crawlDateUpdate(tinyurl, crawlDate):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'crawlDate': crawlDate}})

def timecodeUpdate(tinyurl, startTime, duration, content):
	subtitles.insert_one({
		'youtubeid': tinyurl,
		'starttime': startTime,
		'duration': duration,
		'content': content
	})


# DELETE ENTRY:

def deleteItem(tinyurl):
	videos.delete_one({'youtubeid': tinyurl})


# KEYWORD SEARCH:

def findKeyword(keyword):
	cursor = db.subtitles.find({ "$text": { "$search": keyword}}).sort('youtubeid', ASCENDING)
	return cursor


# CONTENT GRABBER:


def getField(tinyurl, fieldName):
	global fields
	fields[fieldName] = 1
	cursor = db.videos.find_one({"youtubeid": tinyurl}, fields)
	return cursor[fieldName]

def updateField(tinyurl, fieldName, value):
	global fields
	fields[fieldName] = value
	return videos.update_one({'youtubeid': tinyurl}, {"set": fields})
