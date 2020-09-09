########################################
# mode: lexigraph
########################################
'''
displays lexigraph and dynamically builds vocabulary
according to real time user interaction. Users can
cirHighlight relevant words or de-cirHighlight those less
relevant. Program data will log all changes and update
user's vocabulary data base.
'''
from core import program
import math
from gui.objectLib import*
pgrmData = program.data

def init(data, pgrmData):
    x, y = pgrmData.width*0.5, pgrmData.height*0.5
    ###### new words should be init in program data ####
    data.word = program.buildWord(pgrmData.searchWord)
    data.source = MovingText(name=data.word.name, loc=[x, y], size=40,radius=150,
                             font='AGaramondPro-Regular', colr=pgrmData.txtColr)
    initLexigraphElem(data, pgrmData)
    data.synTextAlias = getSynTextAlias(data)
    data.textAlias = getTextAlias(data)
    realTimeSynRecom(data, pgrmData)
    knownTextFilter(data, pgrmData)
    data.guiElem = []
    createGuiElem(data, pgrmData)
    data.startX, data.startY = 0, 0
    data.scrollX, data.scrollY = 0, 0
    data.timer = 0
    pgrmData.initMode = False

def createGuiElem(data, pgrmData):
    '''
    create GUI element in lexigraph
    '''
    x, y = pgrmData.width*0.5, pgrmData.height-50
    text = Text(name='cirHighlight familiar synonyms', loc=(x,y-40), size=15,
                font='helvetica', colr=pgrmData.txtColr, anchor='s')
    button = ClickText(name='build', loc=(x,y), size=20, font='helvetica',
                       colr=pgrmData.txtColr, anchor='s')
    elems = [text, button]
    return elems

def initLexigraphElem(data, pgrmData):
    
    data.posText, data.defText, data.synText, data.hyperText = [], [], [], []
    createPosText(data, pgrmData)
    createDefText(data, pgrmData)
    createSynText(data, pgrmData)
    createHyperText(data, pgrmData)

def createPosText(data, pgrmData):
    '''
    append all partOfSpeech from 
    the searchword into data.posText
    '''
    for p in data.word.pos:
        x, y = getRandomLoc(data, data.source)
        data.posText.append(MovingText(p, [x, y], size=25, 
                            font='AGaramondPro-Regular', colr='black', radius=100))

def createSynText(data, pgrmData):
    '''
    append all sets of synonyms from 
    the searchword into data.synText
    '''
    syns = data.word.syns
    for i in range(len(syns)):
        if isinstance(syns[i], list):
            hyperPos = syns[i][0]
            # x, y = getRandomLoc(data, data.posText[i])
            x, y = data.posText[i].loc[0], data.posText[i].loc[1]
            data.synText.append(MovingText(hyperPos, [x, y], size=25, 
                                  font='AGaramondPro-Regular', colr='black', radius=100))
        else:
            synTextList = []
            for synonym in syns[i]:
                # x, y = getRandomLoc(data, data.posText[i])
                x, y = data.posText[i].loc[0], data.posText[i].loc[1]
                synTextList.append(MovingText(synonym, [x, y], size=20, radius=60,
                                    font='AGaramondPro-Regular', colr=pgrmData.txtColr))
            data.synText.append(synTextList)

def createHyperText(data, pgrmData):
    '''
    append all sets of hypernyms from
    the searchword into data.hyperText
    '''
    syns = data.word.syns
    for i in range(len(syns)):
        if isinstance(syns[i], list):
            hyperTextList = []
            for hypernym in syns[i][2]:
                # x, y = getRandomLoc(data, data.synText[i])
                x, y = data.synText[i].loc[0], data.synText[i].loc[1]
                hyperTextList.append(MovingText(hypernym, [x, y], size=20, 
                  font='AGaramondPro-Regular', colr=pgrmData.txtColr, radius=60))
            data.hyperText.append(hyperTextList)
        else:
            data.hyperText.append([])    # create equal-size lists

def createDefText(data, pgrmData):
    '''
    returns a list of definition of all POS
    '''
    for d in data.word.defs:
        data.defText.append(BoxText(d, loc=[0, 0], size=15, width=200, anchor='sw',
                            font='AGaramondPro-Regular', colr='white'))
    hyperDefSet = []
    for s in data.word.syns:
        if isinstance(s, list):
            hyperDef = s[1]
            hyperDefSet.append(BoxText(hyperDef, loc=[0, 0], size=15, width=200, 
                        anchor='sw', font='AGaramondPro-Regular', colr='white'))
        else:
            hyperDefSet.append(None)
    data.defText.append(hyperDefSet)

def getSynTextAlias(data):
    '''
    returns a list of aliases of all synonym text objects
    '''
    alias = []
    for item in data.synText:
        if isinstance(item, list):
            alias.extend(item)
    for item in data.hyperText:
        if isinstance(item, list):
            alias.extend(item)
    return alias


def getRandomLoc(data, source):
    '''
    returns a randomly generated location within
    '''
    sX, sY = source.loc[0], source.loc[1]
    r = source.radius
    x = random.randint(sX-r, sX+r)
    y = random.randint(sY-r, sY+r)
    return x, y

def getTextAlias(data):
    '''
    returns an alias list of all text objects
    '''
    alias = []
    alias.append(data.source)
    for item in data.posText:
        alias.append(item)
    for item in data.synText:
        if isinstance(item, list):
            alias.extend(item)
        else:
            alias.append(item)
    for item in data.hyperText:
        if isinstance(item, list):
            alias.extend(item)
    return alias

