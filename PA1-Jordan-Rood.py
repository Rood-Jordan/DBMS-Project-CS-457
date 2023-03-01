# Author: Jordan Rood 
# CS 457 : DATABASE MANAGEMENT SYSTEMS
# Programming Assignment 1 - Metadata Management System
# Date: 02-08-2023

import os, sys
import shutil
import re

def manageInput(input: str) -> list:
    # takes in input command, manages it based on length and parses it into a list

    lst = input.split(" ")
    finalLst = []

    if len(lst) == 1:
        finalLst = [lst[0].upper()]
    elif len(lst) == 2:
        finalLst = [lst[0].upper(), lst[1].replace(';', '')]
    elif len(lst) == 3:
        finalLst = [lst[0].upper(), lst[1].upper(), lst[2].replace(';', '')]
    elif len(lst) == 4:
        finalLst = [lst[0].upper(), lst[1], lst[2].upper(), lst[3].replace(';', '')]
    elif len(lst) == 6:
        finalLst = [lst[0].upper(), lst[1].upper(), lst[2], lst[3].upper(), lst[4], lst[5].replace(';', '')]
    elif len(lst) == 7:
        finalLst = [lst[0].upper(), lst[1].upper(), lst[2], lst[3].replace('(', ''), lst[4].replace(',', ''), lst[5], lst[6].replace(');', '')]    
    else:
        # take care of tables with more than two attribute fields
        for x in lst:
            if x.upper() == 'CREATE' or x.upper() == 'TABLE':
                finalLst.append(x.upper())
            else:
                finalLst.append(re.sub(";|,", "", x))

    #print(lst)
    #print(finalLst)

    return finalLst

def createDatabase(input: list, cwd: str):
    # uses fileIO and os to create a new database directory folder

    newDBPath = os.path.join(cwd, input[2])

    if os.path.exists(newDBPath):
        print("!Failed to create database " + input[2] + " because it already exists.")
    else:
        os.mkdir(newDBPath)
        print("Database " + input[2] + " created.")

def dropDatabase(input: list, cwd: str):
    # uses fileIO and os to delete a database directory if it exists

    dbPath = os.path.join(cwd, input[2])

    if not os.path.exists(dbPath):
        print("!Failed to delete database " + input[2] + " because it does not exist.")
    else:
        #os.rmdir(dbPath)
        shutil.rmtree(dbPath, ignore_errors=True)
        print("Database " + input[2] + " deleted.")

def useDatabase(input: list, cwd: str) -> str:
    # takes in cwd to check if database exists and returns a string of the name of the database to use
 
    if len(input) != 2:
        # invalid use input, so return to main
        return ''

    dbToUse = input[1]
    dbPath = os.path.join(cwd, dbToUse)
    
    if not os.path.exists(dbPath):
        print("Error: cannot use " + dbToUse + " because it does not exist.")
        return ''
    else:
        print("Using database " + dbToUse + ".")
        return dbToUse

def createTable(input: list, cwd: str, dbToUse: str):
    # takes in input, path, and the database to use to create a table file within the database to use
    # once file is created the tables attribute names are written to file

    tablePath = os.path.join(cwd, dbToUse, input[2])    

    if os.path.exists(tablePath):
        print("!Failed to create table " + input[2] + " because it already exists.")
    else:
        if not len(input) >= 5:
            return
        
        attributeStr = ''
        # for x in input:
        #     pass
        
        attributeStr = str(input[3] + ' ' + input[4] + ' | ' + input[5] + ' ' + input[6])
        with open(tablePath, 'w') as fp:
            fp.write(attributeStr)
            pass
        fp.close()
        print("Table " + input[2] + " created.")

def dropTable(input: list, cwd: str):
    # uses fileIO and os to delete table file if it exists in the database being used

    tablePath = os.path.join(cwd, input[2])

    if not os.path.exists(tablePath):
        print("!Failed to delete " + input[2] + " because it does not exist.")
    else:
        os.remove(tablePath)
        print("Table " + input[2] + " deleted.")

def selectTable(input: list, cwd: str):
    # uses fileIO to read attribute fields from table file and output them

    tablePath = os.path.join(cwd, input[3])

    if not os.path.exists(tablePath):
        print("!Failed to query table " + input[3] + " because it does not exist.")
    else:
        with open(tablePath, 'r') as fp:
            contents = fp.readline()
            print(contents)
            pass
        fp.close()

def alterTable(input: list, cwd: str):
    # uses fileIO to modify tables attributes

    tablePath = os.path.join(cwd, input[2])

    if not os.path.exists(tablePath):
        print("!Failed to alter table " + input[2] + " because it does not exist.")
    else:
        attributeStr = str(' | ' + input[4] + ' ' + input[5])

        if input[3] == 'ADD':
            with open(tablePath, 'a') as fp:
                fp.write(attributeStr)
                pass
        
        print("Table " + input[2] + " modified.")

    

def main(): 
    try:
        running, dbToUse = True, ''
        cwd = os.getcwd()

        while running:
            userInput = input("")
            listInput = manageInput(userInput)
            
            if 'CREATE' in listInput and 'DATABASE' in listInput:
                createDatabase(listInput, cwd)
            elif 'DROP' in listInput and 'DATABASE' in listInput:
                dropDatabase(listInput, cwd)
            elif 'USE' in listInput:
                dbToUse = useDatabase(listInput, cwd)
            elif 'CREATE' in listInput and 'TABLE' in listInput:
                if dbToUse == '':
                    print("!Failed to create table " + listInput[2] + " because no database is being used.")
                else:
                    createTable(listInput, cwd, dbToUse)
            elif 'DROP' in listInput and 'TABLE' in listInput:
                if dbToUse == '':
                    print("!Failed to create table " + listInput[2] + " because no database is being used.")
                else:
                    dropTable(listInput, os.path.join(cwd, dbToUse))
            elif 'SELECT' in listInput and '*' in listInput and 'FROM' in listInput:
                if dbToUse == '':
                    print("!Failed to create table " + listInput[2] + " because no database is being used.")
                else:
                    selectTable(listInput, os.path.join(cwd, dbToUse))
            elif 'ALTER' in listInput and 'TABLE' in listInput:
                if dbToUse == '':
                    print("!Failed to create table " + listInput[2] + " because no database is being used.")
                else:
                    alterTable(listInput, os.path.join(cwd, dbToUse))
            elif userInput.startswith('--') or userInput == '\r' or userInput == '':
                pass
            elif listInput[0] == 'EXIT' or listInput[0] == '.EXIT':
                running = False
            else:
                print("Error: invalid Input.")
                continue
    
        print("All Done.")
    except:
        print("EOF")

if __name__ == "__main__":
    main()

# look into changing createTable to account for more than two attribute fields