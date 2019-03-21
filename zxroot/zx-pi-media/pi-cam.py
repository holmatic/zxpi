
from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str, ZXCHAR_BLANK, ZXCHAR_INV_FLG

import zxpi_paths

try:
    import picamera
    import picamera.array
    cam_available=True
except:
    cam_available=False

import numpy


import time
import pickle
import random
from enum import Enum

if not cam_available: # load dummy
    p= b'\x80\x02cnumpy.core.multiarray\n_reconstruct\nq\x00cnumpy\nndarray\nq\x01K\x00\x85q\x02c_codecs\nencode\nq\x03X\x01\x00\x00\x00bq\x04X\x06\x00\x00\x00latin1q\x05\x86q\x06Rq\x07\x87q\x08Rq\t(K\x01K0K@\x86q\ncnumpy\ndtype\nq\x0bX\x02\x00\x00\x00u1q\x0cK\x00K\x01\x87q\rRq\x0e(K\x03X\x01\x00\x00\x00|q\x0fNNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK\x00tq\x10b\x89h\x03X=\x0c\x00\x00ple]UNHCB?>====>?@ACDFHJJKMORTWYZ\\bfjnooopsu\xc2\x80vmf`\\ZXWUTSTUWX_cnrohaYRJDB@>>==<>??ABCEGIKMLNPRTWY\\_bejlpooqpr}ohb[WVSRONPRTVY[[]jhe^UMGB@?>>>===?@BCDFIKMNNPQSUXZ\\_dfhkmnnnosykc^XTRPNHGKRVYVOZYo^]ZPGC@?=====>?ABCDFHJLNOORSTVWY[_cfiiilkkmrsfa[UQNKFDCGRYYQPTgwJFDAB@>======?@ACDFGIKLNOPQRTUVW[]aeffhihhjskb]WRNHCAAABGOTY_p}u==<<=<<;;<<<>?@BDEGIKLMOPOPRSUVW[\\`abddeedgpd_ZTOFC@A?;=DLVk\xc2\x9d\xc3\x81\xc2\x93\xc2\x82:::::::;;;<=?@BCEGIJLNOQRQQQRTUWY\\]^aaabbcel_[VOJC@@><8=ENl\xc2\x9d\xc2\xb2\xc3\x8f\xc2\xb8\xc2\xa089889:9;;;=>@ACEGIJLMOPRSRRQRSUWY[\\\\]]^^__deZVPFDA@><98;EZ\xc2\x95\xc2\xb3\xc2\xbf\xc3\x94\xc3\xa3\xc3\x8477777899:;>?@BDEGIKMNPQRSTRQRSUVXYYZZZZZ[]d^WPIA@?;;<67COe\xc2\x92\xc2\xb7\xc3\xa2\xc3\xb5\xc3\xb9\xc3\xb15566679::<=>@BCEGIKLOQRRTUTRSTSTVWXXXXWWWZcXRIB>>;:::;>GUj\xc2\x88\xc3\x88\xc3\xba\xc3\xba\xc3\xba\xc3\xba5456689:;<>?@BDEGIKMPRSTUVUTTSSTTVWWWVUSTX_SLC>=<:868;BJWm\xc2\x95\xc3\x9a\xc3\xba\xc3\xba\xc3\xba\xc3\xba4456789:;<=?@BDEHJKMPRTUWXXVUSSTTUVVVSPQRV\\LD@:;9:988:BLZo\xc2\x8e\xc3\x85\xc3\xb8\xc3\xba\xc3\xba\xc3\xba4456788:;=>?ABDFHJLNQSTVWXYWUTSSTTUTROMMOUSEA<;778867:AJVf\x7f\xc2\xa0\xc3\x90'
    p+=b'\xc3\xb1\xc3\xb9\xc3\xba34567799<=?AACEFHJLPRTVVXY[YWUSSTSSQMLJKMTJA<;663047;AOcy\xc2\x8e\xc2\x9e\xc2\xbc\xc3\x83\xc3\x9d\xc3\xa5\xc3\xa84556889:;=?ABDFGIKMPSUWXY[\\\\ZWUTTSOKIHGHHRE:55773000259ANd\xc2\x83\xc2\x8cl\xc3\x8d\xc3\xb1\xc3\xb93457789:<=@BCEFHJLNPSVXZ[\\^^]YWVUOIGFDBDEO@;61.0531///149>BDL`kz345678:;<=@BDEGIJMOQTWY\\]^_`_^ZWPHGDCCBBEG89862-+,020.-,0414:<DD4556899;<=?BDFGIKMOQTWZ]_aabaa^TJFCABB@@@@0/55320+\')-/.+(\'*).+*-235678:;;=?ACEGIKLNPSVY\\_abaab\\QIC?AB?>9>5++*/2210,\'$%\'$"#%%*(!\x1e2345689;<>?ACEHIKMOPSVY\\^`baaZSNC@CD?=939.,*(\')/00-*($!\x1e\x1f !#<rW 1235679:;=?ACFHIKMOPSVY\\]`aaYQNC?DC?>;1,6.+)\'&%%*/.*\'\x1f\x1d\x1c\x1a\x1b\x1f-CXui023678:;<>@CDFHJLMOPSUXZ]_`YRNB=D@;;;2*+5-*((\'%#"%++\x1f\x1d\x1a\x19\x17\x1d(0>C`m0235789;<>BEFGHJLMOQSUWY[\\VPM?2A?::7-\')-4,)(&&$"" !\x1d\x1c\x18\x17\x18\x1f$)/9:KY0234679;=ADFGIIJKMOQSTVXXRLE=0@>885*%\')*/,\'&%#""!\x1f\x1a\x19\x17\x16\x19"%%(.51>G124568:<?CDFHIKKLNOPRTUUOJD<8=;663(%\'(()))\'$$#""\x1e\x18\x17\x15\x16\x1c#%&%\'+.*3:134568:>@BDFGIKLNNOPQRRMHD91<722/&$\'((\'\'&%$$$" \x1b\x16\x15\x14\x15 #%&&%&\'(&+.124579;=@BDFGIKLNOOOPPLFA:3;410)#$\'(\'\'\'&%#"!" \x19\x15\x13\x13\x18!%%&&\'$#%$"&&124689;=?BCEGHJKMNPOOLF?9;91//\'!%\'\'\'\'&%%$" \x1f\x1f\x17\x14\x13\x12\x19"$%%%%$!!# \x1f! 125679:=?ACEGHJKLNNONHA<970.,%!$\'\'\'\'&&%$#!!!\x15\x12\x11\x13\x1c!$%%&%#"\x1f\x1f#\x1f\x1f\x1f\x1d124678:<>@BDFHJJLMMMME<85/.*"!%&\'\'\'&%%$$#\'4\x1d\x12\x11\x16\x1f"#%&%$"! \x1f #\x1f\x1d\x1c\x1a1256789<>?BDFGIJKLLLLC83.,(!!%\'\'\'\'&&%%$\'2<+!\x1c'
    p+=b'\x1b##%&\'&$"! \x1f!!"\x1e\x1c\x1a\x181247789;=?ACEGIJKLLKI91.,& !%&\'\'\'\'&%$%,=:\'$"%(\'\'\'&&$#! \x1f"#%%!\x1f\x1a\x170247789;=?ACEGIJJLLKH6/+$ #%&&\'\'\'&%%(4=,#%$(+,+)\'%$"!\x1f!%%###\x1a\x1d"\x1b1247878:<>@CEGIIKKLKI?:& #%%&\'&&&&&0?:>/#&,.//-*&$#!!!(&"\x1f\x1e\x1b\x16\x16\x1a\x1d0246889:<>@BDFHIJKLKIEA0$%%%&&&&\'*=VD8=3\x1c(622/,)&#"  &&&$\x1c\x1a\x18\x14\x16\x17\x16%*25889:<=?ACEHIJKLLIEE.&&&&&&&\'4MX>C8;6\x1e\x19951/+(%#! "%"" \x1f\x1a\x17\x15\x16\x18\x15##(2889:<=?ACEGIJKLLIFF*\'&&&&&+=RI78C;99(\x13162/,(&#!\x1f" \x1c\x1e\x1f \x1d\x17\x16\x15\x16\x14$$$&078:;=>ABEGIJKKKIG@(\'\'&&\'1CJ852\'=A8=2\x16$63/*\'$" \x1e!\x1a\x19\x18\x1c\x1e\x1e\x16\x13\x12\x14\x12(\'&\'(-49;=>@BDFHJKKKIH8((\'\'*7E>12+ \x198H8B;\x1c\x1754/*($" \x1e\x1f\x1b\x17\x16\x18\x16\x13\x12\x12\x13\x12\x12&#()),-18<>@ACFGIKKKIH.(((/:@3/,#\x1b\x17\x173N;FB&\x12,3.*\'%!\x1d\x1b\x1c\x1c\x14\x15\x12\x10\x11\x12\x11\x11\x12\x15\x1b\x1b\x1f&,/./48<?@CEGIJKKID*)+9==3-) \x1a\x18\x17\x17+SAHI2\x15 2/)&!\x1b\x19\x1c\x1d\x17\x12\x12\x11\x12\x12\x11\x11\x13\x18\x15\x1a\x1a\x1a\x1e$,/356:>@BDFGJKKJ<,1CI@?1,&\x1e\x1a\x18\x17\x17$XJHM:\x19\x160/(\x1f\x1a\x1a\x1c\x18\x14\x12\x12\x12\x13\x12\x12\x12\x15\x17\x15\x11\x1b\x1a\x1a\x1b\x1f"\'256;=>@BDFHIKK8;INL@@0-&\x1f\x1a\x19\x17\x17\x1c[QDF3 \x15).\x1f\x1b\x1e\x1b\x15\x12\x12\x11\x13\x12\x12\x12\x14\x16\x14\x13\x11\x0e\x1d\x1c\x1b\x1b\x1c\x1d \'28;<=?@CEGIKLILNOL?B..(!\x1c\x1a\x18\x17\x1aYK@A7)\x16!.&\x1f\x19\x15\x13\x12\x13\x13\x12\x12\x13\x14\x16\x14\x11\x10\x10\x0e!\x1f\x1d'
    p+=b'\x1c\x1b\x1c\x1e!*9:;;=?ACEGJMNNPOK?D00*$\x1f\x1d\x1a\x18\x1dPECIL6\x17\x17$#\x1e\x1c\x17\x16\x16\x16\x14\x13\x14\x16\x14\x13\x12\x10\x10\x0f\r/%"\x1f\x1d\x1c\x1c -7999;=>@BDHLNOPOJ@D23/,(#\x1d\x1a&jfIGL?\x1b\x14\x15\x1f#\x1f\x1c\x19\x16\x16\x15\x16\x14\x14\x13\x12\x10\x0f\x0f\x0f\r74+#!\x1f %578889;<;<?CHLNPOIBD59=WZE& &ksPJHD!\x14\x15\x1a"\x1f\x1d\x1b\x19\x18\x16\x15\x14\x13\x12\x11\x10\x0f\x0f\x0f\r8981)\'(077787787:<?@CGMONGCE;F\xc2\x86\xc2\xb6\xc2\xbb\xc2\xacL%"bkUGOF+\x18\x17\x15\x1d\x1f\x1d\x1d\x1a\x19\x15\x14\x13\x12\x12\x11\x10\x0f\x0e\x0f\x0cq\x11h\x05\x86q\x12Rq\x13tq\x14b.'
    print (pickle.loads(p))





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


