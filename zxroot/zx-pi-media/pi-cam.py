
from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str, ZXCHAR_BLANK, ZXCHAR_INV_FLG


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

if not cam_available: # load dummy
    p= b'\x80\x02cnumpy.core.multiarray\n_reconstruct\nq\x00cnumpy\nndarray\nq\x01K\x00\x85q\x02c_codecs\nencode\nq\x03X\x01\x00\x00\x00bq\x04X\x06\x00\x00\x00latin1q\x05\x86q\x06Rq\x07\x87q\x08Rq\t(K\x01K0K@\x86q\ncnumpy\ndtype\nq\x0bX\x02\x00\x00\x00u1q\x0cK\x00K\x01\x87q\rRq\x0e(K\x03X\x01\x00\x00\x00|q\x0fNNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK\x00tq\x10b\x89h\x03X=\x0c\x00\x00ple]UNHCB?>====>?@ACDFHJJKMORTWYZ\\bfjnooopsu\xc2\x80vmf`\\ZXWUTSTUWX_cnrohaYRJDB@>>==<>??ABCEGIKMLNPRTWY\\_bejlpooqpr}ohb[WVSRONPRTVY[[]jhe^UMGB@?>>>===?@BCDFIKMNNPQSUXZ\\_dfhkmnnnosykc^XTRPNHGKRVYVOZYo^]ZPGC@?=====>?ABCDFHJLNOORSTVWY[_cfiiilkkmrsfa[UQNKFDCGRYYQPTgwJFDAB@>======?@ACDFGIKLNOPQRTUVW[]aeffhihhjskb]WRNHCAAABGOTY_p}u==<<=<<;;<<<>?@BDEGIKLMOPOPRSUVW[\\`abddeedgpd_ZTOFC@A?;=DLVk\xc2\x9d\xc3\x81\xc2\x93\xc2\x82:::::::;;;<=?@BCEGIJLNOQRQQQRTUWY\\]^aaabbcel_[VOJC@@><8=ENl\xc2\x9d\xc2\xb2\xc3\x8f\xc2\xb8\xc2\xa089889:9;;;=>@ACEGIJLMOPRSRRQRSUWY[\\\\]]^^__deZVPFDA@><98;EZ\xc2\x95\xc2\xb3\xc2\xbf\xc3\x94\xc3\xa3\xc3\x8477777899:;>?@BDEGIKMNPQRSTRQRSUVXYYZZZZZ[]d^WPIA@?;;<67COe\xc2\x92\xc2\xb7\xc3\xa2\xc3\xb5\xc3\xb9\xc3\xb15566679::<=>@BCEGIKLOQRRTUTRSTSTVWXXXXWWWZcXRIB>>;:::;>GUj\xc2\x88\xc3\x88\xc3\xba\xc3\xba\xc3\xba\xc3\xba5456689:;<>?@BDEGIKMPRSTUVUTTSSTTVWWWVUSTX_SLC>=<:868;BJWm\xc2\x95\xc3\x9a\xc3\xba\xc3\xba\xc3\xba\xc3\xba4456789:;<=?@BDEHJKMPRTUWXXVUSSTTUVVVSPQRV\\LD@:;9:988:BLZo\xc2\x8e\xc3\x85\xc3\xb8\xc3\xba\xc3\xba\xc3\xba4456788:;=>?ABDFHJLNQSTVWXYWUTSSTTUTROMMOUSEA<;778867:AJVf\x7f\xc2\xa0\xc3\x90'
    p+=b'\xc3\xb1\xc3\xb9\xc3\xba34567799<=?AACEFHJLPRTVVXY[YWUSSTSSQMLJKMTJA<;663047;AOcy\xc2\x8e\xc2\x9e\xc2\xbc\xc3\x83\xc3\x9d\xc3\xa5\xc3\xa84556889:;=?ABDFGIKMPSUWXY[\\\\ZWUTTSOKIHGHHRE:55773000259ANd\xc2\x83\xc2\x8cl\xc3\x8d\xc3\xb1\xc3\xb93457789:<=@BCEFHJLNPSVXZ[\\^^]YWVUOIGFDBDEO@;61.0531///149>BDL`kz345678:;<=@BDEGIJMOQTWY\\]^_`_^ZWPHGDCCBBEG89862-+,020.-,0414:<DD4556899;<=?BDFGIKMOQTWZ]_aabaa^TJFCABB@@@@0/55320+\')-/.+(\'*).+*-235678:;;=?ACEGIKLNPSVY\\_abaab\\QIC?AB?>9>5++*/2210,\'$%\'$"#%%*(!\x1e2345689;<>?ACEHIKMOPSVY\\^`baaZSNC@CD?=939.,*(\')/00-*($!\x1e\x1f !#<rW 1235679:;=?ACFHIKMOPSVY\\]`aaYQNC?DC?>;1,6.+)\'&%%*/.*\'\x1f\x1d\x1c\x1a\x1b\x1f-CXui023678:;<>@CDFHJLMOPSUXZ]_`YRNB=D@;;;2*+5-*((\'%#"%++\x1f\x1d\x1a\x19\x17\x1d(0>C`m0235789;<>BEFGHJLMOQSUWY[\\VPM?2A?::7-\')-4,)(&&$"" !\x1d\x1c\x18\x17\x18\x1f$)/9:KY0234679;=ADFGIIJKMOQSTVXXRLE=0@>885*%\')*/,\'&%#""!\x1f\x1a\x19\x17\x16\x19"%%(.51>G124568:<?CDFHIKKLNOPRTUUOJD<8=;663(%\'(()))\'$$#""\x1e\x18\x17\x15\x16\x1c#%&%\'+.*3:134568:>@BDFGIKLNNOPQRRMHD91<722/&$\'((\'\'&%$$$" \x1b\x16\x15\x14\x15 #%&&%&\'(&+.124579;=@BDFGIKLNOOOPPLFA:3;410)#$\'(\'\'\'&%#"!" \x19\x15\x13\x13\x18!%%&&\'$#%$"&&124689;=?BCEGHJKMNPOOLF?9;91//\'!%\'\'\'\'&%%$" \x1f\x1f\x17\x14\x13\x12\x19"$%%%%$!!# \x1f! 125679:=?ACEGHJKLNNONHA<970.,%!$\'\'\'\'&&%$#!!!\x15\x12\x11\x13\x1c!$%%&%#"\x1f\x1f#\x1f\x1f\x1f\x1d124678:<>@BDFHJJLMMMME<85/.*"!%&\'\'\'&%%$$#\'4\x1d\x12\x11\x16\x1f"#%&%$"! \x1f #\x1f\x1d\x1c\x1a1256789<>?BDFGIJKLLLLC83.,(!!%\'\'\'\'&&%%$\'2<+!\x1c'
    p+=b'\x1b##%&\'&$"! \x1f!!"\x1e\x1c\x1a\x181247789;=?ACEGIJKLLKI91.,& !%&\'\'\'\'&%$%,=:\'$"%(\'\'\'&&$#! \x1f"#%%!\x1f\x1a\x170247789;=?ACEGIJJLLKH6/+$ #%&&\'\'\'&%%(4=,#%$(+,+)\'%$"!\x1f!%%###\x1a\x1d"\x1b1247878:<>@CEGIIKKLKI?:& #%%&\'&&&&&0?:>/#&,.//-*&$#!!!(&"\x1f\x1e\x1b\x16\x16\x1a\x1d0246889:<>@BDFHIJKLKIEA0$%%%&&&&\'*=VD8=3\x1c(622/,)&#"  &&&$\x1c\x1a\x18\x14\x16\x17\x16%*25889:<=?ACEHIJKLLIEE.&&&&&&&\'4MX>C8;6\x1e\x19951/+(%#! "%"" \x1f\x1a\x17\x15\x16\x18\x15##(2889:<=?ACEGIJKLLIFF*\'&&&&&+=RI78C;99(\x13162/,(&#!\x1f" \x1c\x1e\x1f \x1d\x17\x16\x15\x16\x14$$$&078:;=>ABEGIJKKKIG@(\'\'&&\'1CJ852\'=A8=2\x16$63/*\'$" \x1e!\x1a\x19\x18\x1c\x1e\x1e\x16\x13\x12\x14\x12(\'&\'(-49;=>@BDFHJKKKIH8((\'\'*7E>12+ \x198H8B;\x1c\x1754/*($" \x1e\x1f\x1b\x17\x16\x18\x16\x13\x12\x12\x13\x12\x12&#()),-18<>@ACFGIKKKIH.(((/:@3/,#\x1b\x17\x173N;FB&\x12,3.*\'%!\x1d\x1b\x1c\x1c\x14\x15\x12\x10\x11\x12\x11\x11\x12\x15\x1b\x1b\x1f&,/./48<?@CEGIJKKID*)+9==3-) \x1a\x18\x17\x17+SAHI2\x15 2/)&!\x1b\x19\x1c\x1d\x17\x12\x12\x11\x12\x12\x11\x11\x13\x18\x15\x1a\x1a\x1a\x1e$,/356:>@BDFGJKKJ<,1CI@?1,&\x1e\x1a\x18\x17\x17$XJHM:\x19\x160/(\x1f\x1a\x1a\x1c\x18\x14\x12\x12\x12\x13\x12\x12\x12\x15\x17\x15\x11\x1b\x1a\x1a\x1b\x1f"\'256;=>@BDFHIKK8;INL@@0-&\x1f\x1a\x19\x17\x17\x1c[QDF3 \x15).\x1f\x1b\x1e\x1b\x15\x12\x12\x11\x13\x12\x12\x12\x14\x16\x14\x13\x11\x0e\x1d\x1c\x1b\x1b\x1c\x1d \'28;<=?@CEGIKLILNOL?B..(!\x1c\x1a\x18\x17\x1aYK@A7)\x16!.&\x1f\x19\x15\x13\x12\x13\x13\x12\x12\x13\x14\x16\x14\x11\x10\x10\x0e!\x1f\x1d'
    p+=b'\x1c\x1b\x1c\x1e!*9:;;=?ACEGJMNNPOK?D00*$\x1f\x1d\x1a\x18\x1dPECIL6\x17\x17$#\x1e\x1c\x17\x16\x16\x16\x14\x13\x14\x16\x14\x13\x12\x10\x10\x0f\r/%"\x1f\x1d\x1c\x1c -7999;=>@BDHLNOPOJ@D23/,(#\x1d\x1a&jfIGL?\x1b\x14\x15\x1f#\x1f\x1c\x19\x16\x16\x15\x16\x14\x14\x13\x12\x10\x0f\x0f\x0f\r74+#!\x1f %578889;<;<?CHLNPOIBD59=WZE& &ksPJHD!\x14\x15\x1a"\x1f\x1d\x1b\x19\x18\x16\x15\x14\x13\x12\x11\x10\x0f\x0f\x0f\r8981)\'(077787787:<?@CGMONGCE;F\xc2\x86\xc2\xb6\xc2\xbb\xc2\xacL%"bkUGOF+\x18\x17\x15\x1d\x1f\x1d\x1d\x1a\x19\x15\x14\x13\x12\x12\x11\x10\x0f\x0e\x0f\x0cq\x11h\x05\x86q\x12Rq\x13tq\x14b.'
    print (pickle.loads(p))


