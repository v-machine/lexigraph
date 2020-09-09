########################################
# mode: search
########################################
'''
search function allowing users to search words
'''
import program
import string
from objectLib import*
pgrmData = program.data

def init(data, pgrmData):
    '''
    initiate data in the current mode
    '''
    x, y = pgrmData.width//2, pgrmData.height//2
    data.timer = 0
    data.cursor = Cursor((x, y), size=0, colr='white')
    data.text = TypedText((x, y), size=55, colr='white',
                          font='AGaramondPro-Regular', anchor='center')
    data.circle = Circle((x, y), radius=75, colr=pgrmData.masterColr)
    pgrmData.initMode = False    # init once only

def mouseHovered(event, data, pgrmData): pass

def mouseScrolled(event, data, pgrmData): pass

def mouseDragged(event, data, pgrmData): pass

def mouseReleased(event, data, pgrmData): pass

def mousePressed(event, data, pgrmData): pass

def keyPressed(event, data, pgrmData):
    data.text.update(event, data, pgrmData)
    if data.text.enter:
        data.transition = True
        pgrmData.mode = 'lexigraph'
        pgrmData.initMode = True
        pgrmData.searchWord = data.text.name.replace(' ', '_')
        pgrmData.user.wordList['fresh'].add(pgrmData.searchWord)

def timerFired(data, pgrmData):
    data.timer += 1
    data.cursor.cursorBlink(data)


def redrawAll(canvas, data):
    # data.cirAnimation.draw(canvas)
    data.circle.draw(canvas)
    data.cursor.draw(canvas)
    data.text.draw(canvas)
    data.cursor.update(data.text)
    data.circle.update(data.text)

data = program.Struct()