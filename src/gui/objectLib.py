#################################################
# object library
#################################################

import random
import string
import math
from core.wordFreqency import wordFreqDict

class Circle(object):
    def __init__(self, loc, radius, colr):
        self.loc = loc
        self.radius = radius
        self.blink = True
        self.colr = colr
        self.margin = 30

    def update(self, text):
        '''
        changing radius based on hosted text
        '''
        if text != None:
            textWidth = (text.bbox[2]-text.bbox[0])*0.5+self.margin
            self.radius = max(75, textWidth)

    def draw(self, canvas):
        loc, r, colr = self.loc, self.radius, self.colr
        canvas.create_oval(loc[0]-r, loc[1]-r, loc[0]+r, loc[1]+r, 
                           width=0, fill=colr)

class Cursor(object):
    def __init__(self, loc, size, colr):
        self.loc = loc
        self.size = size    # size is also height
        self.width = size*0.005
        self.blink = True
        self.colr = colr

    def update(self, text):
        self.loc = (text.bbox[2], text.bbox[3])
        self.size = text.bbox[3]-text.bbox[1]

    def cursorBlink(self, data):
        # cursor blinks every half second
        if data.timer%5 == 0: self.blink = not self.blink  

    def draw(self, canvas):
        if self.blink:
            canvas.create_rectangle(self.loc[0]-self.width, self.loc[1],
                                    self.loc[0]+self.width, self.loc[1]-self.size,
                                    width=0, fill=self.colr)

####  graphical text classes  ####

class Text(object):
    def __init__(self, name, loc, size, font, colr, anchor, width=600):
        self.name = name
        self.loc = loc
        self.size = size
        self.font = font
        self.colr = colr
        self.anchor = anchor
        self.width = width
        self.ID = None      # canvas object id
        self.bbox = None    # bounding box corners
        self.highlightBox = None
        self.highlightCir = None
        self.hovered = False
        self.margin = 10

    def getBbox(self, canvas):
        '''
        returns the two corner cordinates of the bounding box
        '''
        boundingBox = canvas.bbox(self.ID)
        return boundingBox
        
    def draw(self, canvas):
        # cite: https://stackoverflow.com/questions/18800860/
        #             dynamic-sizing-tkinter-canvas-text
        self.ID = canvas.create_text(self.loc, text=self.name, fill=self.colr, 
                                     width=self.width, anchor=self.anchor,
                                     font=self.font+' '+str(self.size))
        self.bbox = self.getBbox(canvas)
        self.radius = (self.bbox[2]-self.bbox[0])*0.5+self.margin

    def visCircle(self, canvas, radius):
        circleBound = self.loc[0]-radius, self.loc[1]-radius,\
                      self.loc[0]+radius, self.loc[1]+radius 
        canvas.create_oval(circleBound, width=0, fill='white')

    def hover(self, event):
        x1, y1, x2, y2 = self.bbox
        if (x1 <= event.x <= x2) and (y1 <= event.y <= y2):
            self.hovered = True
        else: 
            self.hovered = False
        return self.hovered

    #### need to overwrite equality check ####
    # identical synonym are treated as same
    # def __eq__(self):
    #     pass

    # def __hash__(self):
    #     pass

class TypedText(Text):
    def __init__(self, loc, size, font, colr, anchor, width=1000):
        name = ''
        super().__init__(name, loc, size, font, colr, anchor, width)
        self.enter = False

    def update(self, event, data, pgrmData):
        if event.keysym in string.ascii_letters:
            self.name += event.keysym
        if event.keysym == 'space':
            self.name += ' '
        if event.keysym == 'BackSpace':
            self.name = self.name[:-1]
        if event.keysym == 'Return':
            self.enter = True

