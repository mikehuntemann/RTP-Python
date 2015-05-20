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
i = 1

ydl_opts = {
	'outtmpl': 'exports/videos/%(id)s.%(ext)s',
	'format': 'best'
}


def contentSearch(keyword):
	
	dataset = mongo.findKeyword(keyword)
	print dataset
	for document in dataset:
		tinyurl = document['youtubeid']
		print tinyurl
		startTime = document['starttime']
		print startTime
		duration = document['duration']
		print duration
		contentDownload(tinyurl, startTime, duration)
		i += 1

def contentDownload(tinyurl, startTime, duration):
	
	print "contentDownload"
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([tinyurl])	
	for files in os.listdir("exports/videos"):
		if tinyurl in files:
			print "file found in videos, start processing."
			#extract snippet
			commandline2 = "./ffmpeg -i exports/videos/"+tinyurl+".mp4 -ss "+startTime+" -t "+duration+" -strict -2 exports/snippets/"+tinyurl+"_"+str(i)+".mp4"
			snippet = shlex.split(commandline2)
			subprocess.Popen(snippet)
	
	#compelteFilename = "exports/videos/"+tinyurl+".mp4"
	#os.remove(compelteFilename)

if __name__ == '__main__':
	mongo.init()
	contentSearch(keyword)