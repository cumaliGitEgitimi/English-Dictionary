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
import PMI
from math import factorial


colorama.init()



connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                'uid=PhytonThesisUser;pwd=1') 

cursor = connection.cursor() 

tallyTableCount=10000
RemovingfolderPath= "C:\\Users\AT012337\\EnglishDictionary\\Documents\\"
min_MeaningValue=0.3
max_MeaningValue=0.7
max_TopCount=5
meaningWords_TopCount=2
thresholdRateForSimilarity=0.1
useWordnetSimilarity=1
percentageOfSelectingMeaningWord=50
backupPath="C:\\Users\AT012337\\EnglishDictionary\\DocumentsBackup\\"
topCountForBackupPath=3
backupWebSearchWordlist = ["football", "sport", "spor", "ronaldinho", "ball", "faul","spor","foot","captain","el classicco"]
count_Paragraph_Threshold=100
sum_Count_Threshold=100
thresholdCountOfEnglishDictionaryInsert=20
thresholdCountOfSelectingWord=300
parameterMeaningValueCountIfListEmpty=2
thresholdTF_IDFValue=0.03
topCountTFIDF=2
thresholdEnglishDictionaryTempTableInsert=2
thresholdWordCountPerDocument=20

def TruncateSelectedDatabase():
    SQLCommand = ("EXEC TruncateSelectedDatabase")
    cursor.execute(SQLCommand)
    connection.commit() 

class Topic:
    sourceTopic = ""

class MeaningfulWordsSelectionType:
    type=0

class UsePMI:
    value=False

def OpenConnection():

    connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1') 

    cursor = connection.cursor() 


def InsertTallyTable():
    SQLCommand = ("EXEC InsertTally ?")
    Values = [tallyTableCount]
    cursor.execute(SQLCommand,Values)
    connection.commit()
    print(Fore.MAGENTA + 'Tally tablosu dolduruldu.')


def TruncateAllDatabase():
    SQLCommand = ("EXEC TruncateAllDatabase")
    cursor.execute(SQLCommand)
    connection.commit()
    print(Fore.CYAN + 'Tüm tablolar Truncate edildi.')

def findTheSuccessOfTheProject():
    totalSimilarityRate=GetTotalSimilarityRate()
    print(Fore.LIGHTBLUE_EX +"Projenin başarı oranı % : ",totalSimilarityRate*100)

def CheckIsFirstDocument():
    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[SearchedDocuments] (nolock)")
    result_set = cursor.fetchall()
    number_of_rows_SearchedDocuments = result_set[0][0]
    if number_of_rows_SearchedDocuments==0:
        return True
    else:
        return False

def SaveTFIDFMeaningWordsToDB():
    TruncateEnglishDictionaryTempTable()
    meaningWordList=GetTFIDFWordsTopCount()
    if len(meaningWordList)>0:
        for meaningWord in meaningWordList:
            cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock) where Word=?",[meaningWord[0]])
            result_set = cursor.fetchall()
            number_of_rows_MeaningWord = result_set[0][0]
            if number_of_rows_MeaningWord ==0:
                InsertEnglishDictionary(meaningWord[0])
                InsertEnglishDictionaryTemp(meaningWord[0])
            else:
                print(Fore.RED + maxLevelMeaningWord +" kelimesi sözlükte olduğu için tekrar eklenmedi.")


