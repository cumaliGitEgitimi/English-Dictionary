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
import numpy as np
import itertools
import math
import datetime


connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-AT012337;'
                                               'Database=SmallWordsEducation;'
                                                 'uid=PhytonThesisUser;pwd=1') 

cursor = connection.cursor() 


def VectorizeDocument(document_list):
     SelectMeaningWordLoop = ("SELECT distinct * FROM MeaningWord")
     cursor.execute(SelectMeaningWordLoop)
     meaning_words = cursor.fetchall()
     for document in document_list:
         IsDocumentContainWord = []
         for word in meaning_words:
             IsDocumentContainWord.append(CheckContains(document[0],word))
         WriteDocumentVectorToDB(document[0],IsDocumentContainWord,meaning_words)


def GetDocumentList():
    SQLCommand = ("EXEC GetDocumentIdList")
    cursor.execute(SQLCommand)
    return cursor.fetchall()



def CheckContains(document,word):
    #document = document[0]
    word = str(word[1]) # Stemword'ü alabilmek için word index'i 2 seçiliyor.
    IsContains = "SELECT Count(*) FROM Words WHERE DocumentId = ? and StemWord =" + "'" + word + "'" 
    documentId = [document]
    cursor.execute(IsContains,documentId)
    founded = cursor.fetchone()
    if(founded[0] > 0):
        return 1
    else:
        return 0


def WriteDocumentVectorToDB(document,document_vector,meaning_words):
    b = ",".join(str(i) for i in document_vector)
    
    InsertDocumentVector = ("INSERT INTO DocumentVector(DocumentId,Vector) VALUES(?,?) ")
    
    params = [int(document),str(b)]
    
    cursor.execute(InsertDocumentVector,params)

def CalculatePMI():
    document_list = GetDocumentList()
    for document in document_list:
        vectors = GetDocumentVector(document[0])

        i_vals = []
        for i in range(0,len(vectors)): 
           i_vals.append(i) 
           for j in range(0,len(vectors)):

              if i == j :
                   print("P(" + str(i) + "," + str(j) + ")")
                   CalculateTwoWordAssociation(i,j,len(document_list))
                   CalculatePMIFinalization(i,j,document[0])
                   
              if not j in i_vals:
                  if vectors[i] == "1" and vectors[j] == "1":
                      print("P(" + str(i) + "," + str(j) + ")")
                      CalculateTwoWordAssociation(i,j,len(document_list))
                      CalculatePMIFinalization(i,j,document[0])

def CalculateTwoWordAssociation(i,j,documentCount):
    association = 0
    vector_list = GetAllVectors()

    for vector in vector_list:
        if vector[i] == "1" and vector[j] == "1":
            association = association + 1
    #   association = 0 ise laplace düzeltmesi uygulanacak
    association_prop = association / documentCount
    WriteAssociationPropToDB(i,j,association_prop)

def Calculate(i,j,document_list):
    s = 0
    print("D(" + str(i) + "," + str(j) + ")")
    i_vals = [] 
    D1Vector = GetDocumentVector(document_list[i][0])
    D2Vector = GetDocumentVector(document_list[j][0])
    #Dokümanlara ait vektörler çekilip, iki dokümanda da yer alan kelimeleri
    #toplam benzerliğe ekliyoruz.
    for index in range(0,len(D1Vector)):
        if(int(D1Vector[index]) == 1 and int(D2Vector[index]) == 1):
            query = "SELECT PMI FROM [SmallWordsEducation].[dbo].[DocumentsPMI] WHERE WordOneId = ?  OR WordTwoId = ?"
            params = [i,j]
            cursor.execute(query,params)
            results = cursor.fetchone()
            i_vals.append(float(results[0]))
            s = sum(i_vals)
    WriteSimilarityToDB(i,j, s,document_list)

def WriteSimilarityToDB(document1,document2,result,document_list):
    topic1 = document_list[document1][2]    
    topic2 = document_list[document2][2]
    subtopic1 = document_list[document1][3]
    subtopic2 = document_list[document2][3]

    InsertSimilarity = ("INSERT INTO DocumentSimilarity(DocumentOne,DocumentOneTopic,DocumentOneSubTopic,DocumentTwo,DocumentTwoTopic,DocumentTwoSubTopic,SimilarityResult) VALUES(?,?,?,?,?,?,?) ")
    InsertionSimilarityValues = [document1,topic1,subtopic1,document2,topic2,subtopic2,float(result)]
    cursor.execute(InsertSimilarity,InsertionSimilarityValues)


def GetDocumentVector(document):
    query = "SELECT Vector FROM [SmallWordsEducation].[dbo].[DocumentVector] WHERE DocumentId=" + str(document)
    cursor.execute(query)
    results = cursor.fetchall()
    vector = str(results[0])
    vector = vector[2:-3]
    vector_elements = vector.split(',')
    return vector_elements

