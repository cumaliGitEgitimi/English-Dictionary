from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk.data
import pypyodbc
import re
import os         #imports the os
import nltk
import string
from string import punctuation
from itertools import chain
from nltk.corpus import wordnet
#from datetime import datetime
from datetime import date
#import enchant
from nltk.corpus import words
import SequenceMatcherSimilarity
import WordnetSimilarity
from time import gmtime, strftime
import datetime
from termcolor import colored
import shutil
import http.client, urllib.parse, json
import requests
from autocorrect import spell
from colorama import Fore, Back, Style 
from simhash import Simhash

webSearchSaveAndRemoveDirectory = "C:\\Users\AT012337\\Thesis\\Documents\\"
my_api_key = "AIzaSyBADosD5gBwXNLbYyaNAnksXBdK-EpcUZI"
my_cse_id = "1"
connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1') 

cursor = connection.cursor() 
#path= "C:\\Users\\AT012337\\Desktop\\Konu Tespiti\\SmallWord Eğitim Verileri\\"
#destinationPath= "C:\\Users\AT012337\\Thesis\\Konu Tespiti\\SmallWord Eğitim Verileri\\"
thresholdRateForSimilarity=0.4

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def split():
    s = "238 NEO Sports"
    return s.split(" ", 1)[0]

