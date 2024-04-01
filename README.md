# PA5-CS-457 Metadata management system, Basic Data Manipulation, Table Joins, Transactions, and AGGREGATIONS (COUNT, MAX, AVG)

## Student Name: Jordan Rood
---
## Description:
This program allows a database user to manage metadata/create database and tables within.
Metadata meaning the database's high-level info (db's name, creation date/time, etc.)

Furthermore, this program allows insertion, deletion, and modification to tuples within tables.  Extension has also been made to the select command where basic select commands with attribute title specification and basic query operations on data withing tables.

Table joins functionality are also implemented with differing syntactical commands for specific joins such as inner join or left outer join.  Finally, transactions are also implemented to uphold atomicity characteristics between simultaneous processes.

**Data is persistent (e.g., stored on hard drive) through use of relative path functionality.**

---
### Interface:
- Similar, but simpler interface than Sqlite3

- **Database creation** to make folder directory under input database name and **database deletion** by removing folder directory input by user.

- **Table creation** to make file in designated database folder under input table and **table deletion** to delete specified tables input by user.

- **Tuple insertion** by appending parsed and formatted data to table (file) specified

- **Tuple deletion** by reading table data from file, parsing out/removing the given matching arguments, and writing remaining data back to table file.

- **Table joins** to join two tables within a database based on input criteria/commands.  Specific functionality supports inner joins and left outer joins.

- **Tranactions** have a start and a commit so that only one process can only access the database or table they are updating and/or using if they were first to begin a transaction with it.  This also means if a process is already using a table, then it is locked so any commands used on that table by another process will fail.  Any commits will abort as well if made by a process that does not have possession of the lock.

---
## Requirements

* Python 3.9.13
---
## Functionalities

- CREATE DATABASE: creates a new database (i.e., directory).
- DROP DATABASE: deletes a specified database.
- USE DATABASE: specifies a database to use to properly work with tables.
- CREATE TABLE: creates a new table in a specified database (i.e., file within a directory).
- DROP TABLE: deletes a specified table in a specified database.
- SELECT TABLE: retrieves tuples or records from a specified table.
- ALTER TABLE: adds a new column (attribute title) to a specified table.
- INSERT DATA: adds data into specified table relating to metadata input from creation of that table prior.
- UPDATE DATA: modifies data in table based on specifications given (e.g., changing price where name is 'Gizmo' at every occurrence within a table).
- REMOVE DATA: deletes data from table based on given bounds or parameters.
- INNER JOIN TABLES: two basic syntax to compare attribute fields in two tables and join them together if equal comparison.
- LEFT OUTER JOIN TABLES: similar to inner join with comparision between table fields but joins onto the first table input by user.
- BEGIN TRANSACTION: starts a transaction successfully despite if another transaction has started and not been committed previously
- COMMIT TRANSACTION: this command commits a transaction if the process committing is the one with possession of the lock (e.g., the process that started the first uncommitted transaction).  All other commits abort if table is locked by another process.

---
## Sample Execution, Output, and Usage Examples

**Expected output that matches following testscript provided**

Program can be ran by file input (for test scripts 1 through 3) or by inputing all commands individually on command line; this will obtain same expected output. 

To run program by file or script (which can only be done for test scripts 1-3) input this command into the terminal:
```
$ python PA5-Rood.py < PA5_test.sql
```

To run program and input commands individually simply run the python program:

```
$ python PA5-Rood.py
```
and input commands and arguments:
```
COMMANDS <arguments>;
```

* NOTE - PA4 test script commands NEED to be put in individually as some commands are input into one terminal and some in another (in a specific order).

