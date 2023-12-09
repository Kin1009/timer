import time
import winsound
from tkinter import Tk, END, IntVar
from tkinter.ttk import *
from threading import Thread
from win32api import *
from win32gui import *
import win32con
import sys, os
 
class WindowsBalloonTip:
    def __init__(self):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        self.classAtom = RegisterClass(wc)
    def create(self, title, msg):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = CreateWindow(self.classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, self.hinst, None)
        self.hwnd = hwnd
        UpdateWindow(hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(self.hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
w = WindowsBalloonTip()
def balloon_tip(title, msg):
    global w
    w.create(title, msg)
def alert(duration):
    global stop
    for i in range(duration):
        while stop == 0:
            winsound.Beep(1000, 100)
            win.update()
            winsound.Beep(1000, 100)
            win.update()
            winsound.Beep(1000, 100)
            win.update()
            for i in range(100):
                time.sleep(0.0075)
                win.update()
        stop = 0
        return
win = Tk()
win.title("Timer")
win.resizable(0, 0)
valh = IntVar(value=0)
valm = IntVar(value=0)
vals = IntVar(value=0)
Label(win, text="Hours").grid(column=0, row=0)
hours = Spinbox(win, from_=0, to=23, textvariable=valh, width=2)
hours.grid(column=1, row=0)
Label(win, text="Minutes").grid(column=0, row=1)
hours = Spinbox(win, from_=0, to=59, textvariable=valm, width=2)
hours.grid(column=1, row=1)
Label(win, text="Seconds").grid(column=0, row=2)
hours = Spinbox(win, from_=0, to=59, textvariable=vals, width=2)
hours.grid(column=1, row=2)
stop = 0
h = 0
m = 0
s = 0
done = 1
def run():
    global stop, h, m, s, done
    stop = 0
    btt1.config(state="disabled")
    btt2.config(state="disabled")
    btt3.config(state="normal")
    if done == 1:
        h = valh.get()
        m = valm.get()
        s = vals.get()
        done = 0
    h_ = valh.get()
    m_ = valm.get()
    s_ = vals.get()
    while h_ >= 0:
        while m_ >= 0:
            while s_ - 1 >= 0:
                s_ -= 1
                vals.set(s_)
                valm.set(m_)
                valh.set(h_)
                for i in range(100):
                    win.update()
                    time.sleep(1 / 100)
                    if stop == 1:
                        stop = 0
                        return
            s_ = 60
            m_ -= 1
        m_ = 59
        h_ -= 1
    stop = 0
    btt2.config(state="normal")
    btt3.config(state="disabled")
    win.after(10, lambda: alert(100))
    thread = Thread(target=lambda: balloon_tip("Timer", "Time's up!"), daemon=True)
    win.after(10, lambda: thread.start())
    done = 1
    return
def stop_():
    global stop
    btt1.config(state="normal")
    btt2.config(state="normal")
    btt3.config(state="disabled")
    stop = 1
def reset():
    global h, m, s, stop
    stop = 1
    btt1.config(state="normal")
    btt2.config(state="disabled")
    btt3.config(state="disabled")
    valh.set(h)
    valm.set(m)
    vals.set(s)
def exit_():
    stop_()
    exit()
win.protocol('WM_DELETE_WINDOW', exit_)
btt1 = Button(win, text="Run / Resume", command=run)
btt1.grid(column=2,row=0)
btt2 = Button(win, text="Reset", command=reset)
btt2.grid(column=2,row=1)
btt3 = Button(win, text="Pause", command=stop_)
btt3.grid(column=2,row=2)
btt2.config(state="disabled")
btt3.config(state="disabled")
win.mainloop()