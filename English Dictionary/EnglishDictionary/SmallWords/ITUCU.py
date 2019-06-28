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
import WordnetSimilarity
import SequenceMatcherSimilarity
from nltk.corpus import wordnet
from nltk.corpus import words
import WebSearch
import datetime
from autocorrect import spell
import math
from nltk import wordpunct_tokenize
import colorama
from colorama import Fore, Back, Style
import EducationData


colorama.init()



connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1') 

cursor = connection.cursor() 

Topic="science software"


thresholdEnglishDictionaryCountForStopProject=100

def GetWordCountOfEnglishDictionary():
    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock)")
    result_set = cursor.fetchall()
    number_of_rows_EnglishDictionary = result_set[0][0]
    return number_of_rows_EnglishDictionary

def CheckIsFirstDocument():
    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[SearchedDocuments] (nolock)")
    result_set = cursor.fetchall()
    number_of_rows_SearchedDocuments = result_set[0][0]
    if number_of_rows_SearchedDocuments==0:
        return True
    else:
        return False

def EnglishDictionaryCount():
    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock)")
    result_set = cursor.fetchall()
    number_of_rows_MeaningWord = result_set[0][0]
    return number_of_rows_MeaningWord


def RunProjectCountOfEnglishDictionary():
    if EnglishDictionaryCount()==0 and CheckIsFirstDocument()==True:
            WebSearch.searchAndSaveToFile(Topic)
    if GetWordCountOfEnglishDictionary()<thresholdEnglishDictionaryCountForStopProject:
        while(GetWordCountOfEnglishDictionary()<thresholdEnglishDictionaryCountForStopProject):
            EducationData.RunEducationDataProject()
            WebSearch.WebSearch()
        EducationData.findTheSuccessOfTheProject()

RunProjectCountOfEnglishDictionary()