class AppPiCam:
    
    def __init__(self,mgr):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,32,24,0,0,kb_event=self.kb_event, cursor_off=True)
        self.show_offset=0
        self.max_lines=16
        self.f_index_str='1234567890ABCDEFGHI'
        self.f_index=str2zx(self.f_index_str)
        self.actual_lines=0
        self.charmap=[15]*256
        self.build_charmap()
        self.cam=None
        self.camout=None
        self.active=False
        self.delay_s=3.0
        self.show_help()
        self.event=mgr.schedule_event(self.periodic,5.0,5.0)
        self.contrast=0.5
        self.brightness=1.0
        self.invert=False
        self.h_flip=False
        self.v_flip=False
        self.rotate=False
        self.applied_rot=None
    
    
    def close(self):
        if  self.camout is not None:
            self.camout.close()
            self.camout=None
        if  self.cam is not None:
            self.cam.close()
            self.cam=None
    
    def periodic(self):
        if self.active:
            if self.mgr.is_connected():pass
            i=self.get_img_mono()
            self.mgr.update(0.05) # allow for kb inp response
            if self.active:
                self.show_lrg_from_array(i)
                self.event.reschedule(self.delay_s,5.0)
    
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
            if self.rotate != self.applied_rot:
                self.cam.resolution=(64,64) if self.rotate else (64,48)
                self.applied_rot=self.rotate
            self.cam.capture(self.camout,'yuv',use_video_port=True)
            a=self.camout.array[:,:,0]
            if self.rotate: a=numpy.transpose(a)
        else:
            a=pickle.loads(p)
        return a
        
    def show_lrg_from_array(self,a):
        #calculate the mean value etc
        t=time.time()
        
        if self.h_flip:a=numpy.fliplr(a)
        if self.v_flip:a=numpy.flipud(a)
        if self.invert:a=255-a
        
        m=a.mean()/self.brightness
        s=a.std()*self.contrast* (1 if cam_available else random.gauss(1.0,0.1)) # add some dynamics if no camera is there
        l0=m-s
        l1=m
        l2=m+s
            
        brightmap=[ 0 if b<l0  else 3 if b>l2 else 1 if b<l1 else 2    for b in range(256)]
        #print(brightmap)
        #print(a.mean(),a.std())
        
        for row in range(0,a.shape[0],2):
            for col in range(0,a.shape[1],2):
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
                self.mainwin.setchar_raw(self.charmap[code], col//2, row//2)
        #print("Display took %.2fus."%((time.time()-t)*1000000) )
        # now er have an 8bit code that we map for the proper char

    def show_help(self):
        self.mainwin.prttxt(str2zx('\n\n <<< ZX LIVE CAMERA >>> \n\n',upper_inv=False ))
        self.mainwin.prttxt(str2zx('\n\n NEWLINE to start\n\n F fast update\n\n D slow update\n\n I invert\n\n H/V flip  R rotate\n\n 1-5 brightness\n\n 6-0 contrast\n\n X exit',upper_inv=True ))
                                      
    
    def kb_event(self,win,zxchar):
        #win.prtchar(zxchar)
        bright={'1':1.5,'2':1.2, '3':1.0, '4':0.83, '5':0.67}
        contr ={'6':0.2,'7':0.33, '8':0.5, '9':0.8, '0':1.2}
        s=zx2str( [zxchar] )
        self.active=True
        if s in 'xX' or zxchar==12:
            self.close()
            self.active=False
            self.mainwin.close()
            self.event.remove()
            app.clear()
            return
        elif s in 'fF':
            self.delay_s=0.15

        elif s in 'dD':
            self.delay_s=3.0
        elif s in 'iI':
            self.invert=not self.invert
        elif s in 'hH':
            self.h_flip=not self.h_flip
        elif s in 'vV':
            self.v_flip=not self.v_flip
        elif s in 'rR':
            self.rotate=not self.rotate
        elif s in bright:
            self.brightness=bright[s]
        elif s in contr:
            self.contrast=contr[s]
        else:
            self.active=True
        # TODO invers, save_pic, help, exit
        self.event.reschedule(0.2,5.0)



app=[]

print("Import AppPiCam")
def start(mgr):
    print("AppPiCam Start")
    app.append(AppPiCam(mgr))

