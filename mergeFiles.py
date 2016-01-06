#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def findMatchingFiles():
    for subFile in os.listdir("exports/subs"):
        print subFile

    for snippetFile in os.listdir("exports/snippets"):
        print snippetFile