class ClickText(Text):
    def __init__(self, name, loc, size, font, colr, anchor, width=600):
        super().__init__(name, loc, size, font, colr, anchor, width)
        self.clicked = False

    def click(self, event):
        x1, y1, x2, y2 = self.bbox
        if (x1 <= event.x <= x2) and (y1 <= event.y <= y2):
            self.clicked = not self.clicked
        return self.clicked

    def highlight(self, canvas):
        if self.clicked:
            self.highlightBox = canvas.create_rectangle(self.bbox, width=0, fill='yellow')
            self.draw(canvas)
        else:
            # cite: https://stackoverflow.com/questions/23690993/how-do-we-
            # delete-a-shape-thats-already-been-created-in-tkinter-canvas
            canvas.delete(self.highlightBox)

    def cirHighlight(self, canvas):
        if self.clicked or self.hovered:
            r = (self.bbox[2]-self.bbox[0])*0.5+self.margin
            cir = (self.loc[0]-r, self.loc[1]-r, self.loc[0]+r, self.loc[1]+r)

            self.highlightCir = canvas.create_oval(cir, width=0, fill='blue')
            self.colr = 'white'
            self.draw(canvas)
        else:
            self.colr = 'blue'
            canvas.delete(self.highlightCir)

class MovingText(ClickText):
    def __init__(self, name, loc, size, font, colr, radius):
        anchor = 'center'   # applies to all MovingText
        super().__init__(name, loc, size, font, colr, anchor)
        self.radius = radius
        self.speed = [random.randint(-1,1), random.randint(-1,1)]

    def move(self):
        minSpeed, maxSpeed = -10, 10
        self.speed[0] = min(self.speed[0], maxSpeed)
        self.speed[0] = max(self.speed[0], minSpeed)
        self.speed[1] = min(self.speed[1], maxSpeed)
        self.speed[1] = max(self.speed[1], minSpeed)
        self.loc[0] += self.speed[0]
        self.loc[1] += self.speed[1]

    def wallBounce(self, data):
        '''
        change direction if self collides with canvas boundary
        '''
        if self.loc[0] >= data.width-self.radius: self.speed[0] *= -10
        if self.loc[0] <= self.radius: self.speed[0] *= -10
        if self.loc[1] >= data.height-self.radius: self.speed[1] *= -10
        if self.loc[1] <= self.radius: self.speed[1] *= -10

    def wallBounce2(self, data):
        '''
        change direction if self collides with canvas boundary
        '''
        if self.loc[0] >= data.width-self.radius: self.speed[0] *= -.1
        if self.loc[0] <= self.radius: self.speed[0] *= -.1
        if self.loc[1] >= data.height-self.radius: self.speed[1] *= -.1
        if self.loc[1] <= self.radius: self.speed[1] *= -.1

    def bounce(self, other):
        '''
        change direction if self collides with canvas boundary
        '''
        if self.collision(other):
            self.speed[0] += (self.loc[0]-other.loc[0])*(other.radius/self.radius)*.2
            self.speed[1] += (self.loc[1]-other.loc[1])*(other.radius/self.radius)*.2
            other.speed[0] += (other.loc[0]-self.loc[0])*(self.radius/other.radius)*.2
            other.speed[1] += (other.loc[1]-self.loc[1])*(self.radius/other.radius)*.2
        else:
            self.speed[0] *= 0.995
            self.speed[1] *= 0.995

    def bounce2(self, other):
        '''
        change direction if self collides with canvas boundary
        '''
        if self.collision(other):
            self.speed[0] += (self.loc[0]-other.loc[0])*(other.radius/self.radius)*.2
            self.speed[1] += (self.loc[1]-other.loc[1])*(other.radius/self.radius)*.2
            other.speed[0] += (other.loc[0]-self.loc[0])*(self.radius/other.radius)*.2
            other.speed[1] += (other.loc[1]-self.loc[1])*(self.radius/other.radius)*.2

    def attract(self, other):
        '''
        if self is too far from other, move towards other
        '''
        pass
        # if self.distance(other) >= self.radius+other.radius:
        #     attrX = (other.loc[0]-self.loc[0])*10
        #     attrY = (other.loc[1]-self.loc[1])*10
        # else:
        #     self.speed[0] *= 0.5
        #     self.speed[1] *= 0.5

    def collision(self, other):
        '''
        returns true if self collides with other, else false
        '''
        return self.distance(other) <= self.radius+other.radius

    def distance(self, other):
        '''
        returns the distance between self and other
        '''
        return ((self.loc[0]-other.loc[0])**2+\
                (self.loc[1]-other.loc[1])**2)**0.5

