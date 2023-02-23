# Author: Jordan Rood 
# Date: 02-08-2023
# CS 457: Programming Assignment 1 - Metadata Management System

import os, sys


def createDatabase():

    pass

def dropDatabase():

    pass

def createTable():

    pass

def alterTable():

    pass

def selectTable():

    pass

def dropTable():

    pass

def main():
    userInput = input("")
    running = True

    while running:
        userInput = input("")

        if userInput == 'exit' or userInput == 'EXIT':
            running = False
        elif "CREATE DATABASE" in userInput:
            pass
        elif "DROP DATABASE" in userInput:
            pass
        elif "CREATE TABLE" in userInput:
            pass
        elif "DROP TABLE" in userInput:

            pass
    
    print("All Done.")


if __name__ == "__main__":
    main()