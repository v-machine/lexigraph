########################################
# mode: lexigraph
########################################
'''
displays lexigraph and dynamically builds vocabulary
according to real time user interaction. users can
cirhighlight relevant words or de-cirhighlight those less
relevant. program data will log all changes and update
user's vocabulary data base.
'''
from core import program
from core.wordFreqency import wordFreqDict
import math
from gui.objectLib import *
pgrmdata = program.data

def init(data, pgrmdata):
    x, y = pgrmdata.width*0.5, pgrmdata.height*0.5
    ###### new words should be init in program data ####
    data.word = program.buildword(pgrmdata.searchword)
    data.source = MovingText(name=data.word.name, loc=[x, y], size=40,radius=150,
                             font='agaramondpro-regular', colr=pgrmdata.txtcolr)
    initlexigraphelem(data, pgrmdata)
    data.syntextalias = getsyntextalias(data)
    data.textalias = gettextalias(data)
    realtimesynrecom(data, pgrmdata)
    knowntextfilter(data, pgrmdata)
    data.guielem = []
    createguielem(data, pgrmdata)
    data.startx, data.starty = 0, 0
    data.scrollx, data.scrolly = 0, 0
    data.timer = 0
    pgrmdata.initmode = False

def createguielem(data, pgrmdata):
    '''
    create gui element in lexigraph
    '''
    x, y = pgrmdata.width*0.5, pgrmdata.height-50
    text = text(name='cirhighlight familiar synonyms', loc=(x,y-40), size=15,
                font='helvetica', colr=pgrmdata.txtcolr, anchor='s')
    button = ClickText(name='build', loc=(x,y), size=20, font='helvetica',
                       colr=pgrmdata.txtcolr, anchor='s')
    elems = [text, button]
    return elems

def initlexigraphelem(data, pgrmdata):
    
    data.postext, data.deftext, data.syntext, data.hypertext = [], [], [], []
    createpostext(data, pgrmdata)
    createdeftext(data, pgrmdata)
    createsyntext(data, pgrmdata)
    createhypertext(data, pgrmdata)

def createpostext(data, pgrmdata):
    '''
    append all partofspeech from 
    the searchword into data.postext
    '''
    for p in data.word.pos:
        x, y = getrandomloc(data, data.source)
        data.postext.append(MovingText(p, [x, y], size=25, 
                            font='agaramondpro-regular', colr='black', radius=100))

def createsyntext(data, pgrmdata):
    '''
    append all sets of synonyms from 
    the searchword into data.syntext
    '''
    syns = data.word.syns
    for i in range(len(syns)):
        if isinstance(syns[i], list):
            hyperpos = syns[i][0]
            # x, y = getrandomloc(data, data.postext[i])
            x, y = data.postext[i].loc[0], data.postext[i].loc[1]
            data.syntext.append(MovingText(hyperpos, [x, y], size=25, 
                                  font='agaramondpro-regular', colr='black', radius=100))
        else:
            syntextlist = []
            for synonym in syns[i]:
                # x, y = getrandomloc(data, data.postext[i])
                x, y = data.postext[i].loc[0], data.postext[i].loc[1]
                syntextlist.append(MovingText(synonym, [x, y], size=20, 
                                              radius=60, font='agaramondpro-regular', colr=pgrmdata.txtcolr))
            data.syntext.append(syntextlist)

def createhypertext(data, pgrmdata):
    '''
    append all sets of hypernyms from
    the searchword into data.hypertext
    '''
    syns = data.word.syns
    for i in range(len(syns)):
        if isinstance(syns[i], list):
            hypertextlist = []
            for hypernym in syns[i][2]:
                # x, y = getrandomloc(data, data.syntext[i])
                x, y = data.syntext[i].loc[0], data.syntext[i].loc[1]
                hypertextlist.append(MovingText(hypernym, [x, y], size=20, 
                  font='agaramondpro-regular', colr=pgrmdata.txtcolr, radius=60))
            data.hypertext.append(hypertextlist)
        else:
            data.hypertext.append([])    # create equal-size lists

def createdeftext(data, pgrmdata):
    '''
    returns a list of definition of all pos
    '''
    for d in data.word.defs:
        data.deftext.append(BoxText(d, loc=[0, 0], size=15, width=200, anchor='sw',
                            font='agaramondpro-regular', colr='white'))
    hyperdefset = []
    for s in data.word.syns:
        if isinstance(s, list):
            hyperdef = s[1]
            hyperdefset.append(BoxText(hyperdef, loc=[0, 0], size=15, width=200, 
                        anchor='sw', font='agaramondpro-regular', colr='white'))
        else:
            hyperdefset.append(None)
    data.deftext.append(hyperdefset)

def getsyntextalias(data):
    '''
    returns a list of aliases of all synonym text objects
    '''
    alias = []
    for item in data.syntext:
        if isinstance(item, list):
            alias.extend(item)
    for item in data.hypertext:
        if isinstance(item, list):
            alias.extend(item)
    return alias


def getrandomloc(data, source):
    '''
    returns a randomly generated location within
    '''
    sx, sy = source.loc[0], source.loc[1]
    r = source.radius
    x = random.randint(sx-r, sx+r)
    y = random.randint(sy-r, sy+r)
    return x, y

def gettextalias(data):
    '''
    returns an alias list of all text objects
    '''
    alias = []
    alias.append(data.source)
    for item in data.postext:
        alias.append(item)
    for item in data.syntext:
        if isinstance(item, list):
            alias.extend(item)
        else:
            alias.append(item)
    for item in data.hypertext:
        if isinstance(item, list):
            alias.extend(item)
    return alias

