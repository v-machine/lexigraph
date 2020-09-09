########################################
# mode: dictionary
########################################
'''
displays search result in dictionary
'''
import program
from objectLib import*
pgrmData = program.data

def init(data, pgrmData):
    '''
    initiate data in the current mode
    '''
    ####  layout  ####
    x, y = pgrmData.marginCenLeft, pgrmData.marginCenTop
    space = 150
    data.scrollY = 0
    data.scrollSpeed = 10
    data.vocab = Text(pgrmData.searchWord, loc=(x,y), size=50, 
                      font='AGaramondPro-Bold', colr=pgrmData.txtColr, anchor='nw')
    pgrmData.dictData = program.getDictData(pgrmData)

    # creating definition paragraph
    defParagraph = ''
    for meaning in pgrmData.dictData:
        defParagraph += pgrmData.dictData[meaning] +'\n'+meaning+'\n'*2
    data.defns = Text(defParagraph, (x, y+space), size=20, 
                      font='AGaramondPro-Regular', colr=pgrmData.txtColr, anchor='nw')
    pgrmData.initMode = False    # init once only

def drawGuiElem(canvas, data, pgrmData):
    '''
    fixed gui element in dictionary
    '''
    width, height = pgrmData.width, pgrmData.height
    canvas.create_rectangle(0,0, width, 350,
                            fill=pgrmData.bgColr, width=0)
    canvas.create_rectangle(width-50, height-50, width, height, 
                            fill=pgrmData.bgColr, width=0)


def mouseHovered(event, data, pgrmData): pass

def mouseScrolled(event, data, pgrmData):
    '''
    controls vertical mouse scroll
    '''
    scrollY, scrollSpeed = data.scrollY, data.scrollSpeed
    if event.delta > -1: scrollY += scrollSpeed
    if event.delta < 1: scrollY -= scrollSpeed
    explX, explY = data.defns.loc
    data.defns.loc = (explX, explY+scrollY)

def mouseDragged(event, data, pgrmData): pass

def mouseReleased(event, data, pgrmData): pass

def mousePressed(event, data, pgrmData): pass

def keyPressed(event, data, pgrmData): pass

def timerFired(data, pgrmData): pass
    
def redrawAll(canvas, data):
    data.defns.draw(canvas)
    drawGuiElem(canvas, data, pgrmData)
    data.vocab.draw(canvas)

data = program.Struct()