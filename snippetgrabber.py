#!/usr/bin/env python
# -*- coding: utf-8 -*-
# adding library path to imports
from __future__ import unicode_literals

import sys 
import os
import shlex
import subprocess
import time

sys.path.append(os.path.abspath("youtube-dl"))
import youtube_dl

# importing wrapper
sys.path.append(os.path.abspath("lib"))
import mongo

keyword = "NSA"

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

			if len(idCache) > 24: # num of cdus
				while (len(idCache) > 24):
					id = idCache.pop()
					completeFilename = "/Volumes/HDD-internal/MH/Youtube-Crawler/exports/videos/"+id+".mp4"
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
		print duration
		counter += 1
		contentDownload(tinyurl, startTime, duration, counter)
	

def contentDownload(tinyurl, startTime, duration, _counter):
	counter = _counter
	print "contentDownload"
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([tinyurl])	
	for files in os.listdir("exports/videos"):
		if tinyurl in files:	
			print "file found in videos, start processing."
			#extract snippet
			commandline = "./ffmpeg -i exports/videos/"+tinyurl+".mp4 -ss "+startTime+" -t "+str(duration)+" -strict -2 -v error /Volumes/HDD-internal/MH/Youtube-Crawler/exports/snippets/"+tinyurl+"_"+startTime+"-"+str(duration)+".mp4"
			print tinyurl, startTime, duration
			snippet = shlex.split(commandline)
			subprocess.Popen(snippet)
			print "done."
	

if __name__ == '__main__':
	mongo.init()
	contentSearch(keyword)