def SaveTFIDFMeaningWordsToDB1(): 
    #cursor.execute("SELECT Word FROM [SmallWordsEducation].[dbo].[TFIDFWords] (nolock)")
    #tfIDFWordList = cursor.fetchall()
    #spelledTFIDFWordList=SpellWord(tfIDFWordList)
    #LastCheckMeaningWords(spelledTFIDFWordList,True)
    maxLevelMeaningWord=GetMaxLevelMeaningWord()
    originalWord=GetOriginalWord(maxLevelMeaningWord)
    isFirstDocument=CheckIsFirstDocument()

    #if isFirstDocument==False:
    if len(maxLevelMeaningWord)>0:
        TruncateMeaningWordsTable()
        cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock) where Word=?",[maxLevelMeaningWord])
        result_set = cursor.fetchall()
        number_of_rows_MeaningWord = result_set[0][0]
        if number_of_rows_MeaningWord ==0:
            InsertEnglishDictionary(maxLevelMeaningWord)
            #synonymsWordList=FindSynonymsWordsGivenParameterWord(originalWord)
            #if len(synonymsWordList)>0:
            #    i=0
            #    for synonymsWord in synonymsWordList:
            #        if i<2:
            #            InsertEnglishDictionary(synonymsWord)
            #            print(synonymsWord +" kelimesi " + maxLevelMeaningWord +" kelimesi ile benzer olduğu için sözlüğe eklendi.")
            #            i+=1
        else:
            print(Fore.RED + maxLevelMeaningWord +" kelimesi sözlükte olduğu için tekrar eklenmedi.")
    else:
        cursor.execute("EXEC GetEnglishDictionaryTemp")
        englishDictionaryTempWord= cursor.fetchall()
        if len(englishDictionaryTempWord)>0:
            synonymsWordList=FindSynonymsWordsGivenParameterWord(englishDictionaryTempWord[0][0])
            if len(synonymsWordList)>0:
                InsertEnglishDictionaryTemp(synonymsWordList[0])
                InsertOriginalWords(synonymsWordList[0],synonymsWordList[0])
                print(Fore.RED + "TFIDFWords tablosundaki hiç bir kelimenin TF değeri "+ str(thresholdTF_IDFValue)+" değerinden yüksek olmadığı için "+ englishDictionaryTempWord[0][0]+ " kelimesinin synonyms kelimesi temp sözlüğe eklendi ve tekrar web araması yapılacak. Temp sözlüğe eklenen synonyms kelime : "+ synonymsWordList[0])
        return


    #else:
    #    print("Fore.LIGHTBLUE_EX + İlk doküman olduğu için Sözlüğe "+ str(topCountTFIDF)+" adet kayıt eklenecektir.")
    #    meaningWordList=GetParameterTopCountMeaningWord()
    #    for meaningWord in meaningWordList:
    #        cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock) where Word=?",[meaningWord[0]])
    #        result_set = cursor.fetchall()
    #        number_of_rows_MeaningWord = result_set[0][0]
    #        if number_of_rows_MeaningWord ==0:
    #            SQLCommand = ("EXEC InsertEnglishDictionary ?")
    #            Values = [meaningWord[0]]
    #            cursor.execute(SQLCommand,Values)
    #            connection.commit
    #            print(meaningWord[0] +" kelimesi sözlüğe eklendi.")
    #            #synonymsWordList=FindSynonymsWordsGivenParameterWord(meaningWord[0])
    #            #if len(synonymsWordList)>0:
    #            #    i=0
    #            #    for synonymsWord in synonymsWordList:
    #            #        if i<2:
    #            #            InsertEnglishDictionary(synonymsWord)
    #            #            print(synonymsWord +" kelimesi " + meaningWord[0] +" kelimesi ile benzer olduğu için sözlüğe eklendi.")
    #            #            i+=1
    #        else:
    #            print(meaningWord[0] +" kelimesi sözlükte olduğu için tekrar eklenmedi.")


    InsertEnglishDictionaryTemp(maxLevelMeaningWord)
    InsertOriginalWords(maxLevelMeaningWord,maxLevelMeaningWord)
    #synonymsWordList=FindSynonymsWordsGivenParameterWord(maxLevelMeaningWord)
    #if len(synonymsWordList)>0:
    #        InsertEnglishDictionaryTemp(synonymsWordList[0])
    #        InsertOriginalWords(synonymsWordList[0],synonymsWordList[0])


    #cursor.execute("EXEC GetTFIDFWords ?",[thresholdTF_IDFValue])
    ##cursor.execute("EXEC GetTFIDFWordsAverageCalculationResult")
    #meaningWordList = cursor.fetchall()
    #cursor.execute("EXEC GetEnglishDictionary")
    #englishDictionaryWordList = cursor.fetchall()
    #if len(meaningWordList)>thresholdEnglishDictionaryTempTableInsert:
    #    listofTuples=[]
    #    default_data={}
    #    if len(englishDictionaryWordList)>0:
    #        for meaningWord in meaningWordList:
    #            totalSimilarityRate=0
    #            for englishDictionaryWord in englishDictionaryWordList:
    #                similarityRate=SequenceMatcherSimilarity.SimilarityRate(meaningWord[0],englishDictionaryWord[0])
    #                totalSimilarityRate+=similarityRate
    #            averageSmilarityRate=GetAverageSimilarityRate(totalSimilarityRate,len(englishDictionaryWordList))
    #            default_data[meaningWord[0]] = averageSmilarityRate
    #    listofTuples = sorted(default_data.items() , reverse=True, key=lambda x: x[1])
    #    i=1  
    #    for meaningWord in listofTuples:
    #        if i<=thresholdEnglishDictionaryTempTableInsert:
    #            InsertEnglishDictionaryTemp(meaningWord[0])
    #            i+=1

    #else:
    #    if len(meaningWordList)>0:
    #        for meaningWord in meaningWordList:
    #            InsertEnglishDictionaryTemp(meaningWord[0])
    #        synonymsWordList=FindSynonymsWordsGivenParameterWord(originalWord)
    #        if len(synonymsWordList)>0:
    #            totalItemCount=len(meaningWordList)+len(synonymsWordList)
    #            if totalItemCount<=thresholdEnglishDictionaryTempTableInsert:
    #                for synonymsWord in synonymsWordList:
    #                    InsertEnglishDictionaryTemp(synonymsWord)
    #                    InsertOriginalWords(synonymsWord,synonymsWord)
    #            else:
    #                count=thresholdEnglishDictionaryTempTableInsert-len(meaningWordList)
    #                for synonymsWord in synonymsWordList:
    #                    if count>0:
    #                        InsertEnglishDictionaryTemp(synonymsWord)
    #                        InsertOriginalWords(synonymsWord,synonymsWord)
    #                        count-=1
    #    else:
    #        print("TFIDFWords tablosundaki hiç bir kelimenin TF_IDF değeri "+ str(thresholdTF_IDFValue)+" değerinden yüksek olmadığı için Synonyms kelimeler Temp tabloya atılacak.")
    #        for synonymsWord in synonymsWordList:
    #                    InsertEnglishDictionaryTemp(synonymsWord)
    #                    InsertOriginalWords(synonymsWord,synonymsWord)


      
                        
