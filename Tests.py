from DBMS import DBMS
import unittest
import os

unittest.TestLoader.sortTestMethodsUsing = None

class TestDbmsSimulator(unittest.TestCase):

    def setUp(self) -> None:
        self.dbms = DBMS()
        self.CWD = os.getcwd()
        self.dbms.createDatabase('TestDB', self.CWD)
        self.dbToUse = 'SetupDB'


    # unit tests
    def testCreateDatabase_Successful(self):
        self.assertTrue(self.dbms.createDatabase('SetupDB', self.CWD))

    def testCreateDatabase_Unsuccessful(self):
        self.assertFalse(self.dbms.createDatabase('SetupDB', self.CWD))

    def testDropDatabase_Successful(self):
        self.dbms.createDatabase('db1', self.CWD)
        self.assertTrue(self.dbms.dropDatabase('db1', self.CWD))

    def testDropDatabase_Unsuccessful(self):
        # cannot drop db because it does not exist
        self.assertFalse(self.dbms.dropDatabase('db1', self.CWD))

    def testUseDatabase_DbDoesNotExist(self):
        self.assertEqual('', self.dbms.useDatabase('RandomDB', self.CWD))

    def testUseDatabase_DbExists(self):
        self.assertEqual('TestDB', self.dbms.useDatabase('TestDB', self.CWD))
        self.assertNotEqual('', self.dbms.useDatabase('TestDB', self.CWD))

    def testCreateTable_Successful(self):
        self.assertTrue(self.dbms.createTable(['CREATE', 'TABLE', 'Fruit', '(id', 'int,', 'name', 'string);'], self.CWD, self.dbToUse))

    def testCreateTable_TableAlreadyExists(self):
        self.assertFalse(self.dbms.createTable(['CREATE', 'TABLE', 'Fruit', '(id', 'int,', 'name', 'string);'], self.CWD, self.dbToUse))

    def testCreateTable_IncorrectArguments(self):
        self.assertEqual("Invalid Input", self.dbms.createTable(['CREATE', 'TABLE', 'Fruit'], self.CWD, self.dbToUse))

    def testDropTable_Successful(self):
        self.assertEqual("Success.", self.dbms.dropTable('Fruit', os.path.join(self.CWD, 'SetupDB')))

    def testDropTable_Unsuccessful(self):
        self.assertEqual("Unsuccessful - Table does not exist.", self.dbms.dropTable('Fruit', os.path.join(self.CWD, 'SetupDB')))

    def testSelectTable_TableDoesNotExist(self):
        self.assertEqual('Select failed because table does not exist.', self.dbms.selectTable('TableTest', self.CWD, False))

    def testSelectTable_Successful(self):
        self.dbms.createTable(['CREATE', 'TABLE', 'TableTest', '(id', 'int,', 'name', 'string);'], self.CWD, self.dbToUse)
        self.assertIsNotNone(self.dbms.selectTable('TableTest', os.path.join(self.CWD, self.dbToUse), False))

    def testAlterTable_TableDoesNotExist(self):
        input = ['ALTER', 'TABLE', 'tbl_1', 'ADD', 'a3', 'float;']
        self.assertEqual("Table desired to alter does not exist.", self.dbms.alterTable(input, os.path.join(self.CWD, self.dbToUse)))

    def testAlterTable_Successful(self):
        self.dbms.createTable(['CREATE', 'TABLE', 'TableTest2', '(id', 'int,', 'name', 'string);'], self.CWD, 'TestDB')

        input = ['ALTER', 'TABLE', 'TableTest2', 'ADD', 'price', 'float;']
        self.assertEqual("Table modified successfully.", self.dbms.alterTable(input, os.path.join(self.CWD, 'TestDB')))

    def testInsertData_TableToInsertIntoDoesNotExist(self):
        input = ['insert', 'into', 'WrongTable', 'values(1,', "'testName',", '14.99);']
        self.assertFalse(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))

    def testInsertData_Successful(self):
        input = ['insert', 'into', 'TableTest2', 'values(1,', "'testName',", '14.99);']
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))

    def testProcessFileData(self):
        data = ['id int|name string|price float\n', '1|testName|14.99\n']
        self.assertIsNotNone(self.dbms.processFileData(data, 'name', 'name', 'testName', 'changedName'))

    def testUpdateData_InvalidInput(self):
        # sending empty list to mock invalid input given
        self.assertEqual("Invalid input", self.dbms.updateData('Table2', [], os.path.join(self.CWD, "TestDB"), False))

    def testUpdateData_Success(self):
        # fix modify info list param
        modifyInfoLst = ['set', 'name', '=', 'changedName', 'where', 'name', '=', "'testName';"]
        self.assertEqual("Success!", self.dbms.updateData('TableTest2', modifyInfoLst, os.path.join(self.CWD, "TestDB"), True))

    def testUpdateData_TableLocked(self):
        # create locked table to have Branch Coverage
        os.mkdir(os.path.join(self.CWD, "TestDB", "TableName"))
        os.mkdir(os.path.join(self.CWD, "TestDB", "TableName_lock"))

        input = ['set', 'name', '=', 'changedName', 'where', 'name', '=', "'testName';"]
        self.assertEqual("Table is locked so cannot update.", self.dbms.updateData('TableName', input, os.path.join(self.CWD, "TestDB"), False))

    def testSplitFileData(self):
        # helper function that is being tested
        fileInputMock = ['id int|name string|price float\n', '1|apple|2.99\n']
        self.assertIsNotNone(self.dbms.splitFileData(fileInputMock))
        self.assertListEqual([['id int', 'name string', 'price float'], ['1', 'apple', '2.99']], self.dbms.splitFileData(fileInputMock))

    def testRemoveData_TableDoesNotExist(self):
        self.assertFalse(self.dbms.removeData('TableDNE', ['where', 'name', '=', "'changedName';"], os.path.join(self.CWD, "TestDB")))

    def testRemoveData_Successful(self):
        self.assertTrue(self.dbms.removeData('TableTest2', ['where', 'name', '=', "'changedName';"], os.path.join(self.CWD, "TestDB")))

    def testSelectTableWithAttributes_TableDoesNotExist(self):
        input = ['select', 'name,', 'price', 'from', 'Test2', 'where', 'id', '=', '1;']

        self.assertFalse(self.dbms.selectTableWithAttributes(input, ['where', 'id', '=', '1;'], os.path.join(self.CWD, "TestDB")))

    def testSelectTableWithAttributes_Successful(self):
        input = ['select', 'name,', 'price', 'from', 'TableTest2', 'where', 'id', '=', '1;']
        whereList = ['where', 'id', '=', '1;']

        self.assertTrue(self.dbms.selectTableWithAttributes(input, whereList, os.path.join(self.CWD, "TestDB")))

    def testFromParser(self):
        self.assertIsNotNone(self.dbms.fromParser(['select', '*', 'from', 'TableTest2', 'where', 'id', '=', '1;']))
        self.assertListEqual(['from', 'TableTest2'], self.dbms.fromParser(['select', '*', 'from', 'TableTest2', 'where', 'id', '=', '1;']))

    def testTransactionManaging(self):
        self.assertTrue(self.dbms.transactionManaging(os.path.join(self.CWD, "TestDB"), False))
        self.assertTrue(self.dbms.transactionManaging(os.path.join(self.CWD, "TestDB"), True))

    def testCommit_TransactionAborted(self):
        self.assertEqual("Transaction aborted.", self.dbms.commit(self.CWD, False))

    def testCommit_TransactionCommitted(self):
        # self.assertTrue(self.dbms.commit(self.CWD, False))
        self.assertTrue(self.dbms.commit(self.CWD, True))

    def testAverage_TableDoesNotExist(self):
        self.assertEqual("Cannot find average because table does not exist.", self.dbms.average(os.path.join(self.CWD, "TestDB"), 'ThisTableDoesNotExist', 'price'))

    def testAverage_Successful(self):
        # these two records in table w/ avg taken
        input = ['insert', 'into', 'TableTest2', 'values(2,', "'testName',", '49.99);']
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))
        input = ['insert', 'into', 'TableTest2', 'values(3,', "'AnotherName',", '24.99);']
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))

        self.assertEqual(37.49, self.dbms.average(os.path.join(self.CWD, "TestDB"), 'TableTest2', 'price'))

    def testCountTuples_TableDoesNotExist(self):
        self.assertEqual("Table does not exist so cannot count tuples.", self.dbms.countTuples(os.path.join(self.CWD, "SetupDB"), 'TableDNE', 'COUNT(*)'))

    def testCountTuples_Successful(self):
        # inserting more rows to test aggregate functions better
        input = ['insert', 'into', 'TableTest2', 'values(2,', "'testName',", '99.99);']
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))
        input = ['insert', 'into', 'TableTest2', 'values(3,', "'AnotherName',", '4.99);']
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))

        # only one row of data aka 1 tuple so should return 1
        self.assertEqual(4, self.dbms.countTuples(os.path.join(self.CWD, "TestDB"), 'TableTest2', '*'))

    def testMax_TableDoesNotExist(self):
        self.assertEqual("Table does not exist so cannot find MAX.", self.dbms.max(os.path.join(self.CWD, "TestDB"), "TableDNE", 'price'))

    def testMax_Successful(self):
        self.assertEqual(99.99, self.dbms.max(os.path.join(self.CWD, "TestDB"), "TableTest2", 'price'))

    def testProcessUncommittedHandler_LockFileDoesExist(self):
        open("ProcessTable_lock", "x").close()
    
        self.assertTrue(self.dbms.processUncommittedHandler(self.CWD))
        # os.remove(os.path.join(self.CWD, "ProcessTable_lock"))

    # def testProcessUncommittedHandler_LockFileDoesNotExist(self):
    #     self.assertFalse(self.dbms.processUncommittedHandler(os.path.join(self.CWD, "TestDB")))


    def testQueryAndJoinTables_TablesDoNotExist(self):
        self.assertFalse(self.dbms.queryAndJoinTables(['select', '*','from', 'TableDNE', 'T', 'inner', 'join', 'Products', 'P'], ['on', 'T.id', '=', 'P.id'], os.path.join(self.CWD, "TestDB")))

    def testQueryAndJoinTables_SuccessfullyExecuted(self):
        # create another table to join onto
        self.dbms.createTable(['CREATE', 'TABLE', 'Fruit', '(id', 'int,', 'name', 'string);'], self.CWD, "TestDB")
        input = ['insert', 'into', 'Fruit', 'values(1,', "'apple');"]
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))
        input = ['insert', 'into', 'Fruit', 'values(2,', "'orange');"]
        self.assertTrue(self.dbms.insertData(input, os.path.join(self.CWD, 'TestDB')))

        input = ['select', '*','from', 'TableTest2', 'T', 'inner', 'join', 'Fruit', 'F']
        onStmt = ['on', 'T.id', '=', 'F.id;']
        self.assertTrue(self.dbms.queryAndJoinTables(input, onStmt, os.path.join(self.CWD, "TestDB")))

    def testLeftOuterJoin_TablesDoNotExist(self):
        input = ['select', '*', 'from', 'TableTest2', 'T', 'left', 'outer', 'join', 'Products', 'P']
        onStmt = ['on', 'T.id', '=', 'P.id;']

        self.assertFalse(self.dbms.leftOuterJoin(input, onStmt, os.path.join(self.CWD, "TestDB")))

    def testLeftOuterJoin_SuccessfullyExecuted(self):

        # create another table for left outer joining
        self.dbms.createTable(['CREATE', 'TABLE', 'Employees', '(id', 'int,', 'name', 'string);'], self.CWD, "TestDB")
        input1= ['insert', 'into', 'Employees', 'values(1,', "'Jordan');"]
        self.assertTrue(self.dbms.insertData(input1, os.path.join(self.CWD, 'TestDB')))
        input2 = ['insert', 'into', 'Employees', 'values(2,', "'Sidney');"]
        self.assertTrue(self.dbms.insertData(input2, os.path.join(self.CWD, 'TestDB')))

        input3 = ['select', '*', 'from', 'TableTest2', 'T', 'left', 'outer', 'join', 'Employees', 'E']
        onStmt = ['on', 'T.id', '=', 'E.id;']

        self.assertEqual(True, self.dbms.leftOuterJoin(input3, onStmt, os.path.join(self.CWD, "TestDB")))


    # integrations tests
    def testDbAndTblCreationThroughMainControllerIntegration(self):
        pass

    def testDbAndTblRemovalThroughMain(self):
        pass

    def testInsertionAndAlteringDataThroughMain(self):
        pass

    def testSelectsThroughMain(self):
        pass

    def testAggregateFunctionsThroughMain(self):
        pass


# Note - run 'python -m coverage run -m unittest Tests.py' and then 'python -m coverage report' to get code coverage of tests