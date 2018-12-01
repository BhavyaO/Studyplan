from defs.struct import Student


class EnrollCourse():

    def __init__(self, dbApi, studentId):
        self.dbApi = dbApi
        self.fetchStudentObj(studentId)

    def initStudentObj(self):
        self.studentObj = Student()

    def fetchStudentObj(self, studentId):
        self.initStudentObj()
        studentMap = self.dbApi.getStudentDetails(studentId)
        if len(studentMap) == 0:
            print("ERR: Student Data not found in DB")

        self.studentObj.id = studentMap['ID']
        self.studentObj.name = studentMap['NAME']
        self.studentObj.courses = studentMap['COURSES'].split(",")

    def getEnrolledCourseList(self):
        return self.studentObj.courses

    def getAllCourseList(self):
        return self.dbApi.getAllCourses()