def knownTextFilter(data, pgrmData):
    '''
    cirHighlight known synText or hyperText in user's familiar wordList
    '''
    knownWords = program.getKnownWords(pgrmData)
    unseenWords = pgrmData.user.wordList['unseen']

    for syn in data.synTextAlias:
        if syn.name in knownWords and syn.name not in unseenWords:
            syn.clicked = True
        if syn.name in unseenWords:
            syn.clicked = False
                    
def realTimeSynRecom(data, pgrmData):
    '''
    automated word recommendation based on cluster
    algorithm from vocabEstm. assumed familar words are 
    hilighted, users can decirHighlight unseen words. 
    update userWordList based on real time user interaction
    '''
    wordList = list(pgrmData.user.wordList['familiar'])
    newWordList = list(data.word.getSynonyms())
    if len(newWordList) != 0:
        addWords = program.wordRecom(wordFreqDict, wordList, newWordList)
        pgrmData.user.wordList['familiar'] |= (addWords)

def mouseHovered(event, data, pgrmData):
    for i in range(len(data.defText)):
        if not isinstance(data.defText[i], list):
            data.defText[i].showed = data.posText[i].hover(event)
            data.defText[i].follow(data.posText[i])
        else:
            for j in range(len(data.defText[i])):
                if data.defText[i][j] != None:
                    data.defText[i][j].showed = data.synText[j].hover(event)
                    data.defText[i][j].follow(data.synText[j])

def mouseScrolled(event, data, pgrmData): pass

def mouseDragged(event, data, pgrmData):
    startX, startY = data.startX, data.startY
    data.scrollX, data.scrollY = (event.x-startX)*0.1, (event.y-startY)*0.1
    for i in range(len(data.textAlias)):
        data.textAlias[i].loc[0] += data.scrollX
        data.textAlias[i].loc[1] += data.scrollY

def mouseReleased(event, data, pgrmData):
    data.scrollX, data.scrollY = 0, 0

def mousePressed(event, data, pgrmData):
    data.startX, data.startY = event.x, event.y
    familiarWords = pgrmData.user.wordList['familiar']
    unseenWords = pgrmData.user.wordList['unseen']
    
    if data.source.click(event):
        pgrmData.mode = 'dictionary'
        pgrmData.initMode = True
    for synText in data.synTextAlias:
        if synText.click(event):
            familiarWords.add(synText.name)
            unseenWords.discard(synText.name)
            knownTextFilter(data, pgrmData)    # temp fix
        elif synText.name in familiarWords:
            unseenWords.add(synText.name)
            familiarWords.discard(synText.name)
            knownTextFilter(data, pgrmData)    # temp fix
    realTimeSynRecom(data, pgrmData)
    knownTextFilter(data, pgrmData)    # temp fix

    print('familar words:', pgrmData.user.wordList['familiar'])
    print('unseen words:', pgrmData.user.wordList['unseen'])
    
    data.startX, data.startY = event.x, event.y

def keyPressed(event, data, pgrmData): pass

def timerFired(data, pgrmData):
    data.timer += 1
    # sourceText movement
    # data.source.move()

    # hyperText movement
    for i in range(len(data.hyperText)):
        if len(data.hyperText[i]) != 0:
            for hyper in data.hyperText[i]:
                # hyper.attract(data.synText[i])
                hyper.move()

    # synText movement
    for i in range(len(data.synText)):
        if isinstance(data.synText[i], list):
            for syn in data.synText[i]:
                # syn.attract(data.posText[i])
                syn.move()
        else:
            data.synText[i].attract(data.posText[i])
            data.synText[i].move()

    # posText movement
    for i in range(len(data.posText)):
        # data.posText[i].attract(data.source)
        data.posText[i].move()

    # collision detection
    for i in range(len(data.textAlias)):
        data.textAlias[i].wallBounce(pgrmData)
        for j in range(len(data.textAlias)):
            data.textAlias[i].bounce(data.textAlias[j])
    
def redrawAll(canvas, data):    
    for i in range(len(data.hyperText)):
        if len(data.hyperText[i]) != 0:
            for hyper in data.hyperText[i]:
                canvas.create_line(hyper.loc, data.synText[i].loc, 
                                   width=0.1, fill='grey')
                hyper.visCircle(canvas, hyper.radius)
                hyper.draw(canvas)
                hyper.cirHighlight(canvas)
                

    for i in range(len(data.synText)):
        if isinstance(data.synText[i], list):
            for syn in data.synText[i]:
                canvas.create_line(syn.loc, data.posText[i].loc, 
                                   width=0.1, fill='grey')
                syn.visCircle(canvas, syn.radius)
                syn.draw(canvas)
                syn.cirHighlight(canvas)
        else:
            canvas.create_line(data.synText[i].loc, data.posText[i].loc, 
                                   width=0.1, fill='grey')
            data.synText[i].visCircle(canvas, data.synText[i].radius)
            data.synText[i].draw(canvas)

    for text in data.posText:
        canvas.create_line(text.loc, data.source.loc, width=0.1, fill='grey')
        text.visCircle(canvas, text.radius)
        text.draw(canvas)

    data.source.visCircle(canvas, data.source.radius)
    data.source.draw(canvas)

    for defs in data.defText:
        if not isinstance(defs, list):
            defs.show(canvas)
        else:
            for hyperDef in defs:
                if hyperDef != None: hyperDef.show(canvas)

    for button in data.guiElem:
        button.draw(canvas)
    
# lexigraph local data
data = program.Struct()    