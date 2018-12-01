import wx
from defs import Config as CONFIG
from gui.course.CreateCourseFrame import CreateCourseFrame
from gui.student.CreateStudentFrame import CreateStudentFrame
from gui.enrollcourse.CreateEnrollCourseFrame import CreateEnrollCourseFrame


class CreateLauncherFrame(wx.Frame):

    def __init__(self, dbApi):
        self.dbApi = dbApi
        self.initUI()
        self.Show(True)

    def initUI(self):
        wx.Frame.__init__(self, None, -1, "Study Planner - Version " + CONFIG.VERSION)
        boldFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)
        hdrTxt = wx.StaticText(self, -1, "Study Planner", (450, 20))
        hdrTxt.SetFont(boldFont)

        wx.Button(self, 1, 'Manage Course', (450, 60))
        wx.Button(self, 2, 'Manage Student', (450, 100))
        wx.Button(self, 3, 'Enroll Course', (450, 140))

        self.Bind(wx.EVT_BUTTON, self.onCourseManage, id=1)
        self.Bind(wx.EVT_BUTTON, self.onStudentManage, id=2)
        self.Bind(wx.EVT_BUTTON, self.onCourseEnroll, id=3)

        self.Centre()
        self.Show()
        self.Maximize(True)

    def onCourseManage(self, event):
        CreateCourseFrame(self.dbApi)

    def onStudentManage(self, event):
        CreateStudentFrame(self.dbApi)

    def onCourseEnroll(self, event):
        CreateEnrollCourseFrame(self.dbApi)
