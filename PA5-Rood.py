# Author: Jordan Rood 
# CS 457 : DATABASE MANAGEMENT SYSTEMS
# Programming Assignment 4 - Transactions: built off previous assignment(s) Basic Data Manipulation, Metadata Management System, and Table Joins
# Date: 05-04-2023

# Updated April 2024 through testing and DevOps integrations

from MainController import MainController
from SingleQueryController import SingleQueryController

if __name__ == "__main__":
    m = MainController()
    s = SingleQueryController()

    print("-----DBMS Simulator-----\n\n")
    print("This DBMS has two modes.\nThere is the Single Query Controller mode which allows for one query.\nOr the Main Controller which lets you put in as many query's as you want until keyboard interrupt or \'exit\' is input.\n\n")

    controller = input("Do you want to use the Single Query Controller (press 1) or the Main Controller (press 2)? ")
    if input == 1:
        s.main()
    elif input == 2:
        m.main()
    else:
        print("Invalid input.  Please try again.")
