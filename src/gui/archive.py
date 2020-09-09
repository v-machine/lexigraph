########################################
# mode: archive
########################################
'''
archive of all past searched vocabulary
links to lexigrah view when clicked on architeved words
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
    data.scrollY = 0
    data.scrollSpeed = 10
    data.guiElem = createGuiElem(data, pgrmData)
    data.newWords = program.getNewWords(pgrmData)
    data.archivedWords = createArchivedWords(data, pgrmData)
    pgrmData.initMode = False    # init once only

def createGuiElem(data, pgrmData):
    '''
    create GUI element in archive
    '''
    elems = []
    x, y = pgrmData.marginCenLeft, pgrmData.marginCenTop
    space = 40
    options = ['// archivedbetical', '// by level', '// randomized']
    for opt in options:
        button = ClickText(name=opt, loc=(x, y+space), size=20, font='helvetica',
                           colr=pgrmData.txtColr, anchor='sw')
        elems.append(button)
        space += 50
    return elems

def createArchivedWords(data, pgrmData):
    archivedWords = []
    cols = 5
    gridSize = (pgrmData.width-pgrmData.marginCenLeft)//cols
    i = 0
    for word in sorted(list(data.newWords)):
        x = pgrmData.marginCenLeft+gridSize*0.25+gridSize*(i%cols)
        y = pgrmData.height-gridSize*(1+i//cols)
        newWordText = MovingText(word, loc=[x, y], size=25, colr=pgrmData.txtColr,
                                     font='AGaramondPro-Regular', radius=40)
        archivedWords.append(newWordText)
        i += 1
    return archivedWords

def mouseHovered(event, data, pgrmData): 
    for text in data.archivedWords:
        text.hover(event)

def mouseScrolled(event, data, pgrmData):
    '''
    controls vertical mouse scroll
    '''
    scrollY, scrollSpeed = data.scrollY, data.scrollSpeed
    if event.delta > -1: scrollY += scrollSpeed
    if event.delta < 1: scrollY -= scrollSpeed
    for text in data.archivedWords:
        x, y = text.loc
        text.loc = (x, y+scrollY)

def mouseDragged(event, data, pgrmData): pass

def mouseReleased(event, data, pgrmData): pass

def mousePressed(event, data, pgrmData):
    for text in data.archivedWords:
        if text.click(event):
            pgrmData.searchWord = text.name
            pgrmData.mode = 'lexigraph'
            pgrmData.initMode = True
    
def keyPressed(event, data, pgrmData): pass

def timerFired(data, pgrmData): pass

def redrawAll(canvas, data): 
    for text in data.archivedWords:
        text.visCircle(canvas, text.radius)
        text.draw(canvas)
        text.cirHighlight(canvas)
data = program.Struct()