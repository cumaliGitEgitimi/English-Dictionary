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
import requests
import re
import urllib
from string import punctuation
import datetime
import EducationData
import colorama
from colorama import Fore, Back, Style


colorama.init()


subscription_key='806fdf38921049c29a2e0d808a1b202c'
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key" : subscription_key,"mkt":"en-US"}
webSearchSaveAndRemoveDirectory = "C:\\Users\AT012337\\EnglishDictionary\Documents\\"
percentageOfSelectingMeaningWord=10
thresholdCountOfDocumentsOnPath=2
thresholdEnglishDictionaryCountForStopProject=25
#prefix_Search_term="Computer Science"
prefix_Search_term=""
number_of_results_to_return_in_the_response=2
parameter_specifies_the_number_of_results_to_skip=0



connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1')
cursor = connection.cursor() 


def WebSearch():
    a=datetime.datetime.now()
    print(Fore.LIGHTBLUE_EX +"Web aramasına başlanıyor.", a)
    RemoveAllItemsFromFolder()
    result_set=GetMeaningWordForWebSearch()
    number_of_rows_MeaningWords = len(result_set)
    if number_of_rows_MeaningWords > 0:
        searchTerm=""
        for row in result_set:
            searchTerm+=row[0]+" "
        if GetCountOfDocumentsOnPath()<thresholdCountOfDocumentsOnPath and GetWordCountOfEnglishDictionary()<thresholdEnglishDictionaryCountForStopProject:
            searchAndSaveToFile(searchTerm,True)
    else:
        searchAndSaveToFile(prefix_Search_term,True)
    b=datetime.datetime.now()
    print(Fore.MAGENTA +"Web araması süresi " ,b-a)
                 
             
def GetCountOfDocumentsOnPath():
     sortlist = sorted(os.listdir(webSearchSaveAndRemoveDirectory))
     return len(sortlist)



def GetWordCountOfEnglishDictionary():
    #LastCheckEnglishDictionary()
    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock)")
    result_set = cursor.fetchall()
    number_of_rows_EnglishDictionary = result_set[0][0]     
    return number_of_rows_EnglishDictionary



def LastCheckEnglishDictionary():
    SQLCommand = ("select OriginalWord from SmallWordsEducation.dbo.EnglishDictionary e(nolock) inner join SmallWordsEducation.dbo.OriginalWords o(nolock) on e.Word=o.StemWord")
    cursor.execute(SQLCommand)
    englishDictionaryWordList = cursor.fetchall()
    if len(englishDictionaryWordList)>0:
        english_vocab = set(word.lower() for word in nltk.corpus.words.words())
        for englishDictionaryWord in englishDictionaryWordList:
            result=englishDictionaryWord in english_vocab
            if result==False:
                SQLCommand = ("DELETE FROM [SmallWordsEducation].[dbo].[EnglishDictionary] WHERE Word=?")
                Values = [englishDictionaryWord[0]]
                cursor.execute(SQLCommand,Values)  
                connection.commit() 
                print(Fore.RED + englishDictionaryWord[0]+" kelimesi anlamlı bir kelime olmadığı için EnglishDictionary tablosundan silindi.")
            
def RemoveAllItemsFromFolder():
    for root, dirs, files in os.walk(webSearchSaveAndRemoveDirectory):
      for f in files:
        os.unlink(os.path.join(root, f))
      for d in dirs:
        shutil.rmtree(os.path.join(root, d))
    print(Fore.YELLOW +"Path temizlendi.")


def GetMeaningWordForWebSearch():
    cursor.execute("select OriginalWord from SmallWordsEducation.dbo.EnglishDictionaryTemp e(nolock) inner join SmallWordsEducation.dbo.OriginalWords o(nolock) on e.Word=o.StemWord")
    joined_Result=cursor.fetchall()
    if len(joined_Result)>0:
        return joined_Result
    else:
        cursor.execute("select Word from SmallWordsEducation.dbo.EnglishDictionaryTemp e(nolock)")
        result=cursor.fetchall()
        return result

def GetFinalizeSearchTerm(search_term,includeParameter):
    if includeParameter==True:
        if search_term!=Topic.sourceTopic:
           search_term += " " + Topic.sourceTopic
        if search_term=="":
            search_term=Topic.sourceTopic
        search_term += " language:en"
    return search_term


def getMeaningWordForWebSearching():
     cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionaryTemp] (nolock)")
     result_set = cursor.fetchall()
     number_of_rows_MeaningWords = result_set[0][0]
     topCount=CalculateParameterMeaningValueCount(number_of_rows_MeaningWords)
     if topCount<=0:
            topCount=1
     cursor.execute("select top(?) OriginalWord from SmallWordsEducation.dbo.EnglishDictionaryTemp e(nolock) inner join SmallWordsEducation.dbo.OriginalWords o(nolock) on e.Word=o.StemWord Order By e.Id desc", [topCount])
     joined_Result=cursor.fetchall()
     if len(joined_Result)>0:
             return joined_Result
     else:
         cursor.execute("select top(?) Word from SmallWordsEducation.dbo.EnglishDictionaryTemp e(nolock)", [topCount])
         result=cursor.fetchall()
         return result

def CalculateParameterMeaningValueCount(meaningWordsCount):
    result= int((percentageOfSelectingMeaningWord/100)*meaningWordsCount)
    return result

class Topic:
    sourceTopic = "base"

def searchAndSaveToFile(search_term,includeParameter):
    search_term=GetFinalizeSearchTerm(search_term,includeParameter)
    print(Fore.LIGHTCYAN_EX +"Arama yapılacak kelime : "+ search_term)
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML",
               #"count":number_of_results_to_return_in_the_response,
               #"offset":parameter_specifies_the_number_of_results_to_skip,
               "mkt":"en-US"}
    try:
      response = requests.get(search_url, headers=headers, params=params,timeout=7)
      response.raise_for_status()
      for page in response.json()['webPages']['value']:
        page_url = page['url']
        try:
            page_response = requests.get(page_url,headers=headers, params=params,timeout=10)
            soup = BeautifulSoup(page_response.content)
            paragraphs = soup.find_all("p")
            customFileName=re.sub(r'\W+', '', search_term.split(" ", 1)[0] + "_"+page_url) + '.txt'
            cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[SearchedDocuments] (nolock) where DocumentName=?",[customFileName])
            result_set = cursor.fetchall()
            number_of_rows_SearchedDocuments = result_set[0][0]
            if len(paragraphs)>0 and number_of_rows_SearchedDocuments==0:
                file_name = re.sub(r'\W+', '', search_term.split(" ", 1)[0] + "_"+page_url) + '.txt'
                file_name = webSearchSaveAndRemoveDirectory+file_name
                f = open(file_name, "w")
                f.write(str(page_response.content))
                f.close()

                SQLCommand = ("EXEC InsertSearchedDocuments ?")
                Values = [customFileName]
                cursor.execute(SQLCommand,Values)    
                connection.commit()
                if GetCountOfDocumentsOnPath()<number_of_results_to_return_in_the_response:
                    searchAndSaveToFile(search_term,False)
                print(Fore.LIGHTYELLOW_EX +search_term +" kelimesi için Web araması tamamlandı.")
                return
        except:
            pass
    except:
       pass
