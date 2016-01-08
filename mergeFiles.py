#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shlex
import subprocess

sys.path.append(os.path.abspath("lib"))
import mongo


counter = 0

def loadSnippetsToDb():
	for file in os.listdir("exports/snippets/"):
		if file.endswith(".mp4"):
            filename = file.split(".")[0]
            for subfile in os.listdir("exports/subs/"):
                if (subfile.split(".")[0] == filename):
                    mongo.updateSubAndSnippet(filename)
                    counter =+ 1
            else:
                print file+" is no .mp4 file."
    print counter + " matches added to mongoDB."

def bakeSubs():
    dataset = mongo.findKeyword("")
    print dataset.count()
    for filename in dataset:
        try:
            commandline = "./ffmpeg -i exports/snippets/"+filename+".mp4 -vf ass=exports/subs/"+filename+".ass" "exports/baked_files/"+filename+"_sub.mp4"
            snippet = shlex.split(commandline)
            subprocess.Popen(snippet)
        except:
            pass

    print "all videos baked."


if __name__ == '__main__':
    # mongo.init()
    mongo.dropAndReconnect()
    loadSnippetsToDb()
    bakeSubs()