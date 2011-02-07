# coding=utf-8
#Boa:Frame:Frame1

import wx, os, sys, re, ConfigParser, psutil
import  wx.lib.mixins.listctrl  as  listmix
import _winreg as wreg
import cPickle as pickle
import win32api,win32process,win32con

from winpaths import get_appdata

from wx.lib.anchors import LayoutAnchors
from wx.lib.embeddedimage import PyEmbeddedImage
from sorteddict import SortedDict

HBB_VERSION = '1.0.0.3 - "infiltrating the honket"'

try:
    from agw import supertooltip as STT
    bitmapDir = "bitmaps/"
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.supertooltip as STT
    bitmapDir = "agw/bitmaps/"

#----------------------------------------------------------------------
SmallUpArrow = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAADxJ"
    "REFUOI1jZGRiZqAEMFGke2gY8P/f3/9kGwDTjM8QnAaga8JlCG3CAJdt2MQxDCAUaOjyjKMp"
    "cRAYAABS2CPsss3BWQAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
SmallDnArrow = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEhJ"
    "REFUOI1jZGRiZqAEMFGke9QABgYGBgYWdIH///7+J6SJkYmZEacLkCUJacZqAD5DsInTLhDR"
    "bcPlKrwugGnCFy6Mo3mBAQChDgRlP4RC7wAAAABJRU5ErkJggg==")

handbrakepineapple2 = PyEmbeddedImage(
    "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"
    "6bnO+7PwP51DL/C3a5HcAAAAAElFTkSuQmCC")
gethandbrakepineapple2Data = handbrakepineapple2.GetData
gethandbrakepineapple2Image = handbrakepineapple2.GetImage
gethandbrakepineapple2Bitmap = handbrakepineapple2.GetBitmap
gethandbrakepineapple2Icon = handbrakepineapple2.GetIcon

presetsRE = re.compile(ur"\W*<Category>(?P<cat>.*)</Category>\W*<Name>(?P<name>.*)</Name>\W*<Query>(?P<query>.*\-f (\w+).*)</Query>\W*", re.MULTILINE)
upresetsRE = re.compile(ur"\W*<Name>(?P<name>.*)</Name>\W*<Query>(?P<query>.*\-f (\w+).*)</Query>\W*", re.MULTILINE)
CRCRE = re.compile("[_\s]*\[[0-9a-zA-Z]{8,8}\]$")
GroupRE = re.compile("[\[\(][\w\-_]+[\]\)][_\s]*")
WhitespaceRE = re.compile("(.*?)([\s]*)(\.[a-zA-Z0-9]{1,5})$")
ExtRE = re.compile("\-f \w+|\-\-format \w+")
InputRE = re.compile("\-i \"\w+\"|\-\-input \"\w+\"")
OutputRE = re.compile("\-o \"\w+\"|\-\-output \"\w+\"")
StatusRE = re.compile("task (\d+) of (\d+), (\d+\.\d+) %")

STATUS_ENCODED = 1
STATUS_FAILED = 2
STATUS_TOENCODE = 3

STATUSMAP = {
    STATUS_ENCODED: wx.GREEN,
    STATUS_FAILED: wx.RED,
    STATUS_TOENCODE: wx.BLACK,
}

IDM_FILENAME = 0
IDM_OUTNAME = 1
IDM_FOLDER = 2
IDM_EXT = 3
IDM_STATUS = 4

PRE_CAT = 0
PRE_NAME = 1
PRE_QUERY = 2
PRE_EXT = 3

LIST_FILENAME = 0
LIST_OUTNAME = 1
LIST_FOLDER = 2

priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                           win32process.BELOW_NORMAL_PRIORITY_CLASS,
                           win32process.NORMAL_PRIORITY_CLASS,
                           win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                           win32process.HIGH_PRIORITY_CLASS,
                           win32process.REALTIME_PRIORITY_CLASS,
]

priorityNames = [
    "Idle", "Below Normal", "Normal", "Above Normal", "High", "Realtime",
]

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BOTTOM, wxID_FRAME1CHOOSEHBCLI, wxID_FRAME1CLEAR, 
 wxID_FRAME1CLEARCRC, wxID_FRAME1CLEARGRP, wxID_FRAME1ENCODE, 
 wxID_FRAME1ENCODINGTOSTATUS, wxID_FRAME1EXTENSION, wxID_FRAME1NICE, 
 wxID_FRAME1OUTPUTFOLDER, wxID_FRAME1PANEL, wxID_FRAME1PANEL1, 
 wxID_FRAME1PAUSERESUME, wxID_FRAME1PRESETLIST, wxID_FRAME1REPLACEEXTENSION, 
 wxID_FRAME1RESETFAILED, wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, 
 wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, 
 wxID_FRAME1STOPENCODE, wxID_FRAME1TITLE, 
] = [wx.NewId() for _init_ctrls in range(24)]

class MixSortList(wx.ListCtrl, listmix.ColumnSorterMixin):
    def __init__(self, *args, **kwargs):
        self.list = wx.ListCtrl(id=wx.NewId(), name=u'drop',
                                parent=kwargs["parent"], pos=wx.Point(0, 18), size=wx.Size(642, 400),
                                style=wx.LC_REPORT)

        self.il = wx.ImageList(16, 16)
        self.sm_up = self.il.Add(SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(SmallDnArrow.GetBitmap())
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.list.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
                               heading=u'Filename', width=-1)
        self.list.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
                               heading=u'Outfilename', width=-1)
        self.list.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
                               heading=u'Folder', width=-1)

        self.itemDataMap = {}

        listmix.ColumnSorterMixin.__init__(self, 3)

    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

