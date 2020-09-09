######################################################
# vocabulary level estimation
######################################################
'''
returns a probability assignment on the 1/3 million 
most frequently searched words from Google Web Trillion
Word Corpus
'''
from wordFreqency import wordFreqDict

##############################
# file IO
##############################

import random
import csv

def readFile(fileName):
    '''
    read csv file
    '''
    with open(fileName, 'rt', encoding="utf-8") as f:
        return f.read()

def getWordList(fileName):
    '''
    return a list of all english words from the input csv
    '''
    wordList = []
    file = readFile(fileName)
    rows = file.splitlines()
    for row in csv.reader(rows):
        wordList.append(row[0].lower())
    return wordList

def randomSample(lst, sampleSize, seed):
    '''
    randomize a lst by a sampleSize and a fixed seed
    '''
    random.seed(seed)
    return(random.sample(lst, sampleSize))

##############################
# cluster algorithm
##############################

def getClusterProb(wordFreqDict, wordList):
    '''
    returns a dictionary of domains (as values) and the
    probility assigned to each domain (as keys) based
    on the clusters created by the input wordList
    discussion and guidance credit: Harsh, Oz
    '''
    freqRank = sorted(getFreqRank(wordFreqDict, wordList))
    ordDist = getOrdDist(freqRank)
    distDiff = getDistDiff(ordDist)
    meanDistDiff = 1
    meanDistDiff = sum(distDiff)/len(distDiff)
    meanProb = 0 if len(freqRank) == 0 else 1/len(freqRank)
    # print('freqRank:', freqRank)
    # print('ordDist:', ordDist)
    # print('distDiff', distDiff)
    # print('meanDistDiff:', meanDistDiff)
    # print('meanProb:', meanProb)

    ####  param tunning  ####
    meanDistDiff *= 1
    prob = 0
    splits, probList = [], []
    splitDict = dict()

    for i in range(len(distDiff)):
        prob += meanProb
        if distDiff[i] > meanDistDiff:
            splits.append(freqRank[i])
            probList.append(prob)
            prob = 0
    
    # normalize probList:
    total = sum(probList)
    for prob in probList:
        prob /= total

    # print('splits:', splits)
    # print('probList:', probList)
    
    if len(splits) == 0 and len(freqRank) == 0:
        return {(1,len(wordFreqDict)):0}
    elif len(splits) == 0 and freqRank != 0:
        splitDict[(1, freqRank[-1])] = 1
    else:
        splitDict[(1, splits[0])] = probList[0]    # from start for first split        
        for i in range(1, len(splits)):
            splitDict[(splits[i-1], splits[i])] = probList[i]
        if splits[-1] != freqRank[-1]: 
            splitDict[(splits[-1], freqRank[-1])] = 1-sum(probList)

    print(splitDict)
    return splitDict

def getFreqRank(wordFreqDict, wordList):
    '''
    returns a list of word frequency of wordList
    '''
    freqRank = []
    for word in wordList:
        if wordFreqDict.get(word, None) != None:
            freqRank.append(wordFreqDict[word][0])
        else:
            # WordFreqDict[word] = (len(WordFreqDict)+1, 0)
            freqRank.append(len(wordFreqDict)+1)
    return freqRank

def getOrdDist(lst):
    '''
    returns a list distance between ordinal item in lst
    '''
    if len(lst) == 0:
        ordDist = [0]
    else:
        ordDist = [lst[0]]
        for i in range(1, len(lst)):
            dist = lst[i]-lst[i-1]
            ordDist.append(dist)
    return ordDist

def getDistDiff(ordDist):
    '''
    returns a list of ordinal difference between list items
    '''
    distDiff = []
    if len(ordDist) < 2:
        distDiff = [0]
    else:
        for i in range(1, len(ordDist)):
            diff = abs(ordDist[i]-ordDist[i-1])
            distDiff.append(diff)
    return distDiff

##############################
# cross validation
##############################

# 10 fold cross-validation

def getCvFolds(lst, folds):
    '''
    return a list of tuples of train-test pairs
    '''
    cvFolds = []
    segments = []
    sample = len(lst)//folds
    for i in range(folds-1):
        s = random.sample(lst, sample)
        segments.append(s)
        lst = [e for e in lst if e not in segments[i]]
    # take the remainder of the last fold
    segments.append(lst)
    for i in range(len(segments)):
        test = segments[i]
        train = []
        for s in segments[:i]:
            train += s
        for s in segments[i+1:]:
            train += s
        cvFolds.append((train, test))
    return cvFolds

def runCrossValidation(cvFolds, testModel):
    result = dict()
    for fold in cvFolds:
        trainSet, testSet = fold[0], fold[1]
        foldResult = testModel(trainSet, testSet)
        result.update(foldResult)
    return result

def testModel(trainSet, testSet):
    testResult = dict()
    model = getClusterProb(wordFreqDict, trainSet)
    testFreqRank = getFreqRank(wordFreqDict, testSet)
    for i in range(len(testSet)):
        for domain in model:
            word = testSet[i]
            wordFreq = testFreqRank[i]
            if domain[0]<= wordFreq <=domain[1]:
                probility = model[domain]
                testResult[word] = probility
    return testResult