def CalculateSimilarities():
    document_list = GetDocumentList()
    i_vals = []
    for i in range(0,len(document_list)): 
        i_vals.append(i) 
        for j in range(0,len(document_list)):
             if i != j :
                  Calculate(i,j,document_list)


def CalculateSingleWordProbabilityForDocuments(documentId):
    #documentId = document[0]
    query = "SELECT distinct TOP (1000) [DocumentId],[StemWord],[MeaningValue] FROM [SmallWordsEducation].[dbo].[MeaningWord] WHERE DocumentId=" + str(documentId)
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        CalculateSingleProp(r,documentId)

def GetAllVectors():
    query = "SELECT Vector FROM [SmallWordsEducation].[dbo].[DocumentVector]"
    cursor.execute(query)
    results = cursor.fetchall()
    vector_array = []
    for idx in results:
        vector = str(idx)
        vector = vector[2:-3]
        vector_elements = vector.split(',')     
        vector_array.append(vector_elements)
    
    return vector_array      

def CalculateSingleProp(r,documentId):
    singleProp = 0 
    document_list = GetDocumentList()
    vectors = GetAllVectors()
    for vector in vectors:
        if vector[r[0]] == '1':
            singleProp = singleProp + 1

    InsertSingleWordProb = ("INSERT INTO SingleWordProp(DocumentId,Word,Probability) VALUES(?,?,?) ")
    SingleWordValues = [int(documentId),r[1], singleProp / len(document_list)]
    cursor.execute(InsertSingleWordProb,SingleWordValues)

def WriteAssociationPropToDB(word1index,word2index,prop):
    word1 = GetWord(word1index)
    word1 = word1[3:-4]
    word2 = GetWord(word2index)
    word2 = word2[3:-4]
    InsertProbs = ("INSERT INTO ProbabilitiesOfAssociation(Word1,Word1Index,Word2,Word2Index,AssociationProp) VALUES(?,?,?,?,?) ")
    InsertionValues = [word1,word1index,word2,word2index,prop]
    cursor.execute(InsertProbs,InsertionValues)

def GetWord(index):
    query = "SELECT distinct StemWord FROM MeaningWord WHERE WordId=" + str(index)
    cursor.execute(query)
    results = cursor.fetchall()
    return str(results)

def GetWordBag(index):
    query = "SELECT distinct * FROM MeaningWord WHERE WordId=" + str(index)
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def GetSingleProb(word):
    query = "SELECT Probability FROM SingleWordProp WHERE Word=" + "'" + word + "'"
    cursor.execute(query)
    prop = cursor.fetchall()
    return prop[0][0]

def GetAssociatiedProb(word1,word2):
    query = "SELECT AssociationProp FROM ProbabilitiesOfAssociation WHERE Word1=" + "'" + word1 + "'" + "AND Word2=" + "'" + word2 + "'"
    cursor.execute(query)
    prop = cursor.fetchall()
    return prop[0][0]

def CalculatePMIFinalization(i,j,documentId):
    print("PMI Similarity Calculation Started...")
    #documentId = document[0]
    word1 = GetWord(i)
    word1 = word1[3:-4]
    word2 = GetWord(j)
    word2 = word2[3:-4]

    TotalWordsCommands = ("SELECT DISTINCT COUNT(*) FROM MeaningWord")
    cursor.execute(TotalWordsCommands)
    V = list(map(int,cursor.fetchall()[0]))
    word1Bag = GetWordBag(i)
    word2Bag = GetWordBag(j)
    p1 = GetSingleProb(word1)
    p2 = GetSingleProb(word2)
    p12 = GetAssociatiedProb(word1,word2)
    PMI2 = math.log2(((float(p12)) / ((float(p1) * float(p2)))))
    print("P(" + word1 + "," + word2 + ") =" + str(PMI2))
    InsertPMI = ("INSERT INTO DocumentsPMI(WordOne,WordOneId,WordTwo,WordTwoId,DocumentId,PMI) VALUES(?,?,?,?,?,?) ")
    InsertionPMIValues = [word1,int(word1Bag[0][3]),word2,int(word2Bag[0][3]),documentId,float(PMI2)]
    cursor.execute(InsertPMI,InsertionPMIValues)


def RunPMI():
    document_list = GetDocumentList()
    if len(document_list)<2:
        print("PMI hesaplaması için en az 2 doküman sisteme yüklenmelidir.")
        return
    VectorizeDocument(document_list)
   
    for document in document_list:
        CalculateSingleWordProbabilityForDocuments(document[0])  
    CalculatePMI()
    connection.commit()
    #cursor.close()