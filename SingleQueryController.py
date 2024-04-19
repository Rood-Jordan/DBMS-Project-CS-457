import os
from DBMS import DBMS

class SingleQueryController:
    
    def main(self, userInput, dbToUse = ''): 
        # main function which takes in input from command line and matches it with the corresponding function(s)
        # also multiple validity checks here and in additional functions used above

            processLocked = False
            cwd = os.getcwd()
            dbms = DBMS()

            # userInput = input("> ")

            upperInput = userInput.upper()
            listInput = userInput.split(" ")
            # print(listInput)
            # print(userInput)
        
            if upperInput.startswith('CREATE DATABASE') and len(listInput) == 3:
                result = dbms.createDatabase(listInput[2].replace(';', '').replace('\r', ''), cwd)

            elif upperInput.startswith('DROP DATABASE') and len(listInput) == 3:
                result = dbms.dropDatabase(listInput[2].replace(';', '').replace('\r', ''), cwd)

            elif upperInput.startswith('USE') and len(listInput) == 2:
                result = dbms.useDatabase(listInput[1].replace(';', '').replace('\r', ''), cwd)

            elif upperInput.startswith('CREATE TABLE') and len(listInput) >= 5:
                if dbToUse == '':
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to create table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    print("!Failed to create table " + listInput[2].replace('\r', '') + " because no database is being used.")

                else:
                    result = dbms.createTable(listInput, cwd, dbToUse)

            elif upperInput.startswith('DROP TABLE') and len(listInput) == 3:
                if dbToUse == '':
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to drop table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    print("!Failed to drop table " + listInput[2].replace('\r', '') + " because no database is being used.")

                else:
                    result = dbms.dropTable(listInput[2].replace(';', '').replace('\r', ''), os.path.join(cwd, dbToUse))

            elif upperInput.startswith('SELECT * FROM') and len(listInput) == 4:
                if dbToUse == '':
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to query table " + listInput[3].replace(';', '').replace('\r', '') + " because no database is being used.")
                    print("!Failed to query table " + listInput[3].replace(';', '').replace('\r', '') + " because no database is being used.")

                else:
                    result = dbms.selectTable(listInput[3].replace (';', '').replace('\r', ''), os.path.join(cwd, dbToUse), processLocked)

            elif upperInput.startswith('ALTER TABLE') and 'ADD' in upperInput and len(listInput) == 6:
                if dbToUse == '':
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    print("!Failed to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")

                else:
                   result = dbms.alterTable(listInput, os.path.join(cwd, dbToUse.replace(';', '').replace('\r', '')))

            elif upperInput.startswith('INSERT INTO') and 'VALUES' in upperInput and len(listInput) >= 4:
                if dbToUse == '':
                    result = None
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")
                    print("!Failed to alter table " + listInput[2].replace('\r', '') + " because no database is being used.")

                else:
                    result = dbms.insertData(listInput, os.path.join(cwd, dbToUse.replace('\r', '')))

            elif 'SELECT' in listInput and 'COUNT(*)' in listInput:
                if dbToUse == '':
                    result = None
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to count records because no database is in use.")
                    print("!Failed to count records because no database is in use.")

                else:
                    result = dbms.countTuples(os.path.join(cwd, dbToUse), listInput[3].replace(';', '').replace('\r', ''), listInput[1])

            elif 'SELECT' in listInput and 'AVG' in upperInput:
                if dbToUse == '':
                    result = None
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to find average of attribute because no database is in use.")
                    print("!Failed to find average of attribute because no database is in use.")

                else:
                    print("JEREERLEKJRLE")
                    result = dbms.average(os.path.join(cwd, dbToUse), listInput[3].replace(';', '').replace('\r', ''), listInput[1])

            elif 'SELECT' in listInput and 'MAX' in upperInput:
                if dbToUse == '':   
                    result = None
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to find max of attribute because no database is in use.")
                    print("!Failed to find max of attribute because no database is in use.")

                else:
                    result = dbms.max(os.path.join(cwd, dbToUse), listInput[3].replace(';', '').replace('\r', ''), listInput[1])

            elif upperInput.startswith('UPDATE') and (len(listInput) >= 2 and len(listInput) < 4 or len(listInput) == 10):
                if dbToUse == '':
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[1] + " because no database is being used.")
                    print("!Failed to modify table data in " + listInput[1] + " because no database is being used.")

                elif len(listInput) == 10 and upperInput.endswith(';'):
                    result = dbms.updateData(listInput[1], listInput[2:], os.path.join(cwd, dbToUse), processLocked)
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
                        result = dbms.updateData(listInput[1], updateLineInfo.split(" "), os.path.join(cwd, dbToUse), processLocked)
                    else:
                        # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data due to invalid number of commands.")
                        print("!Failed to modify table data due to invalid number of commands.")

            elif upperInput.startswith('DELETE FROM') and len(listInput) >= 7:
                if dbToUse == '':
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2].capitalize() + " because no database is being used.")
                    print("!Failed to modify table data in " + listInput[2].capitalize() + " because no database is being used.")

                else:
                    
                    result = dbms.removeData(listInput[2].capitalize(), listInput[3:], os.path.join(cwd, dbToUse))

            elif upperInput.startswith('SELECT') and len(listInput) >= 3:
                if dbToUse == '':
                    result = True
                    # print(Fore.RED + "!Failed " + Style.RESET_ALL + "to modify table data in " + listInput[2].capitalize() + " because no database is being used.")
                    print("!Failed to modify table data in " + listInput[2].capitalize() + " because no database is being used.")

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

                    if len(listInput) >= 3 and 'left outer join' in userInput:
                        result = dbms.leftOuterJoin(userInput.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))
                    elif len(listInput) >= 3 and 'inner join' in userInput:
                        result = dbms.queryAndJoinTables(userInput.split(" "), whereStr.split(" "), os.path.join(cwd, dbToUse))
                    else:
                        result = dbms.selectTableWithAttributes(listInput, listInput[5:], os.path.join(cwd, dbToUse))  

                # Cannot do transactions in single query controller mode, does not work with characteristics of Begin transaction or commit

            else:
                print("Error: invalid input.")
                result = "Invalid input."
            

            return result
