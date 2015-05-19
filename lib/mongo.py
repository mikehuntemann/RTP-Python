#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo import TEXT

conn = None
videos = None
subtitles = None

def init():
	global conn, videos, subtitles, db

	conn = MongoClient()	
	db = conn['youtube']
	subtitles = db.subtitles
	videos = db.videos
	makeIndex()

def dropAndReconnect():
	db = conn['youtube']
	db.videos.drop()	
	db.subtitles.drop()
	subtitles = db.subtitles
	videos = db.videos
	makeIndex()

def saveUrl(tinyurl):
	try:
		videos.insert_one({'youtubeid': tinyurl, 'randompicked': 0,'infoadded': 0})
	except:
		print "already exists."

def getRandomID():
	cursor = videos.find_one({'randompicked': 0},{"youtubeid": 1})
	return cursor['youtubeid']
	

def pickUpdate(tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'randompicked': 1}})


def getNotPicked():
	count = videos.find({'randompicked': 0}).count()
	print count
	return count


def titleUpdate(title, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'title': title}})


def captionUpdate(caption, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'caption': caption}})


def deleteItem(tinyurl):
	videos.delete_one({'youtubeid': tinyurl})


def infoUpdate(tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'infoadded': 1}})


def updateTimecodes(tinyurl, startTime, duration, content):
	subtitles.insert_one({
		'youtubeid': tinyurl,
		'starttime': startTime,
		'duration': duration,
		'content': content
	})

def makeIndex():
	db.subtitles.ensure_index([("content", TEXT)])
	db.videos.ensure_index(("youtubeid"), unique = True)


def findKeyword(keyword):
	cursor = db.subtitles.find({ "$text": { "$search": keyword}})
	for document in cursor:
		tinyurl = document['youtubeid']
		startTime = document['starttime']
		duration = document['duration']
		return {'tinyurl':tinyurl, 'startTime': startTime, 'duration':duration}


	#cursor = db.subtitles.aggregate(
	#	[
	#		{ "$match": { "$text": { "$search": keyword, "$language": "en" } } },
	#		{ "$project": { "subtitles.content": 1 } }
	#	]
	#)