class AppState(Enum):
    STOP = 0
    SHOW = 1
    MOVIE_REC = 2
    MOVIE_QUERY_YN = 3
    MOVIE_QUERY_NAME = 4
    PIC_QUERY_YN = 5
    PIC_QUERY_NAME = 6
    
    

class AppPiCam:
    
    def __init__(self,mgr):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,32,24,0,0,kb_event=self.kb_event, cursor_off=True)
        self.ctrlwin=None
        self.ctrlwin_timeout=time.time()+20
        self.edlin=None
        self.show_offset=0
        self.max_lines=16
        self.f_index_str='1234567890ABCDEFGHI'
        self.f_index=str2zx(self.f_index_str)
        self.actual_lines=0
        self.charmap=[15]*256
        self.build_charmap()
        self.cam=None
        self.camout=None
        self.app_state=AppState.SHOW
        self.replay_ix=0
        self.delay_s=3.0
        self.event=mgr.schedule_event(self.periodic,1.0,5.0)
        self.contrast=0.5
        self.brightness=1.0
        self.invert=False
        self.h_v_rot=0      # H/V flip or rotate status as three LSB bits
        self.floyd_stb=False
        self.applied_rot=None
        self.check_show_ctrlwin()
        self.movie=[]
        self.last_pic=None
    
    def __enter__(self):
        return self
         
    def __exit__(self, _type, _value, _traceback):    
        self.close()
    
    def close(self):
        self.app_state=AppState.STOP
        if  self.event:
            self.event.remove()
            self.event=None
        if  self.camout is not None:
            self.camout.close()
            self.camout=None
        if  self.cam is not None:
            self.cam.close()
            self.cam=None
        if self.mainwin:
            self.mainwin.close()
            self.mainwin=None
        if self.ctrlwin:
            self.ctrlwin.close()
            self.ctrlwin=None
    
    def check_show_ctrlwin(self):
        if not self.ctrlwin:
            self.ctrlwin=TextWindow(self.mgr,14,13,14,9,border=WindowBorderFrame(str2zx('ZX LIVE CAM')) ,kb_event=self.kb_event, cursor_off=True)
            self.ctrlwin.prttxt(str2zx('F fast S slow\n\nD dith I invrt',upper_inv=True ))
            self.ctrlwin.prttxt(str2zx('\nP pic M movie\n',upper_inv=True ))
            self.ctrlwin.prttxt(str2zx('\nR rotate\n\n1-5 brightness6-0 contrast\n\nX exit',upper_inv=True ))
        elif time.time()>self.ctrlwin_timeout:
            self.ctrlwin.close()
            self.ctrlwin=None
                                    

    def show_help(self):
        self.mainwin.prttxt(str2zx('\n      ZX LIVE CAMERA       \n\n',inverse=True ))
        self.mainwin.prttxt(str2zx('\n\n NEWLINE to start\n\n F fast update    S slow update\n\n D dithering\n\n I invert',upper_inv=True ))
        self.mainwin.prttxt(str2zx('\n\n R rotate\n\n 1-5 bright\n\n 6-0 contrast\n\n X exit',upper_inv=True ))
    
    def periodic(self):
        startt=time.time()
        if self.app_state==AppState.SHOW:
            if self.ctrlwin and time.time()>self.ctrlwin_timeout:
                self.ctrlwin.close()
                self.ctrlwin=None
        if self.app_state in (AppState.SHOW,AppState.MOVIE_REC):
            self.last_pic=self.get_img_mono()
            self.mgr.update(0.05) # allow for kb inp response
            if self.app_state in (AppState.SHOW,AppState.MOVIE_REC):
                lrg=self.calc_lrg_from_array(self.last_pic)
                self.show_lrg(lrg)
                if self.app_state == AppState.MOVIE_REC:
                    if len(self.movie)<50:
                        self.movie.append(self.last_pic)
                        self.ctrlwin.set_prtpos(0, 0)
                        self.ctrlwin.prttxt(str2zx('recording %02d'%len(self.movie) ,upper_inv=True ))
                    else:
                        self.end_movie_rec()
                evt_t=time.time()-startt
                self.event.reschedule(  max(0.05,self.delay_s-evt_t) ,5.0)
        elif self.app_state in (AppState.MOVIE_QUERY_YN,AppState.MOVIE_QUERY_NAME):
            if len(self.movie):
                if self.replay_ix >= len(self.movie): self.replay_ix=0
                lrg=self.calc_lrg_from_array(self.movie[self.replay_ix])
                self.show_lrg(lrg)
                self.replay_ix+=1
                evt_t=time.time()-startt
                self.event.reschedule(  max(0.05,self.delay_s-evt_t) ,5.0)
            
    
    def build_charmap(self):
        for pul in range(4):
            for pur in range(4):
                for pll in range(4):
                    for plr in range(4):
                        c=15
                        ix=pul*64+pur*16+pll*4+plr
                        al=(pul,pur,pll,plr)
                        up=(pul,pur)
                        lo=(pll,plr)
                        if 0 not in al and 3 not in al:
                            # just grey
                            if sum(al)/len(al)>1.5:
                                c=8 # fits to brighter edges
                            else:
                                c=136 # fits to darker edges
                            
                        elif 0 not in up and 3 not in up and 2 not in lo and 3 not in lo:
                            # upper grey, low black
                            c=138
                        elif 0 not in up and 3 not in up and 0 not in lo and 1 not in lo:
                            # upper grey, low white
                            c=10
                        elif 0 not in lo and 3 not in lo and 2 not in up and 3 not in up:
                            # low grey, upper black
                            c=137
                        elif 0 not in lo and 3 not in lo and 0 not in up and 1 not in up:
                            # low grey, upper white
                            c=9
                        else:
                            # binary
                            c=0
                            if pul<=1: c+=1
                            if pur<=1: c+=2
                            if pll<=1: c+=4
                            if plr<=1: c=c^0x87
                        self.charmap[ix]=c
        #print (self.charmap)
    
    def get_img_mono(self):
        a=None
        if cam_available:
            if self.cam is None:
                self.cam=picamera.PiCamera()
            if self.camout is None:
                self.camout=picamera.array.PiYUVArray(self.cam)
                self.cam.resolution=(64,48)
            else:
                self.camout.truncate(0)
            rotate=self.h_v_rot & 1
            if rotate != self.applied_rot:
                self.cam.resolution=(48,64) if rotate else (64,48)
                self.applied_rot=rotate
            self.cam.capture(self.camout,'yuv',use_video_port=True)
            a=self.camout.array[:,:,0]
            if rotate: a=numpy.transpose(a)
        else:
            a=pickle.loads(p)
        return a


    def show_lrg(self,a):
        nr,nc=a.shape
        for row in range(nr):
            for col in range(nc):
                self.mainwin.setchar_raw(a[row,col], col, row)

    def calc_lrg_from_array(self,a):
        #calculate the mean value etc
        t=time.time()
        
        if self.h_v_rot & 4 :a=numpy.fliplr(a)  # H flip
        if self.h_v_rot & 2 :a=numpy.flipud(a)   # V flip
        if self.invert:a=255-a
        
        m=a.mean()/self.brightness
        s=a.std()*self.contrast* (1 if cam_available else random.gauss(1.0,0.1)) # add some dynamics if no camera is there
        l0=m-s
        l1=m
        l2=m+s
        nr,nc=a.shape        

        # optional flody-steinberg
        if self.floyd_stb:
            l0=max(0,int(m-2*s))
            l2=min(255,int(m+2*s))
            for row in range(0,nr):
                for col in range(0,nc):
                    p=a[row,col]
                    n=l2 if p>l1 else l0
                    err=p-n
                    a[row,col]=n
                    if col<nc-1:
                        a[row,col+1]+=err*7//16
                    if row<nr-1:
                        if col>=1:
                            a[row+1,col-1]+=err*3//16
                        a[row+1,col]+=err*5//16
                        if col<nc-1:
                            a[row+1,col+1]+=err*1//16
            
        brightmap=[ 0 if b<=l0  else 3 if b>=l2 else 1 if b<l1 else 2    for b in range(256)]
        #print(brightmap)
        #print(a.mean(),a.std())
        va=numpy.zeros((nr//2,nc//2),dtype=int)
        
        for row in range(0,nr,2):
            for col in range(0,nc,2):
                # get the four points that make up a character
                code=0
                for b in (a[row,col],a[row,col+1],a[row+1,col],a[row+1,col+1]):
                    code*=4
                    if 0:  # this seems to be much slower than the lookup below!
                        if b<l0:
                            c=0
                        elif b>l2:
                            c=3
                        elif b<l1:
                            c=1
                        else:
                            c=2
                        code+=c
                        if c!=brightmap[b]: print("FAIL")
                    else:
                        code+=brightmap[b]
                va[row//2,col//2] = self.charmap[code]
                #self.mainwin.setchar_raw(self.charmap[code], col//2, row//2)
        #print("Display took %.2fus."%((time.time()-t)*1000000) )
        # now er have an 8bit code that we map for the proper char
        return va

    def end_movie_rec(self):
        self.app_state=AppState.MOVIE_QUERY_YN
        if self.ctrlwin: self.ctrlwin.close()
        self.ctrlwin=TextWindow(self.mgr,10,1,18,19,border=WindowBorderFrame() ,kb_event=self.kb_event_query, cursor_off=True)
        self.ctrlwin.prttxt(str2zx('save? Y/N',upper_inv=True ))
                                      
    
    def kb_event(self,win,zxchar):
        #win.prtchar(zxchar)
        bright={'1':1.5,'2':1.2, '3':1.0, '4':0.83, '5':0.67}
        contr ={'6':0.2,'7':0.33, '8':0.5, '9':0.8, '0':1.2}
        s=zx2str( [zxchar] )
        if s in 'xX' or zxchar==12:
            self.close()
            return
        elif s in 'fF':
            self.delay_s=0.15
        elif s in 'sS':
            self.delay_s=3.0
        elif s in 'dD':
            self.floyd_stb=not self.floyd_stb
        elif s in 'iI':
            self.invert=not self.invert
        elif s in 'rR':
            self.h_v_rot += 1
            
        elif s in 'pP':
            if self.app_state==AppState.SHOW:
                self.app_state=AppState.PIC_QUERY_YN
                if self.ctrlwin: self.ctrlwin.close()
                self.ctrlwin=TextWindow(self.mgr,10,1,18,19,border=WindowBorderFrame() ,kb_event=self.kb_event_query, cursor_off=True)
                self.ctrlwin.prttxt(str2zx('save? Y/N',upper_inv=True ))

        elif s in 'mM':
            self.movie.clear()
            self.replay_ix=0
            if self.app_state==AppState.SHOW:
                self.app_state=AppState.MOVIE_REC
                if self.ctrlwin: self.ctrlwin.close()
                self.ctrlwin=TextWindow(self.mgr,13,1,17,19,border=WindowBorderFrame() ,kb_event=self.kb_event_query, cursor_off=True)
                self.ctrlwin.prttxt(str2zx('recording',upper_inv=True ))

        elif s in bright:
            self.brightness=bright[s]
        elif s in contr:
            self.contrast=contr[s]
        # TODO invers, save_pic, help, exit
        self.ctrlwin_timeout=time.time()+3
        self.check_show_ctrlwin()
        self.event.reschedule(0.2,5.0)

    def kb_event_query(self,win,zxchar):
        #win.prtchar(zxchar)
        s=zx2str( [zxchar] )
        if self.app_state in (AppState.PIC_QUERY_NAME,AppState.MOVIE_QUERY_NAME):
            if zxchar in (117,118): # enter,break 
                if zxchar==118: # enter
                    self.edlin.kb_event(zxchar)
                    if self.app_state==AppState.PIC_QUERY_NAME:
                        if self.edlin.val:
                            # safe pic
                            name=zx2str(self.edlin.val, to_lower=True).strip()
                            #path 
                            mwin=self.mgr.show_msg_win(str2zx("save pic .."))
                            p=zxpi_paths.get_current_work_path()/'pics'
                            if not p.exists(): p.mkdir(parents=True)
                            n=p/(name+'.zxscr')
                            with n.open('wb') as f:
                                lrg=self.calc_lrg_from_array(self.last_pic)
                                nr,nc=lrg.shape
                                for row in range(nr):
                                    #for col in range(nc):
                                    f.write(bytes( [v for v in lrg[row]]  ))
                                print("Saved to",str(n))
                            mwin.close()
                    elif self.app_state==AppState.MOVIE_QUERY_NAME:
                        if self.edlin.val:
                            # save movie
                            name=zx2str(self.edlin.val, to_lower=True).strip()
                            #path 
                            p=zxpi_paths.get_current_work_path()/'movies'
                            if not p.exists(): p.mkdir(parents=True)
                            n=p/(name+'.zxmovie')
                            mwin=self.mgr.show_msg_win(str2zx("save movie .."))
                            with n.open('wb') as f:
                                for p in self.movie:
                                    lrg=self.calc_lrg_from_array(p)
                                    nr,nc=lrg.shape
                                    for row in range(nr):
                                        #for col in range(nc):
                                        f.write(bytes( [v for v in lrg[row]]  ))
                                print("Saved as",str(n))
                            mwin.close()
                if self.edlin:
                    self.edlin.close()
                    self.edlin=None
                self.app_state=AppState.SHOW
                self.ctrlwin_timeout=0
                if self.ctrlwin:
                    self.ctrlwin.close()
                    self.ctrlwin=None
            else:
                self.edlin.kb_event(zxchar)
        elif self.app_state in (AppState.MOVIE_REC,):
            self.end_movie_rec()
        else:
            if s in 'yYzZ':
                if self.app_state in (AppState.PIC_QUERY_YN,AppState.MOVIE_QUERY_YN):
                    self.app_state= AppState.PIC_QUERY_NAME if self.app_state==AppState.PIC_QUERY_YN else AppState.MOVIE_QUERY_NAME
                    if self.ctrlwin: self.ctrlwin.close()
                    self.ctrlwin=TextWindow(self.mgr,12,2,18,19,border=WindowBorderFrame() ,kb_event=self.kb_event_query, cursor_off=True)
                    self.ctrlwin.prttxt(str2zx('file name:',upper_inv=True ))
                    self.edlin=LinEd(self.ctrlwin,0,1,11,maxchar=255,history=None)
            else:
                self.app_state=AppState.SHOW
                if self.ctrlwin:
                    self.ctrlwin.close()
                    self.ctrlwin=None
            self.event.reschedule(0.2,5.0)


print("Import AppPiCam")
def start(mgr):
    print("AppPiCam Start")
    with AppPiCam(mgr) as a:
        while a.mainwin: mgr.update(0.5)