def InsertOriginalWords(stemWord,originalWord):
    SQLCommand = ("EXEC InsertOriginalWords ?,?")
    Values = [stemWord,originalWord]
    cursor.execute(SQLCommand,Values)  
    connection.commit()


def InsertEnglishDictionary(meaningWord):
    SQLCommand = ("EXEC InsertEnglishDictionary ?")
    Values = [meaningWord]
    cursor.execute(SQLCommand,Values)
    connection.commit
    print(Fore.GREEN + meaningWord +" kelimesi sözlüğe eklendi.")

def InsertEnglishDictionaryTemp(meaningWord):
    SQLCommand = ("EXEC InsertEnglishDictionaryTemp ?")
    Values = [meaningWord]
    cursor.execute(SQLCommand,Values)
    connection.commit
    print(Fore.GREEN + meaningWord +" kelimesi temp sözlüğe eklendi.")


def GetMaxLevelMeaningWord():
    cursor.execute("EXEC GetMaxLevelMeaningWord ?",[thresholdTF_IDFValue])
    meaningWord = cursor.fetchall()
    if len(meaningWord)==0:
        print(Fore.GREEN + "TFIDFWords tablosundaki tüm kayıtlar tabloya eklendi.")
        return meaningWord
    else:
        return meaningWord[0][0]

def GetOriginalWord(word):
    if len(word)>0:
        cursor.execute("EXEC GetOriginalWord ?",[word])
        originalWord = cursor.fetchall()
        if len(originalWord)==0:
            return word
        else:
            return originalWord[0][0]


def GetParameterTopCountMeaningWord():
    cursor.execute("EXEC GetParameterTopCountMeaningWord ?",[topCountTFIDF])
    meaningWordList = cursor.fetchall()
    return meaningWordList


def GetMeaningWordsCount():

    cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[MeaningWord] (nolock)")
    result_set = cursor.fetchall()
    number_of_rows_MeaningWords = result_set[0][0]
    return number_of_rows_MeaningWords



def CheckSimilarityAndSaveDB():
     cursor.execute("EXEC GetEnglishDictionary")
     englishDictionaryWordList = cursor.fetchall()
     number_of_rows_MeaningWords = GetMeaningWordsCount()
     topCount=CalculateParameterMeaningValueCount(number_of_rows_MeaningWords)
     params = [topCount]
     cursor.execute("EXEC GetMeaningWords_TopCount ?",params)
     meaningWordList = cursor.fetchall()
     spelledMeaningWordListTemp=SpellWord(meaningWordList)
     spelledMeaningWordList=LastCheckSpelledMeaningWordList(spelledMeaningWordListTemp)
     count=0
     TruncateMeaningWordsTable()
     if len(englishDictionaryWordList)>0:
            for meaningWord in spelledMeaningWordList:
                totalSimilarityRate=0
                for englishDictionaryWord in englishDictionaryWordList:
                    similarityRate=SequenceMatcherSimilarity.SimilarityRate(meaningWord,englishDictionaryWord[0])
                    totalSimilarityRate+=similarityRate
                averageSmilarityRate=GetAverageSimilarityRate(totalSimilarityRate,len(englishDictionaryWordList))
                if averageSmilarityRate>=thresholdRateForSimilarity:
                    try:
                        SQLCommand = ("EXEC InsertEnglishDictionary ?")
                        Values = [meaningWord]
                        cursor.execute(SQLCommand,Values)
                        connection.commit()
                        count+=1
                        print(Fore.GREEN + meaningWord +" kelimesi threshold değerinden yüksek olduğu için sözlüğe eklendi.")

                        
                        #FindWordSynonymsAndSaveDB(meaningWord)
                        #print(Fore.CYAN + meaningWord +" kelimesi için Synonyms kelimeler bulundu.")

                        SQLCommand = ("EXEC InsertEnglishDictionaryTemp ?")
                        Values = [meaningWord]
                        cursor.execute(SQLCommand,Values)
                        connection.commit()
                        print(Fore.GREEN + meaningWord +" kelimesi Temp sözlüğe eklendi.")

                    except:
                        pass
     else:
          print(Fore.LIGHTWHITE_EX + "Sözlük boş olduğu için Anlamlı kelimelerin kaynak topic ile benzerlikleri karşılaştırılacak.")
          for meaningWord in spelledMeaningWordList:
              try:
                  similarityRate=SequenceMatcherSimilarity.SimilarityRate(meaningWord,Topic.sourceTopic)
                  if similarityRate>thresholdRateForSimilarity:
                      SQLCommand = ("EXEC InsertEnglishDictionary ?")
                      Values = [meaningWord]
                      cursor.execute(SQLCommand,Values)
                      connection.commit()
                      count+=1
                      print(Fore.GREEN + meaningWord +" kelimesi threshold değerinden yüksek olduğu için sözlüğe eklendi.")

                      #FindWordSynonymsAndSaveDB(meaningWord)
                      #print(Fore.CYAN + meaningWord +" kelimesi için Synonyms kelimer bulundu.")

                      SQLCommand = ("EXEC InsertEnglishDictionaryTemp ?")
                      Values = [meaningWord]
                      cursor.execute(SQLCommand,Values)
                      connection.commit()
                      print(Fore.GREEN + meaningWord +" kelimesi Temp sözlüğe eklendi.")
              except:
                  pass
     

