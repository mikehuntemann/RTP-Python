#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json

# importing wrapper
sys.path.append(os.path.abspath("lib"))
import mongo


API_KEY = "AIzaSyAjrnPLRyykFySLHfsrfz9SS7l8p--Rnjg"

def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url,None,headers)
	response = opener.open(request).read()
	return response


def infoUpdate(tinyurl):
	new_url = 'https://www.googleapis.com/youtube/v3/videos?id='+tinyurl+'&key='+API_KEY+'&fields=items(snippet(publishedAt))&part=snippet'
	response = get_site_html(new_url)
	dataset = json.loads(response)
	for data in dataset['items']:
		date = data['snippet']['publishedAt']
		mongo.updateDate(tinyurl, date)

def processTinys():
	dataset = mongo.getUniqueTinys()
	for tinyurl in dataset['youtubeid']:
		infoUpdate(tinyurl)

if __name__ == '__main__':
	processTinys()