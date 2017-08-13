#!/usr/bin/python
#
# ./TimeMyTalk.py
# Simple countdown clock with large plots to be used to keep time during talks.
# The different talk lengths are hardcoded to simplify control during execution.
# The programme can be controlled either by mouse and buttons or with keystrokes.
# When the time is running out, the programme first changes the background from
# green to red and finally starts blinking between two shades of red.
#
# Keys:
# 1, 3, 4: set length to 15, 30 and 45 minutes (adapted to GLU 2017)
# t:       set length freely with a string in the format MM:SS
# f:       toggle fullscreeen
# Esc:     exit fullscreen
# c:       toggle controls (button) visibility
# S:       toggle start/stop countdown
# q:       quit (without confirmation)
#
# Note: written for python 2.7, to update to python 3.x, change Tkinter to tkinter
#   and tkFont to tkinter.font
#
# Note on fonts: Tk as installed by Ubuntu uses XTF to handle fonts. This
#   gives a large number of true type font families and works well in the
#   version of python installed by Ubuntu. However, the version of Tk installed
#   in Anaconda only supports a limited number of bitmapped X fonts that look
#   horrible when scaled up.
#
# (C) 2017, Giampiero Salvi <giampi@kth.se>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Tkinter import *
import tkFont
#from Tkinter import ttk
import time

