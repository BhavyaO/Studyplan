import sqlite3
from defs import Config as CONFIG


class DbApi():
    def __init__(self):
        self.dbName = "data/db/app.db"
        self.dbConn = None
        self.dbConnect()
        self.initTables()

    def dbConnect(self):
        self.dbConn = sqlite3.connect(self.dbName)

    def dbDisconnect(self):
        self.dbConn.close()

    def initTables(self):
        cursor = self.dbConn.cursor()
        if CONFIG.CREATE_FRESH_TABLES:
            print("Dropping Tables")
            cursor.execute('''DROP TABLE IF EXISTS COURSE''')
            cursor.execute('''DROP TABLE IF EXISTS STUDENT''')
            self.dbConn.commit()
        print("Creating Tables")
        cursor.execute('''CREATE TABLE IF NOT EXISTS COURSE (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       CODE text, NAME text, PERIOD NUMERIC, START_DATE NUMERIC, END_DATE NUMERIC,
                       WEEK_DAYS TEXT, START_TIME NUMERIC, END_TIME NUMERIC)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS STUDENT (ID NUMERIC, NAME TEXT,
                       COURSES TEXT)''')
        self.dbConn.commit()

    def insertIntoCourse(self, courseMap):
        print("Inserting Course Object", courseMap)
        cursor = self.dbConn.cursor()
        cursor.execute('''INSERT INTO COURSE (CODE, NAME, PERIOD, START_DATE, END_DATE, WEEK_DAYS,
                       START_TIME, END_TIME) VALUES (:CODE, :NAME, :PERIOD, :START_DATE, :END_DATE,
                       :WEEK_DAYS, :START_TIME, :END_TIME)''', courseMap)
        self.dbConn.commit()

    def insertIntoStudent(self, StudentMap):
        print("Inserting Student Object", StudentMap)
        cursor = self.dbConn.cursor()
        cursor.execute('''INSERT INTO STUDENT (ID, NAME, COURSES) VALUES (:ID,
                       :NAME, :COURSES)''', StudentMap)
        self.dbConn.commit()

    def isStudentIdExists(self, studentId):
        res = False
        cursor = self.dbConn.cursor()
        sqlQuery = "SELECT ID FROM STUDENT WHERE ID = '" + studentId + "'"
        print(sqlQuery)
        cursor.execute(sqlQuery)
        row = cursor.fetchone()
        if row is not None:
            res = True
        self.dbConn.commit()
        return res

    def isCourseCodeExists(self, code):
        res = False
        cursor = self.dbConn.cursor()
        sqlQuery = "SELECT CODE FROM COURSE WHERE CODE = '" + code + "'"
        print(sqlQuery)
        cursor.execute(sqlQuery)
        row = cursor.fetchone()
        if row is not None:
            res = True
        self.dbConn.commit()
        return res

    def getStudentDetails(self, studentId):
        res = dict()
        self.dbConn.row_factory = sqlite3.Row
        cursor = self.dbConn.cursor()
        query = "SELECT `ID`, `NAME` FROM STUDENT WHERE `ID` = '" + studentId + "'"
        cursor.execute(query)
        row = cursor.fetchone()
        if row is None:
            return res
        for key in row:
            res[key] = row[key]
        self.dbConn.commit()
        return res

    def getAllCourses(self):
        courseList = list()
        self.dbConn.row_factory = sqlite3.Row
        cursor = self.dbConn.cursor()
        query = "SELECT * FROM COURSE ORDER BY START_DATE"
        cursor.execute(query)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            course = list()
            course.append(row["CODE"])
            course.append(row["NAME"])
            course.append(row["PERIOD"])
            course.append(row["START_DATE"])
            course.append(row["END_DATE"])
            course.append(row["WEEK_DAYS"])
            course.append(row["START_TIME"])
            course.append(row["END_TIME"])
            courseList.append(course)
        self.dbConn.commit()
        return courseList