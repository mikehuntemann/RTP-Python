import nltk
import re
import pprint
from nltk import word_tokenize


sqlite = None

def init(_sqlite):
	
	global sqlite
	sqlite = _sqlite

def handleData(tinyurl):
	#nltk.regexp_tokenize(text, pattern)
	pattern = r'''(?x)    # set flag to allow verbose regexps
    	([A-Z]\.)+        # abbreviations, e.g. U.S.A.
   	|	\w+(-\w+)*        # words with optional internal hyphens
   	|	\$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
   	|	\.\.\.            # ellipsis
   	|	[][.,;"'?():-_`]  # these are separate tokens;
	'''

	raw = sqlite.grabText(tinyurl)
	tokens = word_tokenize(raw)
	text = nltk.Text(tokens)
	dataLength = len(tokens)
	#words = [w.lower() for w in tokens]

	print tokens[:dataLength]
	print text.concordance('Mike')

