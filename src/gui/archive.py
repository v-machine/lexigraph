########################################
# mode: archive
########################################
'''
archive of all past searched vocabulary
links to lexigrah view when clicked on architeved words
'''
from core import program
import random
import string
import requests
from gui.objectLib import*
pgrmdata = program.data

def init(data, pgrmdata):
    '''
    initiate data in the current mode
    '''
    data.scrolly = 0
    data.scrollspeed = 10
    data.guielem = createguielem(data, pgrmdata)
    data.newwords = program.getnewwords(pgrmdata)
    data.archivedwords = createarchivedwords(data, pgrmdata)
    pgrmdata.initmode = False    # init once only

def createguielem(data, pgrmdata):
    '''
    create gui element in archive
    '''
    elems = []
    x, y = pgrmdata.margincenleft, pgrmdata.margincentop
    space = 40
    options = ['// archivedbetical', '// by level', '// randomized']
    for opt in options:
        button = ClickText(name=opt, loc=(x, y+space), size=20, font='helvetica',
                           colr=pgrmdata.txtcolr, anchor='sw')
        elems.append(button)
        space += 50
    return elems

def createarchivedwords(data, pgrmdata):
    archivedwords = []
    cols = 5
    gridsize = (pgrmdata.width-pgrmdata.margincenleft)//cols
    i = 0
    for word in sorted(list(data.newwords)):
        x = pgrmdata.margincenleft+gridsize*0.25+gridsize*(i%cols)
        y = pgrmdata.height-gridsize*(1+i//cols)
        newwordtext = MovingText(word, loc=[x, y], size=25, colr=pgrmdata.txtcolr,
                                     font='agaramondpro-regular', radius=40)
        archivedwords.append(newwordtext)
        i += 1
    return archivedwords

def mousehovered(event, data, pgrmdata): 
    for text in data.archivedwords:
        text.hover(event)

def mousescrolled(event, data, pgrmdata):
    '''
    controls vertical mouse scroll
    '''
    scrolly, scrollspeed = data.scrolly, data.scrollspeed
    if event.delta > -1: scrolly += scrollspeed
    if event.delta < 1: scrolly -= scrollspeed
    for text in data.archivedwords:
        x, y = text.loc
        text.loc = (x, y+scrolly)

def mousedragged(event, data, pgrmdata): pass

def mousereleased(event, data, pgrmdata): pass

def mousepressed(event, data, pgrmdata):
    for text in data.archivedwords:
        if text.click(event):
            pgrmdata.searchword = text.name
            pgrmdata.mode = 'lexigraph'
            pgrmdata.initmode = True
    
def keypressed(event, data, pgrmdata): pass

def timerfired(data, pgrmdata): pass

def redrawall(canvas, data): 
    for text in data.archivedwords:
        text.viscircle(canvas, text.radius)
        text.draw(canvas)
        text.cirhighlight(canvas)
data = program.struct()