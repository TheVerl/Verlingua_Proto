#!/usr/bin/python3

# Import Modules
from __future__ import print_function
from array import *
from termcolor import colored
import sys
import click
import re

# Define global variables
routineTable = []
ifTable = []
lookupTable = dict()
fileTable = []
globalFile = None
tempStart = 0
upToLine = 0

# Define classes
class Block:
    def __init__(self, start, end, parentBlock, tableNumber, content):
        self.start = start
        self.end = end
        self.parentBlock = parentBlock
        self.tableNumber = tableNumber
        self.content = content


# Block for the if statement.
class blockIf(Block):
    def __init__(self, start, end, parentBlock, tableNumber, content, expression):
        self.start = start
        self.end = end
        self.parentBlock = parentBlock
        self.tableNumber = tableNumber
        self.content = content
        self.expresion = expression
    #    Block.__init__(start, end, parentBlock, tableNumber)

# Sets the block's variable for it's table number. IDK if this will actually be used, might delete it later.
    def setTableNumber(self):
        self.tableNumber = ifTable[-1]
        #print(self.tableNumber)

    # Trims the file for the code of the if statement, saving it inside the block.
    def defineContent(self):
        foundEnd = False
        foundStart = False
        global globalFile
        file = globalFile
        #print(self.start)
        #print(self.end)
        self.content = []
        self.expression = []
        coomer = open(file, "r")
        while foundEnd != True:
            for line in coomer:
                line = line.replace("\n","")
                line = line.replace("\r","")
                x = line.split(" ")            
                if x[0] == "if":
                    i = 0
                    foundStart = True
                    while (i != len(x)):
                        self.expression.append(x[i])
                        i += 1
                    #print(line)
                    self.content.append(x)
                elif foundStart == True:
                    if x[0] == "endi":
                        foundEnd = True
                        #print(line)
                        self.content.append(x)
                        break
                    else:
                        #print(line)
                        self.content.append(x)
        coomer.close()
        #print("Content is:", self.content)

# Block for the routine (function) statement
class blockRoutine(Block):
    def __init__(self, start, end, parentBlock, tableNumber, content, name):
        self.start = start
        self.end = end
        self.parentBlock = parentBlock
        self.tableNumber = tableNumber
        self.content = content
        self.name = name
    #   Block.__init__(start, end, parentBlock, tableNumber)

# Sets the block's variable for it's table number. IDK if this will actually be used, might delete it later.    
    def setTableNumber(self):
        self.tableNumber = routineTable[-1]
        #print(self.tableNumber)
    
    # Trims the file for the code of the routine, saving it inside the block.
    def defineContent(self):
        foundEnd = False
        foundStart = False
        self.content = []
        i = 0
        x = 0
        while ( foundEnd != True ):
            while ( i != len(fileTable)): 
                #print("\n\r", fileTable[i])
                if fileTable[i][0] == "routine":
                    foundStart = True
                    self.name = fileTable[i][1]
                    #print(line)
                    self.content.append(fileTable[i])
                    i += 1
                    continue
                elif foundStart == True:
                    if fileTable[i][0] == "endr":
                        foundEnd = True
                        #print(line)
                        self.content.append(fileTable[i])
                        i += 1
                        break
                    else:
                        #print(line)
                        self.content.append(fileTable[i])
                        i += 1
                        continue
        #print ("length is", len(self.content), '\n')
        while( x != len(self.content) ):
            fileTable.pop(0)
            x += 1
        #print(fileTable)
        #sys.exit()
        #print("fileTable, after doing block stuff is now:", fileTable, '\n')
        #print("Content is:", self.content, '\n')
        #sys.exit()

# Calculates the line number of a block entry using the block's start and end values and the line in the content list.
def calculateLineNumber(entry, ID, form):
    if (form == "routine"):
        #start = routineTable[ID].start
        end = routineTable[ID].end
        return (end - entry)
    elif(form == "if"):
        end = ifTable[ID].end
        return(end - entry)
    else:
        print(" Why am I unable to find the line number!?!?!?")
        return
    pass

# I forgot what it does, but plug it in if you want mathematical expressions to work.
def variableMath(x, count):
    i = 0
    while i != len(x):
        w = None
        w = findVariable("name", "value", x[i], count, False)
        if w == False:
            i += 1
            #print(i)
        elif w[0] != False:
            #print(i)
            x[i] = w[1]
            #print(command)
            i += 1
    return x

# Checks if a line has variable tags in it.
def doesItHaveVariableTags(x):
    i = 0
    while i != len(x):
        s = x[i]
        remainder = s.rpartition('%')[-1]
        m = re.search('%(.+?)%', s)
        if m:
            found = m.group(1)
        if m != None:
            return True
        else:
            i += 1
    return False  

