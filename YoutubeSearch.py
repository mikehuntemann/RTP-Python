#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


# importing sqlite wrapper
import sqlite

# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))


API_KEY = "AIzaSyAjrnPLRyykFySLHfsrfz9SS7l8p--Rnjg"
keyword = "NSA"
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
			infoSearch(tinyurl)
			i += 1
	
	print 'done saving in db!'
	print i
	return i

def build_new_source():
	# datenbank durchsuchen, random select, flag check, if check = true: bau die url
	# 100 rounds = approx. 1800 entries to db
	
	while (sqlite.getNotPicked() != 0):
		tinyurl = sqlite.getRandomID()

		new_url ='http://www.youtube.com/watch?v='+tinyurl
		print "new url is "+new_url
		get_all_links(new_url)
		
		sqlite.pickUpdate(tinyurl)


def infoSearch(tinyurl):
	#tinyurl aus db laden
	try:
		#tinyurl = sqlite.getRandomIDforInfo()
		new_url = 'https://www.googleapis.com/youtube/v3/videos?id='+tinyurl+'&key='+API_KEY+'&fields=items(id,snippet(title,description),contentDetails(caption))&part=snippet,contentDetails'
		response = get_site_html(new_url)
		dataset = json.loads(response)
		for data in dataset['items']:
			title = data['snippet']['title']
			description = data['snippet']['description']
			caption = data['contentDetails']['caption']
			specificSearch(title, description, caption, tinyurl)
	except:
		print "Infos voll!"



def specificSearch(title, description, tinyurl):
	#uppercase / lowercase?
	if (re.findall(keyword, title)):
		print "match in title"
		sqlite.titleUpdate(title, description, tinyurl)
		sqlite.infoUpdate(tinyurl)
		if (caption == "true"):
				CC = getCapation(tinyurl)
				sqlite.captionUpdate(CC, tinyurl)
				print "sub saved"
		
	elif (re.findall(keyword, description, re.MULTILINE)):
		print "match in description"
		sqlite.titleUpdate(title, description, tinyurl)
		sqlite.infoUpdate(tinyurl)
		if (caption == "true"):
				CC = getCapation(tinyurl)
				sqlite.captionUpdate(CC, tinyurl)
				print "sub saved"

	else:
		sqlite.deleteRow(tinyurl)
		print tinyurl+" deleted"

def getCapation(tinyurl):
	new_url = "http://www.youtube.com/api/timedtext?&lang=en&fmt=srt&v="+tinyurl
	srt = urllib2.urlopen(new_url).read()
	if (srt != ""):
		return srt.decode("utf8")
	else:
		new_url = "http://www.youtube.com/api/timedtext?&lang=de&fmt=srt&v="+tinyurl
		srt = urllib2.urlopen(new_url).read()
		if (srt != ""):
			return srt.decode("utf8")
		else:
			print "no sub in EN or DE!"


if __name__ == '__main__':
	sqlite.init(dbName)
	sqlite.createDb()
	get_all_links('http://www.youtube.com/results?search_query='+keyword)
	build_new_source()
	
	

