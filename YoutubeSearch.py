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



API_KEY = "AIzaSyAjrnPLRyykFySLHfsrfz9SS7l8p--Rnjg"
keyword = "NSA"
dbName = 'youtube'
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}


def build_new_source():
	while (mongo.getNotPicked() != 0):
		tinyurl = mongo.getRandomID()
		new_url ='http://www.youtube.com/watch?v='+tinyurl
		print "new url is "+new_url
		get_all_links(new_url)
		mongo.pickUpdate(tinyurl)


def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url,None,headers)
	response = opener.open(request).read()
	return response


def get_all_links(url):
	links = []
	i = 0
	source = get_site_html(url)
	links = re.findall('\/watch\?v=\w{11}', source)
	for link in links:
		if (link.startswith('/watch?v=') == True):
			tinyurl = link.split('=')[-1]
			if tinyurl in links:
				continue
			links.append(tinyurl) 
			mongo.saveUrl(tinyurl)
			infoSearch(tinyurl)
			i += 1
	
	print 'done saving in db!'


def infoSearch(tinyurl):
	new_url = 'https://www.googleapis.com/youtube/v3/videos?id='+tinyurl+'&key='+API_KEY+'&fields=items(id,snippet(title,description),contentDetails(caption))&part=snippet,contentDetails'
	response = get_site_html(new_url)
	dataset = json.loads(response)
	for data in dataset['items']:
		title = data['snippet']['title']
		description = data['snippet']['description']
		specificSearch(title, description, tinyurl)


def specificSearch(title, description, tinyurl):
	if (re.findall(keyword, title)):
		print "match in title"
		mongo.titleUpdate(title, tinyurl)
		mongo.infoUpdate(tinyurl)
		subtitleDownloader.getCaption(tinyurl)
	elif (re.findall(keyword, description, re.MULTILINE)):
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
	#get_all_links('http://www.youtube.com/results?search_query='+keyword)
	build_new_source()
	


