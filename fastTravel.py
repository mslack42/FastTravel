#! python3
# on Linux, this should be /usr/bin/python3

# Command Line utility
#  - save a given directory to the shelf
#  - delete a given key from the shelf
#  - change directories by suppliying a key in the shelf
#  - list all directories in the shelf
#  - opens a given directory in file explorer (currently just in linux)

import sys, os, shelve
from tabulate import tabulate
import pyautogui

key = ''
command = ''
fastTravelData = 'fastTravelData absolute directory here'

def announceArgFailure():
    print('Invalid arguments supplied - are you sure you\'ve unlocked HM02 Fly yet?')
    sys.exit(1)

def fastTravelTo(key):
    if not isInShelf(key):
        print('No such camp')
        sys.exit(1)
    targetDestination = fetchFromShelf(key)
    pyautogui.typewrite('cd ' + targetDestination)
    pyautogui.typewrite(['enter'])

def saveFastTravelPoint(key):
    # Add current directory and key to fastTravelData
    saveToShelf(key, os.getcwd())
    sys.exit(0)

def removeFastTravelPoint(key):
    # Remove given key its directory from fastTravelData
    print('delete ' + key)
    removeFromShelf(key)
    sys.exit(0)

def listFastTravelPoints(key):
    # Print the current shelf data
    shelfFile = shelve.open(fastTravelData)
    tableData = [[key, shelfFile[key]] for key in shelfFile.keys()]
    print(tabulate(tableData, headers=["Name", "Location"]))

def saveToShelf(key, value):
    shelfFile = shelve.open(fastTravelData)
    shelfFile[key] = value
    shelfFile.close()

def removeFromShelf(key):
    shelfFile = shelve.open(fastTravelData)
    shelfFile.pop(key)
    shelfFile.close()

def isInShelf(key):
    shelfFile = shelve.open(fastTravelData)
    return key in shelfFile.keys()

def fetchFromShelf(key):
    shelfFile = shelve.open(fastTravelData)
    value = shelfFile[key]
    return value

def openDirectory(key):
    if sys.platform == "linux" or sys.platform == "linux2":
        if key == '':
            os.system('gio open .')
            return
        elif not isInShelf(key):
            print('No such camp')
            sys.exit(1)
        targetDestination = fetchFromShelf(key)
        os.system('gio open "%s"' % targetDestination)
    else
        print('Not supported')
        return


def listHelp(key):
    print('How to use Fast Travel:\n\n' + 
    'With no commands a just a key, jump to that camp\n' + 
     'With the -explore command, opens a given camp directory (or the current directory)\n' +
    'With the -set-camp command, save the current directory as a camp under a given name\n' + 
    'With the -clear-camp command, remove the specified camp from your camp list\n' + 
    'With the -list-camps command, see all currently registered camps\n')

commands = {
    '': fastTravelTo,
    '-set-camp': saveFastTravelPoint,
    '-clear-camp': removeFastTravelPoint,
    '-list-camps': listFastTravelPoints,
    '-explore': openDirectory,
    '-help': listHelp
}

def executeCommand():
    selectedCommand = commands.get(command, lambda: announceArgFailure())
    selectedCommand(key)

def parseArgs():
    global key
    global command
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if (arg in commands.keys()):
            command = arg
        else:
            key = arg
    elif len(sys.argv) == 3:
        command = sys.argv[1]
        key = sys.argv[2]
    else:
        announceArgFailure()
    if key == '' and command == '':
        announceArgFailure()

parseArgs()
executeCommand()
