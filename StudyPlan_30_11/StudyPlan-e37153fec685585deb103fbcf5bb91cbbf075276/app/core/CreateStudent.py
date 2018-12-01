from defs.struct import Student
from defs import Const as CONST


class CreateStudent():

    def __init__(self, dbApi):
        self.dbApi = dbApi
        self.initStudentObj()

    def initStudentObj(self):
        self.studentObj = Student()

    def saveStudentObj(self):
        studentMap = dict()
        studentMap['ID'] = self.studentObj.id
        studentMap['NAME'] = self.studentObj.name
        # Always creating student with empty course
        studentMap['COURSES'] = ""
        status = (CONST.SUCCESS, "")
        self.dbApi.insertIntoStudent(studentMap)
        return status

    def validateStudentObj(self):
        status = (CONST.FAIL, "Validation Failed")
        while True:
            if self.studentObj.id is None or len(self.studentObj.id) == 0:
                status = (CONST.FAIL, "Invalid Stduent ID")
                break
            if not self.studentObj.id.isnumeric():
                status = (CONST.FAIL, "Student ID should be numeric")
                break
            if self.studentObj.name is None or len(self.studentObj.name) == 0:
                status = (CONST.FAIL, "Invalid Student Name")
                break
            if self.dbApi.isStudentIdExists(self.studentObj.id):
                status = (CONST.FAIL, "Student ID already exists")
                break
            status = (CONST.SUCCESS, "")
            break

        return status
