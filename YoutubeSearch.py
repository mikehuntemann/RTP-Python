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
					allLinks.append(tinyurl) 
					getDataFromVideo(tinyurl)
					counter += 1
	print counter + " videos added to Mongodb."


def getDataFromVideo(tinyurl):
	url = GOOGLE_API_BASE+tinyurl+'&key='+API_KEY+'&fields=items(id,snippet(title,description),contentDetails(caption))&part=snippet,contentDetails'
	response = getSiteHtml(url)
	dataset = json.loads(response)
	for data in dataset['items']:
		title = data['snippet']['title']
		description = data['snippet']['description']
		checkContentForMatch(title, description, tinyurl)


def checkContentForMatch(title, description, tinyurl):
	if (re.findall(SEARCH_KEY, title)):
		print "match in title"
		mongo.titleUpdate(title, tinyurl)
		mongo.infoUpdate(tinyurl)
		subtitleDownloader.getCaption(tinyurl)
	elif (re.findall(SEARCH_KEY, description, re.MULTILINE)):
		print "match in description"
		mongo.titleUpdate(title, tinyurl)
		mongo.infoUpdate(tinyurl)
		subtitleDownloader.getCaption(tinyurl)
	else:
		print tinyurl+" deleted"


if __name__ == '__main__':
	# init database
	mongo.init()
	#mongo.dropAndReconnect()

	# init subtitle downloader
	subtitleDownloader.init(mongo)

	# search
	getAllLinks('http://www.youtube.com/results?search_query='+SEARCH_KEY)
	#buildNewSource()
	


