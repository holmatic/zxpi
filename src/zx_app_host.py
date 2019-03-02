'''
Created on 30.12.2018

@author: Holmatic
'''


import time
import zx_ser_srv



KEYPATTERN_NO_KEY=0xFFFF
KEYPATTERN_SHIFT_ONLY=0xFEFF

KB_PATTERN_2_ASCII={
    0xFDFD:'A',
    0xDF7F:'B',
    0xEFFE:'C',
    0xF7FD:'D',
    0xF7FB:'E',
    0xEFFD:'F',
    0xDFFD:'G',
    0xDFBF:'H',
    0xF7DF:'I',
    0xEFBF:'J',
    0xF7BF:'K',
    0xFBBF:'L',
    0xF77F:'M',
    0xEF7F:'N',
    0xFBDF:'O',
    0xFDDF:'P',
    0xFDFB:'Q',
    0xEFFB:'R',
    0xFBFD:'S',
    0xDFFB:'T',
    0xEFDF:'U',
    0xDFFE:'V',
    0xFBFB:'W',
    0xF7FE:'X',
    0xDFDF:'Y',
    0xFBFE:'Z',
    0xFD7F:' ',
    0xFB7F:'.',
    0xFDBF:'\n',

    0xFDF7:'1',
    0xFBF7:'2',
    0xF7F7:'3',
    0xEFF7:'4',
    0xDFF7:'5',
    0xDFEF:'6',
    0xEFEF:'7',
    0xF7EF:'8',
    0xFBEF:'9',
    0xFDEF:'0',
    
    0xFAFE:':',
    0xF6FE:';',
    0xEEFE:'?',
    0xDEFE:'/',
    0xDE7F:'*',
    0xEE7F:'<',
    0xF67F:'>',
    0xFA7F:',',
    0xFC7F:'@',# pound
    
    0xFABF:'=',
    0xF6BF:'+',
    0xEEBF:'-',
    0xFCDF:'"',
    0xFADF:')',
    0xF6DF:'(',
    0xEEDF:'$',
    0xFCFD:'#', # graph A
    0xF6FB:'[', # graph E
    0xEEFB:']', # graph R
    0xDEFB:'{', # graph T
    0xDEDF:'}', # graph Y
    0xF6FD:'_', # graph D

    
    }

KB_PATTERN_2_ZXBYTE={
    0xFDFD:38,
    0xDF7F:39,
    0xEFFE:40,
    0xF7FD:41,
    0xF7FB:42,
    0xEFFD:43,
    0xDFFD:44,
    0xDFBF:45,
    0xF7DF:46,
    0xEFBF:47,
    0xF7BF:48,
    0xFBBF:49,
    0xF77F:50,
    0xEF7F:51,
    0xFBDF:52,
    0xFDDF:53,
    0xFDFB:54,
    0xEFFB:55,
    0xFBFD:56,
    0xDFFB:57,
    0xEFDF:58,
    0xDFFE:59,
    0xFBFB:60,
    0xF7FE:61,
    0xDFDF:62,
    0xFBFE:63,
    0xFD7F:0,
    0xFB7F:27,
    0xFDBF:118,
    0xFDF7:29,
    0xFBF7:30,
    0xF7F7:31,
    0xEFF7:32,
    0xDFF7:33,
    0xDFEF:34,
    0xEFEF:35,
    0xF7EF:36,
    0xFBEF:37,
    0xFDEF:28,# 0

    0xFAFE:14,#':',
    0xF6FE:25,#';',
    0xEEFE:15,#'?',
    0xDEFE:24,#'/',
    0xDE7F:23,#'*',
    0xEE7F:19,#'<',
    0xF67F:18,#'>',
    0xFA7F:26,#',',
    0xFC7F:12,#'@',# pound
    
    0xFABF:20,#'=',
    0xF6BF:21,#'+',
    0xEEBF:22,#'-',
    0xFCDF:11,#'"',
    0xFADF:17,#')',
    0xF6DF:16,#'(',
    0xEEDF:13,#'$',
    0xFCFD:8,#'#', # graph A
    0xF6FB:7,#'[', # graph E
    0xEEFB:132,#']', # graph R
    0xDEFB:6,#'{', # graph T
    0xDEDF:134,#'}', # graph Y
    0xF6FD:9,#'_', # graph D
    0xDEBF:136,#'}', # graph H


    0xFCEF:119,# rubout
    0xEEEF:112,# up
    0xDEEF:113,# down
    0xDEF7:114,# left
    0xF6EF:115,# right
        
    }