def GetWordList():
    Values = [thresholdCountOfSelectingWord]
    cursor.execute("EXEC GetWords_TopCount ?",Values)
    wordList = cursor.fetchall()
    return wordList

def LastCheckSpelledMeaningWordList(wordList):
    start=datetime.datetime.now()
    if len(wordList)==0:
        print(Fore.RED + "Anlamlı kelime listesi boş.")
    for word in wordList:
        if not wordnet.synsets(word):
            wordList.remove(word)
            print(Fore.RED + word+" kelimesi anlamlı bir kelime olmadığı için SpelledMeaningWordList listesinden silindi.")
    end=datetime.datetime.now()
    print(Fore.BLUE + "LastCheckSpelledMeaningWordList metodu çalışma süresi: ",(end-start))
    return wordList


def LastCheckMeaningWords(spelledWordList,tfIDFWord):
    if tfIDFWord==False:
        english_vocab = set(word.lower() for word in nltk.corpus.words.words())
        for meaningWord in spelledWordList:
            result=meaningWord in english_vocab
            if result==False:
                SQLCommand = ("DELETE FROM [SmallWordsEducation].[dbo].[Words] WHERE Word=?")
                Values = [meaningWord]
                cursor.execute(SQLCommand,Values)  
                connection.commit() 
                print(Fore.RED + meaningWord+" kelimesi anlamlı bir kelime olmadığı için Words tablosundan silindi.")
    else:
        for meaningWord in spelledWordList:
            result=meaningWord in words.words()
            if result==False:
                SQLCommand = ("DELETE FROM [SmallWordsEducation].[dbo].[TFIDFWords] WHERE Word=?")
                Values = [meaningWord]
                cursor.execute(SQLCommand,Values)  
                connection.commit() 
                print(Fore.RED + meaningWord+" kelimesi anlamlı bir kelime olmadığı için TFIDFWords tablosundan silindi.")

 
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




def CalculateParameterMeaningValueCount(meaningWordsCount):
    result=int((percentageOfSelectingMeaningWord/100)*meaningWordsCount)
    if result==0:
        return parameterMeaningValueCountIfListEmpty 
    return result

            
def FillPathIfFolderPathIsEmpty():
     SQLCommand = ("SELECT TOP(?) Word FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock) order by Id desc")
     Values = [topCountForBackupPath]
     cursor.execute(SQLCommand,Values)
     englishDictionaryWordList = cursor.fetchall()
     if len(englishDictionaryWordList)==0:
         for backupWebSearchWord in backupWebSearchWordlist:
             WebSearch.searchAndSaveToFile(backupWebSearchWord,True)
     else :
         for englishDictionaryWord in englishDictionaryWordList:
             WebSearch.searchAndSaveToFile(englishDictionaryWord[0],True)
         

def SpellWord(wordList):
    start=datetime.datetime.now()
    spelledWordList=[]
    if len(wordList)==0:
        print(Fore.RED + "Anlamlı kelime listesi boş.")
    else:
        for word in wordList:
            spelledWordList.append(spell(word[0]))
    end=datetime.datetime.now()
    print(Fore.LIGHTBLUE_EX + "SpellWord metodu çalışma süresi: ",(end-start))
    return spelledWordList


