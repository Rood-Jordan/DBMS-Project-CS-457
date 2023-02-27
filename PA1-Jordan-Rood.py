# Author: Jordan Rood 
# CS 457 : DATABASE MANAGEMENT SYSTEMS
# Programming Assignment 1 - Metadata Management System
# Date: 02-08-2023

import os, sys

def manageInput(input: str) -> list:
    lst = input.split(" ")

    if len(lst) == 1:
        lst = [lst[0].upper()]
    elif len(lst) == 2:
        lst = [lst[0].upper(), lst[1].replace(';', '')]
    elif len(lst) == 3:
        lst = [lst[0].upper(), lst[1].upper(), lst[2].replace(';', '')]
    elif len(lst) == 7:
        lst = [lst[0].upper(), lst[1].upper(), lst[2], lst[3].replace('(', ''), lst[4].replace(',', ''), lst[5], lst[6].replace(');', '')]
        
        
    #print(lst)

    return lst

def createDatabase(input: list, cwd: str):
    #cwd = os.getcwd()
    newDBPath = os.path.join(cwd, input[2])

    if os.path.exists(newDBPath):
        print("!Failed to create database " + input[2] + " because it already exists.")
    else:
        os.mkdir(newDBPath)
        print("Database " + input[2] + " created.")


def dropDatabase(input: list, cwd: str):
    #cwd = os.getcwd()
    dbPath = os.path.join(cwd, input[2])

    if not os.path.exists(dbPath):
        print("!Failed to delete database " + input[2] + " because it does not exist.")
    else:
        os.rmdir(dbPath)
        print("Database " + input[2] + " deleted.")

def useDatabase(input: list, cwd: str) -> str:
    dbToUse = input[1]
    dbPath = os.path.join(cwd, dbToUse)
    
    if not os.path.exists(dbPath):
        print("Error: cannot use " + dbToUse + " because it does not exist.")
        return ''
    else:
        print("Using database " + dbToUse + ".")
        return dbToUse

def createTable(input: list, cwd: str, dbToUse: str):
    tablePath = os.path.join(cwd, dbToUse, input[2])    

    if os.path.exists(tablePath):
        print("!Failed to create table " + input[2] + " because it already exists.")
    else:
        attributeStr = str(input[3] + ' ' + input[4] + ' | ' + input[5] + ' ' + input[6])
        with open(tablePath, 'w') as fp:
            fp.write(attributeStr)
            pass
        print("Table " + input[2] + " created.")

def dropTable(input: list, cwd: str):
    tablePath = os.path.join(cwd, input[2])

    if not os.path.exists(tablePath):
        print("!Failed to delete " + input[2] + " because it does not exist.")
    else:
        os.remove(tablePath)
        print("Table " + input[2] + " deleted.")

def alterTable():
    print("In alter table")

def selectTable(input: list, cwd: str):
    print("In select table")



    

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
                createTable(listInput, cwd, dbToUse)
            elif 'DROP' in listInput and 'TABLE' in listInput:
                dropTable(listInput, os.path.join(cwd, dbToUse))
            elif 'SELECT' in listInput and '*' in listInput and 'FROM' in listInput:
                selectTable(listInput, cwd)
            elif 'ALTER' in listInput and 'TABLE' in listInput:
                pass
            elif userInput.startswith('--') or userInput == '\r':
                continue
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