from Tkinter import *
from PIL import ImageTk, Image
import tkFont, os, time, serial
import math as m
import mysql.connector as sql
import numpy as np

# global variables
stopVal = True
err = 2.5 # NOTE: This is +/- 2.5 deg error in the direction (accuracy of node)
highHeat = 0
def lowHeat():
    return int(highHeat * .35) # NOTE: smaller values increase proportion of heatmap displayed
colorScale = ((0,0,255),(0,128,255),(0,255,255),(0,255,128),(0,255,0),(128,255,0),(255,255,0),(255,128,0),(255,0,0)) # TODO: Possibly add more colors?

try:
    cnx = sql.connect(user='tkinter', password='password', host='127.0.0.1', database='redhawk')
    cursor = cnx.cursor()
except:
    print "Tkinter code cannot connect to mySQL database"

# global test cases
gridCoord = "12345 67890"
numNodes = 0

#________________________ MAP CALIBRATION CODE ________________________
# TODO: Add all this to a config.txt file
# map 1
mapPath1 = os.path.join(os.path.dirname(__file__), 'Plain.png') #fixed relative filepath errors
#mapPath1 = r'C:\Users\x73395\Documents\GitHub\Red-Hawk\GUI\Plain.png'
gridDim1 = 118 #each grid square is 118 x 118 pixels (with PIL resize)
startingGrid1 = (85500,83500) #first grid at top left of map
startingPixel1 = (72,66) #cooresponding first pixel of startingGrid1
maxX1 = 87700
minX1 = 85500
maxY1 = 83500
minY1 = 82000

# global map variables
img = Image.open(mapPath1)

#________________________ GEO-LOCATION CODE ________________________
grid = np.zeros((img.size[0],img.size[1]))
index = np.indices((img.size[0],img.size[1])).swapaxes(0,2).swapaxes(0,1)

# return grid X index of cooresponding map coordinate
def getGridX(xCoord):
    val = 0
    if (xCoord > maxX1):
        val = maxX1
    elif (xCoord < minX1):
        val = minX1
    else:
        val = xCoord
    return int((((val - startingGrid1[0]) / 100.) * gridDim1) + startingPixel1[0])

# return grid Y index of cooresponding map coordinate
def getGridY(yCoord):
    if (yCoord > maxY1):
        val = maxY1
    elif (yCoord < minY1):
        val = minY1
    else:
        val = yCoord
    return int(startingPixel1[1] - (((val - startingGrid1[1]) / 100.) * gridDim1))

# find the center of the 'red zone' in the heatmap.  This is an extremely naive approach
def getCenter():
    #t0 = time.time()
    vals = tuple(map(tuple,index[np.where(grid == np.amax(grid))]))
    #print "vals: " + str(time.time()-t0)
    x = 0
    y = 0
    c = 0
    #t0 = time.time()
    for n, m in vals:
        x += n
        y += m
        c += 1
    #print "loop: " + str(time.time()-t0)
    avgX = x/c
    avgY = y/c

    centerX = int( ( ( (avgX - startingPixel1[0] ) / (1.0 * gridDim1) ) * 100 ) + startingGrid1[0] )
    centerY = int( ( ( (avgY - startingPixel1[1] ) / (1.0 * gridDim1) ) * -100 ) + startingGrid1[1] )
    centerCoord.set(str(centerX)+"  "+str(centerY))

# return the correct color value based on the global scale, use of len() to allow for explanded scale later
def heat(val):
    heatRange = highHeat - lowHeat()
    segment = float(heatRange) / len(colorScale)
    selection = int((val - lowHeat()) / segment)
    return colorScale[selection - 1]

#iterate over the coord that are above the lowHeat threshold and 'paint' the display
def updateMap():
    #t1 = time.time()
    global img, mapArea, highHeat
    img2 = img.copy()
    pix = img2.load()

    temp = tuple(map(tuple,index[np.where(grid > lowHeat())]))
    testVal = tuple(grid[np.where(grid > lowHeat())])

    for (a,b) in zip(temp,testVal):
        pix[a[0],a[1]] = heat(b)
    getCenter()
    imgResize2 = img2.resize((1000, 705), Image.ANTIALIAS)
    imgDisplay2 = ImageTk.PhotoImage(imgResize2)
    mapArea.configure(image = imgDisplay2)
    mapArea.image = imgDisplay2
    #print "update: " + str(time.time()-t1)
    #print ""

