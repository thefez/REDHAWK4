# TODO: create common funtion for updating variables/colors


import mysql.connector as sql
#import _mysql as sql
import serial
from xbee import XBee
from Tkinter import *

sqlFlag = False
xbeeFlag = False

sqlStatus = "Not Connected"
xbeeStatus = "Not Connected"
connStatus = "Inactive"

def sqlConnect():
    global sqlFlag, sqlStatus, xbeeFlag, xbeeStatus, connFlag,connStatus, sqlVar
    try:
        cnx = sql.connect(connection_timeout=5, user='root', password='redhawk', host='localhost', database='redhawk')
        cursor = cnx.cursor()
        sqlFlag = True
        sqlVar.set("Connected")
        sqlStatusLabel.configure(fg = 'forest green')
    except:
        sqlFlag = False
        sqlStatus = "Not Connected"
        sqlStatusLabel.configure(fg = 'red3')

def xbeeConnect():
    global xbeeFlag
    try:
        port = serial.Serial('/dev/ttyUSB0', 9600)
        xbee = XBee(port)
        xbeeFlag = True
        xbeeVar.set("Connected")
        xbeeStatusLabel.configure(fg = 'forest green')
    except:
        print "test"
        xbeeFlag = False
        xbeeVar.set("Not Connected")
        xbeeStatusLabel.configure(fg = 'red3')


def run():
    global sqlFlag, sqlStatus, xbeeFlag, xbeeStatus, connFlag,connStatus, sqlVar
    if (sqlFlag):
        if(xbeeFlag):
            connVar.set("Active")
            connStatusLabel.configure(fg = 'forest green')
            try:
                data = eval(xbee.wait_read_frame()['rf_data'])
            except:
                pass
                #xbeeFlag = False
                #xbeeVar.set("Failed")
                #xbeeStatusLabel.configure(fg = 'red3')
            try:
                cursor.execute("INSERT INTO data(xCoord, yCoord, dir) VALUES ('{0}','{1}','{2}')".format(data[0], data[1], data[2]))
                cnx.commit()
            except:
                pass
                #sqlFlag = False
                #sqlStatus = "Failed"
                #sqlStatusLabel.configure(fg = 'red3')
            root.after(10,run)
        else:
            print "xbee not true"
    else:
        connVar.set("Inactive")
        connStatusLabel.configure(fg = 'red3')
#______________________________________________________________________________
root = Tk()
root.resizable(width=False, height=False)
root.title('XBee SQL Bridge')

def closeEvent():
    try:
        cursor.close()
        cnx.close()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", closeEvent)

leftFrame = Frame(root)
centerFrame = Frame(root)
rightFrame = Frame(root)

leftFrame.grid(column=0, row=0)
centerFrame.grid(column=1, row=0)
rightFrame.grid(column=2, row=0)

sqlVar = StringVar(centerFrame)
xbeeVar = StringVar(centerFrame)
connVar = StringVar(centerFrame)

sqlLabel = Label(leftFrame, text = 'SQL Connection')
sqlLabel.grid(row = 0, sticky = 'e')
xbeeLabel = Label(leftFrame, text = 'XBee Connection')
xbeeLabel.grid(row = 1, sticky = 'e')
connLabel = Label(leftFrame, text = 'Bridge Connection')
connLabel.grid(row = 2, sticky = 'e')

sqlStatusLabel = Label(centerFrame, textvariable = sqlVar)
sqlStatusLabel.grid(row = 0, sticky = 'nsew')
xbeeStatusLabel = Label(centerFrame, textvariable = xbeeVar, width = 13)
xbeeStatusLabel.grid(row = 1, sticky = 'nsew')
connStatusLabel = Label(centerFrame, textvariable = connVar)
connStatusLabel.grid(row = 2, sticky = 'nsew')

sqlButton = Button(rightFrame, text = 'Reset', command = sqlConnect, width = 10)
sqlButton.grid(row=0)
xbeeButton = Button(rightFrame, text = 'Reset', command = xbeeConnect, width = 10)
xbeeButton.grid(row=1)
connButton = Button(rightFrame, text = 'Reset', command = run, width = 10)
connButton.grid(row=2)

init = True
if (init):
    sqlConnect()
    xbeeConnect()
    run()
    init = False

root.mainloop()
