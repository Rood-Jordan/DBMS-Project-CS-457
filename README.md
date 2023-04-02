# PA2-CS-457 METADATA MANAGEMENT SYSTEM & Basic Data Manipulation

## Student Name: Jordan Rood
---
## Description:
This program allows a database user to manage metadata/create database and tables within.
Metadata meaning the database's high-level info (db's name, creation date/time, etc.)

Furthermore, this program allows insertion, deletion, and modification to tuples within tables.  Extension has also been made to the select command where basic select commands with attribute title specification and basic query operations on data withing tables.

**Data is persistent (e.g., stored on hard drive) through use of relative path functionality.**

---
### Interface:
- Similar, but simpler interface than Sqlite3

- **Database creation** to make folder directory under input database name and **database deletion** by removing folder directory input by user.

- **Table creation** to make file in designated database folder under input table and **

- **Tuple insertersion** by appending parsed and formatted data to table (file) specified

- **Tuple deletion** by reading table data from file, parsing out/removing the given matching arguments, and writing remaining data back to table file.
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

---
## Sample Execution, Output, and Usage Examples

**Expected output that matches following testscript provided**

Program can be ran by file input or by inputing all commands individually on command line; this will obtain same expected output. 

To run program by file or script input:
```
$ python PA2-Rood.py < PA2_test.sql
```

To run program and input commands individually simply run the python program:

```
$ python PA2-Rood.py
```
and input commands and arguments:
```
COMMANDS <arguments>;
```

Additional example input and output is as follows:
```
--CS 457 PA2 test script

CREATE DATABASE CS457_PA2;
USE CS457_PA2;
CREATE TABLE Product (pid int, name varchar(20), price float);

insert into Product values(1,	'Gizmo',      	19.99);
insert into Product values(2,	'PowerGizmo', 	29.99);
insert into Product values(3,	'SingleTouch', 	149.99);
insert into Product values(4,	'MultiTouch', 	199.99);
insert into Product values(5,	'SuperGizmo', 	49.99);

select * from Product;

update Product 
set name = 'Gizmo' 
where name = 'SuperGizmo';

update Product 
set price = 14.99 
where name = 'Gizmo';

select * from Product;

delete from product 
where name = 'Gizmo';

delete from product 
where price > 150;

select * from Product;

select name, price 
from product 
where pid != 2;

.exit

-- Expected output
--
-- Database CS457_PA2 created.
-- Using database CS457_PA2.
-- Table Product created.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- 1 new record inserted.
-- pid int|name varchar(20)|price float
-- 1|Gizmo|19.99
-- 2|PowerGizmo|29.99
-- 3|SingleTouch|149.99
-- 4|MultiTouch|199.99
-- 5|SuperGizmo|49.99
-- 1 record modified.
-- 2 records modified.
-- pid int|name varchar(20)|price float
-- 1|Gizmo|14.99
-- 2|PowerGizmo|29.99
-- 3|SingleTouch|149.99
-- 4|MultiTouch|199.99
-- 5|Gizmo|14.99
-- 2 records deleted.
-- 1 record deleted.
-- pid int|name varchar(20)|price float
-- 2|PowerGizmo|29.99
-- 3|SingleTouch|149.99
-- name varchar(20)|price float
-- SingleTouch|149.99
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

All the functionalities are designed around the use of a multitude of file IO operations due to the layout of databases being folder directories and tables being files within those folders.  The tuple insertion as discussed in section above  is done through taking command from user, parsing input data values, and writing the formatted data into the corresponding table, or file.  Tuple deletion is opposite in that the parameters given to remove are evaluated from the read in table contents and only those that are not matched to the bounds to delete are written back to the file.  This ultimately deletes the data specified from the table file.  The update table functionality operates using a couple helper functions that work to process file data read in and split those values up to make comparisons based on given operations.  The processFileData helper function is called to do this work and returns a list of formatted lines with updates where needed to the updateData function.  To complete the modification operation, the list of lines returned from processFileData is written to the table which reflects all the correct modifications.  Finally, the query operation was updated so that specified attribute columns can be displayed and only data that falls within the given parameters of the command are displayed to the user.  This is done through reading in file data and looping through the parsed values to check if it qualifies under the given query.  If it does, it is printed otherwise it is not.  To conclude, all of these functionalities are implemented with further in line comments describing the sections with more complex code which will show in-depth the specifics of my corresponding functions.