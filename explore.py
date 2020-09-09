########################################
# mode: explore
########################################
'''
display word/ sentence of the day based
either on automated word recommendation
or on users's recently learned words
'''

import program
import string
import requests
from bs4 import BeautifulSoup
from objectLib import*
pgrmData = program.data

def getSentence(word):
    '''
    returns a recent web example sentence (scraped from
    marriam webster) and its source of a given word
    '''
    # cite: https://kaijento.github.io/2017/05/13/
    #               web-scraping-merriam-webster.com/
    # tutorial: https://www.youtube.com/watch?v=ng2o98k983k
    url = 'https://www.merriam-webster.com/dictionary/'
    url += word
    r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'lxml')
    sentence = soup.find('span', 'ex-sent sents', class_='t has-aq').text.strip()
    source = soup.find('span', 'ex-sent sents', class_='aq has-aq').text.strip()
    # cite: https://stackoverflow.com/questions/1546226/
    #       simple-way-to-remove-multiple-spaces-in-a-string
    source = ' '.join(source.split())    
    return (sentence, source)

def init(data, pgrmData):
    '''
    initiate data in the current mode
    '''
    if pgrmData.searchWord != '':
        data.recomWord = pgrmData.searchWord
    else:
        data.recomWord = 'default'
    data.example = getSentence(data.recomWord)
    x1, y1 = pgrmData.marginCenLeft, pgrmData.height/2-100
    data.sentence = Text(name=data.example[0], loc=[x1, y1], colr=pgrmData.txtColr,
                         size=30, font='AGaramondPro-Regular', anchor='w', width=900)
    x2, y2 = x1, pgrmData.height+200
    data.source = Text(name=data.example[1], loc=[x2, y2], colr=pgrmData.txtColr,
                       size=20, font='AGaramondPro-Italic', anchor='w', width=900)
    pgrmData.initMode = False    # init once only

def drawExample(canvas, data):
    data.sentence.draw(canvas)
    data.source.draw(canvas)
    x1, y1, x2, y2 = data.sentence.bbox[0], data.sentence.bbox[3]+50, \
                     data.sentence.bbox[2], data.sentence.bbox[3]+50, 
    canvas.create_line(x1, y1, x2, y2, width=0.5, fill='blue')
    data.source.loc[1] = data.sentence.bbox[3] + 100

def mouseHovered(event, data, pgrmData): pass

def mouseScrolled(event, data, pgrmData): pass

def mouseDragged(event, data, pgrmData): pass

def mouseReleased(event, data, pgrmData): pass

def mousePressed(event, data, pgrmData): pass

def keyPressed(event, data, pgrmData): pass

def timerFired(data, pgrmData): pass

def redrawAll(canvas, data):
    drawExample(canvas, data)
    
data = program.Struct()