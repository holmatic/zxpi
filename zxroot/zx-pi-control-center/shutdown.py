from zx_app_host import TextWindow, WindowBorderFrameShadow, str2zx, zx2str
    

import subprocess

import platform
import time
import sys
from threading  import Thread





import sys
import os






class Shutdown:
    
    def __init__(self,mgr):
        self.mrg=mgr
        self.mainwin=TextWindow(mgr,18,12,6,5,border=WindowBorderFrameShadow(),kb_event=self.kb_event, cursor_off=True)
        self.print_help()

    def print_help(self):
        self.mainwin.prttxt(str2zx('\n',upper_inv=True ))
        self.mainwin.prttxt(str2zx('  ZXPI SHUTDOWN   \n',inverse=True ))
        self.mainwin.prttxt(str2zx('\n\n S shut down pi \n\n X return + go on\n',upper_inv=True ))
        
    def close(self):
        self.mainwin.close()
        
    
    def kb_event(self,win,zxchar):
        s=zx2str( [zxchar] )
        if s in 'sS' or zxchar==12:
            if "Linux" in platform.system():
                self.mainwin.cls()
                self.mainwin.prttxt(str2zx('\nshutdown initiated\n\n    good bye.',upper_inv=True ))
                self.mrg.update(wait_till_sync_done=True)
                subprocess.run(["sudo","shutdown", "-h", "0"]) # sudo is reqired if the process was started via /etc/rc.local
            else:
                self.mainwin.prttxt(str2zx('\nshutdown not supported on %s host.'%( platform.system() ),upper_inv=False ))
        elif s in 'xX':
                self.close()
                app.clear()
                return
        elif s in 'uU':
            if self.proc is None:
                self.start()
        else:
            self.mainwin.cls()
            self.print_help()

app=[]


def start(mgr):
    app.append(Shutdown(mgr))

