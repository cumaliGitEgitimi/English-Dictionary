from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk.data
import pypyodbc
import re
import os         
import nltk
import string
from string import punctuation
from nltk.corpus import wordnet
from nltk.corpus import words


def termFrequency(term, doc): 
	
	""" 
	Input: term: Term in the Document, doc: Document 
	Return: Normalized tf: Number of times term occurs 
	in document/Total number of terms in the document 
	"""
	# Splitting the document into individual terms 
	normalizeTermFreq = doc.lower().split() 

	# Number of times the term occurs in the document 
	term_in_document = normalizeTermFreq.count(term.lower()) 

	# Total number of terms in the document 
	len_of_document = float(len(normalizeTermFreq )) 

	# Normalized Term Frequency 
	normalized_tf = term_in_document / len_of_document 

	return normalized_tf 



def inverseDocumentFrequency(term, allDocs): 
	num_docs_with_given_term = 0
	for doc in allDocs: 
		if term.lower() in allDocs[doc].lower().split(): 
			num_docs_with_given_term += 1
	if numDocsWithGivenTerm > 0: 
		# Total number of documents 
		total_num_docs = len(allDocs) 

		# Calculating the IDF 
		idf_val = log(float(total_num_docs) / num_docs_with_given_term) 
		return idf_val 
	else: 
		return 0


def CalculateTF_IDF():
    return termFrequency()*inverseDocumentFrequency()

