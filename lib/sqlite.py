#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = None
c = None

def init(dbName):
	global conn, c

	conn = sqlite3.connect(dbName + '.db')
	c = conn.cursor()

def save_url(tinyurl):
	c.execute("""SELECT NOT EXISTS(SELECT * FROM urls WHERE youtubeid=?)""", (tinyurl,))
	
	if (c.fetchone()[0]):
		c.execute("""INSERT INTO urls VALUES (?,"0")""", (tinyurl,))
		conn.commit()



#def createDb()
#def getRandom()
#def exists(url)
#def update(url)#