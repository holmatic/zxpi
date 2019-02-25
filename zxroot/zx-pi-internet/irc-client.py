from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str
from subprocess import Popen, PIPE

import time
import sys
import enum
from threading  import Thread





import sys
import os


class ListenerThread:

    def __init__(self,win):
        self.win=win
        self.outThread = None
        self.errThread = None
        
        
    def start(self):
        self.outThread = Thread(target=self.out_handler_thread, args=(self.proc.stdout,))
        self.errThread = Thread(target=self.out_handler_thread, args=(self.proc.stderr,))
        self.outThread.start()
        self.errThread.start()


class LinEd:
    
    def __init__(self,win,xpos,ypos,width,maxchar=255,startval=None,history=None):
        self.win=win
        self.xpos=xpos
        self.ypos=ypos
        self.maxchar=maxchar
        self.width=width
        self.val=startval if startval else b''
        self.cursorpos=len(self.val)
        self.disppos=0
        self.history=history
        self.hist_pos=-1
        self.show()
        self.done=False
    
    def show(self, cursor_shown=True):
        dstr=self.val[self.disppos:]
        if cursor_shown:
            dstr=dstr[:self.cursorpos-self.disppos]+bytes([8])+dstr[self.cursorpos-self.disppos:]
        dstr=dstr[:self.width]
        if len(dstr)<self.width:dstr+=bytes(self.width-len(dstr))
        self.win.set_prtpos(self.xpos,self.ypos)
        self.win.prttxt(dstr)
    
    def kb_event(self,char):
        if char&0x40:   
            # special character or work
            if char==118:
                self.done=True
                if self.history:self.history.append(self.val)
            elif char==119: # del
                if self.cursorpos>0:
                    self.cursorpos-=1
                    self.val=self.val[:self.cursorpos]+self.val[self.cursorpos+1:]
                    self.disppos=min(self.disppos,self.cursorpos)
            elif char==114: # left
                if self.cursorpos>0:
                    self.cursorpos-=1
                    self.disppos=min(self.disppos,self.cursorpos)
            elif char==115: # right
                if self.cursorpos<len(self.val):
                    self.cursorpos+=1
                    self.disppos=max(self.disppos,self.cursorpos+1-self.width)
            elif char==112: # up
                if self.history:
                    if self.hist_pos+1<len(self.history):
                        self.hist_pos+=1
                        self.disppos=0
                        self.val=self.history[self.hist_pos]
                        self.cursorpos=min(len(self.val),self.width-1)
            elif char==113: # down
                if self.history:
                    if self.hist_pos>=1:
                        self.hist_pos-=1
                        self.val=self.history[self.hist_pos]
                    else:
                        self.hist_pos=-1
                        self.val=b''
                    self.disppos=0
                    self.cursorpos=min(len(self.val),self.width-1)
                pass
        else: 
            if len(self.val)<self.maxchar:
                self.val=self.val[:self.cursorpos]+bytes([char])+self.val[self.cursorpos:]
                self.cursorpos+=1
                self.disppos=max(self.disppos,self.cursorpos+1-self.width)
        self.show()
    
    def close(self):
        self.done=True


class InpMode(enum.Enum):
    MENU=0
    INP_SRV=1
    INP_PORT=2
    ONLINE=3

class IrcClient:
    
    def __init__(self,mgr):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,32,20,0,0)
        self.inp_win=TextWindow(mgr,30,2,1,21,border=WindowBorderFrame(),kb_event=self.kb_event, cursor_off=True)
        self.revent=mgr.schedule_event(self.periodic,0.5,0.5)
        self.ed=None
        self.server="irc.freenode.net"
        self.port=6667
        self.inp_mode=InpMode.MENU
        self.choose_site()
        
    def choose_site(self):
        self.mainwin.cls()
        self.mainwin.prttxt(str2zx('\n\n',upper_inv=True ))
        self.mainwin.prttxt(str2zx('       ZXPI IRC CHAT CLIENT     ',inverse=True ))
        self.mainwin.prttxt(str2zx('\n\n S >server (%s)'%(self.server),upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n P >port (%d)'%(self.port),upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n C connect \n\n\n X exit\n\n',upper_inv=True ))
        self.inp_win.cls()
        self.inp_win.prttxt(str2zx('please select'))
        
    def periodic(self):
        pass#self.event.wait(timeout=0.1)

    def close(self):
        if self.ed: self.ed.close()
        self.mainwin.close()
        self.inp_win.close()
    
    def kb_event(self,win,char):
        if self.inp_mode==InpMode.MENU:
            if char==56: # S
                self.inp_win.cls()
                self.inp_win.prttxt(str2zx(' please enter server address: ',inverse=True ))
                self.ed=LinEd(self.inp_win,0,1,29,255,bytes(str2zx(self.server)) )
                self.inp_mode=InpMode.INP_SRV
            elif char==53: # P
                self.inp_win.cls()
                self.inp_win.prttxt(str2zx(' please enter port number: ',inverse=True ))
                self.ed=LinEd(self.inp_win,0,1,6,5,bytes(str2zx(str(self.port))) )
                self.inp_mode=InpMode.INP_PORT
            elif char==61 or char==117: # x or break            
                self.close()
                app.clear()
                # TODO clear threads 
        elif self.inp_mode in (InpMode.INP_SRV,InpMode.INP_PORT):
            if char in (117,118): # enter,break 
                if char==118 and self.ed.val.strip(): # enter
                    if self.inp_mode==InpMode.INP_SRV:
                        self.server=zx2str(self.ed.val,to_lower=True)
                    else:
                        try:
                            self.port=int(zx2str(self.ed.val))
                        except: pass
                self.ed.close()
                self.ed=None
                self.inp_mode=InpMode.MENU
                self.choose_site()
            else:
                self.ed.kb_event(char)
 

app=[]


def start(mgr):
    app.append(IrcClient(mgr))

