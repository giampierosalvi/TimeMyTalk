#!/usr/bin/python
#
# Note: written for python 2.7, to update to python 3.x, change Tkinter to tkinter
#   and tkFont to tkinter.font
#
# Note on fonts: Tk as installed by Ubuntu uses XTF to handle fonts. This
# gives a large number of true type font families and works well in the
# version of python installed by Ubuntu. However, the version of Tk installed
# in Anaconda only supports a limited number of bitmapped X fonts that look
# horrible when scaled up.

from Tkinter import *
import tkFont
#from Tkinter import ttk
import time

class CountDown:
    """Count Down Class"""
    def __init__(self):
        self.rootWindow = Tk()
        self.rootWindow.title('GLU 2017 Timer')
        self.rootWindow.geometry("300x250")
        self.rootWindow.resizable(1,1)
        self.isFullscreen = False
        self.visibleControls = False
        # configure colors
        self.defaultColour = self.rootWindow.cget("bg")
        self.plentyOfTimeColor = 'light green'
        self.shortTimeColor1 = 'orange red'
        self.shortTimeColor2 = 'coral'
        self.stoppedColor = self.outOfTimeColor = 'red'
        # status related variables
        self.time1 = ''
        self.prevSec = ''
        self.mins = 15
        self.secs = 0
        self.hours = 0
        self.running = False
        # GUI widgets
        self.clockfont = tkFont.Font(family="DejaVu Sans", size="20")
        self.clock = Label(self.rootWindow, font=self.clockfont)
        self.controls = Frame(self.rootWindow)
        self.btn_set15 = Button(self.controls, text = 'Set 15 (1)', command = self.set15_btn)
        self.btn_set30 = Button(self.controls, text = 'Set 30 (3)', command = self.set30_btn)
        self.btn_set45 = Button(self.controls, text = 'Set 45 (4)', command = self.set45_btn)
        self.btn_start = Button(self.controls, text = 'Start (S)', command = self.start_btn)
        self.btn_stop = Button(self.controls, state='disabled', text = 'Stop (Z)', command = self.stop_btn)
        # packing widgets in the root window
        self.clock.pack(side="left", fill="both", expand=True)
        self.btn_set15.grid(sticky=EW, row = 1, column = 1, padx = 5, pady = (5,2))
        self.btn_set30.grid(sticky=EW, row = 2, column = 1, padx = 5, pady = (5,2))
        self.btn_set45.grid(sticky=EW, row = 3, column = 1, padx = 5, pady = (5,2))
        self.btn_start.grid(sticky=EW, row = 4, column = 1, padx = 5, pady = 2)
        self.btn_stop.grid(sticky=EW, row = 5, column = 1, padx = 5, pady = (2,5))
        if self.visibleControls:
            self.controls.pack(side="left", fill="y", expand=False)
        self.tick()
        # binding events
        self.rootWindow.bind('<Configure>', self.resize)
        self.rootWindow.bind('S', self.start_btn)
        self.rootWindow.bind('Z', self.stop_btn)
        self.rootWindow.bind('1', self.set15_btn)
        self.rootWindow.bind('3', self.set30_btn)
        self.rootWindow.bind('4', self.set45_btn)
        self.rootWindow.bind('f', self.toggleFullscreen)
        self.rootWindow.bind('<Escape>', self.endFullscreen)
        self.rootWindow.bind('c', self.toggleControlsVisibility)
        self.rootWindow.bind('q', self.Quit)
        # start GUI main loop
        self.rootWindow.mainloop()
    def resize(self, event):
        labelWidth = self.clock.winfo_width()
        labelHeight = self.clock.winfo_height()
        # heuristics to get the full text maximised inside the widget (including the eventual minus sign)
        fontSize = min(int(labelHeight*0.9), int(labelWidth/4.3))
        self.clockfont.configure(size = fontSize)
        self.clock.config(font=self.clockfont)
    def toggleFullscreen(self, event):
        self.isFullscreen = not self.isFullscreen
        self.rootWindow.attributes('-fullscreen', self.isFullscreen)
    def endFullscreen(self, event):
        self.isFullscreen = False
        self.rootWindow.attributes('-fullscreen', self.isFullscreen)
    def toggleControlsVisibility(self, event):
        if self.visibleControls:
            self.controls.pack_forget()
        else:
            self.controls.pack()
        self.visibleControls = not self.visibleControls
    def Quit(self, event):
        print('Quitting')
        self.rootWindow.quit()
    def tick(self):
        # get the current local time from the PC
        if self.running:
            newSec = time.strftime('%S')
        else:
            newSec = ''
            self.prevSec = ''
        if newSec != self.prevSec:
            self.prevSec = newSec
            self.secs = self.secs - 1
            if self.secs < 0:
                self.secs = 59
                self.mins = self.mins - 1
                if self.mins < 0:
                    self.mins = 59
                    self.hours = self.hours - 1
                    if self.hours < 0: 
                        self.hours = 0
                        self.mins = 0
                        self.secs = 0
            if self.mins<5 and self.mins>=4:
                self.clock.config(bg=self.shortTimeColor1)
            if self.mins<4:
                currentColor = self.clock.cget("background")
                nextColor = self.shortTimeColor2 if currentColor == self.shortTimeColor1 else self.shortTimeColor1
                self.clock.config(bg=nextColor)
        #time2 = '%02d:%02d:%02d' % (hours, mins, secs)
        self.time2 = '%02d:%02d' % (self.mins, self.secs)
        # if time string has changed, update it
        if self.time2 != self.time1:
            self.time1 = self.time2
            self.clock.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.clock.after(200, self.tick)
    def start_btn(self, event=None):
        #global running
        self.clock.config(bg=self.plentyOfTimeColor)
        self.btn_start.config(state='disabled')
        self.btn_stop.config(state='normal')
        #self.btn_set15.config(state='disabled')
        #self.btn_set45.config(state='disabled')
        self.running = True
    def stop_btn(self, event=None):
        #global running 
        self.clock.config(bg=self.stoppedColor)
        self.btn_start.config(state='normal')
        self.btn_stop.config(state='disabled')
        #self.btn_set15.config(state='normal')
        #self.btn_set45.config(state='normal')
        self.running = False
    def set_btn(self, event=None):
        self.clock.config(bg=self.defaultColour)
        self.hours = 0
        self.secs = 0
        self.prevSec = ''
        self.time1 = ''
        self.running = False
        self.btn_stop.config(state='disabled')
        self.btn_start.config(state='normal')
    def set15_btn(self, event=None):
        self.set_btn(event)
        self.mins = 15
    def set30_btn(self, event=None):
        self.set_btn(event)
        self.mins = 30
    def set45_btn(self, event=None):
        self.set_btn(event)
        self.mins = 45

counter = CountDown()