def FindSynonymsWordsGivenParameterWord(word):
    SynonymsWordList=[]
    for syn in wordnet.synsets(word):
	                for l in syn.lemmas():
                          if l.name() !=word:
                              SynonymsWordList.append(l.name())
    uniqueList=unique(SynonymsWordList)
    for synonymsWord in SynonymsWordList:
        if not wordnet.synsets(synonymsWord):
            uniqueList.remove(synonymsWord)
    return uniqueList



def unique(list): 
	unique_list = [] 
	for x in list: 
		if x not in unique_list: 
			unique_list.append(x) 
	return unique_list
	



def FindWordSynonymsAndSaveDB(word):
    sourceTopicList=FindSynonymsWordsGivenParameterWord(Topic.sourceTopic)
    synonymsWordList=FindSynonymsWordsGivenParameterWord(word)
    for synonymsWord in synonymsWordList:
        totalSimilarityRate=0
        for sourceTopic in sourceTopicList:
            similarityRate=SequenceMatcherSimilarity.SimilarityRate(synonymsWord,sourceTopic)
            totalSimilarityRate+=similarityRate
        averageSmilarityRate=GetAverageSimilarityRate(totalSimilarityRate,len(sourceTopicList))
        if averageSmilarityRate>=thresholdRateForSimilarity:
            SQLCommand = ("EXEC InsertEnglishDictionary ?")
            Values = [synonymsWord]
            cursor.execute(SQLCommand,Values)
            connection.commit()
            print(Fore.GREEN + synonymsWord +" kelimesi " + word +" kelimesi ile benzer olduğu için sözlüğe eklendi.")
        else:
            print(Fore.RED + synonymsWord +" kelimesi " + word +" kelimesi ile benzer olmadığı için sözlüğe eklenmedi.")
               
   
             
def DeleteWordsForMeaningWordsCalculation():
    try:
        SQLCommand=("EXEC DeleteWordsForMeaningWordsCalculation ?,?")
        Values = [count_Paragraph_Threshold,sum_Count_Threshold]
        cursor.execute(SQLCommand,Values)  
        connection.commit()
        print(Fore.LIGHTBLUE_EX + "DeleteWordsForMeaningWordsCalculation SP'si başarılı olarak çalıştı.")
    except Exception as e:
        print(Fore.RED + "DeleteWordsForMeaningWordsCalculation SP'sinde hata oluştu. Hata " + str(e))
            
		    
def GetTotalSimilarityRate():
     cursor.execute("EXEC GetEnglishDictionary")
     englishDictionaryWordList = cursor.fetchall()
     cursor.execute("SELECT distinct Word FROM [SmallWordsEducation].[dbo].[EnglishDictionary] (nolock)")
     distinctEnglishDictionaryWordList = cursor.fetchall()
     if len(englishDictionaryWordList) > 0:
         totalSimilarityRate=0
         for englishDictionaryWord in englishDictionaryWordList:
             similarityRate=SequenceMatcherSimilarity.SimilarityRate(Topic.sourceTopic,englishDictionaryWord[0])
             totalSimilarityRate+=similarityRate
         averageSmilarityRate=GetAverageSimilarityRate(totalSimilarityRate,len(englishDictionaryWordList))
         return averageSmilarityRate
     else:
         return 0
        
def TruncateMeaningWordsTable():
    SQLCommand = ("Truncate Table [SmallWordsEducation].[dbo].[MeaningWord]")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateEnglishDictionaryTempTable():
    SQLCommand = ("Truncate Table [SmallWordsEducation].[dbo].[EnglishDictionaryTemp]")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateEnglishDictionaryTable():
    SQLCommand = ("Truncate Table [SmallWordsEducation].[dbo].[EnglishDictionary]")
    cursor.execute(SQLCommand)
    connection.commit()
         
def GetAverageSimilarityRate(totalSimilarityRate,englishDictionaryWord):
    if englishDictionaryWord==0:
        return 0
    else:
        result=totalSimilarityRate/englishDictionaryWord
    return result


def SpellChecker():
    spell = SpellChecker()
    misspelled = spell.unknown(['something', 'is', 'hapenning', 'here'])
    for word in misspelled:
        print(spell.correction(word))


def GetContentFreq(content):
    translator = str.maketrans('', '', string.punctuation)
    words = nltk.word_tokenize(content)
    words = [word.translate(translator) for word in words]
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopwords.words('english')]  
    tempWords = []
    for word in words:
        if word != "" and len(word) > 1:
            tempWords.append((word))
    words = tempWords
    return words

