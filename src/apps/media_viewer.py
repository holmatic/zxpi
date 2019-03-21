
from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str

import time


BYTES_PER_SCR=768
BYTES_PER_ROW=32
NUM_ROWS=BYTES_PER_SCR//BYTES_PER_ROW

class MediaViewerCam:
    
    def __init__(self,mgr,filepath):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,32,24,0,0,kb_event=self.kb_event, cursor_off=True)
        self.filepath=filepath
        self.delay_s=0.3
        self.event=None
        self.pic_or_movie=bytes()
        self.pic_or_movie=filepath.open('rb').read()
        self.current_read_pos=0
        self.show_next()
        if len(self.pic_or_movie)>=2*BYTES_PER_SCR:
            self.event=mgr.schedule_event(self.periodic,self.delay_s,self.delay_s)
            
        
    def show_next(self):
        if len(self.pic_or_movie)>=BYTES_PER_SCR:
            if self.current_read_pos>=len(self.pic_or_movie):
                self.current_read_pos=0
            for row in range(NUM_ROWS):
                for col in range(BYTES_PER_ROW):
                    self.mainwin.setchar_raw(self.pic_or_movie[self.current_read_pos], col, row)
                    self.current_read_pos+=1
                
    def periodic(self):
        self.show_next()
    
    def __enter__(self):
        return self
         
    def __exit__(self, _type, _value, _traceback):    
        self.close()
    
    def close(self):
        if  self.event:
            self.event.remove()
            self.event=None
        if self.mainwin:
            self.mainwin.close()
            self.mainwin=None
                                   
                                      
    
    def kb_event(self,win,zxchar):
        self.close()


def start(mgr, filepath):
    print("MediaViewerCam Start")
    with MediaViewerCam(mgr,filepath) as a:
        while a.mainwin: mgr.update(0.5)

