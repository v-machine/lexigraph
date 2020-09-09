########################################
# program data
########################################
from nltk.corpus import wordnet
from core.wordFreqency import wordFreqDict
from core import vocabEstm 
from gui.objectLib import*

class Struct(object): pass
data = Struct()

####################
# nltk wordnet API
####################
# cite: http://www.nltk.org/howto/wordnet.html

####  wordnet constants  ####

posSym = {'a' : 'adj.', 
          's' : 'adj.', 
          'r' : 'adv.', 
          'n' : 'n.',
          'v' : 'v.'}

def getWordnetData(name):
    return wordnet.synsets(name)

def buildWord(name):
    '''
    pipe wordnet data into customizable word object
    '''
    word = Word(name)
    for synset in getWordnetData(name):
        lemmas = synset.lemmas()
        if len(lemmas) == 1 and lemmas[0].name() == name \
        and len(synset.hypernyms()) != 0:
            hypernym = synset.hypernyms()[0]
            hyperSet = set(l.name().replace('_', ' ') for l in hypernym.lemmas())
            antSet = set(l.antonyms()[0].name().replace('_', ' ') \
                         for l in hypernym.lemmas() if l.antonyms())
            hyperDef = hypernym.definition()
            hyperPos = posSym[hypernym.pos()]

            synsPos = posSym[synset.pos()]
            synsDef = synset.definition()

            word.pos.append(synsPos)
            word.defs.append(synsDef)
            word.syns.append([hyperPos, hyperDef, hyperSet])
            word.ants.append([hyperPos, hyperDef, antSet])
        else:
            lemSet = set(l.name().replace('_', ' ') for l in lemmas if l.name() != name)
            antSet = set(l.antonyms()[0].name().replace('_', ' ') \
                         for l in lemmas if l.antonyms())
            synsPos = posSym[synset.pos()]
            synsDef = synset.definition()
            word.pos.append(synsPos)
            word.defs.append(synsDef)
            word.syns.append(lemSet)
            word.ants.append(antSet)
    return word

def getDictData(data):
    '''
    called by dictionary module and returns dictonary data 
    in a dictionary, including definition and POS
    '''
    # cite: http://www.nltk.org/howto/wordnet.html
    dictData = dict()
    for synset in getWordnetData(data.searchWord):
        dictData[synset.definition()] = posSym[synset.pos()]
    return dictData

def initLexicalGraph(data):
    '''
    initiate lexigraph based on user wordList
    '''
    for level in data.user.wordList:
        for name in data.user.wordList[level]:
            word = buildWord(name)
            data.user.lexigraph.storeInGraph(word)

def getKnownWords(data):
    '''
    creating a list of known words based on wordList in the
    user database. levels to include: 'expert', 'familiar',
    'average'
    '''
    knownWords = set()
    expertWords = data.user.wordList['expert']
    familiarWords = data.user.wordList['familiar']
    averageWords = data.user.wordList['average']
    knownWords |= expertWords | familiarWords | averageWords
    return knownWords

def getNewWords(data):
    '''
    creating a list of freshly learned words based on wordList in the
    user database. levels to include: 'expert', 'familiar',
    'average'
    '''
    newWords = set()
    freshWords = data.user.wordList['fresh']
    aquaintedWords = data.user.wordList['aquainted']
    averageWords = data.user.wordList['average']
    newWords |= freshWords | aquaintedWords | averageWords
    return newWords

def saveData():
    '''
    # save user data to a local file
    '''
    pass

# from http://python.omics.wiki/plot/colors/rgb2hex
def rgbToHex(r, g, b):
    '''
    converts rgb values into hex code
    '''
    return '#%02x%02x%02x' % (r, g, b)

def getRelevWords(wordProb):
    '''
    returns a set of most relevant words based
    on estimated word probabilities
    '''
    relevWords = set()
    meanWordProb = sum(list(wordProb.values()))/len(wordProb)
    for word in wordProb:
        if wordProb[word] > meanWordProb:
            relevWords.add(word)
    print('recommended syns:', relevWords)
    return relevWords

def wordRecom(wordFreqDict, wordList, newWordList):
    '''
    returns a set of recommended words
    '''
    newWordProb = getNewWordProb(wordFreqDict, wordList, newWordList)
    print('synonyms prob:', newWordProb)
    return getRelevWords(newWordProb)

