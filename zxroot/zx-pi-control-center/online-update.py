from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str
from subprocess import Popen, PIPE

import time
import sys
from threading  import Thread





import sys
import os






class Updater:
    
    def __init__(self,mgr):
        self.mainwin=TextWindow(mgr,30,22,1,1,border=WindowBorderFrame(),kb_event=self.kb_event, cursor_off=True)
        self.print_help()
        #run('cmd',shell=True,stdout=self,stderr=self,stdin=self)
        #self.proc = Popen(['python','C:\\Users\\Holmatic\\workspace\\serial\\src\\apps\\file_browser.py'],shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.proc = None
        self.revent=mgr.schedule_event(self.periodic,0.5,0.5)
        self.outThread = None
        self.errThread = None

    def print_help(self):
        self.mainwin.prttxt(str2zx('\n\n',upper_inv=True ))
        self.mainwin.prttxt(str2zx('      ZXPI ONLINE UPDATER     ',inverse=True ))
        self.mainwin.prttxt(str2zx('\n\n U start update \n\n X exit\n\n',upper_inv=True ))
        
    # todo exit
    def start(self):
        self.mainwin.cls()
        self.mainwin.prttxt(str2zx('\nstart update attempt...\n',upper_inv=True ))
        self.proc = Popen( ['git','pull','origin','master']  ,shell=False,stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.outThread = Thread(target=self.out_handler_thread, args=(self.proc.stdout,))
        self.errThread = Thread(target=self.out_handler_thread, args=(self.proc.stderr,))
        self.outThread.start()
        self.errThread.start()

    def end_cleanup(self):
        if self.proc is not None:
            if self.proc.poll() is not None:
                self.proc=None # done
        if self.proc is None:
            if self.outThread != None:
                self.outThread.join(3)
                self.outThread = None
            if self.errThread != None:
                self.errThread.join(3)
                self.errThread = None
        
    def close(self):
        self.mainwin.close()
        
    def out_handler_thread(self,p):
        print("out_handler_thread starts...")
        #self.event.set()
        try:
            while True:
                # print("read data: ")
                data = p.read(1)#.decode("utf-8")
                if not data:
                    break
                z=str2zx(data)
                sys.stdout.write(data)
                sys.stdout.flush()
                for c in z:
                    self.mainwin.prtchar(c)
        finally:
            print("Shell Out")
        
    def periodic(self):
        if self.proc is not None:
            # ongoing, see if done
            if self.proc.poll() is not None:
                self.end_cleanup()
                self.print_help()
                
        
        pass#self.event.wait(timeout=0.1)

    
    def kb_event(self,win,zxchar):
        s=zx2str( [zxchar] )
        if s in 'xX' or zxchar==12:
            if self.proc:
                self.proc.terminate()
            else:
                self.close()
                self.active=False
                self.mainwin.close()
                self.revent.remove()
                app.clear()
                return
        elif s in 'uU':
            if self.proc is None:
                self.start()

app=[]


def start(mgr):
    app.append(Updater(mgr))

