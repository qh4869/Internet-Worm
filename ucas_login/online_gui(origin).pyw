# -*- coding:utf-8 -*- 
import requests
import os
from bs4 import BeautifulSoup
import time
import win32api, win32gui  
import win32con, winerror  
import sys
import threading
run_flag = 1
#---------------------gui----------------------
class MainWindow:  
    def __init__(self):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated");  
        message_map = {  
                msg_TaskbarRestart: self.OnRestart,  
                win32con.WM_DESTROY: self.OnDestroy,  
                win32con.WM_COMMAND: self.OnCommand,  
                win32con.WM_USER+20 : self.OnTaskbarNotify,  
        }  
        # Register the Window class.  
        wc = win32gui.WNDCLASS()  
        hinst = wc.hInstance = win32api.GetModuleHandle(None)  
        wc.lpszClassName = "PythonTaskbarDemo"  
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;  
        wc.hCursor = win32api.LoadCursor( 0, win32con.IDC_ARROW )  
        wc.hbrBackground = win32con.COLOR_WINDOW  
        wc.lpfnWndProc = message_map # could also specify a wndproc.  
  
        # Don't blow up if class already registered to make testing easier  
        try:  
            classAtom = win32gui.RegisterClass(wc)  
        except (win32gui.error, err_info):  
            if err_info.winerror!=winerror.ERROR_CLASS_ALREADY_EXISTS:  
                raise  
  
        # Create the Window.  
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  
        self.hwnd = win32gui.CreateWindow( wc.lpszClassName, "Taskbar Demo", style, \
                                           0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,\
                                           0, 0, hinst, None)  
        win32gui.UpdateWindow(self.hwnd)  
        self._DoCreateIcons()  
    def _DoCreateIcons(self):  
        # Try and find a custom icon  
        hinst =  win32api.GetModuleHandle(None)  
        iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "pyc.ico" ))  
        if not os.path.isfile(iconPathName):  
            # Look in DLLs dir, a-la py 2.5  
            iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "DLLs", "pyc.ico" ))  
        if not os.path.isfile(iconPathName):  
            # Look in the source tree.  
            iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "..\\PC\\pyc.ico" ))  
        if os.path.isfile(iconPathName):  
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE  
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)  
        else:  
            print ("Can't find a Python icon file - using default")  
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)  
  
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP  
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "network")  
        try:  
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)  
        except win32gui.error:  
            # This is common when windows is starting, and this code is hit  
            # before the taskbar has been created.  
            print ("Failed to add the taskbar icon - is explorer running?")  
            # but keep running anyway - when explorer starts, we get the  
            # TaskbarCreated message.  
  
    def OnRestart(self, hwnd, msg, wparam, lparam):  
        self._DoCreateIcons()  
  
    def OnDestroy(self, hwnd, msg, wparam, lparam):  
        nid = (self.hwnd, 0)  
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)  
        win32gui.PostQuitMessage(0) # Terminate the app.  
  
    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):  
        if lparam==win32con.WM_LBUTTONUP:  
            print ("You clicked me.")  
        elif lparam==win32con.WM_LBUTTONDBLCLK:  
            print ("You double-clicked me - goodbye")  
            win32gui.DestroyWindow(self.hwnd)  
        elif lparam==win32con.WM_RBUTTONUP:  
            print ("You right clicked me.")  
            menu = win32gui.CreatePopupMenu()
            global run_flag
            if run_flag == 1:
                flags = win32con.MF_STRING | win32con.MF_CHECKED
            else:
                flags = win32con.MF_STRING | win32con.MF_UNCHECKED
            win32gui.AppendMenu( menu, flags, 1023, "Running(60s)")   
            win32gui.AppendMenu( menu, win32con.MF_STRING, 1025, "Exit program")  
            pos = win32gui.GetCursorPos()  
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp  
            win32gui.SetForegroundWindow(self.hwnd)  
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)  
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)  
        return 1  
  
    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)  
        if id == 1023:
            global run_flag
            run_flag = 1 - run_flag
        elif id == 1025:  
            print ("Goodbye")  
            win32gui.DestroyWindow(self.hwnd)
            sys.exit()
        else:  
            print ("Unknown command -", id)
			
#--------------------to do----------------------
class to_do(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        ONLINE = 1
        OFFLINE = 0
        while(1):
            request = requests.get('http://www.baidu.com').content
            soup = BeautifulSoup(request, 'html.parser')
            is_online = soup.find('html')
            if is_online == None:
               flag_online = OFFLINE
            else:
                flag_online = ONLINE
            print(flag_online)
            if flag_online == OFFLINE:
                #id = input('学号：')
                #passwd = input('密码：')
                #if id == '':
                id = 'xxxxxxxxxxxxxxx'
                #if passwd == '':
                passwd = 'xxxxxx'
                userid = '%E7%A7%91%5C' + id
                #print(userid)
                #print(passwd)
                header = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                post_data = {'userId':userid, 'password':passwd, 'queryString':'wlanuserip%3D0bc386d9e643d188b011a0d00c9b5c40%26wlanacname%3D5fcbc245a7ffdfa4%26ssid%3D%26nasip%3D2c0716b583c8ac3cbd7567a84cfde5a8%26mac%3D53ba540bde596b811a6d5617a86fa028%26t%3Dwireless-v2%26url%3D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30',\
                             'passwordEncrypt':'false'}
                requests.post('http://210.77.16.21/eportal/InterFace.do?method=login', data = post_data, headers = header)
                time.sleep(2)
                r2 = requests.get('http://www.baidu.com').content
                soup2 = BeautifulSoup(r2, 'html.parser')
                is_online = soup2.find('html')
                if is_online == None:
                    flag_online = OFFLINE
                else:
                    flag_online = ONLINE
                    print(flag_online)
            global run_flag
            if flag_online == OFFLINE and run_flag == 1:
                delay = 60
            else:
                delay = 7200
            time.sleep(delay)

class wnd(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        w=MainWindow()
        win32gui.PumpMessages()

if __name__ == '__main__':
    thread_login = to_do()
    thread_wnd = wnd()
    thread_login.start()
    thread_wnd.start()
    thread_login.join()
    thread_wnd.join()
