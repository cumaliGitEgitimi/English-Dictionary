import EducationData
import WebSearch 
import os
import time
import pypyodbc
import colorama
from colorama import Fore, Back, Style


colorama.init()

connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1') 

cursor = connection.cursor() 
path="C:\\Users\AT012337\\EnglishDictionary\\Documents\\"
thresholdEnglishDictionaryCountForStopProject=25

def CountDirectoryItems():
        list = os.listdir(path)
        number_files = len(list)
       
        if number_files==0:
             print("Not found.Please fill path with .txt files")
        return number_files

def CheckParameters():
     sortlist = sorted(os.listdir(path))
     if len(sortlist)==0:
        print("Not found.Please fill path with .txt files")
        return
     WebSearch.Topic.sourceTopic=sortlist[0].split("_")[1]
     EducationData.Topic.sourceTopic=sortlist[0].split("_")[1]
     EducationData.MeaningfulWordsSelectionType.type=0
     # 0: tf-idf 
     # 1: Helmholtz
     EducationData.UsePMI.value=False 
     # Bu değer (True) olarak verilirse EducationData.MeaningfulWordsSelectionType.type değeri 0 ve 1 dışında bir değer verilmelidir. Aksi taktirde farklı kaydet metodları aynı anda çalışır.
   
     



def GetWordCountOfEnglishDictionary():
    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock)")             
    result_set = cursor.fetchall()
    number_of_rows_EnglishDictionary = result_set[0][0]
    return number_of_rows_EnglishDictionary


def RunProjectCountOfEnglishDictionary():
    CheckParameters()
    EducationData.TruncateEnglishDictionaryTable()
    while(GetWordCountOfEnglishDictionary()<thresholdEnglishDictionaryCountForStopProject):
        EducationData.RunEducationDataProject()
        WebSearch.WebSearch()
    EducationData.findTheSuccessOfTheProject()

RunProjectCountOfEnglishDictionary()
