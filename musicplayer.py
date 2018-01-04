import os
import time
import wx
import MplayerCtrl as mpc
import wx.lib.buttons as buttons
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')
class Frame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self, parent, id, title, mplayer):
        wx.Frame.__init__(self, parent, id, title)
        self.panel = wx.Panel(self)
 
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        self.currentVolume = 100
 
        self.create_menu()
 
        # create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = self.build_controls()
        sliderSizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mplayer = mpc.MplayerCtrl(self.panel, -1, mplayer)
        self.playbackSlider = wx.Slider(self.panel, size=wx.DefaultSize)
        sliderSizer.Add(self.playbackSlider, 1, wx.ALL|wx.EXPAND, 5)
 
        # create volume control
        self.volumeCtrl = wx.Slider(self.panel)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.on_set_volume)
        controlSizer.Add(self.volumeCtrl, 0, wx.ALL, 5)
 
        # create track counter
        self.trackCounter = wx.StaticText(self.panel, label="00:00")
        sliderSizer.Add(self.trackCounter, 0, wx.ALL|wx.CENTER, 5)
 
        # set up playback timer
        self.playbackTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update_playback)
        #self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        #self.Bind(wx.EVT_SLIDER, self.on_Seek, self.playbackSlider)
 
        mainSizer.Add(self.mplayer, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(sliderSizer, 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(controlSizer, 0, wx.ALL|wx.CENTER, 5)
        self.panel.SetSizer(mainSizer)
 
        self.Bind(mpc.EVT_MEDIA_STARTED, self.on_media_started)
        self.Bind(mpc.EVT_MEDIA_FINISHED, self.on_media_finished)
        self.Bind(mpc.EVT_PROCESS_STARTED, self.on_process_started)
        self.Bind(mpc.EVT_PROCESS_STOPPED, self.on_process_stopped)
 
        self.Show()
        self.panel.Layout()
    #----------------------------------------------------------------------
    def build_btn(self, btnDict, sizer):
        """"""
        bmp = btnDict['bitmap']
        handler = btnDict['handler']
 
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self.panel, bitmap=img,
                                      name=btnDict['name'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)
        
 
    #----------------------------------------------------------------------
    def build_controls(self):
        """
        Builds the audio bar controls
        """
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnData = [{'bitmap':'special_button.png',
                     'handler':self.on_special, 'name':'special'},
                   {'bitmap':'player_prev.png',
                     'handler':self.on_Prev, 'name':'prev'},
                     {'bitmap':'player_play.png',
                    'handler':self.on_play, 'name':'play'},
                   {'bitmap':'player_pause.png', 
                    'handler':self.on_pause, 'name':'pause'},
                   {'bitmap':'player_stop.png',
                    'handler':self.on_stop, 'name':'stop'},
                    {'bitmap':'player_next.png',
                     'handler':self.on_Next, 'name':'next'}]
        for btn in btnData:
            self.build_btn(btn, controlSizer)
        return controlSizer
        
 
    #----------------------------------------------------------------------
    def create_menu(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        add_file_menu_item = fileMenu.Append(wx.NewId(), "&Add File", "Add Media File")
        menubar.Append(fileMenu, '&File')
 
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_add_file, add_file_menu_item)
 
    #----------------------------------------------------------------------
    def onkeypress(self,event):
        keycode=event.GetKeyCode()
        if keycode==wx.WXK_SPACE:
            print "Paused...."
            self.mplayer.Pause()
    #----------------------------------------------------------------------
    def on_add_file(self, event):
        """
        Add a Movie and start playing it
        """
        wildcard = "Media Files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentFolder, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.currentFolder = os.path.dirname(path[0])
            trackPath = '"%s"' % path.replace("\\", "/")
            self.mplayer.Loadfile(trackPath)
##            t_len = self.mplayer.GetProperty('Length')
##            print t_len
            self.playbackSlider.SetRange(0, 20)
            self.playbackTimer.Start(0)
    #----------------------------------------------------------------------
    def on_media_started(self, event):
        print 'Media started!'
 
    #----------------------------------------------------------------------
    def on_media_finished(self, event):
        print 'Media finished!'
        self.playbackTimer.Stop()
 
    #----------------------------------------------------------------------
    def on_pause(self, event):
        global mopau
        global mopla
        mopau=event.GetEventObject()
        self.mplayer.Pause()
        self.playbackTimer.Stop()
        mopau.Disable()
        mopla.Enable()
        '''
        if x:
            self.mplayer.Pause()
            print "Playing..."
            #self.playbackTimer.Stop()
            #self.playbackTimer.Start()'''
 
    #----------------------------------------------------------------------
    def on_Prev(self,event):
        print  "Hello"
        
    #----------------------------------------------------------------------
    def on_special(self,event):
        cap = cv2.VideoCapture(0)
        _playing= self.mplayer.playing
        while True:
            ret, img = cap.read()
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #faces = face_cascade.detectMultiScale(img, 1.3, 5)
            '''for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,0),2)
                #roi_gray = gray[y:y+h, x:x+w]
                #roi_color = img[y:y+h, x:x+w]
                '''
            eyes = eye_cascade.detectMultiScale(img,1.3,5)
            #Draw rectangle along eyes
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                if not self.playbackTimer.IsRunning():
                    self.mplayer.Pause()
                    self.playbackTimer.Start(0)
            cv2.imshow('img',img)
            if self.playbackTimer.IsRunning():
                self.mplayer.Pause()
                self.playbackTimer.Stop()
                
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        cap.release() 
    #----------------------------------------------------------------------
    def on_Next(self,event):
        print "hello"
    #----------------------------------------------------------------------
    def on_play(self,event):
        
        global mopla
        global mopau
        mopla=event.GetEventObject()
        self.mplayer.Pause()
        self.playbackTimer.Start(0)
        mopla.Disable()
        mopau.Enable()
        '''
        if not event.GetIsDown():
            self.on_pause()
            return
 
        if not self.mediaPlayer.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
 
        event.Skip()'''
    #----------------------------------------------------------------------
    def on_process_started(self, event):
        print 'Process started!'
 
    #----------------------------------------------------------------------
    def on_process_stopped(self, event):
        print 'Process stopped!'
 
    #----------------------------------------------------------------------
    def on_set_volume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        self.mplayer.SetProperty("volume", self.currentVolume)
 
    #----------------------------------------------------------------------
    def on_stop(self, event):
        """"""
        print "stopping..."
        self.mplayer.Stop()
        self.playbackTimer.Stop()
 
    #----------------------------------------------------------------------
    def on_update_playback(self, event):
        """
        Updates playback slider and track counter
        """
        try:
            offset = self.mplayer.GetTimePos()
        except:
            return
        print offset
        mod_off = str(offset)[-1]
        if mod_off == '0':
            print "mod_off"
            offset = int(offset)
            self.playbackSlider.SetValue(offset)
            secsPlayed = time.strftime('%M:%S', time.gmtime(offset))
            self.trackCounter.SetLabel(secsPlayed) 
        '''offset = self.mplayer.GetTimePos()
        print offset
        mod_off = str(offset)[-1]
        if mod_off == '0':
            print "mod_off"
            offset = int(offset)
            self.playbackSlider.SetValue(offset)
            secsPlayed = time.strftime('%M:%S', time.gmtime(offset))
            self.trackCounter.SetLabel(secsPlayed)'''
if __name__ == "__main__":
    import os, sys
    
    paths = [r'C:\MPlayer-rtm-svn-31170\mplayer.exe',
             r'E:\MPlayer-rtm-svn-31170\mplayer.exe']
    mplayerPath = None
    for path in paths:
        if os.path.exists(path):
            mplayerPath = path
        
    if not mplayerPath:
        print "mplayer not found!"
        sys.exit()
            
    app = wx.App(redirect=False)
    frame = Frame(None, -1, 'Music Player', mplayerPath)
    app.MainLoop()

