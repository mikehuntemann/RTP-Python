import sqlite3
import urllib2
import urllib
import re
from bs4 import BeautifulSoup


keyword = "nsa"
conn = sqlite3.connect('youtube.db')
c = conn.cursor()
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}


def tableCreate():
	c.execute("""DROP TABLE IF EXISTS urls""")
	c.execute("""CREATE TABLE urls (youtubeid text,randompicked int);""")
	return


def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url,None,headers)
	response = opener.open(request).read()
	return response


def get_tree(url):
	source = get_site_html(url)
	tree = BeautifulSoup(source)
	return tree


def save_to_db(tinyurl):
	if (c.execute("""SELECT NOT EXISTS(SELECT * FROM urls WHERE youtubeid=?)""", (tinyurl,))):
		print 'step 1'
		c.execute("""INSERT INTO urls VALUES (?,"0")""", (tinyurl,))
		conn.commit()


def get_all_links(url):
	# Liste, suchen, link checken, liste checken, liste adden, db adden
	links = []
	source = get_site_html(url)
	i = 0
	links = re.findall('\/watch\?v=\w{11}', source)
	for link in links:
		if (link.startswith('/watch?v=') == True):
			tinyurl = link.split('=')[-1]
			print tinyurl
			if tinyurl in links:
				print 'EXISTS!'
				continue
			links.append(tinyurl) 
			save_to_db(tinyurl)
			print 'ADD!'
			i += 1
	print 'done saving in db!'
	print i


def build_new_source():
	# datenbank durchsuchen, random select, flag check, if check = true: bau die url
	# 100 rounds = approx. 1800 entries to db
	rounds = 0
	while rounds < 1000:
		rounds += 1
		tinyselect = c.execute("""SELECT youtubeid FROM urls WHERE randompicked = 0 ORDER BY RANDOM() LIMIT 1""")
		print tinyselect
		bob = [str(record[0]) for record in c.fetchall()]
		tinyurl = bob[0]
		print tinyurl
		c.execute("""UPDATE urls SET randompicked = 1 WHERE youtubeid=?""", (tinyurl,))
		conn.commit()
		new_url ='http://www.youtube.com/watch?v='+tinyurl
		print "new url is "+new_url
		get_all_links(new_url)


if __name__ == '__main__':
	tableCreate()
	get_all_links('http://www.youtube.com/results?search_query='+keyword)
	build_new_source()