class BoxText(Text):
    def __init__(self, name, loc, size, font, colr, anchor, width=150):
        super().__init__(name, loc, size, font, colr, anchor, width)
        self.showed = False
        self.text1 = None
        self.text2 = None

    def follow(self, other):
        self.loc[0] = other.loc[0]-20
        self.loc[1] = other.loc[1]-40

    def highlight(self, canvas):
        x1, y1, x2, y2 = self.bbox
        margin = 5
        self.highlightBox = canvas.create_rectangle(x1-margin,y1-margin, x2+margin, y2+margin, 
                                                    width=0, fill='blue')
        p1 = (self.loc[0]+20, self.loc[1])
        p2 = (self.loc[0]+20, self.loc[1]+40)
        p3 = (self.loc[0]+40, self.loc[1])
        canvas.create_polygon(p1,p2,p3,width=0, fill='blue')

    def show(self, canvas):
        if self.showed:
            self.text1 = self.draw(canvas)
            self.highlight(canvas)
            self.text2 = self.draw(canvas)
        else:
            canvas.delete(self.text1)
            canvas.delete(self.text2)
            canvas.delete(self.highlightBox)

####  vocabulary classes  ####

class Word(object):
    def __init__(self, name):
        self.name = name
        self.pos = []
        self.defs = []
        self.syns = []  # list of sets
        self.ants = []  # list of sets
        self.concepts = []
        self.freqRank = self.getFreqRank()
        self.level = None
        self.timesSeen = 0
        self.errorCount = 0

    def getSynonyms(self):
        '''
        returns all synonyms of the word in a set
        '''
        allSyns = set()
        for s in self.syns:
            allSyns |= (s[2]) if isinstance(s, list) else allSyns | s
        return allSyns

    def getAntonyms(self):
        '''
        returns all antonym of the word in a set
        '''
        allAnts = set()
        for s in self.ants:
            allAnts |= (s[2]) if isinstance(s, list) else allAnts | s
        return allAnts

    def getFreqRank(self):
        return wordFreqDict.get(self.name, None)

    def masterlvl(self):
        '''
        update level based on self.seen, self.errorCount
        'expert', 'familiar', 'average', 'aquainted', 'new', 'unseen.
        '''
        level = 0
        self.known = level

class LexicalGraph(object):
    def __init__(self):
        self.graph = dict()

    def storeInGraph(self, word):
        '''
        store a new word into lexigraph
        '''
        self.graph[word.name] = word

class User(object):
    def __init__(self, name):
        self.name = name
        self.level = 0
        self.startDate = ''
        self.lastOpened = ''
        self.lexigraph = LexicalGraph()
        self.wordList = {'expert': set(), 'familiar': set(), 'average': set(),
                         'aquainted': set(), 'fresh':set(), 'unseen':set()}
        # self.defaultWords = {'the', 'a', 'this'}
        # self.wordList['familiar'].update(self.defaultWords)

        ####  dummy test data  ####
        
        # testFreshWords = {'impervious', 'inundate', 'ambiguous', 'eloquent', 
        #                   'occlude', 'monotony', 'inimical', 'estimable', 
        #                    'mitigate', 'garrulous'}
        # testFamiliarWords = {'imperviable', 'flood', 'equivocal', 'fluent', 
        #                   'obstruct', 'sameness'}
        # testAverageWords = {'unfriendly', 'computable', 'minify', 'talkative'}
        # self.wordList['fresh'].update(testFreshWords)
        # self.wordList['familiar'].update(testFamiliarWords)
        # self.wordList['average'].update(testAverageWords)