"""
    defw $C4    ; A uml        81
    defw $D6    ; O uml
    defw $DC    ; U uml

    defw $DF    ; sz        84
    defw $E4    ; a uml        85
    defw $F6    ; o uml
    defw $FC    ; u uml     87

    defw $20AC    ; euro
    defw $A3    ; pound                    89
    defw $2580    ; Upper half - G-7   8a
    defw $2584    ; Lower half - G-6

    defw $2588    ; Full Block - G-FGH 8c
    defw $258C    ; Left half - G-5
    defw $2590    ; Right half - G-8     8e
    defw $2596    ; lole - G-4 8f


    defw $2597    ; lori - G-3   90
    defw $2598    ; uple - G-1
    defw $2599    ; L   - G-w
    defw $259a    ; *, - G-y

    defw $259b    ;  - G-e
    defw $259c    ;  - G-r
    defw $259d    ;  - G-2
    defw $259e    ;  - G-t

    defw $259f    ;  - G-q    98
    defw $25b2    ;  - up     99
    defw $25bc    ;  - dn
    defw $25c0    ;  - le

    defw $25b6    ;  - re
    defw $2592     ;  - half gray
    defw $25D6    ;   (|
    defw $25D7    ;   |)            9a

    defw $1E9E    ; Upper case SZ    A0
"""
unicode2zx_tbl={}
zxcode2uni_tbl={}



for zxcode,unicode in enumerate(""" \u2598\u259d\u2580\u2596\u258c\u259e\u259b\u2592_~"\u00a3$:?()><=+-*/;,.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"""):
    uni_lo=unicode.lower()
    if unicode not in unicode2zx_tbl: unicode2zx_tbl[unicode]=zxcode
    if uni_lo not in unicode2zx_tbl: unicode2zx_tbl[uni_lo]=zxcode
    zxcode2uni_tbl[zxcode]=unicode
    zxcode2uni_tbl[zxcode+128]=uni_lo

# add inverse graphics
for zxcode,unicode in enumerate("""\u2588\u259f\u2599\u2584\u259c\u2590\u259a\u259b\u2592!#"""):
    if unicode not in unicode2zx_tbl: unicode2zx_tbl[unicode]=zxcode+128
    zxcode2uni_tbl[zxcode+128]=unicode # override

unicode2zx_tbl['@']=166 #inverse A
unicode2zx_tbl['\n']=118
unicode2zx_tbl['\b']=119
unicode2zx_tbl['\\']=134

zxcode2uni_tbl[118]='\n'
zxcode2uni_tbl[119]='\b'

def str2zx(s, inverse=False, upper_inv=False):
    zx=[   unicode2zx_tbl.get(c,4) | (128 if c not in '\n\r' and (inverse or (upper_inv and c.isupper())) else 0)  for c in s]
    return zx

def zx2str(zx, to_lower=False):
    if to_lower:
        s=''.join([ zxcode2uni_tbl.get(c,'*').lower() for c in zx])
    else:
        s=''.join([ zxcode2uni_tbl.get(c,'*') for c in zx])
    return s


