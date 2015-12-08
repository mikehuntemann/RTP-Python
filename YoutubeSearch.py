#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import requests
import json
from time import gmtime, strftime 

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
YOUTUBE_SEARCH_BASE = variables["YOUTUBE_SEARCH_BASE"]


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


def apiResponseHandler(dataset):
	for data in dataset['items']:
		
		try:
			tinyurl = data['id']
		except:
			pass

		try:	
			publishedAt = data['snippet']['publishedAt']
			mongo.publishedAtUpdate(publishedAt, tinyurl)
		except:
			pass

		try:
			channelId = data['snippet']['channelId']
			mongo.channelIdUpdate(channelId, tinyurl)
		except:
			pass

		try:	
			title = data['snippet']['title']
			mongo.titleUpdate(title, tinyurl)
		except:
			pass

		try:
			description = data['snippet']['description']
			mongo.description(description, tinyurl)
		except:
			pass

		try:
			thumbnails =  data['snippet']['thumbnails']
			mongo.thumbnailsUpdate(thumbnails, tinyurl)
		except:
			pass

		try:
			channelTitle = data['snippet']['channelTitle']
			mongo.channelTitle(channelTitle, tinyurl)
		except:
			pass

		try:
			tags = data['snippet']['tags']
			mongo.tagsUpdate(tags, tinyurl)
		except:
			pass

		try:	
			categoryId = data['categoryId']
			mongo.categoryIdUpdate(categoryId, tinyurl)
		except:
			pass

		try:
			defaultAudioLanguage = data['snippet']['defaultAudioLanguage']
			mongo.defaultAudioLanguageUpdate(defaultAudioLanguage, tinyurl)
		except:
			pass

		try:
			duration = data['contentDetails']['duration']
			mongo.durationUpdate(duration, tinyurl)
		except:
			pass

		try:
			aspectRatio = data['contentDetails']['aspectRatio']
			mongo.aspectRatioUpdate(aspectRatio, tinyurl)
		except:
			pass

		try:
			viewCount = data['statistics']['viewCount']
			mongo.viewCountUpdate(viewCount, tinyurl)
		except:
			pass
		
		try:
			likeCount = data['statistics']['likeCount']
			mongo.likeCountUpdate(likeCount, tinyurl)
		except:
			pass
		
		try:
			dislikeCount = data['statistics']['dislikeCount']
			mongo.dislikeCountUpdate(dislikeCount, tinyurl)
		except:
			pass
		
		try:
			favortiveCount = data['statistics']['favortiveCount']
			mongo.favortiveCountUpdate(favortiveCount, tinyurl)
		except:
			pass
		
		try:
			commentCount = data['statistics']['commentCount']
			mongo.commentCountUpdate(commentCount, tinyurl)
		except:
			pass

		crawlDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		mongo.crawlDateUpdate(crawlDate, tinyurl)



def getDataFromVideo(tinyurl):
	url = GOOGLE_API_BASE+tinyurl+'&key='+API_KEY+'&part=snippet,contentDetails,statistics'
	response = getSiteHtml(url)
	dataset = json.loads(response)
	apiResponseHandler(dataset)


	if (checkContentForMatch(title, description, tags):
		subtitleDownloader.getCaption(tinyurl)
	else:
		mongo.deleteItem(tinyurl)

def checkContentForMatch(title, description, tags):
	for tag in tags:
		if (re.findall(SEARCH_KEY, tag)):
			print "match in tags."
			return True

	if ((re.findall(SEARCH_KEY, title)):
		print "match in title."
		return True

	elif (re.findall(SEARCH_KEY, description, re.MULTILINE)):
		print "match in description."
		return True

	else:
		print "no match in title / description."
		return False



if __name__ == '__main__':
	# init database
	mongo.init()
	#mongo.dropAndReconnect()

	# init subtitle downloader
	subtitleDownloader.init(mongo)

	# search
	getAllLinks(YOUTUBE_SEARCH_BASE+SEARCH_KEY)
	#buildNewSource()
	


