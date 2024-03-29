#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS:
import json
import os
import re
import sys
import requests
from time import gmtime, strftime

# IMPORTING WRAPPER-LIBS:

sys.path.append(os.path.abspath("lib"))
import mongo
import subtitleDownloader


# IMPORT GLOBAL VARIABLES FROM SETTINGS.JSON:

with open("settings.json") as data_file:
	data = json.load(data_file)
	variables = data["data"]

API_KEY = variables["API_KEY"]
SEARCH_KEY = variables["SEARCH_KEY"]
if (SEARCH_KEY == ""):
	SEARCH_KEY = None
DB_KEY = variables["DB_KEY"]
HEADER = variables["HEADER"]
GOOGLE_API_BASE = variables["GOOGLE_API_BASE"]
YOUTUBE_BASE = variables["YOUTUBE_BASE"]
YOUTUBE_SEARCH_BASE = variables["YOUTUBE_SEARCH_BASE"]


# MAKE NEW URLS FOR CRAWLER:

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


# DOWNLOAD URLS HTML:

def getSiteHtml(url):
	r = requests.get(url)
	response = r.text
	return response


# SEARCH FOR ALL LINKS TO YOUTUBE VIDEOS:

def getAllLinks(url):
	links = []
	source = getSiteHtml(url)
	allLinks = re.findall('\/watch\?v=\w{11}', source)
	for link in allLinks:
		if (link.startswith('/watch?v=') == True):
			tinyurl = link.split('=')[-1]
			if tinyurl not in links:
				if (mongo.saveUrl(tinyurl)):
					links.append(tinyurl)
					getDataFromVideo(tinyurl)


# DOWNLOAD METADATA VIA GOOGLE API:

def getDataFromVideo(tinyurl):
	url = GOOGLE_API_BASE+tinyurl+'&key='+API_KEY+'&part=snippet,contentDetails,statistics'
	response = getSiteHtml(url)
	dataset = json.loads(response)
	if (apiResponseHandler(dataset)):
		if (SEARCH_KEY == None):
			title = mongo.getField(tinyurl, "title")
			print "--> "+title
			subtitleDownloader.getCaption(tinyurl)

		else:
			tags = mongo.getField(tinyurl, "tags")
			title = mongo.getField(tinyurl, "title")
			description = mongo.getField(tinyurl, "description")
			if (checkContentForMatch(tags, title, description)):
				subtitleDownloader.getCaption(tinyurl)
			else:
				mongo.deleteItem(tinyurl)
				print "deleted Item: "+ tinyurl


# HANDLE JSON RESPONSE FROM GOOGLE API:

def apiResponseHandler(dataset):
	fields = { 'snippet': ['publishedAt', 'channelId', 'title', 'description', 'thumbnails', 'channelTitle', 'tags'],
			   'contentDetails': ['duration'],
			   'statistics': ['viewCount', 'likeCount', 'dislikeCount', 'commentCount']
			}
	for item in dataset['items']:
		tinyurl = item['id']
		for section in fields.keys():
			if not item[section]:
				break
			for fieldName in fields[section]:
				try:
					if item[section][fieldName]:
						updateName = fieldName + 'Update'
						if hasattr(mongo, updateName):
							getattr(mongo, updateName)(item[section][fieldName], tinyurl)
						else:
							pass
				except:
					pass

		crawlDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		mongo.crawlDateUpdate(crawlDate, tinyurl)

	return True


# SEARCH FOR MATCHING CONTENT:

def checkContentForMatch(tags, title, description):
	print "checking content in: " + title
	if tags:
		for tag in tags:
			if (re.findall(SEARCH_KEY, tag, re.IGNORECASE)):
				print "match in tags."
				return True
	elif title:
		if (re.findall(SEARCH_KEY, title, re.IGNORECASE)):
			print "match in title."
			return True

	elif description:
		if (re.findall(SEARCH_KEY, description, re.MULTILINE & re.IGNORECASE)):
			print "match in description."
			return True

	else:
		print "no match in title / description / tags."
		return False



if __name__ == '__main__':
# INITIATE MONGODB:

	mongo.init()
	# mongo.dropAndReconnect()


# INITIATE MONGODB FOR SUBTITLEDOWNLOADER:

	subtitleDownloader.init(mongo)


# STARTING CRAWLER:
	if (SEARCH_KEY is not None):
		for i in range(1, 50):
			print "collecting links on page " + str(i)
			getAllLinks(YOUTUBE_SEARCH_BASE+SEARCH_KEY+"&page="+str(i))
		#buildNewSource()
	else:
		# getAllLinks("http://www.youtube.com")
		buildNewSource()