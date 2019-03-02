from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str
from subprocess import Popen, PIPE

import time
import sys
import enum
import socket
from threading  import Thread





import sys
import os
from Tools.scripts.pdeps import inverse
from asyncio.tasks import sleep


class ListenerThread:

    def __init__(self,win):
        self.win=win
        self.outThread = None
        self.conn=None
        self.addr=None
        self.nick='user'
        self.passw=''

        
    def start(self, addr,nick,passw):
        self.addr=addr
        self.nick=nick
        self.passw=passw
        self.outThread = Thread(target=self.out_handler_thread, args=(self,))
        self.outThread.start()

    def close(self):
        if self.conn:self.conn.close()
        self.conn=None
        if self.outThread: 
            self.outThread.join(1)

    def send(self,sstr):
        print("SEND:",sstr)
        if self.conn: self.conn.send(sstr.encode("utf-8"))

    def out_handler_thread(self,p):
        print("out_handler_thread starts...")
        nick=self.nick
        registered=False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.addr)
            self.connected=True
            self.conn=s
            try:
                while True:
                    print("read data: ")
                    alldata = self.conn.recv(4096).decode("utf-8").strip()
                    if not alldata:
                        break
                    for data in alldata.splitlines():
                        print(data)
                        z=b''
                        if data.startswith('PING') and ':' in data:
                            self.send('PONG :%s\r\n'%(data.split(':')[1]))
                        elif registered and 'JOIN' in data and '#' in data and data.count(':')==1:
                            h1,h2=data.split(':',maxsplit=2)
                            z=str2zx( '\n<%s> joins %s'%( h2.split("!")[0],h2.split('#')[1]  ) , inverse=True  )
                        elif registered and 'PART' in data and '#' in data and data.count(':')==1:
                            h1,h2=data.split(':',maxsplit=2)
                            z=str2zx( '\n<%s> has left %s'%( h2.split("!")[0],h2.split('#')[1]  ) , inverse=True  )
                        elif registered and 'MODE' in data and '#' in data and data.count(':')==1:
                            pass # ignore
                        elif data.count(':')>=2:
                            h1,h2,txt=data.split(':',maxsplit=2)
                            if "433" in h2: # already in use
                                nick+='ette'
                                registered=False
                            #if 'NOTICE' in h2 and  'No Ident response' in txt:
                            #    registered=False
                            if "001" in h2: # welcome
                                registered=True
                            if not registered:
                                if self.passw: self.send('PASS %s\r\n'%self.passw)
                                self.send('NICK %s\r\n'%nick)
                                self.send('USER %s * * : %s\r\n'%(nick,nick)  )
                                registered=True
                            if registered:
                                if '!' in h2: 
                                    z=str2zx( '\n<%s> %s'%( h2.split("!")[0],txt.strip()  )   )
                                else:
                                    z=str2zx( '\n>> %s'%( txt.strip()  )   )
                            else:
                                z=str2zx('\n'+data+'\n')
                        elif data.count(':')==1:
                            h1,h2=data.split(':')
                            z=str2zx('\n'+h2+'\n')
                        for c in z:
                            self.win.prtchar(c)
                        time.sleep(0.05)
            except:
                print ("Unexpected error:", sys.exc_info()[0])
            finally:
                self.connected=False
                self.conn=None
                
        print("Shell Out")



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
    
    def clear(self,startval=None):
        self.val=startval if startval else b''
        self.cursorpos=len(self.val)
        self.disppos=0
        self.hist_pos=-1
        if not self.done:
            self.show()
    
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
    MENU = enum.auto()
    INP_SRV = enum.auto()
    INP_NICK = enum.auto()
    INP_PORT = enum.auto()
    INP_PWORD = enum.auto()
    ONLINE = enum.auto()

