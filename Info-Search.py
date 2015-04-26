#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
import re
# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))


# importing sqlite wrapper
import sqlite

API_KEY = "AIzaSyAjrnPLRyykFySLHfsrfz9SS7l8p--Rnjg"
dbName = "youtube"
keyword = "NSA"

def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url)
	response = opener.open(request).read()
	return response

def infoSearch():
	#tinyurl aus db laden
	size =  sqlite.getDbSize()
	rounds = 0
	while rounds < size:
		rounds += 1
		print rounds
		tinyurl = sqlite.getRandomIDforInfo()
		print tinyurl
		new_url = 'https://www.googleapis.com/youtube/v3/videos?id='+tinyurl+'&key='+API_KEY+'&fields=items(id,snippet(title,description))&part=snippet'
		response = get_site_html(new_url)
		dataset = json.loads(response)
		for data in dataset['items']:
			title = data['snippet']['title']
			description = data['snippet']['description']
			specificSearch(title, description, tinyurl)


def specificSearch(title, description, tinyurl):
	#uppercase / lowercase?
	if (re.findall(keyword, title)):
		print "match in " + title
		sqlite.titleUpdate(title, description, tinyurl)
		sqlite.infoUpdate(tinyurl)
	elif (re.findall(keyword, description, re.MULTILINE)):
		print "match in" + title
		sqlite.titleUpdate(title, description, tinyurl)
		sqlite.infoUpdate(tinyurl)
	else:
		sqlite.deleteRow(tinyurl)

if __name__ == '__main__':
	sqlite.init(dbName)
	infoSearch()