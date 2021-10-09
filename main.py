import sys
import os
import tkinter.messagebox
import tkinter
from pytube import YouTube

try:
    ytobj = YouTube(sys.argv[1].split("testus://")[-1][:-1])
    print(ytobj.streams)
    os.system("pause")
except Exception as e:
    win = tkinter.Tk()
    win.withdraw()
    tkinter.messagebox.showerror("Error", str(e))
    win.destroy()
