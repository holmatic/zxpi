'''
Created on 30.12.2018

@author: Holmatic
'''



import random
import time
import serial  
import enum          
            
# the command codes are in reality offsets of a Z80 JP command, so they absolutely must be correct
     




zro,one,speed,par,stp  = [0xFD],[0x55,0xFD],4800,serial.PARITY_NONE,serial.STOPBITS_ONE
SYNC_REPLY=42

TIMEOUT_SEC=9.0




def get_serial_port( ser_candidate_names ):
    for n in ser_candidate_names:
        try:
            print("Try to open %s ..."%n)
            ser = serial.Serial(n, speed, timeout=0, parity=par, stopbits=stp, rtscts=0)
            break
        except: pass
   
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    print("Success")
    return ser




class ConnectState(enum.Enum):
    IDLE=0      # offline
    TAPE_COM=1  # attempting tape download or expect upload to safe; includes listen and send states
    SER_COM=2   # full speed serial serial connection established 
    
            
        
class ZXLoadConnectHandler:
    
    def __init__(self,ser):
        self.ser=ser
        self.state=ConnectState.TAPE_COM
        self.tape_out_progress=None # None represents wait&listen time, int is number of bytes in 
        self.tape_out_holdoff=0  #  expected end of (buffered) sendout
        self.last_time_stamp=time.time()
        lfile=bytearray([0x27,0xa7])+bytearray( open("z80_asm/loader.p", "rb").read() ) # dummy name plus p file
        self.loader=[]   
        for fbyte in lfile:
            for bitmask in [1<<(7-n) for n in range(8)]:
                self.loader+= one if bitmask & fbyte else zro
        self.received=b''

    def state_handler(self):
        if self.state == ConnectState.TAPE_COM:
            print(self.ser.in_waiting)
            if self.ser.in_waiting:
                self.received+=self.ser.read_all()
                if b'OK' in self.received:
                    print("Received Loader Reply.")
                    self.received=b''
                    #switch baudrate 
                    wt=self.tape_out_holdoff+0.08-time.time()
                    if(wt>0):
                        print("Wait for holdoff..")
                        time.sleep(wt)
                    self.ser.flush()
                    self.ser.write(b'H')
                    time.sleep(0.01)
                    self.ser.baudrate=460800#115200#230400   # 460800
                    time.sleep(0.04)
                    # send p file
                    self.ser.write(b'L')
                    time.sleep(0.05)  # time to get ready
                    self.send_ser_p_file( bytearray( open("z80_asm/serserv.p", "rb").read() ))
                    #print(len(f), " at %.2fkByte/sec"%( ser.baudrate/10.0/1024 ))
                    #ser.write(f)
                    t=time.time()
                    while time.time()<t+TIMEOUT_SEC:
                        if self.ser.in_waiting:
                            if self.ser.read(1)[-1]==SYNC_REPLY: # expected reply
                                print("Connection established.")
                                self.state=ConnectState.SER_COM
                                return
                        time.sleep(0.05) # no busy polling
                    print("No serial line reply, please check UART interface.")
                    self.ser.baudrate=speed
                    self.last_time_stamp=time.time()
                    self.tape_out_progress = None
            # check to transmit loader in background
            t=time.time()
            if self.tape_out_progress is None:
                # within pause
                if t>=self.last_time_stamp+2.5:
                    # pause end, start
                    self.tape_out_progress=0
                    self.last_time_stamp=t
                    print("Send Loader...")
            if self.tape_out_progress is not None:
                # transmit loader in background
                ttime_sec=t-self.last_time_stamp
                #print("ttime_sec",ttime_sec)
                pre_send_sec=0.8
                while self.tape_out_progress * 10 / 4800  < ttime_sec+pre_send_sec: # send some hundred millisec ahead to have tx buffer always full
                    self.ser.write( [self.loader[self.tape_out_progress]] )
                    self.tape_out_holdoff=pre_send_sec+time.time()
                    self.tape_out_progress+=1
                    if self.tape_out_progress>=len(self.loader):
                        # done
                        self.tape_out_progress=None # listen for result
                        print("Listen...")
                        self.last_time_stamp=time.time() 
                        break
                      
                    

    def report_ser_disconnect(self):
        if self.state!=ConnectState.TAPE_COM:
            print("--DISCONNECT--")
            self.ser.reset_output_buffer()
            self.ser.reset_input_buffer()
            self.ser.baudrate=speed
            self.state=ConnectState.TAPE_COM
            self.tape_out_progress=None
            self.last_time_stamp=time.time()

    def send_ser_p_file(self, f):
        print("Send p file (size %d) in serial data format..."%len(f))
        # we transmit a file but the other side cannot slow us down, so we have to slow down from time to time
        # loader needs about 102 CPU cycles (35us) per byte (TODO calc exactly)
        #print( " throttled to %.2fkByte/sec"%( 64/break_ms/1024 ))
        self.ser.read_all() 
        startt=time.time()
        send_buf=bytearray()
        for i,b in enumerate(f):
            #ser.write([b])
            send_buf.append(b)
            if i%64==2:
                self.ser.write(send_buf)
                send_buf.clear()
                t=time.time()
                required_rx_time=i*0.000035 + 0.001
                actual_tx_time=t-startt
                time.sleep(max(0.001,required_rx_time-actual_tx_time)) 
        if send_buf: self.ser.write(send_buf)
        #time.sleep(0.1) # need a gap after last byte, otherwise loader will not check for stop 
        
        
        