def SeparateWordAndSaveDB():
    counts = dict()
    paraghraphId = 0
    TruncateAllDatabase()
    path=RemovingfolderPath
    sortlist = sorted(os.listdir(path))   
    if len(sortlist)==0:
        print(Fore.RED + path+ " Path'inde doküman kalmadı. Yeni kelimeler ile path dolduruluyor.")
        FillPathIfFolderPathIsEmpty()
        sortlist = sorted(os.listdir(path))
    i = 0
    documentCount=str(len(sortlist))
    print(Fore.LIGHTMAGENTA_EX + path +" Path'inde Toplam "+ documentCount+ " adet doküman var.")
    while(i < len(sortlist)):
        print(Fore.CYAN + str(i)+". sıradaki " + sortlist[i]+ " dokümanı okunmaya başlandı.")
        dna = open(path + "\\" + sortlist[i],encoding='utf8',errors='ignore')
        try:
            soup = BeautifulSoup(dna)
        except Exception as e:
            print(Fore.RED + sortlist[i]+" dokümanında hata oluştu. Hata " + str(e))
        paragraphs = soup.find_all("p")
        paraghraphId = 1
        stemmer = PorterStemmer()
        for element in paragraphs:           
            tokens = GetContentFreq(element.text)
            tagged = pos_tag(tokens)
            nouns = [word for word,pos in tagged \
	            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]	           
            for word in nouns:
                originalWord=word
                stems = stemmer.stem(word)
                try:
                    SQLCommand = ("EXEC InsertOriginalWords ?,?")
                    Values = [stems,originalWord]
                    cursor.execute(SQLCommand,Values)  
                    connection.commit() 
                except Exception as e:
                    print(Fore.RED + "OriginalWords tablosuna insert ederken hata oluştu. Hata :" +str(e))

                if stems in counts.keys():
                    shortest,count = counts[stems]
                    counts[stems] = (shortest,count + 1)
                else:
                    counts[stems] = (stems,1)
            for kok in counts:          
                shortest,count = counts[kok]
                try:
                    if len(shortest)<15:
                        SQLCommand = ("INSERT INTO Words (DocumentId,Word, Count,StemWord,Paragraph)  VALUES (?,?,?,?,?)")
                        Values = [i,shortest,count,kok,paraghraphId]
                        cursor.execute(SQLCommand,Values)  
                        connection.commit() 
                    #else:
                    #    print("Word tablosuna kaydedilmek istenen kelimenin uzunluğu 15 karakterden büyük olduğu için tabloya eklenmedi. Kelime :" + shortest)
                except Exception as e:
                    print(Fore.RED + "Word tablosuna insert ederken oluştu. Hata : "+ str(e))

                    
            counts.clear()
            tokens.clear()
            nouns.clear()
            paraghraphId+=1

            number_of_rows_Words = GetWordsCount(i,False)

        if len(paragraphs)>0 and number_of_rows_Words>0:
            SQLCommand = ("INSERT INTO Documents (Id,DocumentName,Topic,SubTopic)  VALUES (?,?,?,?)")
            Values = [i,sortlist[i],sortlist[i],sortlist[i]]
            cursor.execute(SQLCommand,Values)  
            connection.commit() 
        i+=1
    
def CalculateHelmholtzPrincipleWithSP():
    try:
        SQLCommand = ("EXEC InsertMeaningValue")
        cursor.execute(SQLCommand)
        connection.commit()

        cursor.execute("SELECT StemWord FROM [SmallWordsEducation].[dbo].[MeaningWord] (nolock)")
        meaningWordList = cursor.fetchall()
        print(Fore.LIGHTBLUE_EX + "MeaningWord Listesi : ",meaningWordList)
    except Exception as e:
        print(Fore.RED + "Anlamlı kelimeleri bulurken hata oluştu.Hata : "+str(e))
        print(Fore.LIGHTBLUE_EX + "Bu nedenle DeleteWordsForMeaningWordsCalculation SP'si çalışmaya başladı.")
        DeleteWordsForMeaningWordsCalculation()
        FindMeaningWordsAndSaveDB()
        print(Fore.CYAN + "Anlamlı kelimeler tekrar bulunuyor.")



def CalculateTFIDF():

    SQLCommand = ("EXEC GetTotalDocumentCount")
    cursor.execute(SQLCommand)    
    result = cursor.fetchall()
    totalDocumentCount=result[0][0]
    documentId=0

    SQLCommand = ("EXEC GetDistinctWordList")
    cursor.execute(SQLCommand)
    wordList = cursor.fetchall()

    SQLCommand = ("EXEC GetTotalWordsFrequency")
    cursor.execute(SQLCommand)    
    result = cursor.fetchall()
    totalWordsFrequency = result[0][0]

    for word in wordList:
        SQLCommand = ("EXEC GetTermFrequency ?")
        Values = [word[0]]
        cursor.execute(SQLCommand,Values)
        term = cursor.fetchall()
        termFrequency = term[0][0]

        TF=CalculateTF(termFrequency,totalWordsFrequency)

        SQLCommand = ("EXEC GetDocumentCountOfIncludeTerm ?")
        Values = [word[0]]
        cursor.execute(SQLCommand,Values)    
        document = cursor.fetchall()
        documentCountOfIncludeTerm = len(document)


        IDF=CalculateIDF(documentCountOfIncludeTerm,totalDocumentCount)

        TF_IDF=Calculate_TF_IDF(TF,IDF)

        SQLCommand = ("EXEC InsertTFIDFWords ?,?,?,?,?")
        Values = [documentId,word[0],TF,IDF,TF_IDF]
        cursor.execute(SQLCommand,Values)    
        connection.commit()