class FancyToolTip(STT.SuperToolTip):
    def __init__(self, child, *args, **kwargs):
        STT.SuperToolTip.__init__(self, *args, **kwargs)
        self.SetStartDelay(0.25)
        self.ApplyStyle("Silver")
        self.SetDrawHeaderLine(False)
        self.SetDrawFooterLine(False)
        try:
            head = child.FTTLabel
        except:
            try:
                head = child.GetLabel() or child.GetName().capitalize()
            except:
                head = child.GetName().capitalize()

        t = type(child)
        if t == wx._controls.Choice:
            head = u"%s choice" % head
        elif t == wx._controls.CheckBox:
            head = u"%s?" % head
        elif t == wx._controls.TextCtrl:
            head = u"%s field" % head
        else:
            head = u"%s help" % head
        self.SetHeader(head)
        self.SetDropShadow(True)
        self.SetUseFade(False)
        self.SetEndDelay(600)

    def OnStartTimer(self):
        """ The creation time has expired, create the L{SuperToolTip}. """

        tip = STT.ToolTipWindow(self._widget, self)
        self._superToolTip = tip
        self._superToolTip.CalculateBestSize()
        self._superToolTip.SetPosition(wx.GetMousePosition() + wx.Point(10, 10))
        self._superToolTip.DropShadow(self.GetDropShadow())

        if self.GetUseFade():
            self._superToolTip.StartAlpha(True)
        else:
            self._superToolTip.Show()

        self._startTimer.Stop()
        self._endTimer.Start(self._endDelayTime*1000)

    def SetTarget(self, widget, superparent):
        """
        Sets the target window for L{SuperToolTip}.

        @param widget: the widget to which L{SuperToolTip} is associated. 
        """

        STT.SuperToolTip.SetTarget(self, widget)

        superparent.Bind(wx.EVT_IDLE, self.activityHide)


    def activityHide(self, evt):
        if self._superToolTip and not wx.GetActiveWindow():
            self._superToolTip.Destroy()
        evt.Skip()


class WindowsRegistry:
    def __init__(self, company="spirito GmbH", project="TestProg", write=1):
        """
        handle registry access
        """
        self.write = write
        self.company = company
        self.project = project
        if company:
            self.keyname = "Software\\%s\\%s" % (self.company, self.project)
        else:
            self.keyname = "Software\\%s" % self.project

        try:
            self.key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, self.keyname)
        except:
            if self.write:
                self.key = wreg.CreateKey(wreg.HKEY_CURRENT_USER, self.keyname)

    def set(self, name, value):
        " set value in registry "
        if not self.write:
            raise Exception, "registry is read only"
        wreg.SetValue(self.key, name, wreg.REG_SZ,str(value))

    def pset(self, name, value):
        " set using pickle "
        self.set(name, pickle.dumps(value))

    def get(self, name, default=None):
        " get value out of registry "
        try:
            return wreg.QueryValue(self.key, name)
        except:
            return default

    def pget(self, name, default=None):
        " get using pickle "
        try:
            return pickle.loads(wreg.QueryValue(self.key, name))
        except:
            return default

    def close(self):
        " close the key finally "
        self.key.Close()

    def __del__(self):
        self.close()

class MyStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has three fields
        self.SetFieldsCount(3)
        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([100, 200, -2])
        #self.log = log
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Field 0 ... just text
        self.SetStatusText("A Custom StatusBar...", 0)

        # This will fall into field 1 (the second field)
        self.g = wx.Gauge(self, -1, 100.0, (110, 50), (200, 25), style=wx.GA_SMOOTH)

        # set the initial position of the checkbox
        self.Reposition()

    def setGauge(self, value):
        self.g.SetValue(value)

    def OnSize(self, evt):
        self.Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True

    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()

    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(1)
        self.g.SetPosition((rect.x+2, rect.y+2))
        self.g.SetSize((rect.width-4, rect.height-4))
        self.sizeChanged = False

