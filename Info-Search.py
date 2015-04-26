#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))


# importing sqlite wrapper
import sqlite


API_KEY = "AIzaSyAjrnPLRyykFySLHfsrfz9SS7l8p--Rnjg"
dbName = "youtube"


def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url)
	response = opener.open(request).read()
	return response

def infoSearch():
	#tinyurl aus db laden
	tinyurl = sqlite.getRandomID()
	print tinyurl
	new_url = 'https://www.googleapis.com/youtube/v3/videos?id='+tinyurl+'&key='+API_KEY+'&fields=items(id,snippet(title,description))&part=snippet'
	response = get_site_html(new_url)
	dataset = json.loads(response)
	for data in dataset['items']:
		print '##############'
		print data['snippet']['title']
		print '--------------'
		print data['snippet']['description']
		print '##############'
	#parse json
	#upload in db
if __name__ == '__main__':
	sqlite.init(dbName)
	infoSearch()