########################################
# main function
########################################
'''
main function initializes all program, runs
the program and controls various mode switch
'''
from tkinter import*
from nltk.corpus import wordnet
from objectLib import*
import program
import search, dictionary, lexigraph, explore, pair, archive
pgrmData = program.data

########################################
# mode dispatcher
########################################


def initMode(pgrmData):
    '''
    initiate data in the current mode
    '''

    if pgrmData.initMode:
        mode = eval(pgrmData.mode)
        mode.init(mode.data, pgrmData)

def mouseHovered(event, pgrmData):
    '''
    call mouseHovered() from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.mouseHovered(event, mode.data, pgrmData)
    program.mouseHovered(event, pgrmData)

def mouseReleased(event, pgrmData):
    '''
    call mouseReleased() from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.mouseReleased(event, mode.data, pgrmData)

def mouseScrolled(event, pgrmData):
    '''
    call mouseScrolled() from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.mouseScrolled(event, mode.data, pgrmData)

def mouseDragged(event, pgrmData):
    '''
    call mouseDragged() from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.mouseDragged(event, mode.data, pgrmData)

def mousePressed(event, pgrmData):
    '''
    call mousePressed() from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.mousePressed(event, mode.data, pgrmData)
    program.mousePressed(event, pgrmData)

def keyPressed(event, pgrmData):
    '''
    call keyPressed() from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.keyPressed(event, mode.data, pgrmData)

def timerFired(pgrmData):
    '''
    call timerFired from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.timerFired(mode.data, pgrmData)

def redrawAll(canvas, pgrmData):
    '''
    call redrawAll from the current mode
    '''
    initMode(pgrmData)
    mode = eval(pgrmData.mode)
    mode.redrawAll(canvas, mode.data)
    program.redrawAll(canvas, pgrmData)

########################################
# adapted from course VMC framework
########################################

def run(width=300, height=300):
    '''
    main function that runs the program
    '''
    def redrawAllWrapper(canvas, pgrmData):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, pgrmData.width, pgrmData.height,
                                fill=pgrmData.bgColr, width=0)
        redrawAll(canvas, pgrmData)
        canvas.update()    

    def mouseHoveredWrapper(event, canvas, pgrmData):
        mouseHovered(event, pgrmData)

    def mouseReleasedWrapper(event, canvas, pgrmData):
        mouseReleased(event, pgrmData)
        redrawAllWrapper(canvas, pgrmData)

    def mouseDraggedWrapper(event, canvas, pgrmData):
        pgrmData.B1Release = False
        mouseDragged(event, pgrmData)
        redrawAllWrapper(canvas, pgrmData)

    def mouseScrolledWrapper(event, canvas, pgrmData):
        mouseScrolled(event, pgrmData)
        redrawAllWrapper(canvas, pgrmData)

    def mousePressedWrapper(event, canvas, pgrmData):
        mousePressed(event, pgrmData)
        redrawAllWrapper(canvas, pgrmData)

    def keyPressedWrapper(event, canvas, pgrmData):
        keyPressed(event, pgrmData)
        redrawAllWrapper(canvas, pgrmData)

    def timerFiredWrapper(canvas, pgrmData):
        timerFired(pgrmData)
        redrawAllWrapper(canvas, pgrmData)
        # pause, then call timerFired again
        canvas.after(pgrmData.timerDelay, timerFiredWrapper,
                     canvas, pgrmData)

    # init pgrmData
    program.init(pgrmData)
    pgrmData.width = width
    pgrmData.height = height
    pgrmData.timerDelay = 100 # milliseconds

    # cite: https://stackoverflow.com/questions/18537918/set-window-icon
    root = Tk(className = ' Lexigraph')
    root.iconbitmap('assets/icon.ico')
    root.resizable(width=False, height=False)
    root.geometry(f"{pgrmData.width}x{pgrmData.height}+200+200")

    # create the root and the canvas
    canvas = Canvas(root, width=pgrmData.width, height=pgrmData.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

    # set up events
    # https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter
    root.bind("<Motion>", lambda event:
                            mouseHoveredWrapper(event, canvas, pgrmData))
    root.bind("<B1-Motion>", lambda event:
                            mouseDraggedWrapper(event, canvas, pgrmData))
    root.bind('<ButtonRelease-1>', lambda event:
                            mouseReleasedWrapper(event, canvas, pgrmData))
    root.bind("<MouseWheel>", lambda event:
                            mouseScrolledWrapper(event, canvas, pgrmData))
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, pgrmData))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, pgrmData))
    timerFiredWrapper(canvas, pgrmData)

    # and launch the app
    root.mainloop()  # blocks until window is closed
    # save user data here
    print("program ended")

run(1400, 1000)