class CountDown():
    """Count Down Class"""
    def __init__(self, tkWindow):
        self.mainWindow = tkWindow
        self.mainWindow.title('GLU 2017 Timer')
        self.mainWindow.geometry("300x250")
        self.mainWindow.resizable(1,1)
        self.isFullscreen = False
        self.visibleControls = False
        # configure colors
        self.defaultColour = self.mainWindow.cget("bg")
        self.plentyOfTimeColor = 'light green'
        self.shortTimeColor1 = 'orange red'
        self.shortTimeColor2 = 'coral'
        self.stoppedColor = self.outOfTimeColor = 'red'
        # configure times (in seconds)
        self.refreshRate = 100 # milliseconds. The lower the smoother, but the more CPU intensive
        self.firstWarningSeconds = 5.0 * 60
        self.secondWarningSeconds = 2.0 * 60
        self.accumulatedTime = 0.0 # time accumulated between subsequent start/stop
        self.startTime = 0.0       # time from Event when start button is pressed
        self.talkTime = 15.0 * 60  # lenght of the talk
        self.displayString = self.seconds2string(self.talkTime)
        self.running = False
        # GUI widgets
        self.clockfont = tkFont.Font(family="DejaVu Sans", size="20")
        self.clock = Label(self.mainWindow, font=self.clockfont, text=self.displayString)
        self.controls = Frame(self.mainWindow)
        self.btn_set15 = Button(self.controls, text = 'Set 15 (1)', command = self.set15_btn)
        self.btn_set30 = Button(self.controls, text = 'Set 30 (3)', command = self.set30_btn)
        self.btn_set45 = Button(self.controls, text = 'Set 45 (4)', command = self.set45_btn)
        self.btn_set = Button(self.controls, text = 'Set... (t)', command = self.set_window)
        self.btn_startStop = Button(self.controls, text = 'Start (S)', command = self.toggleRunning_btn)
        # packing widgets in the root window
        self.clock.pack(side="left", fill="both", expand=True)
        self.btn_set15.grid(sticky=EW, row = 1, column = 1, padx = 5, pady = (5,2))
        self.btn_set30.grid(sticky=EW, row = 2, column = 1, padx = 5, pady = (5,2))
        self.btn_set45.grid(sticky=EW, row = 3, column = 1, padx = 5, pady = (5,2))
        self.btn_set.grid(sticky=EW, row = 4, column = 1, padx = 5, pady = (5,2))
        self.btn_startStop.grid(sticky=EW, row = 5, column = 1, padx = 5, pady = 2)
        if self.visibleControls:
            self.controls.pack(side="left", fill="y", expand=False)
        self.tick()
        # binding events
        self.mainWindow.bind('<Configure>', self.resize)
        self.mainWindow.bind('S', self.toggleRunning_btn)
        self.mainWindow.bind('1', self.set15_btn)
        self.mainWindow.bind('3', self.set30_btn)
        self.mainWindow.bind('4', self.set45_btn)
        self.mainWindow.bind('t', self.set_window)
        self.mainWindow.bind('f', self.toggleFullscreen)
        self.mainWindow.bind('<Escape>', self.endFullscreen)
        self.mainWindow.bind('c', self.toggleControlsVisibility)
        self.mainWindow.bind('q', self.Quit)
        # make sure widget instances are deleted
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.Quit)
    def resize(self, event):
        labelWidth = self.clock.winfo_width()
        labelHeight = self.clock.winfo_height()
        # heuristics to get the full text maximised inside the widget (including the eventual minus sign)
        fontSize = min(int(labelHeight*0.9), int(labelWidth/4.3))
        self.clockfont.configure(size = fontSize)
        self.clock.config(font=self.clockfont)
    def toggleFullscreen(self, event):
        self.isFullscreen = not self.isFullscreen
        self.mainWindow.attributes('-fullscreen', self.isFullscreen)
    def endFullscreen(self, event):
        self.isFullscreen = False
        self.mainWindow.attributes('-fullscreen', self.isFullscreen)
    def toggleControlsVisibility(self, event):
        if self.visibleControls:
            self.controls.pack_forget()
        else:
            self.controls.pack()
        self.visibleControls = not self.visibleControls
    def Quit(self, event=None):
        self.mainWindow.quit()
    def seconds2string(self, seconds):
        """ converts possibly negative times to string """
        if seconds<0:
            return '-'+time.strftime("%M:%S", time.gmtime(-seconds))
        else:
            return time.strftime("%M:%S", time.gmtime(seconds))
    def string2seconds(self, string):
        """ converts string to possibly negative times """
        #print('string2seconds', string)
        if string == '':
            return 0.0
        multiply = 1
        if string[0] == '-':
            multiply = -1
            string = string[1:]
        t0 = time.mktime(time.strptime('0:0', '%M:%S'))
        t1 = time.mktime(time.strptime(string, '%M:%S'))
        return multiply * (t1-t0)
    def tick(self):
        # get the current local time from the PC
        if self.running:
            currentTime = time.time()
            elapsedTime = currentTime - self.startTime + self.accumulatedTime
            displayTime = self.talkTime - elapsedTime
            #print('displayTime:', displayTime, 'elapsedTime:', elapsedTime, 'accumulatedTime:', self.accumulatedTime)
            newDisplayString = self.seconds2string(displayTime)
        else:
            newDisplayString = ''
            self.displayString = ''
        # if time string has changed, update it
        if newDisplayString != self.displayString:
            self.displayString = newDisplayString
            if displayTime < self.firstWarningSeconds and displayTime >= self.secondWarningSeconds:
                self.clock.config(bg=self.shortTimeColor1)
            if displayTime < self.secondWarningSeconds:
                currentColor = self.clock.cget("background")
                nextColor = self.shortTimeColor2 if currentColor == self.shortTimeColor1 else self.shortTimeColor1
                self.clock.config(bg=nextColor)
            self.clock.config(text=self.displayString)
        self.clock.after(self.refreshRate, self.tick)
    def toggleRunning_btn(self, event=None):
        if self.running:
            currentTime = time.time()
            self.clock.config(bg=self.stoppedColor)
            self.accumulatedTime = self.accumulatedTime + (currentTime - self.startTime)
            self.btn_startStop.config(text='Start (S)')
            self.running = False
        else:
            self.clock.config(bg=self.plentyOfTimeColor)
            self.startTime = time.time()
            self.btn_startStop.config(text='Stop (S)')
            self.running = True
    def set_btn(self, seconds):
        if self.running:
            self.toggleRunning_btn()
        self.clock.config(bg=self.defaultColour)
        self.accumulatedTime = 0.0
        self.talkTime = seconds
        self.displayString = self.seconds2string(self.talkTime)
        self.clock.config(text=self.displayString)
    def set15_btn(self, event=None):
        self.set_btn(15.0 * 60)
    def set30_btn(self, event=None):
        self.set_btn(30.0 * 60)
    def set45_btn(self, event=None):
        self.set_btn(45.0 * 60)
    def setFromString_btn(self, event=None):
        self.set_btn(self.string2seconds(self.inputString.get()))
    def set_window(self, event=None):
        w = Toplevel(self.mainWindow)
        w.wm_title("Set length")
        l = Label(w, text="Set talk length (MM:SS)")
        l.pack(side="top", fill="both", expand=True, padx=10, pady=5)
        self.inputString=StringVar()
        self.inputString.set('')
        f = Entry(w, textvariable=self.inputString)
        f.pack(side="top", fill="both", expand=True, padx=10, pady=5)
        b = Button(w, text="Ok", width=5, command=self.setFromString_btn)
        b.pack(side="top", expand=True, padx=10, pady=5)

root = Tk()

# If you only want one counter (most common), you can create it
# in the root window like this
counter = CountDown(root)

# If you want several counters, create them in a toplevel of the
# root like this:
# counter1 = CountDown(Toplevel(root))
# counter2 = CountDown(Toplevel(root))
# however in the current implementation, quitting one will quit all
# in this case, you will also want to hide the (empty) root window
# root.withdraw()

# start Tk main loop
root.mainloop()
