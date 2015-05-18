#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient


conn = None
videos = None

def init():
	global conn, videos

	conn = MongoClient()
	conn['youtube'].videos.drop()	
	db = conn['youtube']
	videos = db.videos


def saveUrl(tinyurl):
	videos.insert_one({'youtubeid': tinyurl, 'randompicked': 0,'infoadded': 0})


def getRandomID():
	cursor = videos.find_one({'randompicked': 0},{"youtubeid": 1})
	return cursor['youtubeid']
	

def pickUpdate(tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'randompicked': 1}})


def getNotPicked():
	count = videos.find({'randompicked': 0}).count()
	print count
	return count

def titleUpdate(title, description, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'title': title, 'description': description}})


def captionUpdate(caption, tinyurl):
	videos.update_one({'youtubeid': tinyurl}, {"$set": {'caption': caption}})


def deleteItem(tinyurl):
	videos.delete_one({'youtubeid': tinyurl})


def infoUpdate(tinyurl):
	video.update_one({'youtubeid': tinyurl}, {"$set": {'infoadded': 1}})

