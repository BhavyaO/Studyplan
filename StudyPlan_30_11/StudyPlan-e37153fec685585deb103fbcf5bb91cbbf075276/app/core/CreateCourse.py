from defs.struct import Course
from defs import Const as CONST


class CreateCourse():

    def __init__(self, dbApi):
        self.dbApi = dbApi
        self.initCourseObj()

    def initCourseObj(self):
        self.courseObj = Course()

    def saveCourseObj(self):
        courseMap = dict()
        courseMap['CODE'] = self.courseObj.code
        courseMap['NAME'] = self.courseObj.name
        courseMap['PERIOD'] = self.courseObj.period
        courseMap['START_DATE'] = str(self.courseObj.startDate)
        courseMap['END_DATE'] = str(self.courseObj.endDate)
        courseMap['WEEK_DAYS'] = ",".join(self.courseObj.weekDays)
        time = [str(x) for x in self.courseObj.startTime]
        courseMap['START_TIME'] = ":".join(time)
        time = [str(x) for x in self.courseObj.endTime]
        courseMap['END_TIME'] = ":".join(time)
        status = (CONST.SUCCESS, "")
        self.dbApi.insertIntoCourse(courseMap)
        return status

    def validateCourseObj(self):
        status = (CONST.FAIL, "Validation Failed")
        while True:
            if self.courseObj.code is None or len(self.courseObj.code) == 0:
                status = (CONST.FAIL, "Invalid Course Code")
                break
            if self.courseObj.name is None or len(self.courseObj.name) == 0:
                status = (CONST.FAIL, "Invalid Course Name")
                break
            if self.courseObj.startDate is None:
                status = (CONST.FAIL, "Invalid Course Start Date")
                break
            if self.courseObj.endDate is None:
                status = (CONST.FAIL, "Invalid Course End Date")
                break
            if self.courseObj.endDate <= self.courseObj.startDate:
                status = (CONST.FAIL, "End Date should be larger than the start Date")
                break
            if self.courseObj.weekDays is None or len(self.courseObj.weekDays) == 0:
                status = (CONST.FAIL, "Invalid WeekDays")
                break
            if self.courseObj.startTime is None or len(self.courseObj.startTime) == 0:
                status = (CONST.FAIL, "Invalid Course Start Time")
                break
            if self.courseObj.endTime is None or len(self.courseObj.endTime) == 0:
                status = (CONST.FAIL, "Invalid Course End Time")
                break
            if self.courseObj.endTime <= self.courseObj.startTime:
                status = (CONST.FAIL, "End Time should be larger than the start Time")
                break
            if self.dbApi.isCourseCodeExists(self.courseObj.code):
                status = (CONST.FAIL, "Course Code already exists")
                break
            status = (CONST.SUCCESS, "")
            break

        return status
