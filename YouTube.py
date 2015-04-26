#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import re

# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))


# importing sqlite wrapper
import sqlite



keyword = "nsa"
dbName = "youtube"
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}


def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url,None,headers)
	response = opener.open(request).read()
	return response

def get_all_links(url):
	# Liste, suchen, link checken, liste checken, liste adden, db adden
	links = []
	source = get_site_html(url)
	i = 0
	links = re.findall('\/watch\?v=\w{11}', source)

	for link in links:
		if (link.startswith('/watch?v=') == True):
			tinyurl = link.split('=')[-1]
			
			if tinyurl in links:
				continue

			links.append(tinyurl) 
			sqlite.saveUrl(tinyurl)
			i += 1
	
	print 'done saving in db!'
	print i


def build_new_source():
	# datenbank durchsuchen, random select, flag check, if check = true: bau die url
	# 100 rounds = approx. 1800 entries to db
	rounds = 0
	
	while rounds < 30:
		rounds += 1

		tinyurl = sqlite.getRandomID()

		new_url ='http://www.youtube.com/watch?v='+tinyurl
		print "new url is "+new_url
		get_all_links(new_url)

		sqlite.update(tinyurl)


if __name__ == '__main__':
	sqlite.init(dbName)
	sqlite.createDb()
	get_all_links('http://www.youtube.com/results?search_query='+keyword)
	build_new_source()
