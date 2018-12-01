"""
FileName    : ModifyMessageWin.py
Description : This file contains the implementation for
              View/Edit/Delete message window


Date                Name                            Change Description

15-SEP-2015         Kalai Selvan D                  Initial Draft
"""
import wx
from gui.common import WxWrapper
from common import Constants
from gui.m_trx import M_TRXValidator as validator
from gui.m_trx import ModifyFieldWin as mfw
from gui.m_trx import ModifyFieldGroupWin as mfgw


class ModifyMessageWin():

    def __init__(self, frame, dbApi):
        self.dbApi = dbApi
        self.frame = frame
        self.saveChangesToDb = False
        self.dbMsgStruct = {}
        self.validator = validator.M_TRXUserInputValidator(self.dbApi)
        self.fieldList = self.GetFieldNameList()
        self.msgList = self.GetMessageNameList()
        self.modifyMessageFrame = WxWrapper.Frame_wx(self.frame, \
                                                     title="View/Edit/Delete message structure", size=(1200, 450))

        self.InitUI()

        self.modifyMessageFrame.Show(True)

    def InitUI(self):

        panel = wx.Panel(self.modifyMessageFrame)

        sizer = wx.GridBagSizer(5, 5)

        hdrTxt = wx.StaticText(panel, label="View/Edit/Delete Message Structure")
        sizer.Add(hdrTxt, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=15)

        selMsgNameTxt = wx.StaticText(panel, label="Select Message Name")
        sizer.Add(selMsgNameTxt, pos=(1, 0), flag=wx.LEFT, border=10)

        self.msgNameSearchTxtCtrl = wx.TextCtrl(panel)
        sizer.Add(self.msgNameSearchTxtCtrl, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)

        msgSearchButton = wx.Button(panel, label="Search", id=14)
        sizer.Add(msgSearchButton, pos=(1, 3), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.selMsgNameCombo = wx.ComboBox(panel, style=wx.CB_READONLY, \
                                           choices=self.msgList, id=1)

        sizer.Add(self.selMsgNameCombo, pos=(1, 4), span=(1, 3),
                  flag=wx.EXPAND)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 7),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)

        msgId = wx.StaticText(panel, label="Message ID")
        sizer.Add(msgId, pos=(3, 0), flag=wx.LEFT, border=10)

        self.msgIdTxtCtrl = wx.TextCtrl(panel)
        sizer.Add(self.msgIdTxtCtrl, pos=(3, 1), span=(1, 6), flag=wx.TOP | wx.EXPAND)

        msgName = wx.StaticText(panel, label="Message Name")
        sizer.Add(msgName, pos=(4, 0), flag=wx.LEFT, border=10)

        self.msgNameTxtCtrl = wx.TextCtrl(panel)
        sizer.Add(self.msgNameTxtCtrl, pos=(4, 1), span=(1, 6), flag=wx.TOP | wx.EXPAND)

        fieldNameTxt = wx.StaticText(panel, label="Selected Field/Field Group")
        sizer.Add(fieldNameTxt, pos=(5, 0), flag=wx.LEFT, border=10)

        self.selectedFieldListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        sizer.Add(self.selectedFieldListCtrl, pos=(5, 1), span=(4, 3))

        self.selectedFieldListCtrl.InsertColumn(0, "Selected Fields/Field Groups", width=200)
        self.selectedFieldListCtrl.InsertColumn(1, "Instances", width=75)

        addFieldNameButton = wx.Button(panel, label="<< Add Field", id=wx.ID_COPY, \
                                       size=(140, -1))
        sizer.Add(addFieldNameButton, pos=(6, 5), flag=wx.RIGHT, border=20)

        removeSelButton = wx.Button(panel, label=">> Remove Selection", id=1, \
                                    size=(140, -1))
        sizer.Add(removeSelButton, pos=(8, 5), flag=wx.RIGHT, border=20)

        instance = wx.StaticText(panel, label="Instances")
        sizer.Add(instance, pos=(5, 6), span=(1, 1), flag=wx.LEFT, border=10)

        self.instancesTxtCtrl = wx.TextCtrl(panel)
        sizer.Add(self.instancesTxtCtrl, pos=(6, 6), flag=wx.TOP | wx.EXPAND)

        self.fieldSearchTxtCtrl = wx.TextCtrl(panel)
        sizer.Add(self.fieldSearchTxtCtrl, pos=(5, 8), span=(1, 1), flag=wx.EXPAND)

        fieldSearchButton = wx.Button(panel, label="Search", id=15)
        sizer.Add(fieldSearchButton, pos=(5, 9), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.fieldNameListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER, \
                                             size=(250, -1))
        sizer.Add(self.fieldNameListCtrl, pos=(6, 8), span=(4, 3))

        self.fieldNameListCtrl.InsertColumn(0, "Fields/Field Groups", wx.LIST_FORMAT_RIGHT, \
                                            width=220)
        self.fillFieldNameList(self.fieldList)

        updateButton = wx.Button(panel, label="Update", id=wx.ID_SAVE)
        sizer.Add(updateButton, pos=(9, 1), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        deleteButton = wx.Button(panel, label="Delete", id=wx.ID_DELETE)
        sizer.Add(deleteButton, pos=(9, 2), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        clearButton = wx.Button(panel, label="Clear", id=wx.ID_CLEAR)
        sizer.Add(clearButton, pos=(9, 3), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        refreshButton = wx.Button(panel, label="Refresh", id=16)
        sizer.Add(refreshButton, pos=(9, 4), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        closeButton = wx.Button(panel, label="Close", id=wx.ID_CLOSE)
        sizer.Add(closeButton, pos=(9, 5), span=(1, 1),
                  flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.statusText = wx.StaticText(panel, label="")
        sizer.Add(self.statusText, pos=(10, 1), span=(1, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=10)
        panel.SetSizer(sizer)

        panel.Bind(wx.EVT_COMBOBOX, self.OnMsgSelect, id=1)
        updateButton.Bind(wx.EVT_BUTTON, self.OnUpdate, updateButton)
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete, deleteButton)
        clearButton.Bind(wx.EVT_BUTTON, self.OnClear, clearButton)
        refreshButton.Bind(wx.EVT_BUTTON, self.OnRefresh, refreshButton)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose, closeButton)
        addFieldNameButton.Bind(wx.EVT_BUTTON, self.OnAddField, addFieldNameButton)
        removeSelButton.Bind(wx.EVT_BUTTON, self.OnRemoveField, removeSelButton)
        msgSearchButton.Bind(wx.EVT_BUTTON, self.OnMsgSearch, msgSearchButton)
        fieldSearchButton.Bind(wx.EVT_BUTTON, self.OnFieldSearch, fieldSearchButton)
        self.fieldNameListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnFieldItemActivated, self.fieldNameListCtrl)
        self.selectedFieldListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSelFieldItemActivated,
                                        self.selectedFieldListCtrl)

    def OnRefresh(self, event):
        self.RefreshWindow()

    def OnSelFieldItemActivated(self, event):
        currentItem = event.m_itemIndex

        fieldName = self.selectedFieldListCtrl.GetItemText(currentItem)
        self.openFieldWin(fieldName)

    def OnFieldItemActivated(self, event):
        currentItem = event.m_itemIndex

        fieldName = self.fieldNameListCtrl.GetItemText(currentItem)
        self.openFieldWin(fieldName)

    def openFieldWin(self, fieldName):
        fieldId = fieldName[fieldName.find("<") + 1:fieldName.find(">")]
        print
        "OnFieldItemActivated: ", fieldName, "fieldId:", fieldId[0:2]
        if fieldId[0:2] == "FG":
            self.modifyFieldGrpFrame = mfgw.ModifyFieldGroupWin(self.frame, self.dbApi)
            self.modifyFieldGrpFrame.fillWithSelectedField(fieldName)

        else:
            self.modifyFieldFrame = mfw.ModifyField(self.frame, self.dbApi)
            self.modifyFieldFrame.fillWithSelectedField(fieldName)

    def OnFieldSearch(self, event):
        searchTxt = self.fieldSearchTxtCtrl.GetValue()
        print
        "Search Text:", searchTxt
        filteredList = filter(lambda k: searchTxt in k, self.fieldList)
        self.fillFieldNameList(filteredList)

    def OnMsgSearch(self, event):
        searchTxt = self.msgNameSearchTxtCtrl.GetValue()
        print
        "Search Text:", searchTxt
        filteredMsgList = filter(lambda k: searchTxt in k, self.msgList)
        self.selMsgNameCombo.SetItems(filteredMsgList)

    def OnMsgSelect(self, event):
        self.dbMsgStruct = {}
        self.statusText.SetLabel("")
        item = event.GetSelection()
        print
        "Selected Item is ", item
        msgTxt = self.selMsgNameCombo.GetValue()
        msgId = msgTxt[msgTxt.find("<") + 1:msgTxt.find(">")]
        print
        "Msg Id is ", msgId
        result = self.dbApi.GetMsgStruct(msgId)

        for key in result:
            print
            "[", key, "]:[", result[key], "]"
            self.dbMsgStruct[key] = result[key]

        self.fillWithSelectedField()

    def fillWithSelectedField(self):

        fieldsArr = []
        self.msgIdTxtCtrl.SetValue(str(self.dbMsgStruct['MESSAGE_ID']))
        self.msgNameTxtCtrl.SetValue(str(self.dbMsgStruct \
                                             ['MESSAGE_NAME']))

        self.selectedFieldListCtrl.DeleteAllItems()

        if self.dbMsgStruct['FIELDS']:
            fieldsArr = self.dbMsgStruct['FIELDS'].split(",")

        for field in fieldsArr:
            fieldInstanceArr = field.split("-")
            field = fieldInstanceArr[0]
            fieldInstance = fieldInstanceArr[1]

            if field[:2] == "FG":
                res = self.dbApi.GetFieldGroupStruct(field)
                fieldDisplayTxt = "<" + str(res['FIELD_GROUP_ID']) + ">" + res['FIELD_GROUP_NAME']
            else:
                res = self.dbApi.GetFieldStruct(field)
                fieldDisplayTxt = "<" + str(res['FIELD_ID']) + ">" + res['FIELD_NAME']

            self.selectedFieldListCtrl.Append([fieldDisplayTxt, fieldInstance])

    def GetFieldNameList(self):
        fieldList = []
        dbFieldIdNameArr = self.dbApi.GetAllFieldStruct()
        fieldIdNameLen = len(dbFieldIdNameArr)
        for index in range(fieldIdNameLen):
            displayTxt = "<" + str(dbFieldIdNameArr[index][0]) + ">" + \
                         dbFieldIdNameArr[index][1]
            fieldList.append(displayTxt)

        dbFieldGrpIdNameArr = self.dbApi.GetAllFieldGroupStruct()
        fieldGrpIdNameLen = len(dbFieldGrpIdNameArr)
        for index in range(fieldGrpIdNameLen):
            displayTxt = "<" + str(dbFieldGrpIdNameArr[index][0]) + ">" + \
                         dbFieldGrpIdNameArr[index][1]
            fieldList.append(displayTxt)

        return fieldList

    def GetMessageNameList(self):
        msgList = []
        dbMsgIdNameArr = self.dbApi.GetAllMessageStruct()
        msgIdNameArrLen = len(dbMsgIdNameArr)
        for index in range(msgIdNameArrLen):
            displayTxt = "<" + str(dbMsgIdNameArr[index][0]) + ">" + \
                         dbMsgIdNameArr[index][1]
            msgList.append(displayTxt)

        return msgList

    def OnUpdate(self, event):
        res = {}
        res['STATUS'] = Constants.FAIL
        res['STATUS_TXT'] = "Error in user input"

        msgStruct = {}
        dbMsgId = ""
        dbMsgName = ""
        msgStruct['MESSAGE_ID'] = self.msgIdTxtCtrl.GetValue()
        msgStruct['MESSAGE_NAME'] = self.msgNameTxtCtrl.GetValue()
        msgStruct['FIELDS'] = self.GetSelectedFieldsInCsv()

        if self.dbMsgStruct.has_key('MESSAGE_ID'):
            dbMsgId = self.dbMsgStruct['MESSAGE_ID']

        if self.dbMsgStruct.has_key('MESSAGE_NAME'):
            dbMsgName = self.dbMsgStruct['MESSAGE_NAME']

        for key in msgStruct:
            print
            key, " : ", msgStruct[key]

        while (1):

            if not self.dbMsgStruct.has_key('MESSAGE_ID'):
                res['STATUS'] = Constants.FAIL
                res['STATUS_TXT'] = "Select the message Name to update"
                break

            res = self.validator.validateMessageIdForUpdate \
                (dbMsgId, msgStruct['MESSAGE_ID'])
            if (res['STATUS'] == Constants.FAIL):
                break

            res = self.validator.validateMessageNameForUpdate \
                (dbMsgName, msgStruct['MESSAGE_NAME'])
            if (res['STATUS'] == Constants.FAIL):
                break

            """
            res = self.validator.validateFields\
                    (msgStruct['FIELDS'])
            if (res['STATUS'] == Constants.FAIL):
                break
            """

            if self.IsValueChanged(msgStruct) == False:
                res['STATUS'] = Constants.FAIL
                res['STATUS_TXT'] = "No change to update"

                break

            msgStruct['OLD_MESSAGE_ID'] = dbMsgId
            if self.dbApi.UpdateMessageStructure(msgStruct) == False:
                msg = "Error in updating " + msgStruct['MESSAGE_NAME']
                res["STATUS_TXT"] = msg
                break

            res['STATUS'] = Constants.SUCCESS
            msg = msgStruct['MESSAGE_NAME'] + " is updated in db successfully"
            res["STATUS_TXT"] = msg

            break

        print
        "STATUS : ", res["STATUS_TXT"]
        self.fillStatus(res["STATUS"], res["STATUS_TXT"])

        if res['STATUS'] == Constants.SUCCESS:
            self.saveChangesToDb = True
            self.RefreshWindow()

    def RefreshWindow(self):
        self.ClearDisplayedFields()
        self.UpdateMessageListAfterModify()
        self.dbApi.messageStruct = {}
        self.dbApi.LoadMessageStructFromDb()

    def UpdateMessageListAfterModify(self):
        self.msgList = self.GetMessageNameList()
        self.selMsgNameCombo.SetItems(self.msgList)

    def ClearDisplayedFields(self):

        self.dbMsgStruct = {}
        self.msgIdTxtCtrl.SetValue("")
        self.msgNameTxtCtrl.SetValue("")
        self.instancesTxtCtrl.SetValue("")
        self.selMsgNameCombo.SetItems(self.msgList)
        self.UnselectListCtrlItem(self.fieldNameListCtrl)
        self.selectedFieldListCtrl.DeleteAllItems()
        self.msgNameSearchTxtCtrl.SetValue("")
        self.fieldSearchTxtCtrl.SetValue("")
        self.fillFieldNameList(self.fieldList)

    def GetSelectedFieldsInCsv(self):

        fields = ""
        count = self.selectedFieldListCtrl.GetItemCount()
        firstItem = True
        for row in range(count):
            fieldItem = self.selectedFieldListCtrl.GetItem(itemId=row, col=0)
            instanceItem = self.selectedFieldListCtrl.GetItem(itemId=row, col=1)
            if firstItem == True:
                firstItem = False
            else:
                fields = fields + ","
            txt = fieldItem.GetText()
            fieldId = txt[txt.find("<") + 1:txt.find(">")]
            instance = instanceItem.GetText()
            fields = fields + str(fieldId) + "-" + instance
            print
            fields

        return fields

    def OnClear(self, event):
        print
        "Clear called"
        self.ClearDisplayedFields()
        self.statusText.SetLabel("")

    def OnClose(self, event):
        print
        "Close called"
        self.modifyMessageFrame.Close()

    def fillStatus(self, status, msg):
        self.statusText.SetLabel(msg)
        if status == Constants.FAIL:
            self.statusText.SetForegroundColour((255, 0, 0))
        else:
            print
            "Setting Greeeeen"
            self.statusText.SetForegroundColour((0, 153, 0))

    def OnAddField(self, event):
        selFieldArr = []
        res = {}
        res['STATUS'] = Constants.FAIL
        res['STATUS_TXT'] = "Invalid addition of fields"

        instances = self.instancesTxtCtrl.GetValue()
        selFieldArr = self.GetSelectedListCtrlItem(self.fieldNameListCtrl)

        while (1):
            if (len(selFieldArr) <= 0):
                res['STATUS_TXT'] = "Select the Fields to add"
                break

            res = self.validator.validateFieldInstances \
                (instances)
            if (res['STATUS'] == Constants.FAIL):
                break

            res['STATUS'] = Constants.SUCCESS
            res['STATUS_TXT'] = ""

            break
        if (res['STATUS'] == Constants.SUCCESS):
            for field in selFieldArr:
                row = []
                row.append(field)
                row.append(instances)
                self.selectedFieldListCtrl.Append(row)

        self.fillStatus(res["STATUS"], res["STATUS_TXT"])

    def IsFieldInstanceListSelected(self):

        ret = False
        count = self.selectedFieldListCtrl.GetItemCount()

        for row in range(count):
            if (self.selectedFieldListCtrl.IsSelected(row)):
                ret = True
                break

        return ret

    def GetUnSelectedFieldInstanceList(self):
        unSelFieldArr = []
        count = self.selectedFieldListCtrl.GetItemCount()

        for row in range(count):
            if (self.selectedFieldListCtrl.IsSelected(row)):
                pass
            else:
                fieldItem = self.selectedFieldListCtrl.GetItem \
                    (row, col=0).GetText()
                instanceItem = self.selectedFieldListCtrl.GetItem \
                    (row, col=1).GetText()
                itemDict = {}
                itemDict['FIELD_ITEM'] = fieldItem
                itemDict['INSTANCE_ITEM'] = instanceItem
                unSelFieldArr.append(itemDict)
        return unSelFieldArr

    def OnRemoveField(self, event):

        res = {}
        unSelFieldArr = []
        res['STATUS'] = Constants.FAIL
        res['STATUS_TXT'] = "Invalid removal of fields"

        while (1):
            if (self.IsFieldInstanceListSelected() == False):
                res['STATUS_TXT'] = "Select the Field to remove"
                break

            res['STATUS'] = Constants.SUCCESS
            res['STATUS_TXT'] = ""

            break

        if (res['STATUS'] == Constants.SUCCESS):
            unSelFieldArr = self.GetUnSelectedFieldInstanceList()
            print
            "clearing All item"
            self.selectedFieldListCtrl.DeleteAllItems()

            for field in unSelFieldArr:
                self.selectedFieldListCtrl.Append([field['FIELD_ITEM'], \
                                                   field['INSTANCE_ITEM']])

        print
        "STATUS :", res['STATUS_TXT']
        self.fillStatus(res["STATUS"], res["STATUS_TXT"])

    def IsValueChanged(self, fieldGrpStruct):

        ret = False

        for key in fieldGrpStruct:
            if (str(fieldGrpStruct[key]) == str(self.dbMsgStruct[key])):
                print
                "Both are same"
            else:
                ret = True
                print
                "Both are not same"
                break

        return ret

    def OnDelete(self, event):

        res = {}
        res['STATUS'] = Constants.FAIL
        res['STATUS_TXT'] = "Error in deleting"
        while (1):

            if (not self.dbMsgStruct.has_key('MESSAGE_ID')) or (not self.dbMsgStruct['MESSAGE_ID']):
                res['STATUS'] = Constants.FAIL
                res['STATUS_TXT'] = "Select a message name to Delete"
                break

            if (self.dbApi.DeleteMessageStruct(self.dbMsgStruct['MESSAGE_ID']) != True):
                res['STATUS'] = Constants.FAIL
                res['STATUS_TXT'] = "Error in deleteing message"
                break

            res['STATUS'] = Constants.SUCCESS
            res['STATUS_TXT'] = "Successfully deleted the message [" + self.dbMsgStruct['MESSAGE_NAME'] + "]"
            break

        self.fillStatus(res["STATUS"], res["STATUS_TXT"])

        if res['STATUS'] == Constants.SUCCESS:
            self.saveChangesToDb = True
            self.RefreshWindow()

    def fillFieldNameList(self, fieldListArr):

        self.fieldNameListCtrl.DeleteAllItems()

        for field in fieldListArr:
            self.fieldNameListCtrl.Append(field.split())

    def GetSelectedListCtrlItem(self, listCtrl):

        selection = []

        count = listCtrl.GetItemCount()
        for index in range(count):
            if (listCtrl.IsSelected(index)):
                listCtrl.Select(index, 0)

                item = listCtrl.GetItem(index).GetText()
                selection.append(item)
            else:
                pass

        return selection

    def UnselectListCtrlItem(self, listCtrl):
        count = listCtrl.GetItemCount()
        for index in range(count):
            if (listCtrl.IsSelected(index)):
                listCtrl.Select(index, 0)