# Finds the variable.
def findVariable(x, y, marker, count, bol):
    i = 0
    foundValue = False
    while foundValue != True:
        try:
            if lookupTable[i][x] == marker:
                #memeball = []
                pepe = lookupTable[i][y]
                if bol == True:
                    #memeball = [True, pepe, i]
                    return True, pepe, i
                    foundValue = True
                else:
                    return True, pepe
                    foundValue = True
            else:
                i += 1
        except KeyError:
            #error(5, count, None, None)
            return False
    
# Error handling.
def error(code, x, y, z):
    if (code == 1):                                                                                                                     # Code 1
        s = ("\nLine " + str(z) + " ERROR: Name "+ str(x)+ " already exists for another variable at key " + str(y) + "!\nError Code 1")
        print(colored(s, 'red'))
        return
    if (code == 2):                                                                                                                     # Code 2
        s = ("\nLine " + str(x) + " ERROR: No equal sign in num decleration!\nError Code 2")
        print(colored(s, 'red'))
        return        
    if (code == 3):                                                                                                                     # Code 3
        s = ("\nERROR: Not a compatible file type!\nError Code 3")
        print(colored(s, 'red'))
        return
    if (code == 4):                                                                                                                     # Code 4
        s = ("\nLine " + str(x) + " ERROR: Variable " + str(y) + " not defined!\nError Code 4")
        print(colored(s, 'red'))
        return
    if (code == 5):                                                                                                                     # Code 5
        s = ("\nLine " + str(x) + " ERROR: KeyError trying to find value with findVariable()!\nError Code 5")
        print(colored(s, 'red'))
        return
    if (code == 6):                                                                                                                     # Code 6
        s = ("\nERROR: No Main routine in file!\nError Code 6")
        print(colored(s, 'red'))
        return
    if (code == 7):                                                                                                                     # Code 7
        s = ("\nLine: " + str(x) + " ERROR: No " + y + " named " + z + "!\nError Code 7")
        print(colored(s, 'red'))
        return
    if (code == 8):                                                                                                                     # Code 8
        s = ("\nLine: " + str(x) + " ERROR: Incompatible value for " + y + "!\nError Code 8")
        print(colored(s, 'red'))
        return

# Runs if the line starts with any of the varaible definers. It just defines them.
def cmdVar(pid, tokens, count):
    seperator = " "
    joe = tokens.pop(0)
    if tokens[1] == "=":
        i = 0
        pid = 0
        foundEmptyKey = False
        while foundEmptyKey != True:
            if i in lookupTable:
                try:
                    if lookupTable[i]['name'] == tokens[pid]:
                        error(1, lookupTable[i]['name'], i, count)
                        break
                    else:
                        i += 1
                except KeyError:
                    print(i)
                    i += 1
            else:
                foundEmptyKey = True
        #print("Nothing in " + str(i) + ", writing to it.")
        nigga = variableMath(tokens, count)
        #print(nigga)
        lookupTable[i] = {}
        if joe == "bool":
            pid = 0
            lookupTable[i]['type'] = joe
            lookupTable[i]['name'] = nigga[pid]
            nigga.pop(0)
            nigga.pop(0)
            if ( nigga[pid] != "True" or "False" ):
                error(8, count, "BOOLEAN", None)
        elif joe == "num":
            pid = 0
            lookupTable[i]['type'] = joe
            lookupTable[i]['name'] = nigga[pid]
            nigga.pop(0)
            nigga.pop(0)
            x = seperator.join(nigga)
            x = x.strip()
            if (x.isalpha()):
                error(8, count, "NUMBER", None)
            else:
                lookupTable[i]['value'] = str(eval(x))
        elif joe == "str":
           
            lookupTable[i]['type'] = joe
            pid = 0
            lookupTable[i]['name'] = nigga[pid]
            nigga.pop(0)
            nigga.pop(0)
            lookupTable[i]['value'] = seperator.join(nigga)     
        #print("There is a new", lookupTable[i]['type'], "at key", i, "named", lookupTable[i]['name'], "with a value of", lookupTable[i]['value'], "\n")
    else:
        error(2, count, None, None)
    return

# Runs if the line starts with "echo". Prints out what's after "echo".
def cmdEcho(pid, tokens, count, REPLDetect):
    i = pid
    w = 0
    seperator = " "
    tokens.pop(0)
    # Numbers
    while w != len(tokens):
        s = tokens[w]
        remainder = s.rpartition('%')[-1]
        m = re.search('%(.+?)%', s)
        if m:
            found = m.group(1)
        if m != None:
            selection = tokens[w].split("%")
            marker = selection[1]
            i = 0
            foundVariable = False
            value = findVariable('name', 'value', marker, count, False)
            tokens[w] = str(value[1]) + remainder
        else:
            w += 1
    # New line
    if tokens[-1].endswith("|n"):
        tokens[-1] = tokens[-1][:-2]
        tokens.append('\n\r')
        print(seperator.join(tokens))
    else:
        if REPLDetect == True:
            tokens.append('\n')
            print(seperator.join(tokens), end='')
        else:
            print(seperator.join(tokens) + " ", end='')
    return