class ZxKeyboardScan:
    def __init__(self):
        self.last_key_pattern=KEYPATTERN_NO_KEY
        self.last_change_time=0.0
        self.repeat_time=None
        self.kbuf=bytearray()
        
    def read_kbf(self):
        if len(self.kbuf)>=1:
            rval=self.kbuf[0]
            self.kbuf=self.kbuf[1:]
            return rval
        else:
            return None

    def handle_key_pattern(self, pattern):
        if pattern!=self.last_key_pattern or (pattern not in (KEYPATTERN_SHIFT_ONLY,KEYPATTERN_NO_KEY) and self.repeat_time and time.time()>self.repeat_time ):
            t=time.time()
            if t>self.last_change_time+0.1:
                if pattern not in (KEYPATTERN_SHIFT_ONLY,KEYPATTERN_NO_KEY):
                    #print( "New key %X"%(pattern) )
                    if pattern in KB_PATTERN_2_ZXBYTE:
                        self.last_change_time=t
                        self.kbuf.append(KB_PATTERN_2_ZXBYTE[pattern])
                        if self.repeat_time is None:
                            self.repeat_time=t+0.8
                        else:
                            self.repeat_time+=0.1
                    else: print("Key %X not found"%(pattern))
                else:
                    self.repeat_time=None
                    #print( "Release key" )
                self.last_key_pattern=pattern
                
                
NUM_COL=32                
NUM_LINES=24#24
NUM_Z_POS=8 # currently a byte for depth bitmask

ZXCHAR_BLANK=0
ZXCHAR_INV_FLG=128
ZXCHAR_NEWLINE=118
ZXCHAR_RUBOUT=119   # use for transparent fields



class ScheduledEvent():
    
    def __init__(self,mgr,evt,delay_s,period_s=None):
        self.mgr=mgr
        self.evt=evt
        self.delay_s=delay_s
        self.period_s=period_s
        self.trigger_t=time.time()+delay_s
    
    def reschedule(self,delay_s,period_s=None):
        self.trigger_t=time.time()+delay_s
        self.period_s=period_s
        if self not in self.mgr.periodic_tasks:
            self.mgr.periodic_tasks.append(self)
        self.mgr.periodic_tasks.sort()
    
    def remove(self):
        if self in self.mgr.periodic_tasks:
            self.mgr.periodic_tasks.remove(self)
    
    def __del__(self):
        self.remove()
    
    def check_trigger(self):
        if time.time()>self.trigger_t:
            if self.period_s:
                self.trigger_t=time.time()+self.period_s
                self.mgr.periodic_tasks.sort()
            else:
                self.mgr.periodic_tasks.remove(self)
            self.evt()    
            return True
        else:
            return False

    def __lt__(self,other):
        return self.trigger_t < other.trigger_t


