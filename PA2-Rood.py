# Author: Jordan Rood 
# CS 457 : DATABASE MANAGEMENT SYSTEMS
# Programming Assignment 2 - Basic Data Manipulation: built off previous assignments Metadata Management System
# Date: 03-22-2023

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

    tablePath = os.path.join(cwd, dbToUse, input[2])    

    if os.path.exists(tablePath):
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + input[2] + " because it already exists.")
    else:
        if not len(input) >= 5:
            print("Error: invalid input.")
            return
        
        attributeStr = ''
        
        for i in range(3, len(input), 2):
            # print("i = ", i)

            attributeName = re.sub(";|,", "", input[i])
            attributeType = re.sub(";|,", "", input[i + 1])

            # print("AttributeName = ", attributeName)
            # print("AttributeType = ", attributeType)

            if attributeType.count(')') >= 2 or (attributeType.count(')') == 1 and attributeType.count('(') != 1):
                # if type string contains unbalanced amount of parentheses
                attributeType = attributeType[:-1]

            attributeStr += attributeName.replace('(', '') + ' ' +  attributeType + '|'

        if attributeStr.endswith('|'):
            # format to make sure | is not at end of string
            attributeStr = attributeStr[:-3]

        with open(tablePath, 'w') as fp:
            fp.write(attributeStr + "\n")
            pass
        fp.close()
        print("Table " + input[2] + " created.")


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


def processFileData(data: list, setAttr: str, whereAttr: str, dataToFind: str, dataToSet: str) -> list:
    # splitLines = []
    # for line in data:
    #     splitData = line.replace('\n', '').replace('\t', '').split('|')
    #     splitLines.append(splitData)

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
        print(recordsModified, " record modified.")
    else:
        print(recordsModified, " records modified.")

    print(['|'.join(x) for x in splitLines])
    return ['|'.join(x) for x in splitLines]


def updateData(tblName: str, modifyInfoLst: list, cwd: str):
    recordsModified = 0
    tblPath = os.path.join(cwd, tblName)

    if len(modifyInfoLst) == 9 and 'set' in modifyInfoLst and 'where' in modifyInfoLst:
        attributeToSet = modifyInfoLst[2]
        attributeToFind = modifyInfoLst[6]

        dataToFind = modifyInfoLst[8].replace(';', '').replace('\'', '')
        dataToSet = modifyInfoLst[4].replace('\'', '')

        fp = open(tblPath, 'r')
        fileData = fp.readlines()

        replacedData = processFileData(fileData, attributeToSet, attributeToFind, dataToFind, dataToSet)

        fp.close()

        fp = open(tblPath, 'w')
        fp.write('\n'.join(replacedData))
        fp.close()

    else:
        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid input.")


def removeData(tblName: str, whereLst: list, cwd: str):
    numDeleted, attributeToCheck = 0, ''
    tblPath = os.path.join(cwd, tblName)

    if len(whereLst) == 5 and 'where' in whereLst:
        attributeToCheck = whereLst[2]
    
    file = open(tblPath, 'r')
    fileData = file.readlines()

    data = splitFileData(fileData)
    file.close()    

    operator = whereLst[3]
    operand = whereLst[4].replace(';', '').replace('\'', '')
    
    indexToCheck = 0
    for i, attributeType in enumerate(data[0]):
        #print(attributeToCheck, attributeType, i)
        if attributeToCheck in attributeType:
            indexToCheck = i

    #print("index to check is ", indexToCheck)
    for j in range(len(data)-1, 1, -1):
        if operator == '=':
            if data[j][indexToCheck] == operand:
                data.pop(j)
                numDeleted += 1
        elif operator == '>':
            if data[j][indexToCheck] > operand:
                data.pop(j)
                numDeleted += 1
        else:
            #other operands for extension
            continue
        #print(data)

    finalData = ['|'.join(x) for x in data]
    fp =  open(tblPath, 'w')
    fp.write('\n'.join(finalData) + '\n')
    fp.close()

    if numDeleted == 1:
        print(numDeleted, "record deleted.")
    else:
        print(numDeleted, "records deleted.")


#helper functions
def splitFileData(data: list) -> list:
    splitLines = []
    for line in data:
        splitData = line.replace('\n', '').replace('\t', '').split('|')
        splitLines.append(splitData)

    return splitLines


def main(): 
    try:
        running, dbToUse = True, ''
        cwd = os.getcwd()

        while running:
            userInput = input("")

            upperInput = userInput.upper()
            listInput = userInput.split(" ")

            #print(listInput)
            
            if userInput.startswith('--') or userInput == '' or userInput == '\r':
                pass

            elif upperInput == 'EXIT' or upperInput == '.EXIT\r' or upperInput == '.EXIT':
                running = False

            #elif not upperInput.startswith('UPDATE') and not upperInput.startswith('DELETE FROM'):
                #print("Error: invalid input (and no semi-colon at end of input).")
                #continue

            elif upperInput.startswith('CREATE DATABASE') and len(listInput) == 3:
                createDatabase(listInput[2].replace(';', ''), cwd)

            elif upperInput.startswith('DROP DATABASE') and len(listInput) == 3:
                dropDatabase(listInput[2].replace(';', ''), cwd)

            elif upperInput.startswith('USE') and len(listInput) == 2:
                dbToUse = useDatabase(listInput[1].replace(';', ''), cwd)

            elif upperInput.startswith('CREATE TABLE') and len(listInput) >= 5:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + listInput[2] + " because no database is being used.")
                else:
                    createTable(listInput, cwd, dbToUse)

            elif upperInput.startswith('DROP TABLE') and len(listInput) == 3:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to drop table " + listInput[2] + " because no database is being used.")
                else:
                    dropTable(listInput[2].replace(';', ''), os.path.join(cwd, dbToUse))

            elif upperInput.startswith('SELECT * FROM') and len(listInput) == 4:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + listInput[3].replace(';', '') + " because no database is being used.")
                else:
                    selectTable(listInput[3].replace (';', ''), os.path.join(cwd, dbToUse))

            elif upperInput.startswith('ALTER TABLE') and 'ADD' in upperInput and len(listInput) == 6:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2] + " because no database is being used.")
                else:
                    alterTable(listInput, os.path.join(cwd, dbToUse.replace(';', '')))


            elif upperInput.startswith('INSERT INTO') and 'VALUES' in upperInput and len(listInput) >= 4:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2] + " because no database is being used.")
                else:
                    insertData(listInput, os.path.join(cwd, dbToUse))

            elif upperInput.startswith('UPDATE') and len(listInput) == 2:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2] + " because no database is being used.")
                else:
                    updateLineInfo, counter = '', 0
                    while True or counter > 3:
                        line = input()
                        if ';' not in line:
                            updateLineInfo += ' ' + line
                            counter += 1
                        else:
                            updateLineInfo += ' ' + line
                            break

                    if len(updateLineInfo.split(" ")) == 9:
                        updateData(listInput[1], updateLineInfo.split(" "), os.path.join(cwd, dbToUse))
                    else:
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid number of commands.")
                        print(updateLineInfo)

            elif upperInput.startswith('DELETE FROM') and len(listInput) == 3:
                if dbToUse == '':
                    print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2] + " because no database is being used.")
                else:
                    updateLineInfo, counter = '', 0
                    while True or counter > 2:
                        line = input()
                        if ';' not in line:
                            updateLineInfo += ' ' + line
                            counter += 1
                        else:
                            updateLineInfo += ' ' + line
                            break
                    removeData(listInput[2], updateLineInfo.split(" ") , os.path.join(cwd, dbToUse))

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
