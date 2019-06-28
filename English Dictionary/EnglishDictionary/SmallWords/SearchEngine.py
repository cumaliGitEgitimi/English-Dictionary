from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
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
import numpy as np
import itertools
import requests
import math
import datetime
import pprint
#from py_bing_search import PyBingWebSearch
import colorama
from colorama import Fore, Back, Style
#from yahoo.search.news import NewsSearch
##from yahoo import search
from googleapiclient.discovery import build


colorama.init()


connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1') 

cursor = connection.cursor() 



bing_search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
bing_subscription_key='806fdf38921049c29a2e0d808a1b202c'
google_subscription_key='AIzaSyBADosD5gBwXNLbYyaNAnksXBdK-EpcUZI'
yandex_subscription_key='03.890658727:72bf605f47cc23c006e1a040451201fe'

my_cse_id = "017576662512468239146:omuauf_lfve"
search_term="football"
headers = {"Ocp-Apim-Subscription-Key" : bing_subscription_key,"mkt":"en-US"}
webSearchSaveAndRemoveDirectory = "C:\\Users\AT012337\\Thesis\\SearchEngineDocuments\\Google\\"


def google_search(search_term, api_key, cse_id):
    service = build("customsearch", "v1", developerKey=api_key)
    resultItems = service.cse().list(q=search_term, cx=cse_id,lr="lang_en",num=3,hl="en").execute().get('items', [])
    for page in resultItems:
        page_url = page['link']
        try:
           SaveDocumentGivenURL(page_url)
        except Exception as e:
            print(Fore.RED + "Hata Oluştu: "+ str(e))



def BingSearch(search_term,includeParameter):
    if includeParameter==True:
        if search_term!=Topic:
           search_term += " " + Topic
        if search_term=="":
            search_term=Topic
        search_term += " language:en"

    print(Fore.LIGHTCYAN_EX +"Arama yapılacak kelime : "+ search_term)
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML",
               "mkt":"en-US"}
    try:
      response = requests.get(bing_search_url, headers=headers, params=params,timeout=7)
      response.raise_for_status()
      for page in response.json()['webPages']['value']:
        page_url = page['url']
        SaveDocumentGivenURL(page_url)
    except:
       pass


def SaveDocumentGivenURL(page_url):
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
    except Exception as e:
        print(Fore.RED + "Hata Oluştu: "+ str(e))


def YandexSearch():
    adress="https://yandex.com/search/xml?l10n=en&user=uid-p6s6huhs&key=03.890658727:72bf605f47cc23c006e1a040451201fe"
    yandex_params  = {"query": search_term}
    try:
     response = requests.get(adress, headers=headers, params=yandex_params,timeout=7)
     response.raise_for_status()
     soup = BeautifulSoup(response.text)
     paragraphs = soup.find_all("hlword")
     divs = soup.find_all("passage")
     texts = soup.find_all("text")
     #for page in response.json()['webPages']['value']:
     #  page_url = page['url']
     #  SaveDocumentGivenURL(page_url)
    except:
       pass



#YandexSearch()