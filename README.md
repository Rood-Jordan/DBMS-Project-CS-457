# PA1-CS-457 METADATA MANAGEMENT SYSTEM

This program allows a database user to manage metadata/create database and tables within.
Metadata meaning the database's high-level info (db's name, creation date/time, etc.)

Data should be persistent (e.g., stored on hard drive)

Functionalities:
- Database creation, deletion
- Table creation, deletion, update, and query

Interface:
- similar but simpler interface than Sqlite3

- Database creation to make folder directory
- table creation to make file in designated database folder

- For Invalid input output prompt "Error: unknown command, invalid arguments or missing semicolon"
- <enter> is empty line so should be invalid input

## Requirements

* Python 3.9.13
---

## Sample Execution & Output

**Expected output that matches following testscript provided** 
Can also make all of the commands individually on command line and will obtain same expected output. 

```
--CS457 PA1

CREATE DATABASE db_1;
CREATE DATABASE db_1;
CREATE DATABASE db_2;
DROP DATABASE db_2;
DROP DATABASE db_2;
CREATE DATABASE db_2;


USE db_1;
CREATE TABLE tbl_1 (a1 int, a2 varchar(20));
CREATE TABLE tbl_1 (a3 float, a4 char(20));
DROP TABLE tbl_1;
DROP TABLE tbl_1;
CREATE TABLE tbl_1 (a1 int, a2 varchar(20));
SELECT * FROM tbl_1;
ALTER TABLE tbl_1 ADD a3 float;
SELECT * FROM tbl_1;
CREATE TABLE tbl_2 (a3 float, a4 char(20));
SELECT * FROM tbl_2;
USE db_2;
SELECT * FROM tbl_1;
CREATE TABLE tbl_1 (a3 float, a4 char(20));
SELECT * FROM tbl_1;

.EXIT

-- Expected output
--
-- Database db_1 created.
-- !Failed to create database db_1 because it already exists.
-- Database db_2 created.
-- Database db_2 deleted.
-- !Failed to delete db_2 because it does not exist.
-- Database db_2 created.
-- Using database db_1.
-- Table tbl_1 created.
-- !Failed to create table tbl_1 because it already exists.
-- Table tbl_1 deleted.
-- !Failed to delete tbl_1 because it does not exist.
-- Table tbl_1 created.
-- a1 int | a2 varchar(20)
-- Table tbl_1 modified.
-- a1 int | a2 varchar(20) | a3 float
-- Table tbl_2 created.
-- a3 float | a4 char(20)
-- Using Database db_2.
-- !Failed to query table tbl_1 because it does not exist.
-- Table tbl_1 created.
-- a3 float | a4 char(20)
-- All done.
```
---

### How program organizes multiple databases

To organize the databases, I have implemented functionality so that every database made by the user creates a new directory, or folder, under the name specified by the user.  Every database is separated by directory where it is its very own folder.

### How program manages multiple tables

To manage multiple tables, the database to use is needed to be specified by the user beforehand because this portrays which database (aka folder) that the table to be added should be placed in.  A table is going to be a new txt file under the given name.  Then, the attribute fields given to the table are then added to the file.

### How are these functionalities implemented (Explained at a high level)

All if not most of these functionalities are implemented useing fileIO and the os library.  Through the organizing database creation in folders and tables as files in database folders, fileIO and the os functionality allowed me to efficiently manage the file system and take advantage of these built-in library function to implement all these functions to manage the metadata.
