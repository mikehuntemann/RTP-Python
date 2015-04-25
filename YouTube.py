#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
=======

import sqlite3
>>>>>>> origin/master
import urllib2
import urllib
import re

# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))
<<<<<<< HEAD

# importing sqlite wrapper
import sqlite
=======

# importing sqlite wrapper
import sqlite

keyword = "nsa"
dbName = "youtube"

conn = sqlite3.connect('youtube.db')
c = conn.cursor()
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
>>>>>>> origin/master

keyword = "nsa"
dbName = "youtube"

<<<<<<< HEAD
#conn = sqlite3.connect('youtube.db')
#c = conn.cursor()
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}

=======
def tableCreate():
	c.execute("""DROP TABLE IF EXISTS urls""")
	c.execute("""CREATE TABLE urls (youtubeid text,randompicked int);""")
>>>>>>> origin/master

def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url,None,headers)
	response = opener.open(request).read()
	return response

<<<<<<< HEAD
=======
def get_random_id():
	c.execute("""SELECT youtubeid FROM urls WHERE randompicked = 0 ORDER BY RANDOM() LIMIT 1""")		
	return c.fetchone()[0]

>>>>>>> origin/master

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
			sqlite.save_url(tinyurl)
			i += 1
	
	print 'done saving in db!'
	print i


def build_new_source():
	# datenbank durchsuchen, random select, flag check, if check = true: bau die url
	# 100 rounds = approx. 1800 entries to db
	rounds = 0
	
	while rounds < 1000:
		rounds += 1

<<<<<<< HEAD
		tinyurl = sqlite.getRandomID()
=======
		tinyurl = get_random_id()
>>>>>>> origin/master
		
		new_url ='http://www.youtube.com/watch?v='+tinyurl
		print "new url is "+new_url
		get_all_links(new_url)

<<<<<<< HEAD
		sqlite.update(tinyurl)
=======
		c.execute("""UPDATE urls SET randompicked = 1 WHERE youtubeid=?""", (tinyurl,))
		conn.commit()
>>>>>>> origin/master


if __name__ == '__main__':
	sqlite.init(dbName)
<<<<<<< HEAD
	sqlite.createDb()
=======
	tableCreate()
>>>>>>> origin/master
	get_all_links('http://www.youtube.com/results?search_query='+keyword)
	build_new_source()
