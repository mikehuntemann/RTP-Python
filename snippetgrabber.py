#!/usr/bin/env python
# -*- coding: utf-8 -*-
# adding library path to imports
from __future__ import unicode_literals

import sys 
import os
import shlex
import pexpect
import subprocess

sys.path.append(os.path.abspath("youtube-dl"))
import youtube_dl

# importing wrapper
sys.path.append(os.path.abspath("lib"))
import mongo

keyword = "NSA"


ydl_opts = {
	'outtmpl': 'exports/videos/%(id)s.%(ext)s',
	'format': 'worst'
}


def contentSearch(keyword):
	dataset = mongo.findKeyword(keyword)
	tinyurl = dataset['tinyurl']
	print tinyurl
	startTime = dataset['startTime']
	print startTime
	duration = dataset['duration']
	print duration
	contentDownload(tinyurl, startTime, duration)


def contentDownload(tinyurl, startTime, duration):
	print "contentDownload"
	for files in os.listdir("exports/videos"):
		print "hello."
		if tinyurl in files:
			print "file found in videos, start processing."
			#extract audiofile
			commandline1 = "ffmpeg -i /exports/videos/"+tinyurl+".mp4 -vn -ab 256 /MH/Projects/Youtube-Crawler/exports/soundfiles/"+tinyurl+".mp3"
			audio = shlex.split(commandline1)
			subprocess.call(audio, shell = True)
			
			#extract snippet
			commandline2 = "ffmpeg -i /exports/snippets/"+tinyurl+".mp4 -ss "+startTime+" -codec copy -t "+duration+" "+tinyurl+".mp4"
			#snippet = shlex.split(commandline2)
			subprocess.Popen(commandline1)
			print "snippet done."
	else:
		print "no file found in videos, starting download."
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([tinyurl])	
	print "skipped."
#for thing in (Thing1,Thing2,Thing3):
#	try:
#	thing()
#	break  #break out of loop, don't execute else clause
#except:   #BARE EXCEPT IS USUALLY A BAD IDEA!
#	pass
#else:
#	print "nothing worked"


if __name__ == '__main__':
	mongo.init()
	contentSearch(keyword)