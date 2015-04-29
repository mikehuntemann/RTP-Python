#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import os

sys.path.append(os.path.abspath("youtube-dl"))

from youtube_dl import YoutubeDL

ydl = YoutubeDL({
	#"verbose": True, \ # verbose logging
	"writesubtitles": True, \
	"writeautomaticsub": True, \
<<<<<<< Updated upstream
	#"allsubtitles": True, \
=======
>>>>>>> Stashed changes
	"skip_download": True, \
	"outtmpl": "exports/subs/%(id)s", \
	"subtitleslangs": ["en", "de"]
})

ydl.download(["1gWpmuHAjsU"])