'''
Created on Mar 12, 2016

@author: ACE
'''
import os
import time
import zx_ser_srv
import zx_app_host
from zx_app_host import str2zx


import apps.file_browser

# not needed here but imported to reduce loading time for apps that do use numpy or requests
import numpy 
import requests

if __name__ == '__main__':
    #speed=9600
    try:
        os.system('''"C:\Program Files (x86)\Tasm32\Tasm.exe" -80 -b z80_asm\loader.asm z80_asm\loader.p''')
        os.system('''"C:\Program Files (x86)\Tasm32\Tasm.exe" -80 -b z80_asm\serserv.asm z80_asm\serserv.p''')
        os.system('''"C:\Program Files (x86)\Tasm32\Tasm.exe" -80 -b z80_asm\zxpiload.asm z80_asm\zxpiload.p''')
        os.system('''"C:\Program Files (x86)\Tasm32\Tasm.exe" -80 -b z80_asm\zxpiload.asm z80_asm\zxpiload.p''')
        os.replace('z80_asm\zxpiload.p','..\zxroot\zx81-tools\zxpiload.p')
    except:pass
    time.sleep(1) # as the script might run as an automated startup, wait a bit till cpu gets less busy
    
    con=zx_ser_srv.ZXLoadConnectHandler(zx_ser_srv.get_serial_port( ['COM4','COM3','/dev/ttyAMA0'] ))
    
    #with zx_ser_srv.get_serial_server_connection( ['COM4',] ) as sersrv:
    with zx_ser_srv.ZXSerServ(con) as sersrv:
        
        m=zx_app_host.ZxAppHost(sersrv)
        print(111)
        #for i in range(20):
        #    m.update(1)
        
        
        
#        pc=apps.pi_cam.AppPiCam(m)
#        while True:
#            m.update(0.7)
        #sh=apps.shell.AppShell(m)
        sh=apps.file_browser.AppFileBrowser(m)
        print(112)
        while True:
            m.update(0.7)
        
        
        #w0=zx_app_host.TextWindow(m,30,18,1,1)
        #w0.cls(8)
        def kb_event_w1(win,key):
            print("kb_event_w1")
            win.prtchar(key)
        
        w1=zx_app_host.TextWindow(m,25,20,2,2,border=zx_app_host.WindowBorderFrameShadow(title=str2zx("EDIT win")),kb_event=kb_event_w1 )
        w1.cls()
        w2=zx_app_host.TextWindow(m,20,9,10,4,border=zx_app_host.WindowBorderFrame())
        w2.cls(7)
        w3=zx_app_host.TextWindow(m,3,3,16,7,border=zx_app_host.WindowBorderFrameShadow())
        w3.cls()
        count=[0]
        def periodic():
            count[0]+=1
            #print("hhh",count[0])
            if count[0]==27:
                sersrv.load_p_file('z80_asm/demo/MANIC.P')#
                #sersrv.load_p_file('z80_asm/demo/shufmov.p')#
            elif count[0]==15:
                w2.close()
            else:
                w2.cls( (count[0]+20)&0xBF  )
        e1=m.schedule_event(periodic,0,1.1)
        e2=m.schedule_event(periodic,11.0,7.1)
        while True:
            m.update(0.7)
            w3.cls(61)
            m.update(1.3)
            w3.cls(58)
            
    print("End")
    
    
  
 
   
    