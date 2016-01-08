#!/usr/bin/env python
# -*- coding: utf-8 -*-
# adding library path to imports
from __future__ import unicode_literals

import sys 
import os
import shlex
import subprocess
import shutil
import re

sys.path.append(os.path.abspath("youtube-dl"))
import youtube_dl

# importing wrapper
sys.path.append(os.path.abspath("lib"))
import mongo

keyword = "light"

ydl_opts = {
	'outtmpl': 'exports/videos/%(id)s.%(ext)s',
	'format': 'best'
}


def contentSearch(keyword):
	counter = 0
	currentTiny = ""
	dataset = mongo.findKeyword(keyword)
	idCache = []
	print dataset.count()

	for document in dataset:
		tinyurl = document['youtubeid']
		print tinyurl
		if (currentTiny != tinyurl):
			currentTiny = tinyurl
			idCache.insert(0, currentTiny)

			print "----> IdCache length", len(idCache)

			if len(idCache) > 8: # num of cdus
				while (len(idCache) > 8):
					id = idCache.pop()
					completeFilename = "exports/videos/"+id+".mp4"
					print "----------> REMOVING %s" % id
					try:
						os.remove(completeFilename)
					except:
						pass

			counter = 0
			
		print tinyurl
		startTime = document['starttime']
		print startTime
		durationString = document['duration']
		duration = int(durationString)
		#aincrease snippet length
		if (duration<=3):
			duration += 4
		else:
			duration += 2
		duration = str(duration)
		counter += 1
		contentDownload(tinyurl, startTime, duration, counter)
	

def contentDownload(tinyurl, startTime, duration, counter):
	print "contentDownload"
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([tinyurl])	
	for files in os.listdir("exports/videos"):
		if tinyurl in files:	
			print "file found in videos, start processing."
			commandline = "./ffmpeg -i exports/videos/"+tinyurl+".mp4 -ss "+startTime+" -t "+duration+" -strict -2 -v error exports/snippets/"+tinyurl+"_"+startTime+"-"+duration+".mp4"
			print tinyurl, startTime, duration
			snippet = shlex.split(commandline)
			subprocess.Popen(snippet)
			makeASS(tinyurl, startTime, duration)
			print "done."


def makeASS(tinyurl, startTime, duration):
	global keyword
	dataset = mongo.getSubContent(tinyurl, startTime)
	content = dataset['content']
	print content
	content.lower()
	print "content length is: " + str(len(content))
	words = content.split(" ")
	words[words.index(keyword)] = "{\b1\fs20\c&hFFFF}"+keyword+"{\b0\c}"
	print words
	if len(words) > 50:
		firstLine = words[:len(words)/2]
		firstLine = ' '.join(firstLine)
		print "firstline: " + firstLine
		secondLine = words[len(words)/2:]
		secondLine =   ' '.join(secondLine)
		print "secondline: " + secondLine
		subcontent = firstLine + "\n" + secondLine
		print subcontent
	else:
		subcontent = ' '.join(words)
		print subcontent
	newLine = "\nDialogue: 0,0:00:00.00,0:00:0"+str(duration)+".00,Flag,,0,0,0,,"+subcontent
	newFilename = tinyurl+"_"+startTime+"-"+str(duration)+".ass"
	shutil.copy2('./preset.ass', 'exports/subs/'+newFilename)
	for files in os.listdir("exports/subs/"):
		if newFilename in files:
			with open("exports/subs/"+newFilename, "a") as assFile:
				assFile.write(newLine)
				print ".ass written."




if __name__ == '__main__':
	mongo.init()
	contentSearch(keyword)