Additional example input and output is as follows:
```
-- CS457 PA5
-- 
-- This is an bonus assignment. It is NOT required.
-- It will be counted as five (5) points; thus, the overall possible points you can get are 105.
--
-- Grading: 1 point for design document, 1 point for coding style, and 3 points for three aggregate queries (i.e., COUNT, AVG, and MAX).

CREATE DATABASE db_tpch;
USE db_tpch;

CREATE TABLE Part (Partkey int, Size int);

INSERT INTO Part VALUES (1, 7);
INSERT INTO Part VALUES (2, 1);
INSERT INTO Part VALUES (3, 21);
INSERT INTO Part VALUES (4, 14);
INSERT INTO Part VALUES (5, 15);
INSERT INTO Part VALUES (6, 4);
INSERT INTO Part VALUES (7, 45);
INSERT INTO Part VALUES (8, 41);
INSERT INTO Part VALUES (9, 12);
INSERT INTO Part VALUES (10, 44);

SELECT 	COUNT(*)
FROM	Part;

SELECT 	AVG(Size)
FROM	Part;

SELECT 	MAX(Size)
FROM	Part;

.EXIT

-- Expected output
--
-- Database db_tpch created.
-- Using database db_tpch.
--
-- Table Part created.
--
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
--
-- COUNT(*)
-- 10
--
-- AVG(Size)
-- 20.4
--
-- MAX(Size)
-- 45
--
-- All done.
```
---


## How my program organizes multiple databases:

To organize the databases, I have implemented functionality so that every database made by the user creates a new directory, or folder, under the name specified by the user.  The database creation and delete functions take in the current working directory through use of os built-in functions to get the relative path that you are in when running the program.  This ensures that the data is persistent.   Ultimately, every database is separated by directory where it is its very own folder to keep all organized and separated properly for the user.

---
## How program manages multiple tables:

To manage multiple tables, the database to use is needed to be specified by the user beforehand because this portrays which database (aka folder or directory) that the table to be added should be placed in.  I have control flow functionality that ensures that an error statement is output if trying to create, delete, modify, or query a table when a database is not specified for use before.   If the user has communicated an relevant database to use, a table is then going to be created as a new txt file under the given table name.  Then, the attribute fields given to the create or modify the table are then added to the file with string IO to format it correctly when writing to the file.  Finally, the drop table functionality uses the os library to remove the file desired from input and the query functionality reads from the desired table file.

---
## How are these functionalities implemented (Explained at a high level):

All if not most of these functionalities are implemented using fileIO and the os library to ensure all relative paths used are correct.  Through organizing database creation in folders and tables as files in database folders, fileIO and the os functionality allowed me to efficiently manage the file system and take advantage of these built-in library function to implement all these functions.  Overall, the string, os, and file IO operations available in python allowed me to properly manage the metadata taken in and organize the databases and tables by establishing databases and files within them respectively.

---
## How program stores tuples in the table

The functionality for storing data tuples within tables is made up of multiple steps. First being that a database must be specified to be in use before any interaction with a table can occur.  Therefore, if a tuple is to be inserted without a database in use, then an error message with be displayed to the user.  If a database is specified to be in use, then the input is taken and the table name specified along with its values are parsed to be formatted and appended to the table file.  The values given are formatted using the '|' symbol to distinguish between the differing columns.  Finally, this formatting is done and the tuple is inserted into the given table by appending using file IO operations.

---
## How required functionalities corresponding to tuple insertion, deletion, modification, and query

All the functionalities are designed around the use of a multitude of file IO operations due to the layout of databases being folder directories and tables being files within those folders.  The tuple insertion as discussed in section above  is done through taking command from user, parsing input data values, and writing the formatted data into the corresponding table, or file.  Tuple deletion is opposite in that the parameters given to remove are evaluated from the read in table contents and only those that are not matched to the bounds to delete are written back to the file.  This ultimately deletes the data specified from the table file.  

The update table functionality operates using a couple helper functions that work to process file data read in and split those values up to make comparisons based on given operations.  The processFileData helper function is called to do this work and returns a list of formatted lines with updates where needed to the updateData function.  To complete the modification operation, the list of lines returned from processFileData is written to the table which reflects all the correct modifications.  

Finally, the query operation was updated so that specified attribute columns can be displayed and only data that falls within the given parameters of the command are displayed to the user.  This is done through reading in file data and looping through the parsed values to check if it qualifies under the given query.  If it does, it is printed otherwise it is not.  To conclude, all of these functionalities are implemented with further in line comments describing the sections with more complex code which will show in-depth the specifics of my corresponding functions.

