
import os
from colorama import Fore, Style  # type: ignore
from DBMS import DBMS

class MainController:
    
    def main(self): 
        # main function which takes in input from command line and matches it with the corresponding function(s)
        # also multiple validity checks here and in additional functions used above

        try:
            running, dbToUse, processLocked = True, '', False
            cwd = os.getcwd()
            dbms = DBMS()

            while running:
                userInput = input("> ")

                upperInput = userInput.upper()
                listInput = userInput.split(" ")
                # print(listInput)
                # print(userInput)
                
                if userInput.startswith('--') or userInput == '' or userInput == '\r':
                    pass

                elif upperInput == 'EXIT' or upperInput == '.EXIT\r' or upperInput == '.EXIT':
                    running = False

                elif upperInput.startswith('CREATE DATABASE') and len(listInput) == 3:
                    dbms.createDatabase(listInput[2].replace(';', '').replace('\r', ''), cwd)

                elif upperInput.startswith('DROP DATABASE') and len(listInput) == 3:
                    dbms.dropDatabase(listInput[2].replace(';', '').replace('\r', ''), cwd)

                elif upperInput.startswith('USE') and len(listInput) == 2:
                    dbToUse = dbms.useDatabase(listInput[1].replace(';', '').replace('\r', ''), cwd)

                elif upperInput.startswith('CREATE TABLE') and len(listInput) >= 5:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    else:
                        dbms.createTable(listInput, cwd, dbToUse)

                elif upperInput.startswith('DROP TABLE') and len(listInput) == 3:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to drop table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    else:
                        dbms.dropTable(listInput[2].replace(';', '').replace('\r', ''), os.path.join(cwd, dbToUse))

                elif upperInput.startswith('SELECT * FROM') and len(listInput) == 4:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + listInput[3].replace(';', '').replace('\r', '') + " because no database is being used.")
                    else:
                        dbms.selectTable(listInput[3].replace (';', '').replace('\r', ''), os.path.join(cwd, dbToUse), processLocked)

                elif upperInput.startswith('ALTER TABLE') and 'ADD' in upperInput and len(listInput) == 6:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    else:
                        dbms.alterTable(listInput, os.path.join(cwd, dbToUse.replace(';', '').replace('\r', '')))

                elif upperInput.startswith('INSERT INTO') and 'VALUES' in upperInput and len(listInput) >= 4:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    else:
                        dbms.insertData(listInput, os.path.join(cwd, dbToUse.replace('\r', '')))

                elif upperInput.startswith('UPDATE') and (len(listInput) >= 2 and len(listInput) < 4 or len(listInput) == 10):
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[1] + " because no database is being used.")
                    elif len(listInput) == 10 and upperInput.endswith(';'):
                        dbms.updateData(listInput[1], listInput[2:], os.path.join(cwd, dbToUse), processLocked)
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
                            dbms.updateData(listInput[1], updateLineInfo.split(" "), os.path.join(cwd, dbToUse), processLocked)
                        else:
                            print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid number of commands.")

                elif upperInput.startswith('DELETE FROM') and len(listInput) >= 7:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2].capitalize() + " because no database is being used.")
                    else:
                        # delLineInfo, counter = '', 0
                        # while True or counter <= 2:
                        #     line = input()
                        #     if ';' not in line:
                        #         delLineInfo += ' ' + line
                        #         counter += 1
                        #     else:
                        #         delLineInfo += ' ' + line
                        #         break
                        
                        dbms.removeData(listInput[2].capitalize(), listInput[3:], os.path.join(cwd, dbToUse))

                elif upperInput.startswith('SELECT') and len(listInput) >= 3:
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
                        # print("LineInfo - ", lineInfo)
                        # print("whereStr - ", whereStr)

                        if len(listInput) == 3 and 'left outer join' in userInput:
                            dbms.leftOuterJoin(userInput.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))
                        elif len(listInput) == 3 and 'inner join' in userInput:
                            dbms.queryAndJoinTables(userInput.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))
                        else:
                            dbms.selectTableWithAttributes(listInput, listInput[5:], os.path.join(cwd, dbToUse))  

                elif upperInput == 'BEGIN TRANSACTION;':
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to begin transaction because no database is in use.")
                    else:                
                        processLocked = dbms.transactionManaging(os.path.join(cwd, dbToUse), processLocked)
                
                elif upperInput.startswith('COMMIT;'):
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to begin transaction because no database is in use.")
                    else:
                        processLocked = dbms.commit(os.path.join(cwd, dbToUse), processLocked)

                elif 'SELECT' in listInput and '\tCOUNT(*)\r' in listInput:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to count records because no database is in use.")
                    else:
                        fromLine = input()
                        dbms.countTuples(os.path.join(cwd, dbToUse), fromLine.split('\t')[1].replace(';', '').replace('\r', ''), listInput[1])

                elif 'SELECT' in listInput and 'AVG' in upperInput:
                    if dbToUse == '':
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to find average of attribute because no database is in use.")
                    else:
                        fromLine = input()
                        dbms.average(os.path.join(cwd, dbToUse), fromLine.split('\t')[1].replace(';', '').replace('\r', ''), listInput[1])

                elif 'SELECT' in listInput and 'MAX' in upperInput:
                    if dbToUse == '':   
                        print(Fore.RED + "!Failed " + Style.RESET_ALL + "to find max of attribute because no database is in use.")
                    else:
                        fromLine = input()
                        max(os.path.join(cwd, dbToUse), fromLine.split('\t')[1].replace(';', '').replace('\r', ''), listInput[1])

                else:
                    print("Error: invalid input.")
                    # print(userInput)
                    continue
            
            dbms.processUncommittedHandler(os.path.join(cwd, dbToUse))
            print("All done.")

        except KeyboardInterrupt:
            print(" You cancelled the operation.")
        except Exception:
            print("Error: exception occurred!")
