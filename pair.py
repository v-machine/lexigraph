########################################
# mode: pair
########################################
'''
word paring game used for strengthening
freshly learned or unfamiliar words
'''
import program
import random
import string
import requests
from objectLib import*
pgrmData = program.data

def init(data, pgrmData):
    '''
    initiate data in the current mode
    '''
    data.timer = 0
    data.timesUp = False
    data.seconds = 30
    data.scrollY = 0
    data.scrollSpeed = 10
    data.wordPairs = set()
    totalTargetWords = len(pgrmData.user.wordList['average'])+\
                       len(pgrmData.user.wordList['aquainted'])+\
                       len(pgrmData.user.wordList['fresh'])
    data.num = min(20, totalTargetWords)
    data.wordPairText = []
    data.countDown = createCountDown(data, pgrmData)
    getWordPairs(data, pgrmData)
    createPairText(data, pgrmData)
    data.result = createResult(data, pgrmData)
    pgrmData.initMode = False    # init once only

def createPairText(data, pgrmData):
    width, height = pgrmData.width, pgrmData.height
    margin = 200
    for pair in data.wordPairs:
        for word in pair:
            x = random.randint(margin, width-margin)
            y = random.randint(margin, height-margin)
            text = MovingText(word, loc=[x, y], size=25, colr=pgrmData.txtColr,
                              font='AGaramondPro-Regular', radius=40)
            data.wordPairText.append(text)

def createCountDown(data, pgrmData):
    x, y = pgrmData.width*0.5, pgrmData.height*0.5
    countDown = MovingText(data.seconds, loc=[x, y], colr=pgrmData.txtColr,
                            radius=50, font='Helvetica', size=50)
    return countDown

def getWordPairs(data, pgrmData):
    '''
    return a list of word pairs for the paring game
    '''
    targetWords = getTargetWords(data, pgrmData, data.num)
    synWords = getSynWords(data, pgrmData, targetWords)
    for i in range(len(targetWords)):
        data.wordPairs.add((targetWords[i], synWords[i]))

def getTargetWords(data, pgrmData, num):
    '''
    return a list of target words
    '''
    targetWords = []
    isolatedWords = []

    averageWords = pgrmData.user.wordList['average']
    aquaintedWords = pgrmData.user.wordList['aquainted']
    freshWords = pgrmData.user.wordList['fresh']

    averageWordNum = min(int(0.1*data.num), len(averageWords))
    aquaintedWordNum = min(int(0.3*data.num), len(aquaintedWords))
    freshWordNum = min(int(0.6*data.num), len(freshWords))

    for i in range(averageWordNum): 
        targetWords.extend(random.sample(averageWords, averageWordNum))
    for i in range(aquaintedWordNum): 
        targetWords.extend(random.sample(aquaintedWords, aquaintedWordNum))
    for i in range(freshWordNum): 
        targetWords.extend(random.sample(freshWords, freshWordNum))

    # remove target words that doesn't have synonyms
    for word in targetWords:
        syns = program.buildWord(word).getSynonyms()
        if len(syns) == 0:
            print(word, "doesn't have syn")
            isolatedWords.append(word)
    for word in isolatedWords:
        targetWords.remove(word)
    return targetWords

def getSynWords(data, pgrmData, targetWords):
    '''
    return a list of synonyms to pair with
    each target word
    '''
    synWords = []
    knownWords = program.getKnownWords(pgrmData)
    for word in targetWords:
        syns = program.buildWord(word).getSynonyms()
        found = False
        for s in syns:
            if s in knownWords:
                synWords.append(s)
                found = True
                break
        if not found:
            synWords.extend(random.sample(syns, 1))
    return synWords

def checkPairs(event, data):
    lastText = None
    pair, words = [], []
    for text in data.wordPairText:
        if isinstance(text, ClickText) and text.click(event):
            if lastText != None:
                if isPair(text, lastText, data):
                    pair.extend([text, lastText])
                    lastText = None
                    # do something
                    # text.couple(lastText)
                else:
                    text.clicked = False
                    lastText.clicked = False
                    lastText = None
            else:
                lastText = text
    for text in pair:
        data.wordPairText.remove(text)
        words.append(text.name)
    data.wordPairs.discard(tuple(words))
    data.wordPairs.discard(tuple(words[::-1]))

def isPair(text1, text2, data):
    '''
    returns true if text1, text2 is in 
    data.wordPairs, else false
    '''
    pair = text1.name, text2.name
    return tuple(pair) in data.wordPairs or\
           tuple(pair[::-1]) in data.wordPairs

def createResult(data, pgrmData):
    '''
    display the result when time's up
    '''
    width = pgrmData.width
    left, top = pgrmData.marginCenLeft, pgrmData.marginCenTop
    x, y = left + (width-left)*0.5-50, top + 150
    message = Text(name='', loc=(x, y), colr=pgrmData.txtColr, size=20,
                   font='AGaramondPro-Regular', anchor='n', width=800)
    text = 'Missed Pairs'
    x, y = left + (width-left)*0.5-50, top + 50
    title = Text(name=text, loc=(x, y), colr=pgrmData.txtColr, size=30,
                 font='AGaramondPro-Bold', anchor='center', width=800)
    result = [message, title]
    return result

def updateResult(data, pgrmData):
    missed = ''
    for pair in data.wordPairs:
        line = '%s ------ %s'%(pair[0], pair[1])
        missed += line.center(40) + '\n'
    message = data.result[0]
    message.name = missed

def mouseHovered(event, data, pgrmData): pass

def mouseScrolled(event, data, pgrmData):
    scrollY, scrollSpeed = data.scrollY, data.scrollSpeed
    if event.delta > -1: scrollY += scrollSpeed
    if event.delta < 1: scrollY -= scrollSpeed
    for text in data.result:
        x, y = text.loc
        text.loc = (x, y+scrollY)

def mouseDragged(event, data, pgrmData): pass

def mouseReleased(event, data, pgrmData): pass

def mousePressed(event, data, pgrmData):
    checkPairs(event, data)

def keyPressed(event, data, pgrmData): pass

def timerFired(data, pgrmData):
    data.timer += 1
    if data.timer%10 == 0:
        data.countDown.name -= 1
    if data.countDown.name ==0:
        data.timesUp = True
    for text in data.wordPairText:
        text.move()
        text.wallBounce(pgrmData)
    for i in range(len(data.wordPairText)):
        for j in range(len(data.wordPairText)):
            data.wordPairText[i].bounce2(data.wordPairText[j])   
    updateResult(data, pgrmData)     

def redrawAll(canvas, data):
    if data.timesUp:
        for text in data.result:
            text.draw(canvas)
    else:
        for text in data.wordPairText:
            text.visCircle(canvas, text.radius)
            text.draw(canvas)
            text.cirHighlight(canvas)
        data.countDown.draw(canvas)

data = program.Struct()