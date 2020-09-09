########################################
# word normalized frequency search
# data source: https://www.kaggle.com/rtatman/english-word-frequency/home
########################################

import csv

########################################
# file IO
########################################

def readFile(fileName):
    '''
    read csv file
    '''
    with open(fileName, 'rt', encoding="utf-8") as f:
        return f.read()

def getWordFreqDict(fileName):
    '''
    return a dictionary of 1/3 million most common english
    words as key and their frequency count as value
    '''
    wordFreqDict = dict()
    file = readFile(fileName)
    rows = file.splitlines()
    rank = 0
    for row in csv.reader(rows):   # ignore ',' within quotes
        freq = row[1]
        wordFreqDict[row[0]] = (rank, freq)
        rank += 1
    return wordFreqDict

wordFreqDict = getWordFreqDict('unigram_freq.csv')