---
## How inner join and left outer join are implemented

The table join functionality is split up between a couple functions that are used based on the syntax input by the database user.  In both the join/inner join function and left outer join function, a helper parser function is used to filter through the input given by the user.  This returns a list of the parsed data needed to determine the corresponding tables needed to be read in for the joins.  In both join functions, the table paths are both checked to ensure validity of tables desired to be joined and if valid the function moves on to open and read the designated files line by line.  Next, the attribute fields are printed from tables and they are compared to the command input by the user to mark the indices (attribute fields within the file) that need to be checked and/or compared.

Further, the function continues on to a nested for loop which essentially compares all tuples in first designated table to all other tuples in second designated table.  If they are equal corresponding to the operator then the join of the tables is done and printed.  For left outer join, the implemented functionality differs through further checks done in the nested for loop that is comparing the attribute fields specified.  A left outer join, joins based on the comparison given if they fields are equal.  However, the fields of table 1 are printed with null values (or empty string) if none are equal because a left outer join is meant to join onto left table (aka first table in our implementation)

Overall, nested for loops coupled with File IO are used to implement the comparisons for both inner joins and left outer joins similar to SQL.

---
## How transactions are implemented

Transactions are implemented through use of a couple helper functions as well as some needed modifications to other table and database manipulation functions using a passed around lock variable to indicate what process has access to the locked table from a transaction.  

First, a transaction must be started; the first process to begin a transaction then creates a lock for the file it is accessing.  In my design, I thought the best way to keep order in the original state of the file before a commit would be to read the contents of the file at the start of the transaction and copy it over into the empty <tblName>_lock file.  This way if the transaction data is uncommitted, the original data is still accessible by certain processes when needed.  The lock file also indicates to other processes that another process is accessing it; therefore, it has "locked" other processes out.

Other processes can start transactions successfully, but cannot access the table to make any updates unless the process trying to do so is the one in possession of the lock.  This is simply checked by checking the current directory for a respective lock table.  If there is a lock file and the process is not the one with access to the lock, then it cannot access the table and an error message is output to the terminal.  

The processes each have a state variable that is used throughout the transaction(s) functions to help with the logic as to whether or not that process can update changes to the table and/or commit its transaction successfully.  

Overall, the creation of a lock file and keeping a boolean state variable up to date throughout commands in a process is what helps to decide whether or not a process can commit and have access to a table.  

Upon a commit, if the process lock variable is true then that commit will be successful and the original data within the locked file will be deleted.  The lock boolean will be reset to false upon completion of this command as well.  If the process is the one locked out (e.g., the status variable will be false because it does not possess the lock), the commit will automatically abort and send the appropriate abort message to the terminal.  To note, no updates will persist without a commit and that is due to an additional function that is called upon exiting the program.  This function checks if a <tblName>_lock file exists and if one does, that means that a commit for the process with access to the lock was not made.  Then, the original contents before the transaction is made sure to be in the file through help of the lock file.  Then to finish the lock file is deleted.  Finally, the mentioned functionality is what showcases atomicity between simultaneously running processes. 

---
## How count aggregation is implemented

This functionality works by opening a stream to the designated table file and using readlines().  The readlines function gets each line and stores it in a list.  Therefore, the number of records is the length of the list subtracted by one (due to the first line of attribute names).  This is what finds the total number of tuples within the specified table.

---
## How avg aggregation is implemented

This functionality is implemented where the attribute name is searched for to find the right column within the tuples to look in.  The file contents are then iterated through at the found index to check and each are added to a sum variable to have the total after the loop.  Then, finally to find the average the sum is divided by the length of the data (minus the metadata line) which is the total number of records in the table.  This then outputs the average of the attribute specified from the table input.

---
## How max aggregation is implemented

The max is found similar to the average functionality.  However, after finding the index to check instead of taking the sum each iteration, a comparison is taken to find the greater of the two numbers.  A maximum variable is kept track of throughout to ultimately output the max value found from the attribute within the table desired.