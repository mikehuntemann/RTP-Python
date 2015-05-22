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
mongo = None
framerate = 24

def init(_mongo):
	global ydl, mongo

	mongo = _mongo

	ydl = YoutubeDL({
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
			try:
				compelteFilename = "exports/subs/"+tinyurl+".en.srt"
				content = open(compelteFilename).read().decode("utf8")
				SrtToEntry(content,tinyurl)
				os.remove(compelteFilename)
				print "file removed"
			except:
				pass

def SrtToEntry(content, tinyurl):
	#Splitting subtitle blocks on \n\n
	pieces = content.split("\n\n")
	for piece in pieces:
		try:
			box = piece.split("\n")
			content = box[2]
			rawTimecode = box[1]
			startTime = getStartTime(rawTimecode)
			endTime = getEndTime(rawTimecode)
			timecodeDuration = getDuration(startTime, endTime)
			duration = timeConvert(timecodeDuration)
			mongo.updateTimecodes(tinyurl, startTime, duration, content)
		except:
			continue

def getStartTime(rawTimecode):
	content = rawTimecode
	p = re.compile('\,\d*\W\-->\W\d*\:\d*\:\d*\,\d*', re.I|re.M)
	startTime = p.sub("",content)
	return startTime


def getEndTime(rawTimecode):
	content = rawTimecode
	p = re.compile('\d*\:\d*\:\d*\,\d*\W\-->\W', re.I|re.M)
	front = p.sub("",content)
	q = re.compile('\,\d*', re.I|re.M)
	endTime = q.sub("",front)
	return endTime


def timecode_to_frames(timecode):
	return sum(f * int(t) for f,t in zip((3600*framerate, 60*framerate, framerate, 1), timecode.split(':')))


def frames_to_timecode(frames):
	return '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(frames / (3600*framerate),frames / (60*framerate) % 60,frames / framerate % 60,frames % framerate)


def getDuration(startTime, endTime):
	frames = timecode_to_frames(endTime) - timecode_to_frames(startTime)
	duration = frames_to_timecode(frames)
	return duration


def timeConvert(timecodeDuration):
	duration = timecodeDuration.split(":")
	seconds = duration[2]
	check = list(seconds)
	if (check[0] == "0"):
		return check[1]
	else:
		return seconds
		



