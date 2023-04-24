# Author: Jordan Rood 
# CS 457 : DATABASE MANAGEMENT SYSTEMS
# Programming Assignment 3 - Table Joins: built off previous assignment(s) Basic Data Manipulation and Metadata Management System
# Date: 04-10-2023

import os, sys
import shutil
import re
from colorama import Fore, Style
import fileinput

def createDatabase(dbName: str, cwd: str):
    # uses fileIO and os to create a new database directory folder

    newDBPath = os.path.join(cwd, dbName)

    if os.path.exists(newDBPath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create database " + dbName + " because it already exists.")
    else:
        os.mkdir(newDBPath)
        print("Database " + dbName + " created.")


def dropDatabase(dbName: str, cwd: str):
    # uses fileIO and os to delete a database directory if it exists

    dbPath = os.path.join(cwd, dbName)

    if not os.path.exists(dbPath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to delete database " + dbName + " because it does not exist.")
    else:
        shutil.rmtree(dbPath, ignore_errors=True)
        print("Database " + dbName + " deleted.")


def useDatabase(dbToUse: str, cwd: str) -> str:
    # takes in cwd to check if database exists and returns a string of the name of the database to use

    dbPath = os.path.join(cwd, dbToUse)
    
    if not os.path.exists(dbPath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to use " + dbToUse + " because it does not exist.")
        return ''
    else:
        print("Using database " + dbToUse + ".")
        return dbToUse


def createTable(input: list, cwd: str, dbToUse: str):
    # takes in input, path, and the database to use to create a table file within the database to use
    # once file is created the tables attribute names are written to file using loop and string logic
    # to parse and format attribute field names correctly in table file

    tblName = input[2].replace('(', ' ').split(' ')[0]
    tablePath = os.path.join(cwd, dbToUse, tblName)    

    if os.path.exists(tablePath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + input[2] + " because it already exists.")
    else:
        if not len(input) >= 5:
            print("Error: invalid input - not enough attribute titles.")
            return
        
        attributeStr = ''

        if len(input) % 2 == 0:
            startVal = 2
        else:
            startVal = 3

        for i in range(startVal, len(input), 2):

            attributeName = re.sub(";|,", "", input[i])
            attributeType = re.sub(";|,|\r", "", input[i + 1])

            if '(' in attributeName:
                attributeName = attributeName.replace('(', ' ').split(' ')[-1]

            #print("AttributeName = ", attributeName)
            #print("AttributeType = ", attributeType)

            if attributeType.count(')') >= 2 or (attributeType.count(')') == 1 and attributeType.count('(') != 1):
                # if type string contains unbalanced amount of parentheses
                attributeType = attributeType[:-1]

            attributeStr += attributeName.replace('(', '') + ' ' +  attributeType + '|'


        if attributeStr.endswith('|'):
            # format to make sure | is not at end of string
            attributeStr = attributeStr[:-1]

        with open(tablePath, 'w') as fp:
            fp.write(attributeStr + "\n")
            pass
        fp.close()
        print("Table " + tblName + " created.")


def dropTable(tableName: str, cwd: str):
    # uses fileIO and os to delete table file if it exists in the database being used

    tablePath = os.path.join(cwd, tableName)

    if not os.path.exists(tablePath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to delete " + tableName + " because it does not exist.")
    else:
        os.remove(tablePath)
        print("Table " + tableName + " deleted.")


def selectTable(tableName: str, cwd: str):
    # uses fileIO to read attribute fields from table file and output them

    tablePath = os.path.join(cwd, tableName)

    if not os.path.exists(tablePath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + tableName + " because it does not exist.")
    else:
        with open(tablePath, 'r') as fp:
            contents = fp.readlines()
            pass

        for x in contents:
            print(x.replace('\n', ''))

        fp.close()


def alterTable(input: list, cwd: str):
    # uses fileIO to modify tables attributes

    tablePath = os.path.join(cwd, input[2])

    if not os.path.exists(tablePath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + input[2] + " because it does not exist.")
    else:
        
        attributeStr = ''

        for i in range(4, len(input), 2):
            attributeStr += ' | ' + input[i] + ' ' + input[i + 1].replace(';', '')

            if i == len(input):
                attributeStr += ' | '

        if input[3] == 'ADD':
            with open(tablePath, 'a') as fp:
                fp.write(attributeStr + "\n")
                pass
            fp.close()

        print("Table " + input[2] + " modified.")


def insertData(data: list, cwd: str):
    # takes in data to insert as a list and path so specified table can be found and used
    # data list is iterated through for parsing and formatting
    # then formatted data is appended into table file 

    tblName = data[2]
    tblPath = os.path.join(cwd, tblName)

    if not os.path.exists(tblPath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to insert data because table" + tblName + "does not exist.")
    else:
        dataStr = ''
        for i in range(3, len(data)):
            dataStr += data[i].replace('values(', '').replace(',', '|').replace(');', '').replace('\t', '').replace('\'', '')

        with open(tblPath, 'a+') as fp:
            dataInFile = fp.read()

            if not dataInFile.endswith('\n'):
                fp.write(f'{dataStr}\n')
            else:
                fp.write(f'\n{dataStr}\n')

        fp.close()

        print("1 new record inserted.")

# update data helper function
def processFileData(data: list, setAttr: str, whereAttr: str, dataToFind: str, dataToSet: str) -> list:
    # filters through file data to match values to corresponding columns
    # then it analyzes for matches in data if they fall into the parameters given by user the updates are made
    # through updating a list to return to update function 

    splitLines = splitFileData(data)
    
    indexToReplaceAt, colToSetAt, recordsModified = 0, 0, 0
    for index, dataType in enumerate(splitLines[0]):
        if whereAttr in dataType:
            indexToReplaceAt = index
        elif setAttr in dataType:
            colToSetAt = index

    for i in range(1, len(splitLines)):
        if splitLines[i][indexToReplaceAt] == dataToFind:
            if setAttr == whereAttr:
                splitLines[i][indexToReplaceAt] = dataToSet
            else:
                splitLines[i][colToSetAt] = dataToSet
            recordsModified += 1

    if recordsModified == 1:
        print(str(recordsModified) + " record modified.")
    else:
        print(str(recordsModified) + " records modified.")

    return ['|'.join(x) for x in splitLines]


def updateData(tblName: str, modifyInfoLst: list, cwd: str):
    # takes in update parameters from user and validates and parses it to send to helper function for updates
    # then list is returned from helper function to then be written back to the table file line by line

    tblPath = os.path.join(cwd, tblName)

    if len(modifyInfoLst) >= 9 and 'set' in modifyInfoLst and 'where' in modifyInfoLst:
        inputList = [elem for elem in modifyInfoLst if elem != '']
        parsedInput = [i for i in inputList if i != '\r']

        attributeToSet = parsedInput[1]
        attributeToFind = parsedInput[5]

        dataToFind = parsedInput[7].replace(';', '').replace('\'', '').replace('\r', '')
        dataToSet = parsedInput[3].replace('\'', '')
        #print(dataToFind, dataToSet)

        fp = open(tblPath, 'r')
        fileData = fp.readlines()

        replacedData = processFileData(fileData, attributeToSet, attributeToFind, dataToFind, dataToSet)

        fp.close()

        fp = open(tblPath, 'w')
        fp.write('\n'.join(replacedData))
        fp.close()

    else:
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid input.")


def removeData(tblName: str, whereStmt: list, cwd: str):
    # File IO operations are used to read file data and check lines (aka tuples) for matching attributes
    # from specified values to delete. Function ensures that correct attribute types are being checked.
    # Then, updates are made to list of lines and written back with deleted info removed

    numDeleted, attributeToCheck = 0, ''
    tblPath = os.path.join(cwd, tblName)

    if not os.path.exists(tblPath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to delete data from table " + tblName.replace('\r', '') + " because table not found.")

    if len(whereStmt) == 5 and 'where' in whereStmt:
        attributeToCheck = whereStmt[2]
    
    file = open(tblPath, 'r')
    fileData = file.readlines()

    data = splitFileData(fileData)
    file.close()    

    operator = whereStmt[3]
    operand = whereStmt[4].replace(';', '').replace('\'', '').replace('\r', '')
    
    indexToCheck = 0
    for i, attributeType in enumerate(data[0]):
        if attributeToCheck in attributeType:
            indexToCheck = i

    # iterates over filedata from back to front so that pop() does not cause problems to traversal
    for j in range(len(data)-1, 0, -1):
        if operator == '=':
            if data[j][indexToCheck] == operand:
                data.pop(j)
                numDeleted += 1
        elif operator == '>':
            if float(data[j][indexToCheck]) > float(operand):
                data.pop(j)
                numDeleted += 1
        else:
            #other operands for extension in next assignments
            continue

    finalData = ['|'.join(x) for x in data]
    fp =  open(tblPath, 'w')
    fp.write('\n'.join(finalData) + '\n')
    fp.close()

    if numDeleted == 1:
        print(str(numDeleted) + " record deleted.")
    else:
        print(str(numDeleted) + " records deleted.")


#helper function - splits lines of data up from file readlines()
def splitFileData(data: list) -> list:
    splitLines = []
    for line in data:
        splitData = line.replace('\n', '').replace('\t', '').split('|')
        splitLines.append(splitData)

    return splitLines


def selectTableWithAttributes(infoLst: list, whereStmt: list, cwd: str):
    # function parses where commands and select commands to compare read in data points
    # from file to where boundaries and if select and where bounds apply, then the data
    # is formatted and printed

    tblName = infoLst[5].capitalize()
    tblPath = os.path.join(cwd, tblName)
    operator, operand = whereStmt[2], whereStmt[3].replace(';', '').replace('\r', '')
    boundArg = whereStmt[1]

    if not os.path.exists(tblPath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + tblName + " because it does not exist.")
    else:
        attributesToQuery = []
        for data in infoLst:
            if data != 'from':
                attributesToQuery.append(data.replace(',', ''))
            else:
                break

        attributesToQuery.remove('select')
        if '' in attributesToQuery:
            attributesToQuery.remove('')
        if '\r' in attributesToQuery:
            attributesToQuery.remove('\r')

        file = open(tblPath, 'r')
        fileData = file.readlines()
        splitByAttribute = [line.split("|") for line in fileData]
        file.close()

        indiciesToPrint, indexToCheck = [], 0
        attributeTitles = splitByAttribute[0]
        for index, attribute in enumerate(attributeTitles):
            
            for i in attributesToQuery:
                if i in attribute:
                    indiciesToPrint.append(index)
                elif i in boundArg:
                    indexToCheck = index

        for j in range(0, len(splitByAttribute)):
            for k in indiciesToPrint:
                if operator == '!=' and splitByAttribute[j][indexToCheck] == operand:
                        continue
                elif k % len(indiciesToPrint) == 0:
                    print(splitByAttribute[j][k].replace('\n', ''))
                else:
                    print(splitByAttribute[j][k].replace('\n', '') + '|', end="")            
    

def fromParser(input:list):
    # function takes input list from user to then parse and remove not needed 
    # information to for selections and joins

    fromList = []    
        
    for x in input:
        if x == "select" or x == "\r" or x == "*":
            pass
        elif x == 'where':
            break
        else:
            fromList.append(x.replace(',', ''))
    return fromList

def queryAndJoinTables(input: list, whereList: list, cwd: str):
    # this function uses helper fromParser function to parse input command data
    # then uses this to find two tables to join or inner join.  Table files are opened
    # and read from by lines and a nested loop is used to compare and print joined table 
    # data based on query parameters.  Indicies are found before comparison so that correct 
    # attribute fields are being analyzed.

    fromList = fromParser(input)

    if 'inner' and 'join' in fromList:
        tbl1, tbl2 = fromList[1], fromList[5]
    else:
        tbl1, tbl2 = fromList[1], fromList[3]

    if not os.path.exists(os.path.join(cwd, tbl1)) and os.path.exists(os.path.join(cwd, tbl2)):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to join tables because one or both do not exist.")
    else:
        operator, operand1, operand2 = whereList[2], whereList[1].split(".")[1], whereList[3].replace(';', '').replace('\r', '').split(".")[1]

        file1 = open(os.path.join(cwd, tbl1), 'r')
        file2 = open(os.path.join(cwd, tbl2), 'r')

        fileData1 = file1.readlines()
        fileData2 = file2.readlines()

        #print(fromList)
        #print(whereList)
        attributeFields = fileData1[0].strip() + '|' + fileData2[0].strip()
        tblOneIndex, tblTwoIndex = 0, 0
        print(attributeFields)

        # find indicies (from both tables) to check in nested for loop for joining
        for index, attr in enumerate(fileData1[0].split("|")):
            if operand1 in attr:
                tblOneIndex = index

        for index, attr in enumerate(fileData2[0].split("|")):
            if operand2 in attr:
                tblTwoIndex = index

        for i in fileData1:
            for j in fileData2:
                #check condition parsed from the given query
                if operator == '=' and i.split("|")[tblOneIndex] == j.split("|")[tblTwoIndex]:
                    print(i.replace('\n', '') + "|" + j.replace('\n', ''))

        file1.close()
        file2.close()


def leftOuterJoin(input: list, whereLst: list, cwd: str):
    # implements left outer join functionality through use of file IO operations to 
    # check two tables and find indicies to compare parameters given for join table 
    # result.  Nested for loop is used to compare the two data file contents and 
    # if equal a join is done and if not equal with other data from second table 
    # after all comparisons, then table 1 contents printed with null values.

    fromList = fromParser(input)
    tbl1, tbl2 = fromList[1], fromList[6]

    if not os.path.exists(os.path.join(cwd, tbl1)) and os.path.exists(os.path.join(cwd, tbl2)):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to join tables because one or both do not exist.")
    else:
        file1 = open(os.path.join(cwd, tbl1))
        file2 = open(os.path.join(cwd, tbl2))

        tblData1 = file1.readlines()
        tblData2 = file2.readlines()

        attributeFields = tblData1[0].strip() + '|' + tblData2[0].strip()
        tblOneIndex, tblTwoIndex = 0, 0
        operator, operand1, operand2 = whereLst[2], whereLst[1].split(".")[1], whereLst[3].replace(';', '').replace('\r', '').split(".")[1]

        print(attributeFields)

        # find indicies (from both tables) to check in nested for loop for joining
        for index, attr in enumerate(tblData1[0].split("|")):
            if operand1 in attr:
                tblOneIndex = index

        for index, attr in enumerate(tblData2[0].split("|")):
            if operand2 in attr:
                tblTwoIndex = index

        # iterate through both file contents comparing data and having left outer joins printed
        nullCount = 0
        for i in range(1, len(tblData1)):
            for j in range(1, len(tblData2)):
                if operator == '=' and tblData1[i].split("|")[tblOneIndex] == tblData2[j].split("|")[tblTwoIndex]:
                    print(tblData1[i].replace('\n', '') + "|" + tblData2[j].replace('\n', ''))
                    nullCount += 1
            if nullCount == 0:
                print(tblData1[i].replace('\n', '') + "|" + "|")
            nullCount = 0

        file1.close()
        file2.close()


def main(): 
    try:
        running, dbToUse = True, ''
        cwd = os.getcwd()

        while running:
            userInput = input("")

            upperInput = userInput.upper()
            listInput = userInput.split(" ")
            
            if userInput.startswith('--') or userInput == '' or userInput == '\r':
                pass

            elif upperInput == 'EXIT' or upperInput == '.EXIT\r' or upperInput == '.EXIT':
                running = False

            elif upperInput.startswith('CREATE DATABASE') and len(listInput) == 3:
                createDatabase(listInput[2].replace(';', '').replace('\r', ''), cwd)

            elif upperInput.startswith('DROP DATABASE') and len(listInput) == 3:
                dropDatabase(listInput[2].replace(';', '').replace('\r', ''), cwd)

            elif upperInput.startswith('USE') and len(listInput) == 2:
                dbToUse = useDatabase(listInput[1].replace(';', '').replace('\r', ''), cwd)

            elif upperInput.startswith('CREATE TABLE') and len(listInput) >= 5:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + listInput[2].replace('\r', '') + " because no database is being used.")
                else:
                    createTable(listInput, cwd, dbToUse)

            elif upperInput.startswith('DROP TABLE') and len(listInput) == 3:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to drop table " + listInput[2].replace('\r', '') + " because no database is being used.")
                else:
                    dropTable(listInput[2].replace(';', '').replace('\r', ''), os.path.join(cwd, dbToUse))

            elif upperInput.startswith('SELECT * FROM') and len(listInput) == 4:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + listInput[3].replace(';', '').replace('\r', '') + " because no database is being used.")
                else:
                    selectTable(listInput[3].replace (';', '').replace('\r', ''), os.path.join(cwd, dbToUse))

            elif upperInput.startswith('ALTER TABLE') and 'ADD' in upperInput and len(listInput) == 6:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")
                else:
                    alterTable(listInput, os.path.join(cwd, dbToUse.replace(';', '').replace('\r', '')))

            elif upperInput.startswith('INSERT INTO') and 'VALUES' in upperInput and len(listInput) >= 4:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")
                else:
                    insertData(listInput, os.path.join(cwd, dbToUse.replace('\r', '')))

            elif upperInput.startswith('UPDATE') and len(listInput) >= 2 and len(listInput) < 4:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[1] + " because no database is being used.")
                else:
                    updateLineInfo, counter = '', 0
                    while True or counter <= 3:
                        line = input()
                        if ';' not in line:
                            updateLineInfo += ' ' + line
                            counter += 1
                        else:
                            updateLineInfo += ' ' + line
                            break

                    if len(updateLineInfo.split(" ")) >= 9 and len(updateLineInfo.split(" ")) < 11:
                        updateData(listInput[1], updateLineInfo.split(" "), os.path.join(cwd, dbToUse))
                    else:
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid number of commands.")

            elif upperInput.startswith('DELETE FROM') and len(listInput) >= 3 and len(listInput) < 5:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2].capitalize() + " because no database is being used.")
                else:
                    delLineInfo, counter = '', 0
                    while True or counter <= 2:
                        line = input()
                        if ';' not in line:
                            delLineInfo += ' ' + line
                            counter += 1
                        else:
                            delLineInfo += ' ' + line
                            break
                    removeData(listInput[2].capitalize(), delLineInfo.split(" ") , os.path.join(cwd, dbToUse))

            elif upperInput.startswith('SELECT') and len(listInput) >= 3 and len(listInput) < 5:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2].capitalize() + " because no database is being used.")
                else: 
                    lineInfo, whereStr, counter = userInput, '', 0
                    while True or counter <= 3:
                        line = input()
                        if ';' not in line:
                            lineInfo += ' ' + line
                            counter += 1
                        else:
                            lineInfo += ' ' + line
                            whereStr = line
                            break

                    if len(listInput) == 3 and 'left outer join' in lineInfo:
                        leftOuterJoin(lineInfo.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))
                    elif len(listInput) == 3:
                        queryAndJoinTables(lineInfo.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))
                    else:
                        selectTableWithAttributes(lineInfo.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))  
                    
            else:
                print("Error: invalid input.")
                print(userInput)
                continue
    
        print("All done.")
    except KeyboardInterrupt:
        print(" You cancelled the operation.")
    except:
        print("Error: exception occurred!")

if __name__ == "__main__":
    main()