
from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str, ZXCHAR_BLANK, ZXCHAR_INV_FLG

from pathlib import Path
from shutil import copyfile
import importlib
import traceback




class AppFileBrowser:
    
    def __init__(self,mgr):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,30,22,1,1,border=WindowBorderFrame(),kb_event=self.kb_event, cursor_off=True)
        self.cwd=Path.cwd()/'..'/'zxroot' #Path.home()
        self.cwdfiles=[]
        self.show_offset=0
        self.max_lines=16
        self.f_index_str='1234567890ABCDEFGHI'
        self.f_index=str2zx(self.f_index_str)
        self.actual_lines=0
        self.get_dir()
        self.show_dir()

    def get_dir(self):
        try:
            self.cwdfiles=[e for e in self.cwd.iterdir()]
            self.cwdfiles.sort()
        except PermissionError:
            print("PermissionError")
        self.show_offset=0
        

    def show_dir(self):
        self.mainwin.cls()
        xs=self.mainwin.xsize
        # current path
        self.mainwin.prttxt(str2zx(str(self.cwd)[-xs:]))
        # directory
        self.mainwin.set_prtpos(0,2)
        numf=len(self.cwdfiles)
        actual_lines=min(self.max_lines, numf-self.show_offset  )
        for linenum in range(actual_lines):
            f=self.cwdfiles[linenum+self.show_offset]
            dirchar=4 if f.is_dir() else ZXCHAR_BLANK
            self.mainwin.prttxt( [self.f_index[linenum]|ZXCHAR_INV_FLG,ZXCHAR_BLANK,dirchar] + str2zx(f.name[:xs-4]+'\n'))
        self.mainwin.set_prtpos(0,self.max_lines+2)  
        # Show bas to orient
        if numf<=self.max_lines:
            self.mainwin.prttxt(str2zx('_'*xs))
        else:
            s1=self.show_offset*xs//numf
            s2=s1+actual_lines*xs//numf
            for i in range(xs):
                self.mainwin.prtchar(131 if s1<=i<=s2 else 9)
        self.mainwin.set_prtpos(1,self.max_lines+4)
        self.mainwin.prttxt(str2zx('%s-%s'%(self.f_index_str[0],self.f_index_str[actual_lines-1]) , inverse=True))
        self.mainwin.prttxt(str2zx(':select',upper_inv=True ))
        self.mainwin.prttxt(str2zx('  Prev', upper_inv=True if self.show_offset>0 else False  ))
        self.mainwin.prttxt(str2zx('  Next', upper_inv=True if self.show_offset+self.max_lines<len(self.cwdfiles) else False ))
        self.mainwin.prttxt(str2zx('  Up',   upper_inv=True if self.cwd.parents else False ))
        
                                   
    
    def kb_event(self,win,zxchar):
        #win.prtchar(zxchar)
        s=zx2str( [zxchar] )
        redraw=False
        if s in 'nN':
            self.show_offset+=self.max_lines
            redraw=True
        elif zxchar==12: # break
            mwin=self.mgr.show_msg_win(str2zx("exit. bye."))
            raise Exception('Exit')
        elif s in 'pP':
            self.show_offset-=self.max_lines
            redraw=True
        elif s in 'uUxX':
            if  self.cwd.parents:
                self.cwd=self.cwd.parents[0]
                self.get_dir()
                redraw=True
        elif s in 'wW':       
            self.mgr.show_dialog(str2zx('press NEWLINE',upper_inv=True ))   
        elif zxchar in self.f_index:
            ix=self.f_index.index(zxchar)+self.show_offset
            if ix<len(self.cwdfiles):
                fi=self.cwdfiles[ix]
                if fi.is_dir():
                    self.cwd=fi
                    self.get_dir()
                    redraw=True
                elif fi.suffix.lower()=='.p':
                    name=str(fi)
                    print("LOAD ",name)
                    mwin=self.mgr.show_msg_win(str2zx("load %s .."%(name)))
                    mwin.close()
                    self.mgr.server.load_p_file(name)
                elif fi.suffix.lower()=='.py':
                    mwin=self.mgr.show_msg_win(str2zx("open %s .."%(fi.stem)))
                    try:
                        spath=self.cwdfiles[ix]
                        target=Path.cwd()/'apps'/'tmp'/self.cwdfiles[ix].name
                        if spath!=target: copyfile(str(spath),str(target))
                        print ("Copy from ", str(spath))
                        print ("Copy to ", str(target))
                        module="apps.tmp."+fi.stem # we are already in apps
                        newmod=importlib.import_module(module)
                        importlib.reload(newmod)
                        mwin.close()
                        newmod.start(self.mgr)
                    except Exception as e:
                        mwin.close()
                        print(e)
                        traceback.print_exc()
                        self.mgr.show_dialog(str2zx("error loading module"))
#                    eval("print(globals())")
 #                   print("Eval GLOB",modcmd)
  #                  eval("print(globals())", globals())
   #                 r=eval(modcmd, globals())
    #                print("LOADed PYTHON ")
                    
        if redraw:
    
            self.show_offset=min(self.show_offset, len(self.cwdfiles)-2 )
            self.show_offset=max(0,self.show_offset)
            self.show_dir()
            
            
        #if s=='\n': s='\r\n'


