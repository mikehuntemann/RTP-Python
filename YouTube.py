

import sqlite3
import urllib2
import urllib
import re
from bs4 import BeautifulSoup


keyword = "nsa"
conn = sqlite3.connect('youtube.db')
c = conn.cursor()
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
#headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}

def tableCreate():
	c.execute("""DROP TABLE IF EXISTS urls""")
	c.execute("""CREATE TABLE urls (youtubeid text,randompicked int);""")
	return

def get_site_html(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url,None,headers)
	response = opener.open(request).read()
	#print response
	return response 

def get_tree(url):
	source = get_site_html(url)
	tree = BeautifulSoup(source)
	return tree

def get_all_p(url):
	tree = get_tree(url)
	pees = tree.findAll('p')
	return pees

#def get_all_links(url):
#	
#	tree = get_tree(url)
#	for link in tree.findAll('a'):
#		print link.get('href')
#	print "Links auf der Seite: "
#	print len(tree.find_all('a'))
#	return

def get_all_imgs(url):
	tree = get_tree(url)
	for tag in tree.findAll('img'):
		print tag.get('src')
	print "Bilder auf der Seite: "
	print len(tree.findAll('img'))
	return

def save_to_db(tinyurl):
	if (c.execute("""SELECT NOT EXISTS(SELECT * FROM urls WHERE youtubeid=?)""", (tinyurl,))):
		print 'step 1'
		c.execute("""INSERT INTO urls VALUES (?,"0")""", (tinyurl,))

		conn.commit()


#Youtube Links
def get_all_links(url):
	content = 0
	# Liste, suchen, link checken, liste checken, liste adden, db adden
	links = []
	source = get_site_html(url)
	#tree = get_tree(url)
	i = 0
	#links = tree.findAll('a')
	links = re.findall('\/watch\?v=\w{11}', source)
	#print links

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
	print 'flag'
	rounds = 0
	# 100 rounds = -1800 entries 
	while rounds < 1000:
		rounds += 1
		tinyselect = c.execute("""SELECT youtubeid FROM urls ORDER BY RANDOM() LIMIT 1""")
		bob = [str(record[0]) for record in c.fetchall()]
		tinyurl = bob[0]
		new_url ='http://www.youtube.com/watch?v='+tinyurl
		print "new url is "+new_url
		get_all_links(new_url)
		continue


#https://github.com/nateberman/Python-WebImageScraper/blob/master/image_scraper.py
def download_all_imgs(url):
	tree = get_tree(url)
	images = [img for img in tree.findAll('img')]
	print (str(len(images)) + " images found.")
	print 'Downloading images to current working directory.'
	#compile our unicode list of image links
	image_links = [each.get('src') for each in images]
	for each in image_links:
		filename=each.split('/')[-1]
		urllib.urlretrieve(each, filename)
	return image_links




if __name__ == '__main__':
	#tableCreate()
	get_all_links('http://www.youtube.com/results?search_query='+keyword)
	build_new_source()
