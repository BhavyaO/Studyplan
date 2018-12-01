import wx
import wx.adv
from defs import Const as CONST
from core.CreateStudent import CreateStudent


class CreateStudentFrame(wx.Frame, CreateStudent):

    def __init__(self, dbApi):
        CreateStudent.__init__(self, dbApi)
        self.initUI()
        self.Show(True)

    def initUI(self):
        wx.Frame.__init__(self, None, -1, "Create Student")
        boldFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)
        hdrTxt = wx.StaticText(self, -1, "Enroll Student", (10, 20))
        hdrTxt.SetFont(boldFont)

        wx.StaticLine(self, -1, (10, -1), style=wx.LI_HORIZONTAL)

        wx.StaticText(self, -1, 'Student ID', (10, 60))
        wx.StaticText(self, -1, 'Student Name', (10, 100))

        self.id = wx.TextCtrl(self, -1, '', (110, 55), (120, -1))
        self.name = wx.TextCtrl(self, -1, '', (110, 95), (120, -1))

        wx.Button(self, 1, 'Save', (10, 180))
        wx.Button(self, 2, 'Clear', (120, 180))
        wx.Button(self, 3, 'Cancel', (240, 180))

        self.statusText = wx.StaticText(self, label="", pos=(10, 280))

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

    def onSave(self, event):
        self.clearStatus()
        self.studentObj.id = self.id.GetValue()
        self.studentObj.name = self.name.GetValue()
        ret, text = self.validateStudentObj()
        if (ret != CONST.SUCCESS):
            self.updateStatus(ret, text)
            return
        ret, text = self.saveStudentObj()
        if (ret != CONST.SUCCESS):
            self.updateStatus(ret, text)
            return
        self.updateStatus(CONST.SUCCESS, "Updated Successfully")

    def onClear(self, event):
        self.clearStatus()
        self.initStudentObj()
        self.id.SetValue("")
        self.name.SetValue("")

    def onCancel(self, event):
        print("Closing ..")
        self.Close()