def getNewWordProb(wordFreqDict, wordList, newWordList):
    '''
    returns a list of estimated relevant words based on a list of familar
    words from the user data base
    '''
    freqProbDistrb = vocabEstm.getClusterProb(wordFreqDict, wordList)
    freqDomList = sorted(freqProbDistrb.keys())
    newFreqRank = getFreqRank(wordFreqDict, newWordList)
    newWordProb = dict()
    for i in range(len(newWordList)):
        word = newWordList[i]
        wordRank = newFreqRank[i]
        for domain in freqDomList:
            if wordRank > domain[0]:
                newWordProb[word] = freqProbDistrb[domain]
    return newWordProb

def getFreqRank(wordFeqDict, wordList):
    '''
    returns a list of word frequency of wordList
    for polygrams returns the average frequency
    '''
    freqRank = []
    for word in wordList:
        if len(word.split(' ')) > 1:
            subFreq = []
            for subWord in word.split(' '):
                subFreq.append(getUnigramRank(wordFreqDict, subWord))
            freqRank.append(sum(subFreq)/len(subFreq))
        else:
            freqRank.append(getUnigramRank(wordFreqDict, word))
    return freqRank

def getUnigramRank(wordFeqDict, unigram):
    '''
    return the frequency ranking of the input unigram
    '''
    if wordFreqDict.get(unigram) != None:
        return wordFreqDict[unigram][0]
    else:
        return len(wordFreqDict)+1

######################################################################

# wordList = vocabEstm.getWordList('TOEFL_Vocab.csv')
# newWordList = ['drink', 'take up', 'sop', 'absorb', 'suck in',\
#                'soak', 'take in', 'draw', 'assimilate', 'ingest']
# newWordProb = getNewWordProb(wordFreqDict, wordList, newWordList)
# for w in newWordProb:
#     print(w, newWordProb[w])
# print(getRelevWords(newWordProb))

######################################################################

def init(data):
    # initiate wordnet

    ####  backend  ####
    wordnet.synsets('')
    data.searchWord = ''
    data.lexigraph = LexicalGraph()
    data.dictData = dict()  # use return from getDictData
    data.user = User('Carolyn')
    data.mode = 'search'
    data.initMode = True
    data.bgColr = 'gray91'
    data.txtColr = 'blue'
    data.masterColr = 'blue'

    ####  front end  ####
    data.margin = 30
    data.marginTop = 50
    data.marginMenu = 100
    data.marginCenTop = 200
    data.marginCenLeft = 400
    data.guiElem = []
    initGuiElem(data)

def initGuiElem(data):
    icon = ClickText(name='LEXI-\nGRAPH', loc=(data.margin, data.marginMenu), 
                          size=25, font='Helvetica-Bold', anchor='sw',
                          colr=data.txtColr)
    data.guiElem.append(icon)

    menu = ['explore', 'search', 'dictionary', 'pair', 'archive']
    margin = data.marginCenLeft+45
    for elem in menu:
        button = ClickText(name=elem, loc=(margin, data.marginMenu), 
                          size=20, font='Helvetica-Bold', anchor='s',
                          colr=data.txtColr)
        data.guiElem.append(button)
        margin += 200

def hoverHighlight(canvas, elem):
    x1, y1, x2, y2 = elem.bbox
    space, thickness = 10, 3
    loc = x1, y2+space, x2, y2+space+thickness
    canvas.create_rectangle(loc, width=0, fill=data.txtColr)

def hoverHints(canvas, data, elem):
    hint = {'LEXI-\nGRAPH':'displays lexical graph of current search word',
            'explore':'explore recent example usage on web',
            'search':'type and search word',
            'dictionary':'displays traditional dictionary definition',
            'pair':'timed synonym pairng game', 
            'archive':'review learned words'}
    x, y = data.width*0.5, data.height-50
    tag = canvas.create_text((x, y), text=hint[elem.name], fill=data.txtColr,
                       font='Helvetica-Regular 15', anchor='s')
    width = canvas.bbox(tag)[2]-canvas.bbox(tag)[0] 
    canvas.create_line(x-width*0.2, y+15, x+width*0.2, y+15, width=0.5, fill='blue')

def redrawAll(canvas, data):
    '''
    display all of the graphic elements
    '''
    for elem in data.guiElem:
        elem.draw(canvas)
        if elem.hovered:
            hoverHighlight(canvas, elem)
            hoverHints(canvas, data, elem)

def mouseHovered(event, data):
    '''
    hover interaction with GUI elements
    '''
    for elem in data.guiElem: elem.hover(event)

def mousePressed(event, data):
    '''
    click interaction with GUI elements
    '''
    for elem in data.guiElem:
        if isinstance(elem, ClickText) and elem.click(event):
            elem.clicked = False
            data.initMode = True
            if elem.name == 'LEXI-\nGRAPH':
                data.mode = 'lexigraph'
            else:
                data.mode = elem.name