def GetD():
    cursor.execute("Select CAST((Select Sum(Count) from Words) AS FLOAT)")
    result_set = cursor.fetchall()
    number_of_rows_Words = result_set[0][0]
    return number_of_rows_Words

def GetP(stemWord,documentId):
    cursor.execute("Select Sum(x.TotalWord) From (Select Sum(COUNT) as TotalWord From Words Where Paragraph in ( Select Distinct Paragraph from Words where StemWord=? and DocumentId=?) group by Paragraph) as x",[stemWord,documentId])
    result_set = cursor.fetchall()
    number_of_rows_Words = result_set[0][0]
    return number_of_rows_Words    

def GetN(D,P):
    return D/P
    
        
def GetWordsCount(documentId,type):
    if type==False:
        cursor.execute("SELECT count(*) FROM [SmallWordsEducation].[dbo].[Words] (nolock) where DocumentId=?",[documentId])
        result_set = cursor.fetchall()
        number_of_rows_Words = result_set[0][0]
        return number_of_rows_Words
    else:
        cursor.execute("SELECT distinct count(*) FROM [SmallWordsEducation].[dbo].[Words] (nolock)")
        result_set = cursor.fetchall()
        number_of_rows_Words = result_set[0][0]
        return number_of_rows_Words

def NewFindMeaningWordsAndSaveDB():

    SQLCommand = ("EXEC GetTotalDocumentCount")
    cursor.execute(SQLCommand)    
    result = cursor.fetchall()
    totalDocumentCount=result[0][0]
    documentId=0


    while(totalDocumentCount>documentId):

        SQLCommand = ("EXEC GetWordListOnDocument ?")
        Values = [documentId]
        cursor.execute(SQLCommand,Values)
        wordList = cursor.fetchall()

        SQLCommand = ("EXEC GetMaxTermOnDocument ?")
        Values = [documentId]
        cursor.execute(SQLCommand,Values)    
        MaxTermOnDocument = cursor.fetchall()
        maxTermCountOnDocument = MaxTermOnDocument[0][1]

        for word in wordList:
            SQLCommand = ("EXEC GetTermCountOnDocument ?,?")
            Values = [documentId,word[0]]
            cursor.execute(SQLCommand,Values)
            term = cursor.fetchall()
            termCountOnDocument = term[0][1]

            TF=CalculateTF(termCountOnDocument,maxTermCountOnDocument)

            SQLCommand = ("EXEC GetDocumentCountOfIncludeTerm ?")
            Values = [word[0]]
            cursor.execute(SQLCommand,Values)    
            document = cursor.fetchall()
            documentCountOfIncludeTerm = len(document)


            IDF=CalculateIDF(documentCountOfIncludeTerm,totalDocumentCount)

            TF_IDF=Calculate_TF_IDF(TF,IDF)

            SQLCommand = ("EXEC InsertTFIDFWords ?,?,?,?,?")
            Values = [documentId,word[0],TF,IDF,TF_IDF]
            cursor.execute(SQLCommand,Values)    
            connection.commit()

        documentId+=1    
    



def CalculateTF(termFrequency,totalWordsFrequency):
    return termFrequency/totalWordsFrequency

def CalculateIDF(documentCountOfIncludeTerm,totalDocumentCount):
    normalizationValue=0
    if documentCountOfIncludeTerm==0:
        documentCountOfIncludeTerm+=1
    if math.log(totalDocumentCount/documentCountOfIncludeTerm)==0:
        normalizationValue=1
    return normalizationValue+math.log(totalDocumentCount/documentCountOfIncludeTerm)

def Calculate_TF_IDF(TF,IDF):
    return TF*IDF

def DeleteMeaningLessWords():
    cursor.execute("SELECT distinct Word FROM [SmallWordsEducation].[dbo].[Words] (nolock)")
    wordList = cursor.fetchall()
    spelledWordList=SpellWord(wordList)
    LastCheckMeaningWords(spelledWordList,False)
    
def SaveHelmholtzMeaningWordToDB(): 
     TruncateEnglishDictionaryTempTable()
     params = [meaningWords_TopCount]
     #cursor.execute("EXEC GetTFIDFWords_TopCount ?",params)
     cursor.execute("EXEC GetMeaningWords_TopCount ?",params)
     meaningWordList = cursor.fetchall()
     for meaningWord in meaningWordList:
         InsertEnglishDictionary(meaningWord[0])
         InsertEnglishDictionaryTemp(meaningWord[0])

