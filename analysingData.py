import nltk
import re
import pprint
from nltk import word_tokenize


sqlite = None

def init(_sqlite):
	
	global sqlite
	sqlite = _sqlite

def handleData(tinyurl):
	raw = sqlite.grabText(tinyurl)
	tokens = word_tokenize(raw)
	text = nltk.Text(tokens)
	dataLength = len(tokens)
	#words = [w.lower() for w in tokens]

	print tokens[:dataLength]
	print text.concordance('Mike')
