import wx
import wx.adv
from defs import Const as CONST
from core.CreateCourse import CreateCourse


class CreateCourseFrame(wx.Frame, CreateCourse):

    def __init__(self, dbApi):
        CreateCourse.__init__(self, dbApi)
        self.initUI()
        self.Show(True)

    def initUI(self):
        wx.Frame.__init__(self, None, -1, "Create Course")
        self.weekDays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        self.periods = ["1", "2", "3", "4", "5"]

        boldFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)
        hdrTxt = wx.StaticText(self, -1, "Create Course", (10, 20))
        hdrTxt.SetFont(boldFont)

        wx.StaticLine(self, -1, (10, -1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self, -1, 'Course Code', (10, 60))
        wx.StaticText(self, -1, 'Course Name', (10, 100))
        wx.StaticText(self, -1, 'Period', (10, 140))
        wx.StaticText(self, -1, 'From Date', (10, 240))
        wx.StaticText(self, -1, 'To Date', (10, 280))
        wx.StaticText(self, -1, 'Weekdays', (10, 340))
        wx.StaticText(self, -1, 'From Time', (10, 450))
        wx.StaticText(self, -1, 'To Time', (10, 490))

        self.code = wx.TextCtrl(self, -1, '', (110, 55), (120, -1))
        self.name = wx.TextCtrl(self, -1, '', (110, 95), (120, -1))
        self.period = wx.ListBox(self, -1, (110, 135), (120, -1), self.periods, wx.LB_SINGLE)
        startDateCtrl = wx.adv.DatePickerCtrl(self, pos=(110,235), size=(120, -1), style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        endDateCtrl = wx.adv.DatePickerCtrl(self, pos=(110,275), size=(120, -1), style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY | wx.adv.DP_ALLOWNONE)
        self.weekDayCtrl = wx.ListBox(self, -1, (110, 315), (120, -1), self.weekDays, wx.LB_EXTENDED)
        self.startTimeCtrl = wx.adv.TimePickerCtrl(self, pos=(110, 445), size=(120, -1), style = wx.adv.TP_DEFAULT)
        self.endTimeCtrl = wx.adv.TimePickerCtrl(self, pos=(110, 485), size=(120, -1), style = wx.adv.TP_DEFAULT)

        wx.Button(self, 1, 'Save', (10, 520))
        wx.Button(self, 2, 'Clear', (120, 520))
        wx.Button(self, 3, 'Cancel', (240, 520))

        self.statusText = wx.StaticText(self, label="", pos=(10, 580))

        self.Bind(wx.adv.EVT_DATE_CHANGED, self.onStartDateChanged, startDateCtrl)
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.onEndDateChanged, endDateCtrl)
        self.Bind(wx.EVT_LISTBOX, self.onWeekdayChanged, self.weekDayCtrl)
        self.Bind(wx.adv.EVT_TIME_CHANGED, self.onStartTimeChanged, self.startTimeCtrl)
        self.Bind(wx.adv.EVT_TIME_CHANGED, self.onEndTimeChanged, self.endTimeCtrl)
        self.Bind(wx.EVT_BUTTON, self.onSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.onClear, id=2)
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=3)

        self.Centre()
        self.Show()
        self.Maximize(True)

    def clearStatus(self):
        self.updateStatus(CONST.SUCCESS, "")

    def updateStatus(self, status, text):
        self.statusText.SetLabel(text)
        if status == CONST.FAIL:
            self.statusText.SetForegroundColour((255, 0, 0))
        else:
            self.statusText.SetForegroundColour((0, 153, 0))

    def onStartDateChanged(self, event):
        self.courseObj.startDate = event.GetDate()
        print("Start Date is ", self.courseObj.startDate)

    def onEndDateChanged(self, event):
        self.courseObj.endDate = event.GetDate()
        print("End Date is ", self.courseObj.endDate)

    def onWeekdayChanged(self, event):
        weekDays = (self.weekDayCtrl.GetSelections())[:]
        self.courseObj.weekDays.clear()
        for index in weekDays:
            self.courseObj.weekDays.append(self.weekDays[index])
        print("Selected Day", self.courseObj.weekDays)

    def onStartTimeChanged(self, event):
        self.courseObj.startTime = self.startTimeCtrl.GetTime()
        print("Start Time is ", self.courseObj.startTime)

    def onEndTimeChanged(self, event):
        self.courseObj.endTime = self.endTimeCtrl.GetTime()
        print("Start Time is ", self.endTimeCtrl.GetTime())

    def onSave(self, event):
        self.clearStatus()
        self.courseObj.code = self.code.GetValue()
        self.courseObj.name = self.name.GetValue()
        ret, text = self.validateCourseObj()
        if (ret != CONST.SUCCESS):
            self.updateStatus(ret, text)
            return
        ret, text = self.saveCourseObj()
        if (ret != CONST.SUCCESS):
            self.updateStatus(ret, text)
            return
        self.updateStatus(CONST.SUCCESS, "Updated Successfully")

    def onClear(self, event):
        self.clearStatus()
        self.initCourseObj()
        self.code.SetValue("")
        self.name.SetValue("")

    def onCancel(self, event):
        print("Closing ..")
        self.Close()