class SerNotConnected(IOError):
    """If serial server is not connected or not running on ZX side"""

#CMD_POKE=0
#CMD_PEEK=CMD_POKE+15
CMD_OUT=999#TODO
CMD_IN=999#TODO
CMD_SYNC=256-24
CMD_NOP=256-5
CMD_POKE=CMD_SYNC-77
CMD_PEEK=CMD_POKE+15
CMD_FAST=CMD_PEEK+11
CMD_OVERLAY=CMD_POKE+33

ADDR_OVERLAY=16477 # 30 bytes in the calculator area
ADDR_LOADER=32719-0 # 29 bytes at end on mem that must not be overritten
        
        
class ZXSerServ:

    # packetsize for transmit
    TXPSIZE=42
    
    
    
    def __init__(self,con_handler):
        self.con_handler=con_handler
        self.ser=con_handler.ser
        self.tx_data=[]
        self.expected_syncs=0
        self.expected_data_info=[]
        self.peek_info={}       # this could be mem address => time-value dicts
        self.io_in_info={}      # this could be in address => time-value dicts
        self.last_ok_t=time.time()
        self.pending_callbacks=[]
 
 
    def __enter__(self):
        return self
         
    def __exit__(self, _type, _value, _traceback):    
        self.close()
        
    def close(self):
        self.con_handler.report_ser_disconnect()
        self.ser.close()

    def send_pending_tx_data(self):
        if self.con_handler.state!=ConnectState.SER_COM: raise SerNotConnected()
        if self.tx_data:
            t=time.time()
            while self.expected_syncs>=1:
                self.handle_input()
                if time.time() > t+TIMEOUT_SEC:
                    self.ser_disconnect()
                    raise SerNotConnected()
            self.ser.write(self.tx_data)
            self.tx_data=[]


    def flush_tx(self):
        if self.con_handler.state!=ConnectState.SER_COM: raise SerNotConnected()
        if self.tx_data:
            while len(self.tx_data)+1 < self.TXPSIZE:
                self.tx_data.append(CMD_NOP)
            self.tx_data.append(CMD_SYNC)
            self.expected_data_info.append( (CMD_SYNC,) )
            self.expected_syncs+=1
            t=time.time()
            while self.expected_syncs>=3:
                # NOTE: Recursion may/will occur from events in handle_input:
                # we have to make sure everything is safe for this 
                self.handle_input()
                if time.time() > t+TIMEOUT_SEC and self.expected_syncs>=3:
                    self.ser_disconnect()
                    raise SerNotConnected()
            #print("Write:",self.tx_data)
            self.ser.write(self.tx_data)
            self.tx_data=[]

    def send_command(self, sendbytes, expected_info=None):
        if self.con_handler.state!=ConnectState.SER_COM: raise SerNotConnected()
        if len(self.tx_data)+len(sendbytes)>=self.TXPSIZE:
            # too big, fist send off the data
            self.flush_tx()
        self.tx_data+=sendbytes
        if expected_info is not None:
            self.expected_data_info.append(expected_info)
    
    def is_connected(self):
        return self.con_handler.state==ConnectState.SER_COM
    
    def handle_while_not_connected(self):
        self.con_handler.state_handler()
        if self.con_handler.state==ConnectState.SER_COM:
            # The serserv sends an initial sync to start:
            print("Connect, clear in queue, txdata has %d items"%len(self.tx_data))
            self.expected_data_info.clear()
            #self.tx_data.clear()
            self.expected_syncs=0
            # initial sync is now directly 
            #self.expected_data_info.append( (CMD_SYNC,) )
            #self.expected_syncs+=1
            self.last_ok_t=time.time()
    
    def ser_disconnect(self):
        if self.con_handler.state==ConnectState.SER_COM:
            self.expected_data_info.clear()
            print("Disconn, clear in queue, txdata has %d items"%len(self.tx_data))
            self.tx_data.clear()
            self.expected_syncs=0
            self.con_handler.report_ser_disconnect() # will change ConnectState
    
    
    def handle_input(self):
        t=time.time()
        if self.con_handler.state!=ConnectState.SER_COM:
            self.handle_while_not_connected()
        if self.con_handler.state==ConnectState.SER_COM:
            while self.expected_data_info:
                if self.ser.in_waiting:
                    i=self.ser.read(1)  # TODO: Read more and loop afterwards? Detect unexpected data?
                    #print("Received:", [int(b) for b in i] )
                    cmd=self.expected_data_info[0]
                    self.expected_data_info=self.expected_data_info[1:]
                    if cmd[0]==CMD_SYNC:
                        if i[0]!=42:
                            print("SYNC ERROR" ,i)
                        self.expected_syncs-=1
                    elif  cmd[0]==CMD_PEEK:
                        # word result callback?
                        self.peek_info[cmd[1]]=i[0]
                        if cmd[2]is not None:
                            addr=cmd[1]-1
                            self.pending_callbacks.append( ( cmd[2] , addr, 256*i[0]+self.peek_info[addr] )  )
                            #cmd[2](addr, 256*i[0]+self.peek_info[addr])
                        #print(self.peek_info) 
                    elif  cmd[0]==CMD_IN:
                        self.io_in_info[cmd[1]]=i[0]
                        #print(self.io_in_info) 
                    self.last_ok_t=max(t,self.last_ok_t)
                else:
                    # nothing received
                    if t>self.last_ok_t+TIMEOUT_SEC:
                        self.ser_disconnect()
                        raise SerNotConnected()
                    break
            else:
                # nothing expected
                self.last_ok_t=max(t,self.last_ok_t)
   

    def request_peek_word(self,addr,result_callback=None): # result callback gets (addr, dataword)
        self.send_command( (CMD_PEEK,addr%256,addr//256), (CMD_PEEK,addr,None) )
        addr+=1
        self.send_command( (CMD_PEEK,addr%256,addr//256), (CMD_PEEK,addr,result_callback) )
    
    def cmd_peek(self, memaddr):
        self.send_command( (CMD_PEEK,memaddr%256,memaddr//256), (CMD_PEEK,memaddr,None) )


    def cmd_in(self, io_addr):
        self.send_command( (CMD_IN,io_addr%256,io_addr//256), (CMD_IN,io_addr,None) )
    
    def cmd_out(self, io_addr, data):
        self.send_command( (CMD_OUT,io_addr%256,io_addr//256, data) )

    def cmd_poke(self, memaddr, data):
        self.send_command( (CMD_POKE,1,memaddr%256,memaddr//256, data) )

    def cmd_multipoke(self, memaddr, data):
        self.send_command( [CMD_POKE,len(data),memaddr%256,memaddr//256]+data )
   
    def run_test(self, seconds=3):
        self.check_initial_connect() # we cannot send anything before making shure the peer listens
        self.dfileaddr=None
        
        def on_dfile_read(addr,data):
            print("DFILE screenaddr read",addr,data)
            self.dfileaddr=data

        self.request_peek_word(16396, on_dfile_read)
        self.flush_tx()
        
        # retrieve initial sync
        t=time.time()
        while self.dfileaddr is None:
            if time.time() > t+3: raise Exception()
            self.handle_input()
        print("sv_dfile",self.dfileaddr)

        self.cmd_poke(self.dfileaddr+1+0, 0) # pos 0,0 of screen
        
        # loop
        i=0
        t=start=time.time()
        while time.time()<start+seconds:
            if i%1000==999 and i<2000:
                print("Speed %.0f pokes/sec"%( 1000/(time.time()-t) ) )
                t=time.time()
            x=random.randint(1,26)
            y=random.randint(1,18)
            v1=random.randint(0,63)
            v2=random.randint(0,63)
            v3=random.randint(0,63)
            if random.randint(0,9)>=5: v1+=128
            if random.randint(0,9)>=5: v2+=128
            if random.randint(0,9)>=5: v3+=128
            memaddr=self.dfileaddr+35+x+33*y
            self.cmd_multipoke(memaddr, [v1,v2,v3]  )
            i+=1
        
        t=time.time()
        while self.expected_data_info and time.time()<t+2:
            self.handle_input()
            
    def load_p_file(self,fname):
        # make sure we have the overlay and loader loaded
        #OVERLAY
        self.send_command( (CMD_FAST,) ) # FAST would use the stack which is our loader space so call this first
        """
        21 76 06        LD HL, 0676H    ; return address in NEXT-LINE like when LOADING
        E3              EX (SP),HL ; E5 PUSH HL
        21 15 40        LD HL,ELINEHI
        34              INC (HL) ; make sure no match during load
        21 09 40        LD HL,4009h    ; start of BASIC area to load
        C3 CF 7F        JP 32719  ; +4000H?
        """
        lod=[]
        lod.append([0xe1, 0xe1, 0xe1,  0x21, 0x76, 0x06, 0xE3]) # E1 pop hl to cleanup 
        lod.append([0x21, 0x15, 0x40, 0x34])
        lod.append([0x21, 0x09, 0x40, 0xC3, ADDR_LOADER%256, ADDR_LOADER//256])
        addr=ADDR_OVERLAY
        for chunk in lod:
            self.cmd_multipoke(addr, chunk  )
            addr+=len(chunk)
        
        # LOADER
        # LOADER
        """ PLOADER:
0084   403C 2B              DEC HL
0085   403D                 ; wait for byte
0086   403D             PLDWLOOP:
0087   403D 3E 3D           LD A, ADDR_SELB+A_LSR
0088   403F D3 EF           OUT (COM_ADDR),A
0089   4041 DB 6F           IN A, (COM_DAT)
0090   4043 E6 01           AND 1            ; bit 0 is RX data ready
0091   4045 28 0A           JR Z, PLDWT
0092   4047                 ; read a byte
0093   4047 3E 38           LD A, ADDR_SELB+A_RHR
0094   4049 D3 EF           OUT (COM_ADDR),A
0095   404B DB 6F           IN A, (COM_DAT)
0096   404D                 ; standard load operation
0097   404D 23              INC HL            ; had a DEC before, so inc heres
0098   404E 77              LD  (HL),A
0099   404F 18 EC           JR PLDWLOOP
0100   4051             PLDWT: ; No byte available, time to check for end
0101   4051                 ; deselect UART here in case this is the last byte
0102   4051 AF              XOR A
0103   4052 D3 EF           OUT (COM_ADDR),A
0104   4054 CD FC 01        CALL UPDATE
0105   4057 18 E3           JR PLOADER    ; follow by dec
        """
        lod=[]
        lod.append([0x2B,0x3E,0x3D,0xD3,0xEF,0xDB,0x6F,0xE6])
        lod.append([0x01,0x28,0x0A,0x3E,0x38,0xD3,0xEF,0xDB])
        lod.append([0x6F,0x23,0x77,0x18,0xEC,0xAF,0xD3,0xEF])
        lod.append([0xCD,0xFC,0x01,0x18,0xE3])
        addr=ADDR_LOADER
        for chunk in lod:
            self.cmd_multipoke(addr, chunk  )
            addr+=len(chunk)

        print("LOADED OVERLAYS")
                  
        self.flush_tx()
        time.sleep(0.02)
        while len(self.tx_data)<self.TXPSIZE: # make sure peer has enough data to start after sync
            self.tx_data.append(CMD_NOP)
        self.tx_data.append(CMD_OVERLAY)
        self.send_pending_tx_data() # we cannot jest flash here as cmd_overlay has to be the latest incoming byte before the file
        #
    
        f=bytearray( open(fname, "rb").read() )
        print("Send file (size %d) in serial data format..."%len(f))
        #print(len(f), " at %.2fkByte/sec"%( ser.baudrate/10.0/1024 ))
        #ser.write(f)
        break_s=0.002
        #print( " throttled to %.2fkByte/sec"%( 64/break_ms/1024 ))
        send_buf=bytearray()
        for i,b in enumerate(f):
            #ser.write([b])
            send_buf.append(b)
            if i%64==2:
                self.ser.write(send_buf)
                send_buf=bytearray()
                time.sleep(break_s)   # 2ms works, 0.5 not , 1 at the edge
        if send_buf: self.ser.write(send_buf) # last <64
        time.sleep(0.1) # make sure peer checks for end 
        print("done ")
        self.ser_disconnect()
       
            

        
