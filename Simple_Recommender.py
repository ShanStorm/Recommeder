import numpy as np 
import nltk
import re
from nltk.corpus import stopwords
import urllib
import feedparser
import json 

base_url = 'http://export.arxiv.org/api/query?'
q = input("Enter search query")
max_results = input("Enter size of sample")
terms = []
start = 0
terms = remStopwords(q)
qf = 'all:'+terms[0]
if len(terms)>1:
	for i in range(1,len(terms)):
		qf = qf + 'AND' + 'all:'+ terms[i]

query = 'search_query=%s&start=0&max_results=%i'%(qf, max_results)

tf = []
itf = []
title = []
abstract = []
dlist = []
rel = []
x=0

with libreq.urlopen(base_url+query) as url:
	r = url.read()
	feed = feedparser.parse(r)
	for entry in feed.entries:
		title[x] = entry.title
		abstract[x] = entry.summary	
		dlist[x] = title[x]+abstract[x]
		x=x+1
		if x>=max_results:
			break
	max_1=0
	max_2=0
	while x>0:
		for i in range(len(terms)):
			temptf = termFreq(terms[i], dlist[x])
			if temptf>max_1:
				max_1 = temptf
				tf[x] = max_1
			tempitf = inverseDocFreq(terms[i], dlist)
			if tempitf>max_2:
				max_2 = tempitf
				itf[x] = max_2		
		rel[x] = tf[x]*idf[x]
		x=x-1

	result = {res[i]: title[i] for i in range(len(res))}
	json.dump(result, open("C:\\Users\\Admin\\Desktop\\AcadPaperRelevence.txt","w"))

	max = 0
	tot = 5
	while tot > 0:
		for i in result:
			if i>max:
				max = i
		print(result[max])
		tot=tot-1
		



#arxiv.query(query=q, max_results=10000)


def remStopwords(query):
	newQ = []
	eng_stop = set(stopwords.words('english'))
	newQ = [term for term in query if term not in eng_stop]
	return newQ


def termFreq(term, doc):
	normalizeTermFreq = doc.lower().split()
	term_count = normalizeTermFreq.count(term.lower())
	word_count = float(len(normalizeTermFreq))
	normalized_tf = term_count/word_count
	return normalized_tf

def inverseDocFreq(term, doclist):
	docs_with_term = 0
	for doc in doclist:
		if term.lower() in doclist[doc].lower().split():
			docs_with_term+=1

	if docs_with_term>0:
		total_docs = len(doclist)
		idf_val = log(float(total_docs)/docs_with_term)
		return idf_val
	else:
		return 0

