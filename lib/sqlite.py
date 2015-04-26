#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = None
c = None

def init(dbName):
	global conn, c

	conn = sqlite3.connect(dbName + '.db')
	c = conn.cursor()

def saveUrl(tinyurl):
	c.execute("""SELECT NOT EXISTS(SELECT * FROM urls WHERE youtubeid=?)""", (tinyurl,))
	
	if (c.fetchone()[0]):
		c.execute("""INSERT INTO urls VALUES (?,"0")""", (tinyurl,))
		conn.commit()


def createDb():
	c.execute("""DROP TABLE IF EXISTS urls""")
	c.execute("""CREATE TABLE urls (youtubeid text,randompicked int);""")

def getRandomID():
	c.execute("""SELECT youtubeid FROM urls WHERE randompicked = 0 ORDER BY RANDOM() LIMIT 1""")		
	return c.fetchone()[0]

def update(tinyurl):
	c.execute("""UPDATE urls SET randompicked = 1 WHERE youtubeid=?""", (tinyurl,))
	conn.commit()
