import wx
import wx.adv
from defs import Const as CONST
from core.EnrollCourse import EnrollCourse
from core.CreateStudent import CreateStudent



class CreateEnrollCourseFrame(wx.Frame, EnrollCourse):

    def __init__(self, dbApi):
        self.dbApi = dbApi
        self.initUI()
        self.Show(True)

    def initUI(self):
        wx.Frame.__init__(self, None, -1, "Enroll Course")
        boldFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD)
        hdrTxt = wx.StaticText(self, -1, "Enroll Course", (450, 20))
        hdrTxt.SetFont(boldFont)
        languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript', 'PHP', 'VB.NET', 'C#']
        panel = wx.Panel(self)
        self.text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)


        #box = wx.BoxSizer(wx.HORIZONTAL)

        #box = wx.BoxSizer(wx.HORIZONTAL)
        #box.Add(lst, 0, wx.EXPAND)
        #box.Add(self.text, 1, wx.EXPAND)
        #self.Bind(wx.EVT_LISTBOX, self.onListBox, lst)
        #sizer = wx.GridBagSizer(25, 25)
        wx.StaticText(self, -1, 'Student ID', (10, 60))
        wx.StaticText(self, -1, 'Student Name', (10, 100))
        wx.ListBox(self, size=(10, 140), choices=languages, style=wx.LB_EXTENDED)

        #self.selectedFieldListCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        #sizer.Add(self.selectedFieldListCtrl, pos=(10, 140), span=(4, 3))
        #wx.ListCtrl(self, "Selected Courses", width=200)
        #self.selectedFieldListCtrl.InsertColumn(0, "Selected Fields/Field Groups", width=200)
        #self.selectedFieldListCtrl.InsertColumn(1, "Instances", width=75)
        #wx.ListCtrl(self,-1,'Selected Courses'(10,140))
        #wx.ListCtrl(self,-1,'All Courses'(50,140))
        wx.Button(self, 1, 'Save', (10, 520))
        wx.Button(self, 2, 'Clear', (120, 520))
        wx.Button(self, 3, 'Cancel', (240, 520))

        self.id = wx.TextCtrl(self, -1, '', (110, 55), (120, -1))
        self.name = wx.TextCtrl(self, -1, '', (110, 95), (120, -1))


        #self.Bind(wx.EVT_BUTTON, self.onSave, id=1)
        #self.Bind(wx.EVT_BUTTON, self.onClear, id=2)
        #self.Bind(wx.EVT_BUTTON, self.onCancel, id=3)

        self.Centre()
        self.Show()
        self.Maximize(True)


