import os
import shutil
import re
from colorama import Fore, Style  # type: ignore
# from DBMS import DBMS

class DBMS:

    def createDatabase(self, dbName: str, cwd: str) -> bool:
        # uses fileIO and os to create a new database directory folder

        newDBPath = os.path.join(cwd, dbName)

        if os.path.exists(newDBPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create database " + dbName + " because it already exists.")
            return False
        else:
            os.mkdir(newDBPath)
            print("Database " + dbName + " created.")
            return True


    def dropDatabase(self, dbName: str, cwd: str):
        # uses fileIO and os to delete a database directory if it exists

        dbPath = os.path.join(cwd, dbName)

        if not os.path.exists(dbPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to delete database " + dbName + " because it does not exist.")
            return False
        else:
            shutil.rmtree(dbPath, ignore_errors=True)
            print("Database " + dbName + " deleted.")
            return True


    def useDatabase(self,  dbToUse: str, cwd: str) -> str:
        # takes in cwd to check if database exists and returns a string of the name of the database to use

        dbPath = os.path.join(cwd, dbToUse)
        
        if not os.path.exists(dbPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to use " + dbToUse + " because it does not exist.")
            return ''
        else:
            print("Using database " + dbToUse + ".")
            return dbToUse


    def createTable(self, input: list, cwd: str, dbToUse: str):
        # takes in input, path, and the database to use to create a table file within the database to use
        # once file is created the tables attribute names are written to file using loop and string logic
        # to parse and format attribute field names correctly in table file
        
        # print(input)

        tblName = input[2].replace('(', ' ').split(' ')[0]
        tablePath = os.path.join(cwd, dbToUse, tblName)    

        if os.path.exists(tablePath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + input[2] + " because it already exists.")
            return False
        else:
            if not len(input) >= 5:
                print("Error: invalid input - not enough attribute titles.")
                return "Invalid Input"
            
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
            return True


    def dropTable(self, tableName: str, cwd: str):
        # uses fileIO and os to delete table file if it exists in the database being used

        tablePath = os.path.join(cwd, tableName)

        if not os.path.exists(tablePath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to delete " + tableName + " because it does not exist.")
            return "Unsuccessful - Table does not exist."
        else:
            os.remove(tablePath)
            print("Table " + tableName + " deleted.")
            return "Success."


    def selectTable(self, tableName: str, cwd: str, thisProcessLocked: bool):
        # uses fileIO to read attribute fields from designated table file and output 
        # also has lock file checks to determins if process has lock and which file has the
        # current data.

        contents = [str]
        tablePath = os.path.join(cwd, tableName)
        print(tablePath)

        if not os.path.exists(tablePath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + tableName + " because it does not exist.")
            return 'Select failed because table does not exist.'
        else:
            lockFile = tablePath + '_lock'
            if os.path.exists(lockFile): #and not thisProcessLocked:
                tablePath = lockFile

            with open(tablePath, 'r') as fp:
                contents = fp.readlines()
                pass

            for x in contents:
                print(x.replace('\n', ''))

            fp.close()
            return contents


    def alterTable(self, input: list, cwd: str):
        # uses fileIO to modify tables attributes

        tablePath = os.path.join(cwd, input[2])
        print(tablePath)

        if not os.path.exists(tablePath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + input[2] + " because it does not exist.")
            return "Table desired to alter does not exist."
        else:
            
            attributeStr = ''

            for i in range(4, len(input), 2):
                attributeStr += '|' + input[i] + ' ' + input[i + 1].replace(';', '')

                if i == len(input):
                    attributeStr += '|'

            if input[3] == 'ADD':
                print(attributeStr)
                with open(tablePath, 'r+') as fp:
                    first_line = fp.readline().rstrip('\n')
                    fp.seek(0)
                    fp.write(f"{first_line}{attributeStr}\n")

                    fp.write(fp.read())
                    # fp.write(attributeStr + "\n")
                    pass
                fp.close()

            print("Table " + input[2] + " modified.")
            return "Table modified successfully."


    def insertData(self, data: list, cwd: str):
        # takes in data to insert as a list and path so specified table can be found and used
        # data list is iterated through for parsing and formatting
        # then formatted data is appended into table file 

        tblName = data[2]
        tblPath = os.path.join(cwd, tblName)

        if not os.path.exists(tblPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to insert data because table" + tblName + "does not exist.")
            return False
        else:
            parsedData = []
            for x in data:
                parsedData.append(x.split('\t'))
                if x.endswith(';'):
                    break
            #print(parsedData)
            dataStr, start = '', 3

            flatParsedData = [elem for sublist in parsedData for elem in sublist]
            flatParsedData = [elem for elem in flatParsedData if elem != '']

            if len(flatParsedData) % 2 != 0:
                start = 4

            for i in range(start, len(flatParsedData)):
                dataStr += flatParsedData[i].replace('values(', '').replace('VALUES', '').replace(',', '|').replace(');', '').replace('\t', '').replace('\'', '').replace('(', '')

            print(dataStr)
            with open(tblPath, 'a+') as fp:
                dataInFile = fp.read()

                if not dataInFile.endswith('\n'):
                    fp.write(f'{dataStr}\n')
                else:
                    fp.write(f'\n{dataStr}\n')

            fp.close()

            print("1 new record inserted.")
            return True

    # update data helper function
    def processFileData(self, data: list, setAttr: str, whereAttr: str, dataToFind: str, dataToSet: str) -> list:
        # filters through file data to match values to corresponding columns
        # then it analyzes for matches in data if they fall into the parameters given by user the updates are made
        # through updating a list to return to update function 
        
        # print(data)
        # print("whereAttr - ", whereAttr)
        # print("setAttr - ", setAttr)
        # print("dataToFind - ", dataToFind)
        # print("dataToSet - ", dataToSet)

        splitLines = self.splitFileData(data)
        #print("split lines in process ", splitLines)

        indexToReplaceAt, colToSetAt, recordsModified = 0, 0, 0
        for index, dataType in enumerate(splitLines[0]):
            #print(index, dataType)
            if whereAttr in dataType:
                indexToReplaceAt = index
            elif setAttr in dataType:
                colToSetAt = index

        #print(splitLines)

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


    def updateData(self, tblName: str, modifyInfoLst: list, cwd: str, thisProcessUsingLock):
        # takes in update parameters from user and validates and parses it to send to helper function for updates
        # then list is returned from helper function to then be written back to the table file line by line
        # updates are done only if the process requesting has the lock
       
        # print("Table name - ", tblName)
        # print(" modifyInfoList - ", modifyInfoLst)
        tblPath = os.path.join(cwd, tblName)

        if not os.path.exists(tblPath):
            tblPath = os.path.join(cwd, tblName.capitalize())
            tblName = tblName.capitalize()
        #print(modifyInfoLst)
        #print(tblPath)

        # checks for a lock file and status and if exist and not process that is  
        # using lock, should not be able to update
        if os.path.exists(tblPath + '_lock') and not thisProcessUsingLock:
            print("Error: Table " + tblName + " is locked!")
            return "Table is locked so cannot update."
        elif len(modifyInfoLst) >= 8 and 'set' in modifyInfoLst and 'where' in modifyInfoLst:
            inputList = [elem for elem in modifyInfoLst if elem != '']
            parsedInput = [i for i in inputList if i != '\r']

            attributeToSet = parsedInput[1]
            attributeToFind = parsedInput[5]

            dataToFind = parsedInput[7].replace(';', '').replace('\'', '').replace('\r', '')
            dataToSet = parsedInput[3].replace('\'', '')
            #print('data to find is ' + dataToFind, 'data to set is ' + dataToSet)

            fp = open(tblPath, 'r')
            fileData = fp.readlines()

            replacedData = self.processFileData(fileData, attributeToSet, attributeToFind, dataToFind, dataToSet)

            fp.close()

            fp = open(tblPath, 'w')
            fp.write('\n'.join(replacedData))
            fp.close()
            return "Success!"

        else:
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid input.")
            return "Invalid input"


    def removeData(self, tblName: str, whereStmt: list, cwd: str):
        # File IO operations are used to read file data and check lines (aka tuples) for matching attributes
        # from specified values to delete. Function ensures that correct attribute types are being checked.
        # Then, updates are made to list of lines and written back with deleted info removed
        
        # print("Table name - ", tblName)
        # print("whereStmt - ", whereStmt)

        numDeleted, attributeToCheck = 0, ''
        tblPath = os.path.join(cwd, tblName)

        if not os.path.exists(tblPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to delete data from table " + tblName.replace('\r', '') + " because table not found.")
            return False
        else:
            if len(whereStmt) == 4 and 'where' in whereStmt:
                attributeToCheck = whereStmt[1]
            
            file = open(tblPath, 'r')
            fileData = file.readlines()

            data = self.splitFileData(fileData)
            file.close()    

            operator = whereStmt[2]
            operand = whereStmt[3].replace(';', '').replace('\'', '').replace('\r', '')
            
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
            return True


    #helper function - splits lines of data up from file readlines()
    def splitFileData(self, data: list) -> list:
        splitLines = []
        for line in data:
            splitData = line.replace('\n', '').replace('\t', '').split('|')
            splitLines.append(splitData)

        return splitLines


    def selectTableWithAttributes(self, infoLst: list, whereStmt: list, cwd: str):
        # function parses where commands and select commands to compare read in data points
        # from file to where boundaries and if select and where bounds apply, then the data
        # is formatted and printed

        # print("InfoLst - ", infoLst)
        # print("wherestmt - ", whereStmt)

        tblName = infoLst[4].capitalize()
        tblPath = os.path.join(cwd, tblName)
        operator, operand = whereStmt[2], whereStmt[3].replace(';', '').replace('\r', '')
        boundArg = whereStmt[1]

        if not os.path.exists(tblPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + tblName + " because it does not exist.")
            return False
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
            return True
        

    def fromParser(self, input:list):
        # function takes input list from user to then parse and remove not needed 
        # information to for selections and joins

        fromList = []    
            
        for x in input:
            if x == "select" or x == "\r" or x == "*" or x == '':
                pass
            elif x == 'where':
                break
            else:
                fromList.append(x.replace(',', ''))
        return fromList


    def queryAndJoinTables(self, input: list, whereList: list, cwd: str):
        # this function uses helper fromParser function to parse input command data
        # then uses this to find two tables to join or inner join.  Table files are opened
        # and read from by lines and a nested loop is used to compare and print joined table 
        # data based on query parameters.  Indicies are found before comparison so that correct 
        # attribute fields are being analyzed.

        fromList = self.fromParser(input)

        if 'inner' and 'join' in fromList:
            tbl1, tbl2 = fromList[1], fromList[5]
        else:
            tbl1, tbl2 = fromList[1], fromList[3]

            print(os.path.exists(os.path.join(cwd, tbl1)))

        if not os.path.exists(os.path.join(cwd, tbl1)) or not os.path.exists(os.path.join(cwd, tbl2)):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to join tables because one or both do not exist.")
            return False
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
            return True


    def leftOuterJoin(self, input: list, whereLst: list, cwd: str):
        # implements left outer join functionality through use of file IO operations to 
        # check two tables and find indicies to compare parameters given for join table 
        # result.  Nested for loop is used to compare the two data file contents and 
        # if equal a join is done and if not equal with other data from second table 
        # after all comparisons, then table 1 contents printed with null values.

        fromList = self.fromParser(input)
        tbl1, tbl2 = fromList[1], fromList[6]

        if not os.path.exists(os.path.join(cwd, tbl1)) or not os.path.exists(os.path.join(cwd, tbl2)):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to join tables because one or both do not exist.")
            return False
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
            return True


    def transactionManaging(self, cwd: str, processLocked: bool):
        # This function begins a transaction by reading transaction file contents and writing the state before 
        # the transaction began to a <tblName>_lock file.  This lock file is what keeps state as well as 
        # makes it so no other operation in another process can access the original table while the first transacaction
        # is not committed.  This is what keeps atomicity between processes.

        tableLst = os.listdir(cwd)
        
        for file in tableLst:
            lockTablePath = os.path.join(cwd, file + '_lock')
            tblPath = os.path.join(cwd, file)
            #print(lockTablePath)

            if os.path.exists(lockTablePath) or '_lock' in file:
                break
            else:
                # open and read contents from table starting transaction with
                with open(tblPath, 'r') as fp:
                    contents = fp.readlines()
                    pass

                # write the contents of transaction file to lock file to keep state of table before transaction started
                with open(lockTablePath, 'w') as fp:
                    fp.write(''.join(contents))
                    pass
                fp.close()
                processLocked = True

        print("Transaction starts.")
        return processLocked


    def commit(self, cwd: str, processUsingLock: bool):
        # this function handles transaction committs through use of a process 
        # status variable and os path functionality to commit changes and remove
        # the lock file.

        if not processUsingLock:
            print("Transaction abort.")
            return "Transaction aborted."
        else:
            # process using lock and needs to be committed
            # so delete lock file and set lock status to false
            # loops through db directory in case of multiple table
            tableLst = os.listdir(cwd)

            for tableName in tableLst:
                if os.path.exists(os.path.join(cwd, tableName + '_lock')):
                    os.remove(os.path.join(cwd, tableName + '_lock'))

                    print("Transaction committed.")
                    processUsingLock = False

        return processUsingLock


    def countTuples(self, cwd: str, tblName: str, attribute: str):
        
        tblPath = os.path.join(cwd, tblName)

        if not os.path.exists(tblPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to count records in " + tblName + " table because it does not exist.")
            return "Table does not exist so cannot count tuples."            
        else:
            with open(tblPath, 'r') as fp:
                data = fp.readlines()
                pass
            
            # print("Data in Count - ", data)
            print(attribute.replace('\t', '').replace('\r', ''))
            # lines of file minus the metadata line
            print("Table Count is ", len(data) - 1)
            return (len(data) - 1)


    def average(self, cwd: str, tblName: str, attribute: str):

        tblPath = os.path.join(cwd, tblName)
        attributeToFind = attribute.replace('AVG(', '').replace(')', '').replace('\t', '').replace('\r', '')

        if not os.path.exists(tblPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to count records in " + tblName + " table because it does not exist.")
            return "Cannot find average because table does not exist."
        else:
            with open(tblPath, 'r') as fp:
                data = fp.readlines()
                pass

            attributeNames = data[0].split('|')
            indexToAvg = 0
            for index, attr in enumerate(attributeNames):
                if attributeToFind in attr:
                    indexToAvg = index
            
            # print("Data in AVG - ", data)

            sum = 0
            for i in range(1, len(data)):
                splitLines = data[i].split('|')
                sum += float(splitLines[indexToAvg].replace('\n', ''))

            avg = sum / (len(data) - 1)
            
            print(attribute.replace('\t', '').replace('\r', ''))
            print("Average is ", avg)
            return avg


    def max(self, cwd: str, tblName: str, attribute: str):

        tblPath = os.path.join(cwd, tblName)
        attributeToFind = attribute.replace('MAX(', '').replace(')', '').replace('\t', '').replace('\r', '')

        if not os.path.exists(tblPath):
            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to count records in " + tblName + " table because it does not exist.")
            return "Table does not exist so cannot find MAX."
        else:
            maximum = 0

            with open(tblPath, 'r') as fp:
                data = fp.readlines()
                pass

            attributeNames = data[0].split('|')
            indexToCheckMax = 0
            for index, attr in enumerate(attributeNames):
                if attributeToFind in attr:
                    indexToCheckMax = index

            for i in range(1, len(data)):
                splitLines = data[i].split('|')
                if float(maximum) <= float(splitLines[indexToCheckMax].replace('\n', '')):
                    maximum = splitLines[indexToCheckMax]

            print(attribute.replace('\t', '').replace('\r', ''))
            print("Max is ", maximum)
            return float(maximum.replace("\n", ''))


    def processUncommittedHandler(self, cwd: str):
        # checks if a lock file exists because if it does that means the process with access to the lock 
        # did not commit, so then the status in the lock needs to be written back to what it was before 
        removedLocks = False

        tables = os.listdir(cwd)
        print("Tables in handler - ", tables)
        for tbl in tables:
            tblPath = os.path.join(cwd, tbl)
            if os.path.exists(tblPath + '_lock'):
                #os.remove(os.path.join(cwd, dbToUse, tbl))
                #os.rename(os.path.join(cwd, dbToUse, tbl + '_lock'), os.path.join(cwd, dbToUse, tbl))
                with open(tblPath + '_lock', 'r') as fp:
                    originalContents = fp.readlines()
                    pass
                fp.close()
                with open(tblPath, 'w') as file:
                    file.write(''.join(originalContents))
                    pass
                file.close()
                os.remove(tblPath + '_lock')
                removedLocks = True
        return removedLocks