def iterateThorughBlock(form, ID):
    #print("If I was actually filled with code, I would be going through the block.")
    #sys.exit()
    if (form == "routine"):
        i = 1
        length = len(routineTable[ID].content) - 1
        while (i != length):
            line = calculateLineNumber(i, ID, "routine")
            indicator(routineTable[ID].content[i], line, False)
            i += 1
            #print(i)
            #print(ID)
            #print(routineTable[ID].content)
        return
    elif (form == "if"):
        print("If statement iteration is under construction.")
        sys.exit()
    pass

# Reads through the file for the second time, going through main and then branching out from there through routine calls, handling all the blocks.
def secondReading(command, count):
    if (command[0] == "run"):
        i = 0
        while (i != len(routineTable)):
            if command[1] == routineTable[i].name:
                iterateThorughBlock('routine', i)
                return
            else:
                #print(i)
                i += 1
        line = calculateLineNumber(count, i)
        error(7, line, "ROUTINE", command[1])
    elif (command[0] == "if"):
        i = 0 
        x = 0
        command.pop(0)
        while (i != len(ifTable)):
            if command == ifTable[i].expression:
                iterateThorughBlock('if', i)
            else:
                i += 1
        line = calculateLineNumber(count, i)
        error(7, line, "IF_STATEMENT", command)
    else:
        indicator(command, count, False)

# Reads through the file for the first time, generating the blocks.
def firstReading(command, count):
    #print(count)
    global tempStart
    #print(tempStart)
    if (command[0] == "routine"): tempStart = count
    if (command[0] == "if"):      tempStart = count
    if (command[0] == "endi"):   
        ifTable.append(blockIf(tempStart, count, None, 0, None, None))
        ifTable[-1].defineContent()
        ifTable[-1].setTableNumber()
        tempStart = 0
        #print(ifTable)
    if (command[0] == "endr"):   
        routineTable.append(blockRoutine(tempStart, count, None, 0, None, None))
        routineTable[-1].defineContent()
        routineTable[-1].setTableNumber()
        tempStart = 0
        #print(routineTable)
    
# Sends the line data to other functions to handle depending on the beginning tag. Also does some maths stuff.
def indicator(command, count, isREPLOn):
    #print(command)
    seperator = " "
    x = findVariable('name', 'name', command[0], count, True)
    #print(command)
    #print(x)
    #print(doesItHaveVariableTags(command))
    if x == False or doesItHaveVariableTags(command) == True:
        if (command[0] == "num"):     cmdVar(1, command, count)
        if (command[0] == "echo"):    cmdEcho(1, command, count, isREPLOn)
        if (command[0] == "str"):     cmdVar(1, command, count)
            
    elif x[0] != False or doesItHaveVariableTags(command) != True:
        isNumber = False
        i = 0
        command.pop(0)
        command.pop(0)
        #print(command)
        #print(len(command))
        nigga = variableMath(command, count)
        #print(command)
        y = seperator.join(nigga)
        #print(y)
        result = str(eval(y))
        #print(result)
        lookupTable[x[2]]['value'] = result
        #print(express)
        return
    return

# Init function.
@click.command()
@click.option('--repl', type=click.BOOL, default='false', help="REPL")
@click.option('--file', type=click.Path(exists=True), help="input file")
def init(repl, file):
    isThereAMainRoutine = False
    i = 0
    global globalFile
    globalFile = file
    if file.endswith('.verl'):
        wojak = open(file, "r")
        count = 0
        # Puts the file into fileTable
        for line in wojak:
            if line.strip():
                line = line.replace('\n','')
                line = line.replace('\r','')
                x = line.split(" ")
                count += 1
                fileTable.append(x)
                #firstReading(x, count)
        #print(fileTable)
        # Then reads from fileTable
        while ( i < len(fileTable)):
            firstReading(fileTable[i], i)
            i += 1
        #print(len(routineTable))
        i = 0
        while i != len(routineTable):
            #print(routineTable[i].content[0][1])
            if(routineTable[i].content[0][1] == "main"):
                isThereAMainRoutine = True
                break
            else:
                i += 1
                #print(i)
        if isThereAMainRoutine == True:
            mainID = i
            print("Yay! the main function is at", routineTable[mainID].start, "!")
            i = 0
            while i != len(routineTable[mainID].content):
                line = routineTable[mainID].content[i]
                #print(line)
                secondReading(line, i)
                i += 1   
                #print(i)
            print('\r')
            sys.exit()
        else:
            error(6, None, None, None)
        #print("\r")
        sys.exit()
    else:
        error(3, None, None, None)


if __name__ == '__main__':
    init()