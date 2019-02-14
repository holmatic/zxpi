
from zx_app_host import TextWindow, WindowBorderFrame, str2zx, zx2str, ZXCHAR_BLANK, ZXCHAR_INV_FLG, ZXCHAR_NEWLINE


import time

import requests
from html.parser import HTMLParser



class MyHTMLParser(HTMLParser):
    
    def __init__(self, testdata=[]):
        HTMLParser.__init__(self)
        self.testdata=testdata
        self.reset_counters()
            
    def reset_counters(self):
        self.tcount=0
        self.cnttags={'dfn': 0}
        self.cnts=[] # [0 for _ in cnttags]
        self.out_data=[]
        
    
    def handle_starttag(self, tag, attrs):
        self.tcount+=1
        if tag in self.cnttags:
            self.cnttags[tag]+=1
        else:
            self.cnttags[tag]=1

    def handle_endtag(self, tag):
        self.tcount-=1
        if tag in self.cnttags:
            self.cnttags[tag]-=1
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        
        for td in self.testdata:
            if "td" in data:
                print("DATA %s :\n\n%s\n\n"%(data, str(self.cnttags)) )

        if self.cnttags=={'html': 1, 'head': 0, 'meta': 1, 'title': 0, 'link': 10, 'body': 1, 'div': 5, 'a': 1, 'span': 0, 'h1': 0, 'p': 0, 'form': 0, 'fieldset': 0, 'input': 0, 'button': 0, 'i': 0, 'ul': 1, 'li': 1, 'img': 0, 'h2': 0, 'br': 0, 'strong': 0, 'dl': 1, 'dt': 1, 'dd': 0, 'dfn': 0}:
            print("Topic :", data )
            self.out_data.append( [data,'N/A','N/A'] )
        if self.cnttags=={'dfn': 0, 'html': 1, 'head': 0, 'meta': 1, 'title': 0, 'link': 10, 'body': 1, 'div': 4, 'a': 1, 'span': 1, 'h1': 0, 'p': 0, 'form': 0, 'fieldset': 0, 'input': 0, 'button': 0, 'i': 0, 'ul': 1, 'li': 1, 'img': 0, 'h2': 0, 'br': 0, 'strong': 0, 'dl': 1, 'dt': 0, 'dd': 1}: #  self.tcount==23:
            s=data.strip()
            if s:
                print("Who :", s )
                if self.out_data:self.out_data[-1][1]=data
        if self.cnttags=={'dfn': 0, 'html': 1, 'head': 0, 'meta': 1, 'title': 0, 'link': 10, 'body': 1, 'div': 6, 'a': 1, 'span': 0, 'h1': 0, 'p': 0, 'form': 0, 'fieldset': 0, 'input': 0, 'button': 0, 'i': 0, 'ul': 1, 'li': 1, 'img': 0, 'h2': 0, 'br': 0, 'strong': 0, 'dl': 1, 'dt': 1, 'dd': 0}:
            s=data.strip()
            if ':' in s and '.' in s: 
                print("When :", s )
                if self.out_data:self.out_data[-1][2]=data

class AppWebZxForumDe:
    
    def __init__(self,mgr):
        self.mgr=mgr
        self.mainwin=TextWindow(mgr,32,24,0,0,kb_event=self.kb_event, cursor_off=True)
        self.show_offset=0
        self.max_lines=20
        self.do_exit=False
        self.url='https://forum.tlienhard.com/phpBB3/viewforum.php?f=2'
        #print(r.text)
        self.show()

    
    def show(self):
        self.mainwin.cls()
        self.mainwin.prttxt(str2zx("wait for \n"+self.url[:28]+'..\n',upper_inv=False ))
        self.mgr.update(wait_till_sync_done=True)
        
        while True:
            r=requests.get(self.url, timeout=6.0)
            if r.status_code==requests.codes.ok: break
            self.mainwin.prttxt(str2zx("retrieved %d, try again..\n"%(r.status_code),upper_inv=False ))
            self.mgr.update(0.5)
            if self.do_exit: return
        
        self.mainwin.prttxt(str2zx("parse..\n",upper_inv=False ))
        self.mgr.update(wait_till_sync_done=True)
        if self.do_exit: return
        #print(r.text)
        parser = MyHTMLParser()
        parser.feed(r.text)
        self.mainwin.cls()
        self.mainwin.prttxt(str2zx(self.url[:32],inverse=True ))
        self.mainwin.prttxt([ZXCHAR_NEWLINE]+[10]*32)
        d=parser.out_data
        lines=0
        for entry in d:
            hd,nm,dt=entry
            numchar=len(hd)+len(nm)+len(dt)+1
            numlines=(numchar+31)//32
            addspc=' '*(32*numlines-numchar)
            if lines+numlines+1>self.max_lines:
                break
            lines+=numlines+1
            self.mainwin.prttxt(str2zx(hd,upper_inv=False ))
            self.mainwin.prttxt(str2zx(addspc))
            self.mainwin.prttxt(str2zx(nm, inverse=True))
            self.mainwin.prttxt(str2zx(' '))
            self.mainwin.prttxt(str2zx(dt, inverse=False))
            self.mainwin.prttxt([10]*32)
    
    def close(self):
        if  self.mainwin is not None:
            self.mainwin.close()
            self.mainwin=None
    
                                       
    
    def kb_event(self,win,zxchar):
        #win.prtchar(zxchar)
        s=zx2str( [zxchar] )

        if s in 'xXuU' or zxchar==12:
            self.do_exit=True
            self.close()
        else:
            self.show()



app=[]

def start(mgr):
    print("AppWebZxForumDe Start")
    app.append(AppWebZxForumDe(mgr))





if __name__ == '__main__': # tester for direct exec
    r=requests.get('https://forum.tlienhard.com/phpBB3/viewforum.php?f=2')
    #print(r.text)
    parser = MyHTMLParser()
    parser.feed(r.text)

