import wx
from db_api.DbApi import DbApi
from gui.CreateLauncherFrame import CreateLauncherFrame


class MyApp(wx.App):

    def OnInit(self):
        # Initialising the DB
        dbApi = DbApi()
        CreateLauncherFrame(dbApi)
        return True


app = MyApp(0)
app.MainLoop()