class ZxAppHost():
    
    def __init__(self, server):
        self.server=server
        self.screenaddr=None
        self.screenbuf=[ bytearray(NUM_COL) for _i in range(NUM_LINES) ]
        self.z_buffer=[ bytearray(NUM_COL) for _i in range(NUM_LINES) ] # a bit for every z pos
        self.curr_screen=[]
        self.invalidate_curr_screen()
        self.syncline=0
        self.kb_scan=ZxKeyboardScan()
        self.active_windows=[]  # last ones have highest prio
        self.periodic_tasks=[]
        self.kb_event_window=None
        self.dialogwin=None
        self.last_kb_read_t=time.time()

    def is_connected(self):
        return self.server.is_connected()

    def invalidate_curr_screen(self):
        scr = bytearray( [255 for _n in range(NUM_COL)] )
        self.curr_screen=[ scr[:] for _i in range(NUM_LINES) ]
        

    def schedule_event(self,evt,delay_s,period_s):
        se=ScheduledEvent(self,evt,delay_s,period_s)
        self.periodic_tasks.append( se )
        self.periodic_tasks.sort()
        return se
        
        
    def register_win(self,win):
        zpos=len(self.active_windows)
        self.active_windows.append(win)
        win.set_z_pos(zpos)
        for x in range(NUM_COL):
            for y in range(NUM_LINES):
                if win.screenbuf[y][x]!=ZXCHAR_RUBOUT:  # active area
                    self.z_buffer[y][x] |= win.z_priobit
                    win.setchar_raw(win.screenbuf[y][x],x,y)
        if win.border: win.border.draw(win)
        if win.kb_event: self.kb_event_window=win
        
        
    def unregister_win(self,win):
        if win in self.active_windows:
            ix=self.active_windows.index(win)
            for x in range(NUM_COL):
                for y in range(NUM_LINES):
                    if win.screenbuf[y][x]!=ZXCHAR_RUBOUT:  # active area
                        self.z_buffer[y][x] &= ~win.z_priobit
                        if 0 == self.z_buffer[y][x]: # no window left
                            self.screenbuf[y][x]=ZXCHAR_BLANK
                        elif  self.z_buffer[y][x] < win.z_priobit:    # need to redraw lower-prio window?
                            for i in range(ix-1,-1,-1): # down towards lowest prio
                                otherwin=self.active_windows[i]
                                if otherwin and (otherwin.z_priobit & self.z_buffer[y][x]):
                                    otherwin.setchar_raw(otherwin.screenbuf[y][x],x,y)
                                    break
            self.active_windows[ix]=None
            # clean up all removed windows at the end, may be multiple if not deleted in LIFO order
            while self.active_windows and self.active_windows[-1] is None:
                del self.active_windows[-1]
            if self.kb_event_window is win:
                self.kb_event_window=None
                # find new window to retrieve events
                for w in reversed(self.active_windows):
                    if w is not None and w.kb_event is not None:
                        self.kb_event_window=w # highest prio one will get the evernts now
                        break



    def cls(self):
        self.screenbuf=[ bytearray(NUM_COL) for _i in range(NUM_LINES) ]
        self.z_buffer=[ bytearray(NUM_COL) for _i in range(NUM_LINES) ] # a bit for every z pos

    def incremental_sync(self):
        if self.screenaddr:
            sl=self.syncline
            while sl<NUM_LINES: #24
                self.syncline+=1
                if self.screenbuf[sl] != self.curr_screen[sl]: # TODO use difflib here?s
                    t=self.screenbuf[sl][:] # we might have concurrent accesses if we use threads, copy to stay consistent
                    spos=None
                    lpos=0
                    for i,(s,c) in enumerate(zip(t,self.curr_screen[sl])):
                        if s!=c:
                            lpos=i
                            if spos is None: spos=i
                    #print("Sync",self.screenaddr+1+33*sl+spos,lpos)
                    self.server.cmd_multipoke(self.screenaddr+1+33*sl+spos, list(t[spos:lpos+1]) )
                    self.curr_screen[sl]=t
                    return False
                sl=self.syncline
            self.syncline=0
        return True

    def on_dfile_read(self,addr,data):
        print("DFILE screenaddr read",addr,data)
        self.screenaddr=data
        if NUM_LINES>23:
            print("DFILE extension")
            # on 1 k zeddy, we cannot load with full screen expanded. Need to expand last line manually, but thread-safe as we are in SLOW
            self.server.cmd_multipoke(self.screenaddr+1+33*23+32, [0x76,0x80] ) # new DFILE end VAR end first
            self.server.cmd_multipoke(self.screenaddr+1+33*23+1,  [4]*31 )
            self.server.cmd_multipoke(self.screenaddr+1+33*23+0,  [4,4] ) # override the DFILE end last

    def on_kbdata_read(self,_addr,data):
        #print("KBDAta read",addr,data)
        self.kb_scan.handle_key_pattern(data)
        kbin=self.kb_scan.read_kbf()
        if kbin is not None:
            print("Key",kbin)
            if self.kb_event_window and self.kb_event_window.kb_event:
                self.kb_event_window.kb_event(self.kb_event_window,kbin)
    
    def exec_inp_events(self):
        if self.server.pending_callbacks:
            evt,p1,p2=self.server.pending_callbacks[-1]
            del  self.server.pending_callbacks[-1]
            evt(p1,p2)  # this may trigger action leading to recursion
            return True
        else:
            return False

    def update(self,waittime=0.0,wait_till_sync_done=False):
        evtt=time.time()
        try:
            if self.screenaddr is None:
                self.server.request_peek_word(16396, self.on_dfile_read)
                self.server.flush_tx()
                self.screenaddr=False # mark that screenaddr requested but not yet retrieved 
            while True:
                if time.time()>self.last_kb_read_t+0.02:
                    self.server.request_peek_word(16421, self.on_kbdata_read)    
                    self.server.flush_tx()
                    self.last_kb_read_t=time.time()
                self.server.handle_input() # get all available input, may result in kb events
                if self.exec_inp_events(): 
                    pass # nothing more for this cycle
                elif self.periodic_tasks and self.periodic_tasks[0].check_trigger():
                    pass # nothing more for this cycle
                elif self.incremental_sync():
                    # sync done
                    if waittime>0:
                        time.sleep(0.01)
                    elif wait_till_sync_done:
                        self.server.flush_tx()
                        break
                # condition at end of loop, only one iteration if no waittime
                if time.time()>=evtt+waittime and not wait_till_sync_done: break
        except zx_ser_srv.SerNotConnected:
            if self.screenaddr is not None:
                self.invalidate_curr_screen()
                self.screenaddr=None
                self.kb_scan.kbuf.clear()
                self.kb_scan.last_key_pattern=KEYPATTERN_NO_KEY
            while True:
                self.server.handle_input()
                if time.time()>=evtt+waittime: break
                if self.periodic_tasks:
                    self.periodic_tasks[0].check_trigger()
                time.sleep(0.05)

    def show_msg_win(self, msg, kb_event=None):
        w=min(len(msg),24)
        h=1+len(msg)//24
        tw=TextWindow(self,w+3,h+4,14-w//2,8-h//2,border=WindowBorderFrameShadow(),kb_event=kb_event)
        tw.set_prtpos(1,1)
        tw.prttxt(msg)
        self.update(wait_till_sync_done=True)
        return tw

                
    def show_dialog(self, msg):
        if self.dialogwin is None:
            ret=[]

            self.dialogwin=self.show_msg_win(msg,kb_event=lambda _w,s: ret.append(s) )
            while not ret:
                self.update(0.1)
            print("Done")
            self.dialogwin.close()
            self.dialogwin=None
            


class WindowBorder():
    
    def __init__(self):
        pass
    
    def draw(self,win):
        pass


class WindowBorderFrame(WindowBorder):
    
    def __init__(self, title=None):
        WindowBorder.__init__(self)
        self.title=title
    
    def draw(self,win):
        win.setchar_raw(7,win.xpos-1, win.ypos-1)
        win.setchar_raw(132,win.xpos+win.xsize+0, win.ypos-1)
        win.setchar_raw(130,win.xpos-1, win.ypos+win.ysize+0)
        win.setchar_raw(129,win.xpos+win.xsize+0, win.ypos+win.ysize+0)
        for x in range(win.xpos, win.xpos+win.xsize):
            win.setchar_raw(3,x, win.ypos-1)
            win.setchar_raw(131,x, win.ypos+win.ysize+0)
        for y in range(win.ypos, win.ypos+win.ysize):
            win.setchar_raw(5,win.xpos-1, y)
            win.setchar_raw(133,win.xpos+win.xsize+0, y)
        if self.title:
            x=win.xpos
            if 1: # outside
                win.setchar_raw(133,x, win.ypos-2);x+=1
                for c in self.title:#(185,174,185,177,170):
                    win.setchar_raw(c|0x80,x, win.ypos-2);x+=1
                win.setchar_raw(5,x, win.ypos-2);x+=1
            else: # inside
                win.setchar_raw(128,x-1, win.ypos-1)
                win.setchar_raw(128,x, win.ypos-1);x+=1
                for c in self.title:#(185,174,185,177,170):
                    win.setchar_raw(c|0x80,x, win.ypos-1);x+=1
                win.setchar_raw(128,x, win.ypos-1);x+=1


class WindowBorderFrameShadow(WindowBorderFrame):
    
    def __init__(self, title=None):
        WindowBorderFrame.__init__(self, title=title)
    
    def draw(self,win):
        WindowBorderFrame.draw(self,win)
        for x in range(win.xpos, win.xpos+win.xsize+1):
            win.setchar_raw(8,x, win.ypos+win.ysize+1)
        for y in range(win.ypos, win.ypos+win.ysize+2):
            win.setchar_raw(8,win.xpos+win.xsize+1, y)

class TextWindow():


    def __init__(self, mgr,xsize,ysize,xpos,ypos,border=None,kb_event=None, cursor_off=False):
        self.mgr=mgr
        self.xsize=xsize
        self.ysize=ysize
        self.xpos=xpos
        self.ypos=ypos
        self.kb_event=kb_event
        self.border=border
        
        self.prpos_x=0
        self.prpos_y=0
        self.cursor_active=True if kb_event and not cursor_off else False
        self.z_priobit=0
        self.z_compare=-1
        self.screenbuf=[ bytearray([ZXCHAR_RUBOUT for _n in range(NUM_COL)]) for _i in range(NUM_LINES) ]
        # draw area
        for x in range(self.xpos, self.xpos+self.xsize):
            for y in range(self.ypos, self.ypos+self.ysize):
                self.screenbuf[y][x]=ZXCHAR_BLANK
        if self.border: self.border.draw(self)
        self.mgr.register_win(self)
        self.toggle_cursor()


    def __enter__(self):
        return self
         
    def __exit__(self, _type, _value, _traceback):    
        self.close()
        
    def close(self):
        if self.mgr:
            self.mgr.unregister_win(self)
            self.z_priobit=0  # deactivate
            self.z_compare=-1
            self.mgr=None


    def set_z_pos(self,pos):
        self.z_priobit=1<<pos
        self.z_compare=self.z_priobit*2-1

    def toggle_cursor(self): 
        if self.cursor_active:
            c=self.screenbuf[self.ypos+self.prpos_y][self.xpos+self.prpos_x]^0x80#,
            self.setchar_raw(c,self.xpos+self.prpos_x,self.ypos+self.prpos_y)

    def setchar_raw(self,char,x,y):
        self.screenbuf[y][x]=char
        if self.z_compare>=self.mgr.z_buffer[y][x]:
            self.mgr.screenbuf[y][x]=char


    def cls(self, char=ZXCHAR_BLANK):
        self.toggle_cursor()
        for x in range(self.xpos, self.xpos+self.xsize):
            for y in range(self.ypos, self.ypos+self.ysize):
                self.setchar_raw(char, x, y)
        self.prpos_x=0
        self.prpos_y=0
        self.toggle_cursor()
        
    def newline(self):
        self.prpos_x=0
        if self.prpos_y+1<self.ysize:
            self.prpos_y+=1
        else:
            #scroll
            for x in range(self.xpos, self.xpos+self.xsize):
                for y in range(self.ypos, self.ypos+self.ysize):
                    self.setchar_raw(self.screenbuf[y+1][x] if y+1<self.ypos+self.ysize else ZXCHAR_BLANK , x, y)
            
    def set_prtpos(self,x,y):
        self.toggle_cursor()
        self.prpos_x=x
        self.prpos_y=y
        self.toggle_cursor()
            
        
    def prtchar(self,char):
        self.toggle_cursor()
        if char&0x40:   
            # special character or work
            if char==118:
                self.newline()
            elif char==119:
                if self.prpos_x>0:
                    self.prpos_x-=1
                    self.setchar_raw(ZXCHAR_BLANK,self.xpos+self.prpos_x,self.ypos+self.prpos_y)
            elif char==114: # left
                if self.prpos_x>0:
                    self.prpos_x-=1
            elif char==115: # right
                if self.prpos_x+1<self.xsize:
                    self.prpos_x+=1
            elif char==112: # up
                if self.prpos_y>0:
                    self.prpos_y-=1
            elif char==113: # down
                if self.prpos_y+1<self.ysize:
                    self.prpos_y+=1
        else: 
            self.setchar_raw(char,self.xpos+self.prpos_x,self.ypos+self.prpos_y)
            if self.prpos_x+1<self.xsize:
                self.prpos_x+=1
            else:
                self.newline()
        self.toggle_cursor()    

    def prttxt(self,zxtext):
        for c in zxtext:
            self.prtchar(c)
        
            
        
        