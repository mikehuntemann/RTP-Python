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
	print dataset
	for document in dataset:
		tinyurl = document['youtubeid']
		if (currentTiny != tinyurl):
			compelteFilename = "exports/videos/"+tinyurl+".mp4"
			try:
				os.remove(compelteFilename)
			currentTiny = tinyurl
			counter = 0
			
		print tinyurl
		startTime = document['starttime']
		print startTime
		duration = document['duration']
		#aincrease snippet length
		duration = int(duration)+2
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
			# -threads 0 <--- multicore processing in ffmpeg
			commandline = "./ffmpeg -i exports/videos/"+tinyurl+".mp4 -ss "+startTime+" -t "+str(duration)+" -strict -2 exports/snippets/"+tinyurl+"_"+str(counter)+".mp4"
			snippet = shlex.split(commandline)
			subprocess.Popen(snippet)
			print "done."
	

if __name__ == '__main__':
	mongo.init()
	contentSearch(keyword)