class IrcClient:
    
    def __init__(self,mgr):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,32,20,0,0)
        self.inp_win=TextWindow(mgr,30,2,1,21,border=WindowBorderFrame(),kb_event=self.kb_event, cursor_off=True)
        self.revent=mgr.schedule_event(self.periodic,0.5,0.5)
        self.ed=None
        self.nick='zx-user' 
        self.server="irc.freenode.net"
        self.pword=''
        self.port=6667
        self.inp_mode=InpMode.MENU
        self.listener=ListenerThread(self.mainwin)
        self.choose_site()
        self.revent=mgr.schedule_event(self.periodic,2,2)
        self.channel=''

    def periodic(self):
        if self.inp_mode==InpMode.ONLINE and self.listener.self.conn:
            self.mainwin.prttxt(str2zx('\n\nDISCONNECT\n\n',upper_inv=True ))
            self.disconnect()
        
    def choose_site(self):
        self.mainwin.cls()
        self.mainwin.prttxt(str2zx('\n\n',upper_inv=True ))
        self.mainwin.prttxt(str2zx('       ZXPI IRC CHAT CLIENT     ',inverse=True ))
        self.mainwin.prttxt(str2zx('\n\n N >nick   (%s)'%(self.nick),upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n S >server (%s)'%(self.server),upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n P >port   (%d)'%(self.port),upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n W >password (%s)'%('*'*len(self.pword) if len(self.pword) else 'none'),upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n C connect \n\n\n X exit\n\n',upper_inv=True ))
        self.inp_win.cls()
        self.inp_win.prttxt(str2zx('please select'))
        
    def connect(self):
        self.revent.reschedule(3.0,1.0) # give 3 sec for connect
        self.listener.start(  (self.server,self.port),self.nick,self.pword  )
        self.inp_mode=InpMode.ONLINE
        self.mainwin.cls()
        self.mainwin.prttxt(str2zx('\n\nCONNECT to %s..\n\n'%(self.server),upper_inv=True )) 
               
    def disconnect(self):
        self.listener.close()
        self.inp_mode=InpMode.MENU
        
    def periodic(self):
        pass#self.event.wait(timeout=0.1)

    def close(self):
        self.disconnect()
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
            elif char==60: # W
                self.inp_win.cls()
                self.inp_win.prttxt(str2zx(' please enter pass word: ',inverse=True ))
                self.ed=LinEd(self.inp_win,0,1,29,255)
                self.inp_mode=InpMode.INP_PWORD
            elif char==51: # N
                self.inp_win.cls()
                self.inp_win.prttxt(str2zx(' please enter nickname: ',inverse=True ))
                self.ed=LinEd(self.inp_win,0,1,29,255,bytes(str2zx(self.nick)))
                self.inp_mode=InpMode.INP_NICK
            elif char==40: # C
                self.inp_win.cls()
                self.inp_win.prttxt(str2zx('   /join /part /quit /help',inverse=False ))
                self.ed=LinEd(self.inp_win,0,1,29,255)
                self.connect()
            elif char==61 or char==117: # x or break            
                self.close()
                app.clear()
                # TODO clear threads 
        elif self.inp_mode in (InpMode.INP_SRV,InpMode.INP_PORT,InpMode.INP_PWORD,InpMode.INP_NICK):
            if char in (117,118): # enter,break 
                if char==118: # enter
                    if self.inp_mode==InpMode.INP_SRV:
                        if self.ed.val.strip(): self.server=zx2str(self.ed.val,to_lower=True)
                    if self.inp_mode==InpMode.INP_NICK:
                        if self.ed.val.strip(): self.nick=zx2str(self.ed.val,to_lower=True)
                    elif self.inp_mode==InpMode.INP_PWORD:
                        self.pword=zx2str(self.ed.val,to_lower=True)
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
        elif self.inp_mode==InpMode.ONLINE:
            if char==118: # enter
                s=zx2str(self.ed.val, to_lower=True).strip()
                self.ed.clear()
                if s.startswith("/q"):
                    self.listener.send('QUIT :bye\r\n'  )
                    time.sleep(0.1)
                    self.disconnect()
                    self.ed.close()
                    self.ed=None
                    self.inp_mode=InpMode.MENU
                    self.choose_site()
                elif s.startswith("/join ") and len(s.split())==2:
                    self.channel='#'+s.split()[1]
                    self.listener.send('JOIN %s\r\n'%(self.channel)  )
                elif s.startswith("/part") and self.channel:
                    self.listener.send('PART %s\r\n'%(self.channel)  )
                    self.channel=''
                elif s.startswith("/list"):
                    self.listener.send('LIST\r\n' )
                elif s.startswith("/names"):
                    self.listener.send('NAMES %s\r\n'%(self.channel)  )
                elif s.startswith("/h"):
                    z=str2zx( '\n\n HELP on the irc client usage \n\n'  ,inverse=True )
                    z+=str2zx( '\n/JOIN <mychannel>  join channel\n      (just omit the hash tag)\n'  ,upper_inv=True )
                    z+=str2zx( '\n/PART   leave the channel\n'  ,upper_inv=True )
                    z+=str2zx( '\n/NAMES  show who is there\n'  ,upper_inv=True )
                    z+=str2zx( '\n/LIST   list all channels\n'  ,upper_inv=True )
                    z+=str2zx( '\n/QUIT   exit from server\n'  ,upper_inv=True )
                    z+=str2zx( '\notherwise, just type a message to the channel you joined\n'  ,upper_inv=True )
                    z+=str2zx( '\n        have fun       '  ,inverse=True )
                    self.mainwin.prttxt(z)
                elif s.startswith("/"):
                    z=str2zx( '\n??? unknown cmd %s'%(  s.strip()  )   )
                    self.mainwin.prttxt(z)
                else :
                    self.listener.send('PRIVMSG %s :%s\r\n'%(self.channel,s)  )
                    z=str2zx( '\n<%s> %s'%( self.nick,s.strip()  )   )
                    self.mainwin.prttxt(z)
            else:
                self.ed.kb_event(char)
            

app=[]


def start(mgr):
    app.append(IrcClient(mgr))