def GetTFIDFWordsTopCount():
    cursor.execute("EXEC GetTFIDFWordsTopCount ?,?",[meaningWords_TopCount,thresholdTF_IDFValue])
    meaningWordList = cursor.fetchall()
    return meaningWordList


def SavePMIMeaningWordToDB():
    TruncateEnglishDictionaryTempTable()
    params = [meaningWords_TopCount]
    cursor.execute("EXEC GetTotalPMI ?",params)
    meaningWordList = cursor.fetchall()
    for meaningWord in meaningWordList:
        InsertEnglishDictionary(meaningWord[0])
        InsertEnglishDictionaryTemp(meaningWord[0])

def calculate_combinations(n, r):
    return factorial(n) // factorial(r) // factorial(n-r)

def CalculateHelmholtzPrincipleWithCode():

    SQLCommand = ("EXEC GetTotalDocumentCount")
    cursor.execute(SQLCommand)    
    result = cursor.fetchall()
    totalDocumentCount=result[0][0]
    D=GetD()
    for documentId in range(totalDocumentCount):
        params = [documentId]
        cursor.execute("EXEC GetWordListOnDocument ?",params)    
        wordList = cursor.fetchall()
        for word in wordList:
            cursor.execute("select Count(Paragraph) from Words (nolock) where StemWord=? and DocumentId=?",[word[0],documentId])
            m = cursor.fetchall()
            cursor.execute("select ISNULL(Sum(Count),0) from Words (nolock)  where StemWord=? and DocumentId=?",[word[0],documentId])
            K = cursor.fetchall()            
            P=GetP(word[0],documentId)
            N=GetN(D,P)
            if K[0][0]==0 or m[0][0]==0:
                K[0][0]+=1
                m[0][0]+=1
            combinationValue=calculate_combinations(K[0][0],m[0][0])
            numberOfFalseAlarms= combinationValue * (1/(float(N)**(m[0][0]-1)))
            #meaningValue= math.log(float(numberOfFalseAlarms)) /-m[0][0]
            meaningValue= float(numberOfFalseAlarms) / m[0][0]

            if float(meaningValue)>0 and math.log(float(numberOfFalseAlarms))/-m[0][0]>0:
                SQLCommand = ("INSERT INTO MeaningWord (DocumentId,StemWord,MeaningValue,YAS)  VALUES (?,?,?,?)")
                Values = [documentId,word[0],float(meaningValue),float(numberOfFalseAlarms)]
                cursor.execute(SQLCommand,Values)  
                connection.commit() 


def CloseDBConnection():
    cursor.close()
    connection.close()

def RunEducationDataProject():
    a=datetime.datetime.now()
    print(Fore.CYAN + "Dokümanlar okunup kelimelere ayrılmaya başlandı.",a)
    SeparateWordAndSaveDB()
    b=datetime.datetime.now()
    print(Fore.LIGHTBLUE_EX + "Okuma süresi ", b-a)
    number_of_rows_Words = GetWordsCount(0,True)
    if number_of_rows_Words<thresholdWordCountPerDocument:
        print(Fore.RED + "Okunan dokümandaki kelime sayısı "+ str(thresholdWordCountPerDocument)+" kelimeden az olduğu için Web araması tekrar yapılacak.")
        return
    print(Fore.LIGHTMAGENTA_EX + "Anlamsız kelimeler siliniyor. " , b)
    DeleteMeaningLessWords()
    c=datetime.datetime.now()
    print(Fore.LIGHTBLUE_EX + "Anlamsız kelimeleri silme süresi " , c-b)
    print(Fore.LIGHTYELLOW_EX + "Anlamlı kelimeler bulunuyor. " , c)

    if MeaningfulWordsSelectionType.type==0:
        CalculateTFIDF()
    if MeaningfulWordsSelectionType.type==1:
        CalculateHelmholtzPrincipleWithCode()  # SP çağrısı da yapılabilir. CalculateHelmholtzPrincipleWithSP() metodu kullanılabilir.

    if UsePMI.value==True:
        if GetMeaningWordsCount()<1:
            print("Anlamlı kelime sayısı 0 olduğu için Web araması tekrar yapılacak.")
            return
        PMI.RunPMI()

    d=datetime.datetime.now()
    print(Fore.LIGHTGREEN_EX + "Anlamlı kelimeleri bulma süresi " , d-c)
    print(Fore.LIGHTBLUE_EX + "Benzerliğe göre sözlüğe eklenecek. " , d)

    if UsePMI.value==True:
        MeaningfulWordsSelectionType.type=-1
        SavePMIMeaningWordToDB()

    if MeaningfulWordsSelectionType.type==0:
        SaveTFIDFMeaningWordsToDB()

    if MeaningfulWordsSelectionType.type==1:
        SaveHelmholtzMeaningWordToDB()

    e=datetime.datetime.now()
    print(Fore.CYAN + "Benzerliğe göre sözlüğe ekleme süresi " , e-d)