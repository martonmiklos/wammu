# Wammu - Phone manager
# Copyright (c) 2003 - 2004 Michal Čihař 
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
'''
Generic thread wrapper used for reading things from phone
'''

import sys
import threading
import wx
import Wammu.Events
import Wammu.Error
from Wammu.Utils import Str_ as _

class Thread(threading.Thread):
    def __init__(self, win, sm):
        threading.Thread.__init__(self)
        self.win = win
        self.sm = sm
        self.canceled = False

    def run(self):
        try:
            sys.excepthook = Wammu.Error.Handler
        except:
            print _('Failed to set exception handler.')
        self.Run()

    def Cancel(self):
        self.canceled = True
        
    def ShowError(self, info, finish = False):
        if finish:
            self.ShowProgress(100)
        lck = threading.Lock()
        lck.acquire()
        evt = Wammu.Events.ShowMessageEvent(
            message = Wammu.Utils.FormatError(_('Error while communicating with phone'), info),
            title = _('Error Occured'),
            type = wx.ICON_ERROR,
            lock = lck)
        wx.PostEvent(self.win, evt)
        lck.acquire()

    def ShowMessage(self, title, text):
        lck = threading.Lock()
        lck.acquire()
        evt = Wammu.Events.ShowMessageEvent(
            message = text,
            title = title,
            type = wx.ICON_INFORMATION,
            lock = lck)
        wx.PostEvent(self.win, evt)
        lck.acquire()

    def ShowProgress(self, progress):
        evt = Wammu.Events.ProgressEvent(
            progress = progress,
            cancel = self.Cancel)
        wx.PostEvent(self.win, evt)

    def SendData(self, type, data, last = True):
        evt = Wammu.Events.DataEvent(
            type = type,
            data = data,
            last = last)
        wx.PostEvent(self.win, evt)

    def Canceled(self):
        lck = threading.Lock()
        lck.acquire()
        evt = Wammu.Events.ShowMessageEvent(
            message = _('Action canceled by user!'),
            title = _('Action canceled'),
            type = wx.ICON_WARNING,
            lock = lck)
        wx.PostEvent(self.win, evt)
        lck.acquire()
        self.ShowProgress(100)