class Frame1(wx.Frame):


    def _init_coll_topSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.gridBagSizer1, 1, border=0,
              flag=wx.ALL | wx.EXPAND)

    def __init_coll_gridBagSizer1_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(1)
        parent.AddGrowableCol(0)

    def __init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.drop.list, (1, 0), border=0, flag=wx.EXPAND | wx.ALL,
                         span=(1, 1))
        parent.AddWindow(self.bottom, (2, 0), border=0, flag=0 | wx.ALL,
                         span=(1, 1))
        parent.AddWindow(self.title, (0, 0), border=0,
                         flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL,
                         span=(1, 1))
        parent.AddWindow(self.panel1, (0, 1), border=0, flag=0, span=(3, 1))

    def _init_sizers(self):
        # generated method, don't edit
        self.topSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.gridBagSizer1 = wx.GridBagSizer(hgap=5, vgap=5)
        self.gridBagSizer1.SetCols(2)
        self.gridBagSizer1.SetRows(3)
        self.gridBagSizer1.SetFlexibleDirection(wx.BOTH)

        self.boxSizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_topSizer_Items(self.topSizer)

        self.panel.SetSizer(self.topSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name=u'Frame1', parent=prnt,
              pos=wx.Point(604, 319), size=wx.Size(746, 638),
              style=wx.DEFAULT_FRAME_STYLE, title=u'HBBatchster %s')
        self.SetClientSize(wx.Size(730, 600))
        self.SetMinSize(wx.Size(730, 600))
        self.Bind(wx.EVT_CLOSE, self.OnFrame1Close)

        self.panel = wx.Panel(id=wxID_FRAME1PANEL, name=u'panel', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(730, 600),
              style=wx.TAB_TRAVERSAL)

        self.bottom = wx.Panel(id=wxID_FRAME1BOTTOM, name=u'bottom',
              parent=self.panel, pos=wx.Point(0, 423), size=wx.Size(642, 145),
              style=wx.TAB_TRAVERSAL)
        self.bottom.SetBackgroundColour(wx.Colour(212, 208, 200))
        self.bottom.SetMinSize(wx.Size(642, 145))
        self.bottom.SetMaxSize(wx.Size(-1, -1))

        self.title = wx.StaticText(id=wxID_FRAME1TITLE,
              label=u'Drop your files below', name=u'title', parent=self.panel,
              pos=wx.Point(270, 0), size=wx.Size(101, 13), style=0)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1',
              parent=self.panel, pos=wx.Point(647, 0), size=wx.Size(75, 284),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetMinSize(wx.Size(-1, -1))
        self.panel1.SetMaxSize(wx.Size(180, 3200))

        self.clear = wx.Button(id=wxID_FRAME1CLEAR, label=u'Clear',
              name=u'clear', parent=self.panel1, pos=wx.Point(0, 44),
              size=wx.Size(75, 23), style=0)
        self.clear.Enable(False)
        self.clear.Bind(wx.EVT_BUTTON, self.OnClearButton, id=wxID_FRAME1CLEAR)

        self.encode = wx.Button(id=wxID_FRAME1ENCODE, label=u'Encode',
              name=u'encode', parent=self.panel1, pos=wx.Point(0, 19),
              size=wx.Size(75, 23), style=0)
        self.encode.Enable(False)
        self.encode.Bind(wx.EVT_BUTTON, self.OnEncodeButton,
              id=wxID_FRAME1ENCODE)

        self.presetList = wx.Choice(choices=[], id=wxID_FRAME1PRESETLIST,
              name=u'presetList', parent=self.bottom, pos=wx.Point(61, 3),
              size=wx.Size(211, 21), style=wx.HSCROLL)
        self.presetList.SetMaxSize(wx.Size(170, 21))
        self.presetList.SetToolTipString(u'A list of the currently defined HandBrake presets and user-presets.\n\nTo edit them please launch HandBrake GUI or edit the config files.')
        self.presetList.Bind(wx.EVT_CHOICE, self.OnPresetListChoice,
              id=wxID_FRAME1PRESETLIST)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Preset:', name='staticText1', parent=self.bottom,
              pos=wx.Point(8, 5), size=wx.Size(35, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Extension:', name='staticText2', parent=self.bottom,
              pos=wx.Point(8, 32), size=wx.Size(51, 13), style=0)

        self.extension = wx.TextCtrl(id=wxID_FRAME1EXTENSION, name=u'extension',
              parent=self.bottom, pos=wx.Point(61, 29), size=wx.Size(48, 21),
              style=0, value=u'')
        self.extension.SetToolTipString(u'The extension of the resulting files.\n\nDetermined by the chosen preset - can be edited manually afterwards.')
        self.extension.Bind(wx.EVT_TEXT, self.OnExtensionText,
              id=wxID_FRAME1EXTENSION)

        self.clearCRC = wx.CheckBox(id=wxID_FRAME1CLEARCRC,
              label=u'Try to clear CRC in Filename', name=u'clearCRC',
              parent=self.bottom, pos=wx.Point(6, 56), size=wx.Size(194, 16),
              style=0)
        self.clearCRC.SetValue(False)
        self.clearCRC.SetToolTipString(u'Clears CRC tags in the original filename for the out file name.\n\n</b>Example:\nFile_[0AA0B0BA].avi -> File.avi')
        self.clearCRC.Bind(wx.EVT_CHECKBOX, self.OnClearCRCCheckbox,
              id=wxID_FRAME1CLEARCRC)

        self.replaceExtension = wx.CheckBox(id=wxID_FRAME1REPLACEEXTENSION,
              label=u'Replace original extension', name=u'replaceExtension',
              parent=self.bottom, pos=wx.Point(6, 101), size=wx.Size(200, 13),
              style=0)
        self.replaceExtension.SetValue(True)
        self.replaceExtension.SetToolTipString(u'Replaces the original extension with the selected one instead of appending it to the filename.\n\n</b>Example:\nFile.avi -> File.mkv\n\ninstead of:\nFile.avi -> File.avi.mkv')
        self.replaceExtension.Bind(wx.EVT_CHECKBOX,
              self.OnReplaceExtensionCheckbox, id=wxID_FRAME1REPLACEEXTENSION)

        self.chooseHBCLI = wx.FilePickerCtrl(id=wxID_FRAME1CHOOSEHBCLI,
              message='Select HandBrakeCLI.exe', name=u'chooseHBCLI',
              parent=self.bottom, path='', pos=wx.Point(336, 32),
              size=wx.Size(300, 20),
              style=wx.FLP_DEFAULT_STYLE | wx.FLP_USE_TEXTCTRL,
              wildcard=u'HandBrakeCLI.exe')

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Path to HandBrakeCLI:', name='staticText3',
              parent=self.bottom, pos=wx.Point(219, 36), size=wx.Size(110, 13),
              style=0)

        self.outputFolder = wx.DirPickerCtrl(id=wxID_FRAME1OUTPUTFOLDER,
              message='Select a folder', name=u'outputFolder',
              parent=self.bottom, path='', pos=wx.Point(336, 57),
              size=wx.Size(300, 20), style=wx.DIRP_DEFAULT_STYLE)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Override output folder:', name='staticText4',
              parent=self.bottom, pos=wx.Point(219, 60), size=wx.Size(112, 13),
              style=0)

        self.stopEncode = wx.Button(id=wxID_FRAME1STOPENCODE, label=u'Stop',
              name=u'stopEncode', parent=self.panel1, pos=wx.Point(0, 69),
              size=wx.Size(75, 23), style=0)
        self.stopEncode.Bind(wx.EVT_BUTTON, self.OnStopEncodeButton,
              id=wxID_FRAME1STOPENCODE)

        self.resetFailed = wx.Button(id=wxID_FRAME1RESETFAILED,
              label=u'Reset Failed', name=u'resetFailed', parent=self.panel1,
              pos=wx.Point(0, 94), size=wx.Size(75, 23), style=0)
        self.resetFailed.Bind(wx.EVT_BUTTON, self.OnResetFailedButton,
              id=wxID_FRAME1RESETFAILED)

        self.pauseResume = wx.Button(id=wxID_FRAME1PAUSERESUME, label=u'Pause',
              name=u'pauseResume', parent=self.panel1, pos=wx.Point(0, 118),
              size=wx.Size(75, 23), style=0)
        self.pauseResume.Enable(False)
        self.pauseResume.Bind(wx.EVT_BUTTON, self.OnPauseResumeButton,
              id=wxID_FRAME1PAUSERESUME)

        self.encodingToStatus = wx.StaticText(id=wxID_FRAME1ENCODINGTOSTATUS,
              label=u'', name=u'encodingToStatus', parent=self.bottom,
              pos=wx.Point(6, 125), size=wx.Size(0, 13), style=0)

        self.clearGRP = wx.CheckBox(id=wxID_FRAME1CLEARGRP,
              label=u'Try to clear garbage in Filename', name=u'clearGRP',
              parent=self.bottom, pos=wx.Point(6, 80), size=wx.Size(200, 13),
              style=0)
        self.clearGRP.SetValue(True)
        self.clearGRP.SetToolTipString(u'Clears garbage in filename, such as brackets with stuff inside.\n\n</b>Example:\n[Rumpel]File_(Season1).avi -> File.avi')
        self.clearGRP.Bind(wx.EVT_CHECKBOX, self.OnClearGRPCheckbox,
              id=wxID_FRAME1CLEARGRP)

        self.nice = wx.Choice(choices=[], id=wxID_FRAME1NICE, name=u'nice',
              parent=self.bottom, pos=wx.Point(336, 82), size=wx.Size(130, 21),
              style=0)
        self.nice.Bind(wx.EVT_CHOICE, self.OnNiceChoice, id=wxID_FRAME1NICE)
        self.nice.SetToolTipString(u'Selects the encoding process priority ("niceness").\n\n"Below Normal" (default) or "Normal" suggested.')

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'Encoding priority:', name='staticText5',
              parent=self.bottom, pos=wx.Point(219, 84), size=wx.Size(85, 13),
              style=0)

        self._init_sizers()

    def __init_customs(self, parent):
        self.drop = MixSortList(parent=self.panel)
        self.drop.list.SetMinSize(wx.Size(400, 400))
        self.__init_coll_gridBagSizer1_Items(self.gridBagSizer1)
        self.__init_coll_gridBagSizer1_Growables(self.gridBagSizer1)

        # statusbar
        #self.statusBar = CustomStatusBar(id=wxID_FRAME1STATUSBAR,
        #      name=u'statusBar', parent=self, style=0)
        #self._init_coll_statusBar_Fields(self.statusBar)
        self.statusBar = MyStatusBar(parent=self)

        # filepicker f ix
        d = wx.Size(300, 20)
        self.chooseHBCLI.SetInitialSize()
        self.chooseHBCLI.SetMinSize(d)
        self.chooseHBCLI.SetMaxSize(d)
        self.chooseHBCLI.SetSize(d)
        self.outputFolder.SetInitialSize()
        self.outputFolder.SetMinSize(d)
        self.outputFolder.SetMaxSize(d)
        self.outputFolder.SetSize(d)

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)
        self.drop.list.Bind(wx.EVT_LIST_KEY_DOWN, self.OnItemDelete)
        
        self.SetTitle(self.GetTitle() % HBB_VERSION)

    def getTTChildren(self, win):
        children = []
        for child in win.Children:
            if len(child.Children) > 0:
                children += self.getTTChildren(child)
            else:
                if child.GetToolTip():
                    children.append(child)
        return children

    def __init_fancy_tooltips(self, parent):
        children = self.getTTChildren(self)
        self.TTips = []
        for child in children:
            tt = child.GetToolTip()
            tip = FancyToolTip(child, tt.GetTip())
            tip.SetTarget(child, self)

            self.TTips.append(tip)
            tt.SetTip("")        

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.__init_customs(parent)

        self.presetList.FTTLabel = "Preset"

        self.__init_fancy_tooltips(parent)

        self.SetStatusBar(self.statusBar)

        self.DragAcceptFiles(True)
        self.drop.list.DragAcceptFiles(True)

        # events
        wx.EVT_DROP_FILES(self.drop.list, self.fdrop)
        wx.EVT_DROP_FILES(self, self.fdrop)
        self.chooseHBCLI.Bind(wx.EVT_FILEPICKER_CHANGED, self.HBPathChosen)
        self.outputFolder.Bind(wx.EVT_DIRPICKER_CHANGED, self.OutputFolderChosen)
        #self.drop.list.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete)

        self.gotPaths = False
        self.hbpath = None
        self.appDataPath = get_appdata()
        self.cli = None
        self.selectedNiceness = 1
        self.getConfig()
        self.getHBPathes()

        self.encoding = False
        self.stopped = False
        self.path = os.path.dirname(os.path.abspath(sys.argv[0]))    

        # icon
        ib=wx.IconBundle()
        #ib.AddIconFromFile(os.path.join(self.path, "handbrakepineapple2.ico"), wx.BITMAP_TYPE_ICO)
        ib.AddIcon(gethandbrakepineapple2Icon())
        self.SetIcons(ib)    


        self.selectedPreset = None
        self.choseExt = "mkv"
        self.presets = SortedDict()
        self.initPresets()
        self.initNiceness()

        if self.lastUsedExt:
            self.extension.SetValue(self.lastUsedExt)
            

        self.lastFileDrop = None
        self.initiatedKill = False
        self.closing = False

        self.process = None
        self.lastPID = None
        self.lastStatusText = ""
        self.currentFile = None
        self.outFolder = None
        self.paused = False
        self.current = 0
        self.queueCount = 0
        self.currentlyEncodingTo = u""

        self.topSizer.Fit(self)

        self.SetStatusText(u"Waiting", 0)

        self.Bind(wx.EVT_TIMER, self.cliTimer)
        self.t = wx.Timer(self)
        self.t.Start(500)

    def getHBPathes(self):
        if self.cli:
            if os.path.exists(self.cli):
                self.hbpath = os.path.split(self.cli)[0]
                self.SetStatusText(u"Custom HandBrake path reused (%s)" % self.cli, 2)
                self.gotPaths = True
                self.chooseHBCLI.SetPath(self.cli)
                return

        try:
            x = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Handbrake")
            value, typ = wreg.QueryValueEx(x, "DisplayIcon")
            if os.path.exists(value):
                self.hbpath = os.path.split(value)[0]
                self.cli = value

        except:
            pass
        else:
            self.gotPaths = True
            self.chooseHBCLI.SetPath(self.cli)
            self.SetStatusText(u"HandBrake path found via registry (%s)" % self.cli, 2)


    def cliTimer(self, e):
        if self.lastStatusText and not self.initiatedKill and self.encoding:
            self.SetStatusText(self.lastStatusText, 2)
            s = StatusRE.search(self.lastStatusText)
            if s:
                try:
                    at, of, percent = s.groups()
                    pac = 100.0 / int(of) * (int(at) - 1) + float(percent) / float(of)
                    self.statusBar.setGauge(pac)

                except Exception, e:
                    print e
                    pass

    def presetRep(self, p):
        return p.replace("&amp;", "&")

    def initPresets(self):
        try:
            #pf = open(os.path.join(self.hbpath, "presets.xml")).read()
            pf = open(os.path.join(self.appDataPath, "HandBrake", "presets.xml")).read()
            for cat, name, query, ext in presetsRE.findall(pf):
                name = self.presetRep(name)
                outn = u"%s: %s" % (cat, name)
                self.presets[outn] = [cat, name, query, ext]
        except:
            pass
        try:
            #pf = open(os.path.join(self.hbpath, "user_presets.xml")).read()
            pf = open(os.path.join(self.appDataPath, "HandBrake", "user_presets.xml")).read()
            for name, query, ext in upresetsRE.findall(pf):
                name = self.presetRep(name)
                outn = u"%s: %s" % ("USER", name)
                self.presets[outn] = ["USER", name, query, ext]
        except:
            pass
        self.presetList.AppendItems(self.presets.keys())

        if self.lastUsedPreset:
            self.selectedPreset = self.lastUsedPreset
            self.presetList.SetStringSelection(self.lastUsedPreset)
            self.choseExt = self.presets[self.lastUsedPreset][PRE_EXT]

        #self.presetList.SetSize(self.presetList.GetBestSize())
        #self.presetList.Fit()
        
    def initNiceness(self):
        self.nice.AppendItems(priorityNames)
        self.nice.SetSelection(self.selectedNiceness)

    def getConfig(self):
        r = WindowsRegistry(company=None, project="HBBatchster", write=1)
        self.clearFNCRC = r.pget("clearCRC") or True
        self.clearGRPNAME = r.pget("clearGroupName") or True
        self.cli = r.pget("HBCLIPath") or None
        self.lastUsedPreset = r.pget("lastUsedPreset") or None
        self.lastUsedExt = r.pget("lastUsedExt") or None
        self.replaceExt = r.pget("replaceExt") or True
        self.selectedNiceness = r.pget("niceness") or 1
        r.close()

        self.clearCRC.SetValue(self.clearFNCRC)
        self.clearGRP.SetValue(self.clearGRPNAME)
        self.replaceExtension.SetValue(self.replaceExt)

    def writeConfig(self):
        r = WindowsRegistry(company=None, project="HBBatchster", write=1)
        r.pset("clearCRC", self.clearFNCRC)
        r.pset("clearGroupName", self.clearGRPNAME)
        r.pset("HBCLIPath", self.cli)
        r.pset("lastUsedPreset", self.lastUsedPreset)
        r.pset("lastUsedExt", self.lastUsedExt)
        r.pset("replaceExt", self.replaceExt)
        r.pset("niceness", self.selectedNiceness)
        r.close()

    def toggleListActions(self):
        if self.drop.list.GetItemCount() > 0 and self.extension.GetValue() and self.cli and os.path.exists(self.cli) and self.selectedPreset:
            if not self.encoding:
                self.clear.Enable(True)
                self.encode.Enable(True)
                self.stopEncode.Enable(False)
                self.resetFailed.Enable(True)
                self.enablePause(False)
            else:
                self.stopEncode.Enable(True)
                self.encode.Enable(False)
                self.resetFailed.Enable(False)
                self.clear.Enable(False)
                self.enablePause()
        else:
            self.clear.Enable(False)
            self.encode.Enable(False)
            self.resetFailed.Enable(False)
            self.stopEncode.Enable(False)
            self.enablePause(False)

        if self.encoding:
            self.clear.Enable(False)
            self.encode.Enable(False)
            self.resetFailed.Enable(False)
            self.pauseResume.Enable(True)
            self.enablePause()


    def findOutFileName(self, p, fn, ext):
        add = u""
        nfn = nfn = u"%s%s.%s" % (fn, add, ext)
        while os.path.exists(os.path.join(p, nfn)):
            nfn = u"%s%s.%s" % (fn, add, ext)
            add += u"_"
        return p, nfn

    def listItemStatus(self, i, status):
        self.drop.list.SetItemTextColour(i, STATUSMAP[status])

    def filesToList(self, items):
        idm = self.drop.itemDataMap
        d = len(idm) + 1
        self.origExtCache = dict()
        for item in items:
            folder, fn = os.path.split(item)
            ext = os.path.splitext(fn)[1][1:]
            
            index = self.drop.list.InsertStringItem(sys.maxint, fn)

            ommit, out = self.findOutFileName(folder, fn, ".%s" % self.choseExt)
            self.drop.list.SetStringItem(index, 1, out)            
            self.drop.list.SetStringItem(index, 2, folder)
            self.drop.list.SetItemData(index, d)

            idm[d] = [fn, out, folder, ext, STATUS_TOENCODE]
            self.listItemStatus(index, STATUS_TOENCODE)
            d+=1

        self.toggleListActions()
        self.drop.list.SetColumnWidth(LIST_FILENAME, wx.LIST_AUTOSIZE)
        self.drop.list.SetColumnWidth(LIST_OUTNAME, wx.LIST_AUTOSIZE)
        self.drop.list.SetColumnWidth(LIST_FOLDER, wx.LIST_AUTOSIZE)

    def doClearFNCRC(self, fn):
        base, ext = os.path.splitext(fn)
        return "%s%s" % (re.sub(CRCRE, "", base), ext)

    def doClearGroupName(self, fn):
        base, ext = os.path.splitext(fn)
        return "%s%s" % (re.sub(GroupRE, "", base), ext)

    def setListExts(self, ext, changedBool = False):
        off = -1
        ext = ext[1:]
        if len(self.drop.itemDataMap) == 0:
            return
        for key, data in self.drop.itemDataMap.iteritems():
            iext = data[3]
                
            if iext != ext or changedBool:
                it = self.drop.list.FindItemData(off, key)
                nout = data[IDM_FILENAME]
                if self.clearFNCRC:
                    nout = self.doClearFNCRC(nout)
                if self.clearGRPNAME:
                    nout = self.doClearGroupName(nout)
                if self.replaceExt:
                    nout = nout[:nout.rfind(".")]
                    
                # replace whitespace before extension
                res = re.findall(WhitespaceRE, nout)
                if res:
                    nout = "%s%s" % (res[0][0], res[0][2])
                
                while nout.endswith(" "):
                    nout = nout[:-1]

                ommit, nout = self.findOutFileName(data[IDM_FOLDER] if not self.outFolder else self.outFolder, nout, ext)
                self.drop.itemDataMap[key][IDM_OUTNAME] = nout
                self.drop.itemDataMap[key][IDM_EXT] = ext

                self.drop.list.SetStringItem(it, LIST_OUTNAME, nout)


        self.drop.list.SetColumnWidth(LIST_OUTNAME, wx.LIST_AUTOSIZE)

    def OnListCtrl1ListDeleteItem(self, event):
        event.Skip()

    def fdrop(self, evt):
        gf = evt.GetFiles()
        self.lastFileDrop = gf
        self.filesToList(gf)
        self.setListExts(".%s" % self.choseExt)

    def OnCloseStream(self, evt):
        self.process.CloseOutput()

    def readStream(self, process):
        errs = ""
        ins = ""
        stream = process.GetInputStream()
        if stream.CanRead():
            ins = stream.read()

        stream = process.GetErrorStream()
        if stream.CanRead():
            errs = stream.read()

        return [ins, errs]


    def OnIdle(self, evt):
        try:
            if self.process is not None and not self.initiatedKill:
                ins, err = self.readStream(self.process)
                if ins:
                    self.lastStatusText = ins.split("\r")[-1]

        except Exception, e:
            print e
            pass

    def OnProcessEnded(self, evt):
        failed = bool(evt.GetExitCode())
        print 'OnProcessEnded, pid:%s,  exitCode: %s\n' % (evt.GetPid(), evt.GetExitCode())

        ins, err = self.readStream(self.process)
        #print ins, err

        self.process.Destroy()
        self.process = None
        self.lastPID = None
        self.encoding = False
        self.paused = False
        self.encodingToStatus.SetLabel(u'')
        self.currentlyEncodingTo = u""
        if self.initiatedKill:
            self.initiatedKill = False
        self.lastStatusText = ""
        if self.closing:
            self.Close()

        if self.currentFile:
            if not failed:
                self.drop.itemDataMap[self.currentFile][IDM_STATUS] = STATUS_ENCODED
                self.drop.list.SetItemBackgroundColour(self.drop.list.FindItemData(-1, self.currentFile), wx.GREEN)
                self.statusBar.setGauge(100.0)
                self.SetStatusText(u"File successfully encoded", 2)
            else:
                self.drop.itemDataMap[self.currentFile][IDM_STATUS] = STATUS_FAILED
                self.drop.list.SetItemBackgroundColour(self.drop.list.FindItemData(-1, self.currentFile), wx.RED)
                self.SetStatusText(u"Something went wrong ...", 2)
            self.currentFile = None
            self.encodeNext()

    def OnClearButton(self, event):
        self.drop.list.DeleteAllItems()
        self.drop.itemDataMap = {}
        self.toggleListActions()
        self.stopped = False
        event.Skip()

    def getNext(self):
        tec = 0
        for i in range(self.drop.list.GetItemCount()):
            idata = self.drop.list.GetItemData(i)
            fn, newfn, folder, ext, status = self.drop.itemDataMap[idata]
            if status in [STATUS_TOENCODE, STATUS_ENCODED, STATUS_FAILED]:
                tec += 1

        eof = 0
        for i in range(self.drop.list.GetItemCount()):
            idata = self.drop.list.GetItemData(i)
            fn, newfn, folder, ext, status = self.drop.itemDataMap[idata]
            if status == STATUS_TOENCODE:
                self.SetStatusText(u"Encoding %s/%s" % (eof+1, tec))
                self.current = eof
                self.queueCount = tec
                return idata, fn, newfn, folder, ext, status
            elif status in [STATUS_ENCODED, STATUS_FAILED]:
                eof += 1

        return [None] * 6

    def buildNextEncodeString(self, q, folder, fn, newfn, ext):
        # replace ext
        q = re.sub(ExtRE, "-f %s" % ext, q)
        q = re.sub(OutputRE, "", q)
        q = re.sub(InputRE, "", q)
        q = '%s -i "%s" -o "%s"' % (q, os.path.join(folder, fn), os.path.join(folder if not self.outFolder else self.outFolder, newfn))
        return q

    def encodeNext(self):
        if self.stopped:
            self.stopped = False
            self.paused = False
            self.encoding = False
            self.toggleListActions()
            
            self.SetStatusText(u"Stopped")
            self.statusBar.setGauge(100.0)
            self.doResetFailed()
            self.SetStatusText(u"Encoding stopped", 2)
            return
        
        idata, fn, newfn, folder, ext, status = self.getNext()
        if fn:
            self.encoding = True
            self.encodingToStatus.SetLabel(u'Encoding "%s"' % newfn)
            self.currentlyEncodingTo = newfn

        self.toggleListActions()
        if not fn:
            self.SetStatusText(u"Finished")
            self.SetStatusText(u"All tasks completed", 2)
            self.statusBar.setGauge(100.0)
            return

        if not self.selectedPreset:
            return

        self.statusBar.setGauge(0.0)
        self.SetStatusText(u"Encoding started", 2)

        self.drop.list.SetItemBackgroundColour(self.drop.list.FindItemData(-1, idata), wx.LIGHT_GREY)
        q = self.presets[self.selectedPreset][PRE_QUERY]
        self.currentFile = idata
        launch = self.buildNextEncodeString(q, folder, fn, newfn, ext)
        self.process = wx.Process(self)
        self.process.Redirect();
        
        #pid = wx.Execute(u"%s %s" % (self.cli, launch), wx.EXEC_ASYNC | wx.EXEC_NOHIDE, self.process)
        pid = wx.Execute(u"%s %s" % (self.cli, launch), wx.EXEC_ASYNC, self.process)
        
        self.setPriority(pid, self.selectedNiceness)
        
        self.lastPID = pid
        
    def doPauseResume(self, t="p"):
        if self.process:
            p = psutil.Process(self.lastPID)
            if t == "p":
                p.suspend()
                self.encodingToStatus.SetLabel(u'Paused encoding "%s"' % self.currentlyEncodingTo)
                return
            p.resume()
            self.encodingToStatus.SetLabel(u'Encoding "%s"' % self.currentlyEncodingTo)
            
            
    def pause(self):
        self.doPauseResume("p")
        
    def resume(self):
        self.doPauseResume("r")
        
    def doResetFailed(self):
        for item, values in self.drop.itemDataMap.iteritems():
            self.drop.itemDataMap[item][IDM_STATUS] = STATUS_TOENCODE
            self.drop.list.SetItemBackgroundColour(self.drop.list.FindItemData(-1, item), wx.WHITE)
            
    def enablePause(self, do=True):
        self.paused = not do
        self.pauseResume.Enable(do)
        if self.encoding and self.paused:
            self.pauseResume.SetLabel(u"Resume")
        elif (self.encoding and not self.paused) or not self.encoding:
            self.pauseResume.SetLabel(u"Pause")
            
        
    # taken from: http://code.activestate.com/recipes/496767/ (r1)
    def setPriority(self, pid=None, priority=1):
        """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
            2 is normal priority.  Default sets the priority of the current
            python process but can take any valid process ID. """
            
        if pid == None:
            pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, priorityclasses[priority])

    def OnEncodeButton(self, event):
        self.stopped = False
        self.SetStatusText(u"Starting Encode %s/%s" % (self.current + 1, self.queueCount), 0)
        if not self.encoding:
            self.encodeNext()
        event.Skip()

    def OnItemDelete(self, event):
        o = event.GetEventObject()
        kc = event.GetKeyCode()
        dl = self.drop.list
        todel = []
        if kc == wx.WXK_DELETE and not self.encoding:
            for i in range(0, dl.GetItemCount()):
                state = dl.GetItemState(i, wx.LIST_STATE_SELECTED)
                if state == wx.LIST_STATE_SELECTED:
                    d = dl.GetItem(i).GetData()
                    todel.append(d)

            for data in todel:
                dl.DeleteItem(dl.FindItemData(-1, data))
                del(self.drop.itemDataMap[data])
        event.Skip()


    def OnPresetListChoice(self, event):
        o = event.GetEventObject()
        s = o.GetStringSelection()
        if self.presets.has_key(s):
            cat, name, query, ext = self.presets[s]
            self.extension.SetValue(ext)
            self.setListExts(".%s" % ext)
            self.toggleListActions()
            self.choseExt = ext
            self.selectedPreset = s
            self.lastUsedPreset = s
            self.lastUsedExt = ext

        event.Skip()


    def OnExtensionText(self, event):
        v = event.GetEventObject().GetValue()
        self.setListExts(".%s" % v)
        self.toggleListActions()
        self.choseExt = v
        self.lastUsedExt = v
        event.Skip()

    def OnClearCRCCheckbox(self, event):
        self.clearFNCRC = bool(event.GetEventObject().GetValue())
        self.setListExts(".%s" % (self.extension.GetValue() or "mkv"), True)
        self.writeConfig()
        event.Skip()

    def OnClearGRPCheckbox(self, event):
        self.clearGRPNAME = bool(event.GetEventObject().GetValue())
        self.setListExts(".%s" % (self.extension.GetValue() or "mkv"), True)
        self.writeConfig()
        event.Skip()

    def OnFrame1Close(self, event):
        self.writeConfig()
        if self.process:
            if self.lastPID:
                try:
                    self.process.Kill(self.lastPID, wx.SIGKILL, wx.KILL_CHILDREN)
                    self.initiatedKill = True
                    self.closing = True
                    self.SetStatusText(u"Closing", 0)
                    self.SetStatusText(u"Killing HandBrakeCLI child...", 2)
                except:
                    pass

        if not self.initiatedKill:
            event.Skip()

    def HBPathChosen(self, event):
        self.cli = event.GetEventObject().GetPath()
        self.hbpath = os.path.split(self.cli)[0]
        self.writeConfig()
        event.Skip()

    def OutputFolderChosen(self, event):
        self.outFolder = event.GetEventObject().GetPath()
        self.setListExts(".%s" % self.choseExt, changedBool = True)
        event.Skip()

    def OnStopEncodeButton(self, event):
        self.stopped = True
        if self.process:
            if self.lastPID:
                try:
                    self.SetStatusText(u"Killing HandBrakeCLI child...", 2)
                    self.process.Kill(self.lastPID, wx.SIGKILL, wx.KILL_CHILDREN)
                    self.SetStatusText(u"Stopping", 0)
                    
                except:
                    pass
        event.Skip()

    def OnResetFailedButton(self, event):
        self.doResetFailed()        
        event.Skip()

    def OnPauseResumeButton(self, event):
        if self.paused:
            event.GetEventObject().SetLabel(u"Pause")
            self.paused = False
            self.SetStatusText(u"Resuming at %s/%s" % (self.current + 1, self.queueCount), 0)
            self.resume()
            self.getNext()
        else:
            event.GetEventObject().SetLabel(u"Resume")
            self.paused = True
            self.pause()
            self.SetStatusText(u"Paused at %s/%s" % (self.current + 1, self.queueCount), 0)
        event.Skip()

    def OnReplaceExtensionCheckbox(self, event):
        self.replaceExt = event.GetEventObject().GetValue()
        self.setListExts(".%s" % self.choseExt, changedBool=True)
        self.writeConfig()
        event.Skip()

    def OnNiceChoice(self, event):
        self.selectedNiceness = event.GetEventObject().GetSelection()
        self.writeConfig()
        event.Skip()



