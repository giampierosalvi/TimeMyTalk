#!/usr/bin/python
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
        self.defaultColour = self.rootWindow.cget("bg")
        self.time1 = ''
        self.prevSec = ''
        self.mins = 15
        self.secs = 0
        self.hours = 0
        self.running = False
        #clock = Label(rootWindow, font=('fixed', 20, 'bold'))
        self.clockfont = tkFont.Font(family="DejaVu Sans", size="20")
        self.clock = Label(self.rootWindow, font=self.clockfont)
        #clock.grid(row = 1, column = 2, padx = 5, pady = (5,2))
        self.clock.pack(side="top", fill="both", expand=True)
        self.tick()
        self.rootWindow.bind('<Configure>', self.resize)
        self.rootWindow.mainloop()
    def resize(self, event):
        self.clockfont.configure(size = int(self.rootWindow.winfo_width()/4.0))
        self.clock.config(font=self.clockfont)
    def tick(self):
        # get the current local time from the PC
        if self.running:
            newSec = time.strftime('%S')
        else:
            newSec = ''
            prevSec = ''
        if newSec != prevSec:
            prevSec = newSec
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
                        self.clock.config(bg='red')
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
    def start_btn(self):
        #global running
        self.clock.config(bg='green')
        self.btn_start.config(state='disabled',background=self.defaultColour)
        self.btn_stop.config(state='normal',bg='dark red')
        self.btn_set15.config(state='disabled')
        self.btn_set45.config(state='disabled')
        self.running = True
    def stop_btn(self):
        #global running 
        self.clock.config(bg='dark red')
        self.btn_start.config(state='normal',bg='green')
        self.btn_stop.config(state='disabled',bg=self.defaultColour)
        self.btn_set15.config(state='normal')
        self.btn_set45.config(state='normal')
        self.running = False
    def set15_btn(self):
        #global prevSec, time1, secs, mins, hours, running 
        self.clock.config(bg=self.defaultColour)
        self.hours = 0
        self.mins = 15
        self.secs = 0
        self.prevSec = ''
        self.time1 = ''
        self.running = False
        self.btn_stop.config(state='disabled',bg=self.defaultColour)
        self.btn_start.config(state='normal',bg='green')
        self.btn_set15.config(state='disabled')
        self.btn_set45.config(state='normal')
    def set45_btn(self):
        #global prevSec, time1, secs, mins, hours, running 
        self.clock.config(bg=self.defaultColour)
        self.hours = 0
        self.mins = 45
        self.secs = 0
        self.prevSec = ''
        self.time1 = ''
        self.running = False
        self.btn_stop.config(state='disabled',bg=self.defaultColour)
        self.btn_start.config(state='normal',bg='green')
        self.btn_set15.config(state='normal')
        self.btn_set45.config(state='disabled')

if False:
    btn_set15 = Button(rootWindow, state='disabled', text = 'Set 15 (1)', command = set15_btn)
    btn_set45 = Button(rootWindow, state='disabled', text = 'Set 45 (4)', command = set45_btn)
    btn_set15.grid(sticky=EW, row = 1, column = 3, padx = 5, pady = (5,2))
    btn_set45.grid(sticky=EW, row = 2, column = 3, padx = 5, pady = (5,2))
    btn_start = Button(rootWindow, text = 'Start (S)', bg='green', command = start_btn)
    btn_start.grid(sticky=EW, row = 3, column = 3, padx = 5, pady = 2)
    btn_stop = Button(rootWindow, state='disabled', text = 'Stop (Z)', command = stop_btn)
    btn_stop.grid(sticky=EW, row = 4, column = 3, padx = 5, pady = (2,5))
    #btn_exit = Button(rootWindow, text = 'exit', command = exit)
    #btn_exit.grid(row = 4, column = 1, padx = 5, pady = 5) 


counter = CountDown()