# Take the 3-tuple from the nodes and plot the cone of probable location on the number array
# NOTE: uses global err to plot area of cone, theis was a theoretical +/- 2.5 degrees, but may be larger
# TODO: reduce many if statements into legitimate looking code
# TODO: I believe there may be a way to only call m.tan() once.  Find the two points where the edges of the cone meet the
#       boundary of the map, then find the two linear equations (from origin to high boundary / low boundary) to determine
#       a y value at a given x or vise versa.
def plot(xCoord,yCoord,direction):
    global highHeat, numNodes, numPackets
    numNodes += 1
    numPackets.set(numNodes)
    step = 0

    if ((direction >= 0 and direction < 45) or (direction >= 315 and direction < 360)):
        xValTop = m.tan(m.radians(direction + err))
        xValBot = m.tan(m.radians(direction - err))
        while (yCoord + step < maxY1):
            XVAR1 = getGridX(int(xValBot*step) + xCoord)
            XVAR2 = getGridX(int(xValTop*step) + xCoord)
            grid[XVAR1:XVAR2,getGridY(yCoord + step)] += 1
            step += 1
        highHeat = np.amax(grid)

    if (direction >= 45 and direction < 135):
        direction = 90 - direction
        yValTop = m.tan(m.radians(direction + err))
        yValBot = m.tan(m.radians(direction - err))
        while (xCoord + step < maxX1):
            YVAR1 = getGridY(int(yValTop*step) + yCoord)
            YVAR2 = getGridY(int(yValBot*step) + yCoord)
            grid[getGridX(xCoord + step),YVAR1:YVAR2] += 1
            step += 1
        highHeat = np.amax(grid)

    if (direction >= 135 and direction < 225):
        direction = 180 - direction
        xValTop = m.tan(m.radians(direction + err))
        xValBot = m.tan(m.radians(direction - err))
        while (yCoord - step > minY1):
            XVAR1 = getGridX(int(xValBot*step) + xCoord)
            XVAR2 = getGridX(int(xValTop*step) + xCoord)
            grid[XVAR1:XVAR2,getGridY(yCoord - step)] += 1
            step += 1
        highHeat = np.amax(grid)

    if (direction >= 225 and direction < 315):
        direction = direction - 90
        yValTop = m.tan(m.radians(direction + err))
        yValBot = m.tan(m.radians(direction - err))
        while (xCoord - step > minX1):
            YVAR1 = getGridY(int(yValTop*step) + yCoord)
            YVAR2 = getGridY(int(yValBot*step) + yCoord)
            grid[getGridX(xCoord - step),YVAR1:YVAR2] += 1
            step += 1
        highHeat = np.amax(grid)

# Helper function to call main loop
def start():
    global stopVal
    stopVal = False
    read()
    #use to fill mySQL db with test cases, comment out read() above
    #cursor.execute("INSERT INTO data(xCoord, yCoord, dir) VALUES (86500,82800,0),(86500,82800,45),(86500,82800,90),(86500,82800,135),(86500,82800,180),(86500,82800,225),(86500,82800,270),(86500,82800,315)")
    #cnx.commit()

# Helper function to stop main loop
def stop():
    global stopVal
    stopVal = True

# Main loop
# NOTE: must use the .after() to schedule the iterations as the tkinter main loop will never update with an embedded infinite loop
def read():
    global stopVal, numNodes
    cursor.execute("SELECT * FROM data LIMIT 1")
    val = cursor.fetchone()
    cnx.commit() # needed after empty query return

    if (val != None):
        plot(val[1], val[2], val[3])
        if (numNodes % 1 == 0): #change this to change frequency of GUI update
            updateMap()
        cursor.execute("DELETE FROM data WHERE id = %s" % val[0])
        cnx.commit()

    if (not stopVal):
        root.after(100,read)


#***************************************************************************************
#************************************* T E S T *****************************************
#************************************* C O D E *****************************************
#***************************************************************************************
count = 0
# test plot
node = ((86000,82000,45),(86000,82100,41),(86000,82200,37),(86000,82300,33),(86000,82400,29),(86000,82500,27),(86900,82000,80),(86800,82000,75),(86700,83000,0),(86700,82900,7))
# test plot
node1 = ((86000,83000,180),(86000,83000,190),(86000,83000,65),(86000,83000,90),(86000,83000,100),(86000,83000,110),(86000,83000,120))
# test plot in all quandrants
node2 = ((86500,82800,0),(86500,82800,45),(86500,82800,90),(86500,82800,135),(86500,82800,180),(86500,82800,225),(86500,82800,270),(86500,82800,315))
# time test worst case plotting
node3 = ((86600,83500,180),(87700,83500,236),(87700,82700,270),(87700,82000,304),(86600,82000,0),(85500,82000,56),(85500,82700,90),(85500,83500,124))

node4 = ((86500,82100,0),(86371,82228,10),(86242,82357,23),(86114,82485,38),(85985,82614,53),(85857,82742,67),(85728,82871,79),(85600,83000,90))

