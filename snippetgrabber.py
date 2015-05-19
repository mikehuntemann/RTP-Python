#!/usr/bin/env python
# -*- coding: utf-8 -*-
# adding library path to imports
import sys 
import os
sys.path.append(os.path.abspath("lib"))

# importing wrapper
import mongo

keyword = "NSA"


def dbIndexing():
	mongo.makeIndex()

def contentSearch(keyword):
	mongo.findKeyword(keyword)
	

if __name__ == '__main__':
	mongo.init()
	dbIndexing()
	contentSearch(keyword)