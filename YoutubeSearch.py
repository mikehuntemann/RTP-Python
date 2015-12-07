#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import requests
import json


# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))

# importing wrapper
import mongo

import subtitleDownloader
#import analysingData


with open("settings.json") as settings_file:
	variables = json.load(settings_file)


API_KEY = variables["API_KEY"]
SEARCH_KEY = variables["SEARCH_KEY"]
DB_KEY = variables["DB_KEY"]
HEADER = variables["HEADER"]
GOOGLE_API_BASE = variables["GOOGLE_API_BASE"]
YOUTUBE_BASE = variables["YOUTUBE_BASE"]


def buildNewSource():
	while (mongo.getNotPicked() != 0):
		try:
			tinyurl = mongo.getRandomID()
			url = YOUTUBE_BASE + tinyurl
			print "now crawling " + url + "."
			getAllLinks(url)
			mongo.pickUpdate(tinyurl)
		except:
			continue

def getSiteHtml(url):
	respone = None
	opener = urllib2.build_opener()
	try:
		request = urllib2.Request(url, None, HEADER)
		response = opener.open(request).read()
	except:
		pass	
	return response
	

def getAllLinks(url):
	links = []
	counter = 0
	source = getSiteHtml(url)
	allLinks = re.findall('\/watch\?v=\w{11}', source)
	for link in allLinks:
		if (link.startswith('/watch?v=') == True):
			tinyurl = link.split('=')[-1]
			if tinyurl not in links:
				if (mongo.saveUrl(tinyurl)):
					links.append(tinyurl) 
					getDataFromVideo(tinyurl)
					counter += 1
	print counter + " videos added to Mongodb."


def apiResponseHandler(dataset, fields):
	# make all data available to specific variables
	# global?

	for data in dataset['videos']:
		tinyurl = data['id']
		published = data['snippet']['publishedAt']
		channelId = data['snippet']['channelId']
		title = data['snippet']['title']
		description = data['snippet']['description']
		thumbnailUrl =  data['snippet']['thumbnails']['high']
		categoryId = data['categoryId']
		duration = data['contentDetails']['duration']
		aspectRatio = data['contentDetails']['aspectRatio']
		viewCount = data['statistics']['viewCount']
		likeCount = data['statistics']['likeCount']
		dislikeCount = data['statistics']['dislikeCount']
		favortiveCount = data['statistics']['favortiveCount']
		commentCount = data['statistics']['commentCount']

	# return chosen fields as variables
	return 

def getDataFromVideo(tinyurl):
	url = GOOGLE_API_BASE+tinyurl+'&key='+API_KEY+'&part=snippet,contentDetails,statistics'
	response = getSiteHtml(url)
	dataset = json.loads(response)
	apiResponseHandler(dataset)
	# woher bekomme ich die variablen?
	if (checkContentForMatch(title, description):
		mongo.titleUpdate(title, tinyurl)
		mongo.infoUpdate(tinyurl)
		subtitleDownloader.getCaption(tinyurl)
	else:
		mongo.deleteItem(tinyurl)

def checkContentForMatch(title, description):
	if ((re.findall(SEARCH_KEY, title)):
		print "Match in title."
		return True

	elif (re.findall(SEARCH_KEY, description, re.MULTILINE)):
		print "Match in description."
		return True

	else:
		print "No match in title / description."
		return False



if __name__ == '__main__':
	# init database
	mongo.init()
	#mongo.dropAndReconnect()

	# init subtitle downloader
	subtitleDownloader.init(mongo)

	# search
	getAllLinks('http://www.youtube.com/results?search_query='+SEARCH_KEY)
	#buildNewSource()
	