def knowntextfilter(data, pgrmdata):
    '''
    cirhighlight known syntext or hypertext in user's familiar wordlist
    '''
    knownwords = program.getknownwords(pgrmdata)
    unseenwords = pgrmdata.user.wordlist['unseen']

    for syn in data.syntextalias:
        if syn.name in knownwords and syn.name not in unseenwords:
            syn.clicked = True
        if syn.name in unseenwords:
            syn.clicked = False
                    
def realtimesynrecom(data, pgrmdata):
    '''
    automated word recommendation based on cluster
    algorithm from vocabestm. assumed familar words are 
    hilighted, users can decirhighlight unseen words. 
    update userwordlist based on real time user interaction
    '''
    wordlist = list(pgrmdata.user.wordlist['familiar'])
    newwordlist = list(data.word.getsynonyms())
    if len(newwordlist) != 0:
        addwords = program.wordRecom(wordFreqDict, wordlist, newwordlist)
        pgrmdata.user.wordlist['familiar'] |= (addwords)

def mousehovered(event, data, pgrmdata):
    for i in range(len(data.deftext)):
        if not isinstance(data.deftext[i], list):
            data.deftext[i].showed = data.postext[i].hover(event)
            data.deftext[i].follow(data.postext[i])
        else:
            for j in range(len(data.deftext[i])):
                if data.deftext[i][j] != None:
                    data.deftext[i][j].showed = data.syntext[j].hover(event)
                    data.deftext[i][j].follow(data.syntext[j])

def mousescrolled(event, data, pgrmdata): pass

def mousedragged(event, data, pgrmdata):
    startx, starty = data.startx, data.starty
    data.scrollx, data.scrolly = (event.x-startx)*0.1, (event.y-starty)*0.1
    for i in range(len(data.textalias)):
        data.textalias[i].loc[0] += data.scrollx
        data.textalias[i].loc[1] += data.scrolly

def mousereleased(event, data, pgrmdata):
    data.scrollx, data.scrolly = 0, 0

def mousepressed(event, data, pgrmdata):
    data.startx, data.starty = event.x, event.y
    familiarwords = pgrmdata.user.wordlist['familiar']
    unseenwords = pgrmdata.user.wordlist['unseen']
    
    if data.source.click(event):
        pgrmdata.mode = 'dictionary'
        pgrmdata.initmode = True
    for syntext in data.syntextalias:
        if syntext.click(event):
            familiarwords.add(syntext.name)
            unseenwords.discard(syntext.name)
            knowntextfilter(data, pgrmdata)    # temp fix
        elif syntext.name in familiarwords:
            unseenwords.add(syntext.name)
            familiarwords.discard(syntext.name)
            knowntextfilter(data, pgrmdata)    # temp fix
    realtimesynrecom(data, pgrmdata)
    knowntextfilter(data, pgrmdata)    # temp fix

    print('familar words:', pgrmdata.user.wordlist['familiar'])
    print('unseen words:', pgrmdata.user.wordlist['unseen'])
    
    data.startx, data.starty = event.x, event.y

def keypressed(event, data, pgrmdata): pass

def timerfired(data, pgrmdata):
    data.timer += 1
    # sourcetext movement
    # data.source.move()

    # hypertext movement
    for i in range(len(data.hypertext)):
        if len(data.hypertext[i]) != 0:
            for hyper in data.hypertext[i]:
                # hyper.attract(data.syntext[i])
                hyper.move()

    # syntext movement
    for i in range(len(data.syntext)):
        if isinstance(data.syntext[i], list):
            for syn in data.syntext[i]:
                # syn.attract(data.postext[i])
                syn.move()
        else:
            data.syntext[i].attract(data.postext[i])
            data.syntext[i].move()

    # postext movement
    for i in range(len(data.postext)):
        # data.postext[i].attract(data.source)
        data.postext[i].move()

    # collision detection
    for i in range(len(data.textalias)):
        data.textalias[i].wallbounce(pgrmdata)
        for j in range(len(data.textalias)):
            data.textalias[i].bounce(data.textalias[j])
    
def redrawall(canvas, data):    
    for i in range(len(data.hypertext)):
        if len(data.hypertext[i]) != 0:
            for hyper in data.hypertext[i]:
                canvas.create_line(hyper.loc, data.syntext[i].loc, 
                                   width=0.1, fill='grey')
                hyper.viscircle(canvas, hyper.radius)
                hyper.draw(canvas)
                hyper.cirhighlight(canvas)
                

    for i in range(len(data.syntext)):
        if isinstance(data.syntext[i], list):
            for syn in data.syntext[i]:
                canvas.create_line(syn.loc, data.postext[i].loc, 
                                   width=0.1, fill='grey')
                syn.viscircle(canvas, syn.radius)
                syn.draw(canvas)
                syn.cirhighlight(canvas)
        else:
            canvas.create_line(data.syntext[i].loc, data.postext[i].loc, 
                                   width=0.1, fill='grey')
            data.syntext[i].viscircle(canvas, data.syntext[i].radius)
            data.syntext[i].draw(canvas)

    for text in data.postext:
        canvas.create_line(text.loc, data.source.loc, width=0.1, fill='grey')
        text.viscircle(canvas, text.radius)
        text.draw(canvas)

    data.source.viscircle(canvas, data.source.radius)
    data.source.draw(canvas)

    for defs in data.deftext:
        if not isinstance(defs, list):
            defs.show(canvas)
        else:
            for hyperdef in defs:
                if hyperdef != None: hyperdef.show(canvas)

    for button in data.guielem:
        button.draw(canvas)
    
# lexigraph local data
data = program.struct()    