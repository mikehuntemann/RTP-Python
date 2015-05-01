#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import string

# adding library path to imports
import sys
import os
sys.path.append(os.path.abspath("youtube-dl"))
from youtube_dl import YoutubeDL

ydl = None
sqlite = None

def init(_sqlite):
	global ydl, sqlite

	sqlite = _sqlite

	ydl = YoutubeDL({
		#"verbose": True, \ # verbose logging
		"writesubtitles": True, \
		"writeautomaticsub": True, \
		"skip_download": True, \
		"outtmpl": "exports/subs/%(id)s", \
		"subtitleslangs": ["en"]
	})


def getCaption(tinyurl):
	ydl.download([tinyurl])
	for files in os.listdir("exports/subs"):
		if tinyurl in files:
			print "found file"
			compelteFilename = "exports/subs/"+tinyurl+".en.srt"
			content = open(compelteFilename).read().decode("utf8")
			sqlite.captionUpdate(content,tinyurl)
			os.remove(compelteFilename)
			print "file removed"
			convertSrtToText(tinyurl)


def convertSrtToText(tinyurl):
	content = sqlite.grabCaption(tinyurl)
	#regular expression for selection timecode
	p = re.compile('\n?\n?\n?\d*\n\d*\:\d*\:\d*\,\d*\W\-->\W\d*\:\d*\:\d*\,\d*', re.I|re.M)
	textFile = p.sub("", content)
	#tokenized = re.split(r'[ \t\n]+', textFile)
	sqlite.textUpdate(textFile, tinyurl)
	print "Sub converted to text."