#Get Content 1-gram, 2-gram, 3-gram Freqs
def SeparateWordAndSaveDB():
    counts = dict()
    paraghraphId = 0
    #TruncateAllDatabase() #TruncateSelectedDatabase()
    #InsertTallyTable()
    path = input("Enter the Directory location to list:")
    sortlist = sorted(os.listdir(path))   
    i = 0
    while(i < len(sortlist)):
        dna = open(path + "\\" + sortlist[i],encoding='utf8',errors='ignore')
        soup = BeautifulSoup(dna)
        paragraphs = soup.find_all("p")
        paraghraphId = 1
        stemmer = PorterStemmer()
        for paragraph in paragraphs:           
            tokens = GetContentFreq(paragraph.text)
            tagged = pos_tag(tokens)
            nouns = [word for word,pos in tagged \
	            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
            for word in nouns:
                stems = stemmer.stem(word)
                if stems in counts.keys():
                    shortest,count = counts[stems]
                    counts[stems] = (shortest,count + 1)
                else:
                    counts[stems] = (stems,1)
            for kok in counts:       
                try:
                    shortest,count = counts[kok]
                    SQLCommand = ("INSERT INTO Words (DocumentId,Word, Count,StemWord,Paragraph)  VALUES (?,?,?,?,?)")
                    Values = [i,shortest,count,kok,paraghraphId]
                    cursor.execute(SQLCommand,Values)  
                    connection.commit() 
                except:
                    pass


def GetContentFreq(content):
    #Read Words
    translator = str.maketrans('', '', string.punctuation)
    words = nltk.word_tokenize(content)
    words = [word.translate(translator) for word in words]
    #Remove one letters
    words = [word for word in words if len(word) > 1]
    #Remove numbers
    words = [word for word in words if not word.isnumeric()]
    #Convert lowercase
    words = [word.lower() for word in words]
    #Remove stop-words
    words = [word for word in words if word not in stopwords.words('english')]  

    tempWords = []
    #for word in words:
    #    #word = re.sub(r'(\w)\1+', r'\1', word)
    #    tempWords.append((word))
    #words = tempWords
    tempWords = []
    for word in words:
        if word != "" and len(word) > 1:
            tempWords.append((word))
    words = tempWords
    return words


def GetCountOfDocumentsOnPath():
     sortlist = sorted(os.listdir(webSearchSaveAndRemoveDirectory))
     return len(sortlist)


def LastCheckMeaningWords():
    cursor.execute("SELECT StemWord FROM [SmallWordsEducation].[dbo].[MeaningWord] (nolock)")
    meaningWordList = cursor.fetchall()
    for meaningWord in meaningWordList:
        if not wordnet.synsets(meaningWord[0]):
            SQLCommand = ("DELETE FROM [SmallWordsEducation].[dbo].[MeaningWord] WHERE StemWord=?")
            Values = [meaningWord[0]]
            cursor.execute(SQLCommand,Values)  
            connection.commit() 

def FindSynonymsWordsGivenParameterWord(word):
    SynonymsWordList=[]
    for syn in wordnet.synsets(word):
	    for l in syn.lemmas():
             if l.name() != word:
                SynonymsWordList.append(l.name())
    return SynonymsWordList


def GetAverageSimilarityRate(totalSimilarityRate,englishDictionaryWord):
    if englishDictionaryWord==0:
        return 0
    else:
        result=totalSimilarityRate/englishDictionaryWord
    return result

#def FindWordSynonymsAndSaveDB(word):
#    sourceTopic="game"
#    sourceTopicList=FindSynonymsWordsGivenParameterWord(sourceTopic)
#    synonymsWordList=FindSynonymsWordsGivenParameterWord(word)
#    for synonymsWord in synonymsWordList:
#        totalSimilarityRate=0
#        for sourceTopic in sourceTopicList:
#            similarityRate=SequenceMatcherSimilarity.SimilarityRate(synonymsWord,sourceTopic)
#            totalSimilarityRate+=similarityRate
#        averageSmilarityRate=GetAverageSimilarityRate(totalSimilarityRate,len(sourceTopicList))
#        if averageSmilarityRate>=thresholdRateForSimilarity:
#            SQLCommand = ("EXEC InsertEnglishDictionary ?")
#            Values = [l.name()]
#            cursor.execute(SQLCommand,Values)
#            connection.commit()
#            print(l.name() +" kelimesi " + word +" kelimesi ile benzer olduğu için sözlüğe eklendi.")
#        else:
#            print(synonymsWord +" kelimesi " + word +" kelimesi ile benzer olmadığı için sözlüğe eklenmedi.")


##print(FindWordSynonymsAndSaveDB("sport"))


def SpellWord(wordList):
    spelledWordList=[]
    for word in wordList:
        spelledWordList.append(spell(word[0]))
    return spelledWordList

def LastCheckSpelledMeaningWordList(wordList):
    for word in wordList:
        if not wordnet.synsets(word):
            wordList.remove(word)
            print(word+" kelimesi anlamlı bir kelime olmadığı için SpelledMeaningWordList listesinden silindi.")
    return wordList



#topCount=100
#params = [topCount]
#cursor.execute("EXEC GetMeaningWords_TopCount ?",params)
#meaningWordList = cursor.fetchall()
#spelledMeaningWordListTemp=SpellWord(meaningWordList)
#spelledMeaningWordList=LastCheckSpelledMeaningWordList(spelledMeaningWordListTemp)
#print(spelledMeaningWordList)

def FindSynonymsWordsGivenParameterWord(word):
    SynonymsWordList=[]
    for syn in wordnet.synsets(word):
	                for l in syn.lemmas():
                          if l.name() !=word:
                              SynonymsWordList.append(l.name())
    return SynonymsWordList

def FindWordSynonymsAndSaveDB(word):
    sourceTopicList=FindSynonymsWordsGivenParameterWord("sport")
    synonymsWordList=FindSynonymsWordsGivenParameterWord(word)
    for synonymsWord in synonymsWordList:
        for sourceTopic in sourceTopicList:
            similarityRate=SequenceMatcherSimilarity.SimilarityRate(synonymsWord,sourceTopic)
            totalSimilarityRate+=similarityRate
        averageSmilarityRate=GetAverageSimilarityRate(totalSimilarityRate,len(sourceTopicList))
        if averageSmilarityRate>=thresholdRateForSimilarity:
            SQLCommand = ("EXEC InsertEnglishDictionary ?")
            Values = [l.name()]
            cursor.execute(SQLCommand,Values)
            connection.commit()
            print(synonymsWord +" kelimesi " + word +" kelimesi ile benzer olduğu için sözlüğe eklendi.")
        else:
            print(synonymsWord +" kelimesi " + word +" kelimesi ile benzer olmadığı için sözlüğe eklenmedi.")
thresholdCountOfSelectingWord=100

def GetWordList():
    SQLCommand = ("SELECT top(?) Word From Words (nolock)")
    Values = [thresholdCountOfSelectingWord]
    cursor.execute(SQLCommand,Values)
    wordList = cursor.fetchall()
    return wordList

#path= "C:\\Users\AT012337\\Thesis\\Konu Tespiti\\SmallWord Eğitim Verileri\\"
#sortlist = sorted(os.listdir(path)) 
#i = 0
#dna = open(path + "\\" + sortlist[i],encoding='utf8',errors='ignore')
#soup = BeautifulSoup(dna)
#html_str = '''
#<td><a href="http://www.fakewebsite.com">Please can you strip me?</a>
#<br/><a href="http://www.fakewebsite.com">I am waiting....</a>
#</td>
#'''
#soup = BeautifulSoup(html_str)

#print(soup.get_text())

# Python program to print 
# colored text and background 
#class colors: 
#	reset='\033[0m'
#	bold='\033[01m'
#	disable='\033[02m'
#	underline='\033[04m'
#	reverse='\033[07m'
#	strikethrough='\033[09m'
#	invisible='\033[08m'
#	class fg: 
#		black='\033[30m'
#		red='\033[31m'
#		green='\033[32m'
#		orange='\033[33m'
#		blue='\033[34m'
#		purple='\033[35m'
#		cyan='\033[36m'
#		lightgrey='\033[37m'
#		darkgrey='\033[90m'
#		lightred='\033[91m'
#		lightgreen='\033[92m'
#		yellow='\033[93m'
#		lightblue='\033[94m'
#		pink='\033[95m'
#		lightcyan='\033[96m'
#	class bg: 
#		black='\033[40m'
#		red='\033[41m'
#		green='\033[42m'
#		orange='\033[43m'
#		blue='\033[44m'
#		purple='\033[45m'
#		cyan='\033[46m'
#		lightgrey='\033[47m'

#print(colors.bg.green, "SKk", colors.fg.red, "Amartya") 
#print(colors.bg.lightgrey, "SKk", colors.fg.red, "Amartya") 


#import colorama
#from colorama import Fore, Back, Style
#colorama.init()

## Set the color semi-permanently
#print(Fore.CYAN)
#print("Text will continue to be cyan")
#print("until it is reset or changed")
#print(Style.RESET_ALL)

## Colorize a single line and then reset
#print(Fore.RED + 'You can colorize a single line.' + Style.RESET_ALL)

## Colorize a single word in the output
#print('Or a single ' + Back.GREEN + 'words' + Style.RESET_ALL + ' can be highlighted')

## Combine foreground and background color
#print(Fore.BLUE + Back.WHITE)
#print('Foreground, background, and styles can be combined')
#print("==========            ")

#print(Style.RESET_ALL)
#print('If unsure, reset everything back to normal.')


#import colorama
#from colorama import Fore, Back, Style
#colorama.init()
#print(Fore.MAGENTA + 'some red text')
#print(Fore.GREEN + 'some green text')
#print(Back.LIGHTYELLOW_EX + 'and with a green background')
#print(Style.DIM)
#print(Style.RESET_ALL)
#print('back to normal now')

#str="ahmetoprak63"
#print (len(str))


#print (Simhash('aa').distance(Simhash('aa')))
#print (Simhash('bb').distance(Simhash('bb')))


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

#print('%x' % Simhash(get_features('How are you? I am fine. Thanks.'))).value
#print ('%x' % Simhash(get_features('How are u? I am fine.     Thanks.'))).value
#print ('%x' % Simhash(get_features('How r you?I    am fine. Thanks.'))).value

#from math import factorial

#def calculate_combinations(n, r):
#    return factorial(n) // factorial(r) // factorial(n-r)

#s = 3,51111111111111
#t = 1

#print(s ** t) # 0,2848101265822786‬

import math
import jieba
#import jieba.analyse

class SimHash(object):

    def __init__(self):
        pass
    def getBinStr(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)

    def getWeight(self, source):
        # fake weight with keyword
        return ord(source)
    def unwrap_weight(self, arr):
        ret = ""
        for item in arr:
            tmp = 0
            if int(item) > 0:
                tmp = 1
            ret += str(tmp)
        return ret

    def simHash(self, rawstr):
        seg = jieba.cut(rawstr)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=100, withWeight=True)
        ret = []
        for keyword, weight in keywords:
            binstr = self.getBinStr(keyword)
            keylist = []
            for c in binstr:
                weight = math.ceil(weight)
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        # Reducing Dimensions of Lists
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def getDistince(self, hashstr1, hashstr2):
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                length += 1
        return length


#simhash = SimHash()
#s1 = u'I am very happy'
#s2 = u'I am very happu'

#hash1 = simhash.simHash(s1)
#hash2 = simhash.simHash(s2)
#distince = simhash.getDistince(hash1, hash2)
#value = 5
#Print ("Heming Distance:", "distince," "Judgment Distance:", "Value," "Similarity:", "distince<=value")

from simhash import Simhash
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
def tokenize(sequence):
    words = word_tokenize(sequence)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    return filtered_words
#q1 = "How can I be a good geologist?"
#q2 = "What should I do to be a great geologist?"
#print('Tokenize simhash:', Simhash(tokenize(q1)).distance(Simhash(tokenize(q2))))