#test function
def testPlot():
    for x in node4:
        plot(x[0],x[1],x[2])
    updateMap()

    u2time = 0
    #print "Timing plot1() over 30 iterations"
    for x in range(0):
        t0 = time.time()
        for x in node4:
            plot(x[0],x[1],x[2])
        t1 = time.time()
        u2time += (t1-t0)
    root.update()
    #print "Plot1 total time: %.3f seconds" % (u2time)
    #print "Plot1 average time: %.3f seconds\n" % (u2time/30)

#***************************************************************************************
#***************************************************************************************
#***************************************************************************************
#***************************************************************************************


#________________________ GUI CODE ________________________
# NOTE: couldn't decide on final look of the GUI.  Also, tkinter sucks.  Switch to .pack for better results
root = Tk()
root.title('REDHAWK-3')
#root.geometry('1000x600')
#root.minsize(width=1000, height=600)

def closeEvent():
    stop()
    try:
        cursor.close()
        cnx.close()
    except:
        pass
    img.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", closeEvent)

# fonts:
helv22 = tkFont.Font(family='Helvetica',size=22, weight=tkFont.BOLD)
redHawkColor = '#b30000'
numPackets = IntVar()
centerCoord = StringVar()
centerCoord.set("*****  *****")

menubar = Menu(root)
plotMenu = Menu(menubar, tearoff=0)
plotMenu.add_command(label="Start", command=start)
plotMenu.add_command(label="Stop", command=stop)
plotMenu.add_separator()
plotMenu.add_command(label="Exit", command=closeEvent)
menubar.add_cascade(label="Menu", menu=plotMenu)

root.config(menu=menubar)


#---------------------Container Creations:-----------------------------
#
#               ----------------------------------
#               |           top_frame            |
#               ----------------------------------
#               |       |                        |
#               | ctr_  |       ctr_right        |
#               | left  |                        |
#               |       |                        |
#               |_______|________________________|
#               |___________btm_frame____________|

# create all of the main containers
top_frame = Frame(root)#, bg=redHawkColor)#, width = 840, height=50, pady=3)
center = Frame(root)#, bg='black')#, width=50, height=40, padx=3, pady=3)
btm_frame = Frame(root)#, bg=redHawkColor, width = 840, height = 10, pady=3)

# layout all of the main containers
#root.grid_rowconfigure(1, weight=1)
#root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0)
center.grid(row=1, sticky=S+E)
btm_frame.grid(row = 4, sticky=W)

# TOP FRAME: create widgets
model_label = Label(top_frame, text = 'REDHAWK-3', font=helv22)#, bg=redHawkColor)

# TOP FRAME: widget layout:
model_label.grid(row = 0, columnspan = 3)

# MIDDLE: layout main containers:
#center.grid_rowconfigure(0, weight=1)
#center.grid_columnconfigure(1, weight=1)

ctrLeft = Frame(center)#, width=200, height=190)
ctrRight = Frame(center)#, bg='white', width=220, height=190, padx=3, pady=3)

ctrLeft.grid(row=0, column = 0, sticky=N+W)
ctrRight.grid(row=0, column = 1, sticky=E)
# general image definitions
imgResize = img.resize((1000, 705), Image.ANTIALIAS)
imgDisplay = ImageTk.PhotoImage(imgResize)
#Grid.rowconfigure(ctrRight, 0, weight=1)
mapArea = Label(ctrRight, image = imgDisplay)
mapArea.grid(row = 0, column = 0)

# MIDDLE: create buttons/labels
ansLabelText = Label(ctrLeft, text = "Coordinate: ")
ansLabel = Label(ctrLeft, textvariable = centerCoord)

nodeCountText = Label(ctrLeft, text = "Plotted: ")
nodeCount = Label(ctrLeft, textvariable = numPackets)

startButton = Button(ctrLeft, text="Start Plotting", width=18, command=start)
stopButton = Button(ctrLeft, text="Stop Plotting", width=18, command=stop)
showNodes = Button(ctrLeft, text="TEST", width=18, command=testPlot)

variable = StringVar(ctrLeft)
variable.set("West Point, NY") # default value
w = OptionMenu(ctrLeft, variable, "West Point, NY", "New York City, NY", "Cornwall, NY")

# MIDDLE: layout buttons/labels
#layout 10-digit coordinates
ansLabelText.grid(row=0, column=0)
ansLabel.grid(row=0, column=1)

#layout node info
nodeCountText.grid(row=1, column=0)
nodeCount.grid(row=1, column=1)

#layout buttons
startButton.grid(columnspan=2)
stopButton.grid(columnspan=2)
showNodes.grid(columnspan=2)

#drop down menu
w.grid(columnspan=2)

#BOTTOM FRAME: create & layout widget
group_label = Label(btm_frame, text='REDHAWK-3 AY17: CDTs Orion Boylston, Kyle Broughton, Hannah Grosso, Rachel Kim, and Jeffrey Schanz')
group_label.grid(row = 0, column = 0)

#testPlot()
root.mainloop()
