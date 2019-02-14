from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str
from subprocess import Popen, PIPE

import time
import sys
from threading  import Thread





import sys
import os






class AppShell:
    
    def __init__(self,mgr):
        self.mainwin=TextWindow(mgr,30,22,1,1,border=WindowBorderFrame(),kb_event=self.kb_event)
        #run('cmd',shell=True,stdout=self,stderr=self,stdin=self)
        #self.proc = Popen(['python','C:\\Users\\Holmatic\\workspace\\serial\\src\\apps\\file_browser.py'],shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.proc = Popen('cmd',shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.revent=mgr.schedule_event(self.periodic,0.5,0.5)
        print("AppShell starts...")
        self.outThread = Thread(target=self.out_handler_thread, args=(self.proc.stdout,))
        self.errThread = Thread(target=self.out_handler_thread, args=(self.proc.stderr,))
        self.outThread.start()
        self.errThread.start()
        
    # todo exit
        
    def out_handler_thread(self,p):
        print("out_handler_thread starts...")
        #self.event.set()
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
        print("Shell Out")
        
    def periodic(self):
        pass#self.event.wait(timeout=0.1)

    
    def kb_event(self,win,char):
        if char==12:
            self.mainwin.close()
            app.clear()
            # TODO clear threads 
        else:
            win.prtchar(char)
            s=zx2str( [char] )
            #if s=='\n': s='\r\n'
            self.proc.stdin.write(s)
            self.proc.stdin.flush()


app=[]

print("HelloWorld Import n2")
def start(mgr):
    print("HelloWorld Start n")
    gurgel()
    app.append(AppShell(mgr))

