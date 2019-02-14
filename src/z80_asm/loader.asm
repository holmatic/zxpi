; SYSINFO81 
; 	GPL
; 	Oliver Lange
; 	Version 1.0.1

; Compile with "tasm -80 -b sysinfo.asm sysinfo.p" 



; 2010/2011: Modifiziert für Spar-Interface mit TTLs - Siehe Forum
; 			 256 Bytes RAM an 3E00h nicht mehr nötig




 
#define db .byte ;  cross-assembler definitions 
#define dw .word 
#define ds .block 
#define org .org 
#define end .end 



#define COM_ADDR  0EFh
#define COM_DAT   06Fh

#define ADDR_LED  020h
#define ADDR_SELA 030h
#define ADDR_SELB 038h
#define A_RHR 00h
#define A_THR 00h
#define A_IER 01h
#define A_FCR 02h
#define A_ISR 02h
#define A_LCR 03h
#define A_MCR 04h
#define A_LSR 05h
#define A_MSR 06h
#define A_SCPAD 07h

#define ADDR_DISABLE 0
#define UPDATE	01FCh	; LOAD/SAVE adress update subroutine in ROM

;;#define VERBOSE 1
 
org     $4009 ; BASIC PROGRAMM
;= System variables ============================================ 
 
   db 0     	;VERSN 
   dw 0     	;E_PPC 
   dw dfile      ;D_FILE 
   dw dfile+1    ;DF_CC 
   dw var   	;VARS 
   dw 0     	;DEST 
   dw var+1      ;E_LINE 
   dw last-1     ;c_ADD 
   dw 0     	;X_PTR 
   dw last  	;STKBOT 
   dw last  	;STKEND 
   db 0     	;BERG 
   dw membot     ;MEM 
   db 0     ;not used 
   db 2     ;DF_SZ 
   dw 1     ;S_TOP 
   db $FF,$FF,$FF     ;LAST_K 
   db 55    ;MARGIN 
   dw line10     ;NXTLIN 
   dw 0     ;OLDPPC 
   db 0     ;FLAGX 
   dw 0     ;STRLEN 
   dw $0C8D      ;T_ADDR 
   dw 0     ;SEED 
   dw $FFFF      ;FRAMES 
   db 0,0   ;COORDS 
   db $BC   ;PR_CC 
   db 33,24      ;S_POSN 
   db 01000000B  ;CDFLAG 


   :ds 33    ;Print buffer --- now used for loader code, all loaded programs need to have the same !
; relocatible loader code
PLOADER:
	DEC HL
	; wait for byte
PLDWLOOP:
	LD A, ADDR_SELB+A_LSR
    OUT (COM_ADDR),A
    IN A, (COM_DAT)
	AND 1			; bit 0 is RX data ready
	JR Z, PLDWT
	; read a byte
	LD A, ADDR_SELB+A_RHR
    OUT (COM_ADDR),A
    IN A, (COM_DAT)
    ; standard load operation
	INC HL			; had a DEC before, so inc heres
	LD  (HL),A
	JR PLDWLOOP
PLDWT: ; No byte available, time to check for end
	; deselect UART here in case this is the last byte
	XOR A
    OUT (COM_ADDR),A
	CALL UPDATE
	JR PLOADER	; follow by dec
PLOADEND:
   ds 4    ; Remaining space of 33 byte print buffer, after 29 byte loader

membot: 
   ds 30    ;Calculator´s memory area 
   ds 2     ;not used 
 
;= First BASIC line, asm code ================================== 
 
line0: 
   db 0,0   ;line number 
   dw line10-$-2 ;line length 
   db $ea   ; REM 


#define ELINE	4014h  ; Systemvariable, die das Ende des abzuspeichernen BASIC-Programs anzeigt
#define ELINEHI	4015h  ; Systemvariable, die das Ende des abzuspeichernen BASIC-Programs anzeigt

#define SHOW	0207h  ; ROM-Routinen
#define FAST	02E7h
#define RCLS	0A2Ah
#define GETKEY	02BBh


#DEFINE RST_PRTCHAR RST 10H
#DEFINE c_SPACE 0
#DEFINE c_NEWLINE 76H
#DEFINE c_0 1CH

#DEFINE c_A 38
#DEFINE c_B (c_A+1)
#DEFINE c_C (c_A+2)
#DEFINE c_D (c_A+3)
#DEFINE c_E (c_A+4)
#DEFINE c_F (c_A+5)
#DEFINE c_G (c_A+6)
#DEFINE c_H (c_A+7)
#DEFINE c_I (c_A+8)
#DEFINE c_J (c_A+9)
#DEFINE c_K (c_J+1)
#DEFINE c_L (c_J+2)
#DEFINE c_M (c_J+3)
#DEFINE c_N (c_J+4)
#DEFINE c_O (c_J+5)
#DEFINE c_P (c_J+6)
#DEFINE c_Q (c_J+7)
#DEFINE c_R (c_J+8)
#DEFINE c_S (c_J+9)
#DEFINE c_T (c_S+1)
#DEFINE c_U (c_S+2)
#DEFINE c_V (c_S+3)
#DEFINE c_W (c_S+4)
#DEFINE c_X (c_S+5)
#DEFINE c_Y (c_S+6)
#DEFINE c_Z (c_S+7)



;
;   === Main entry point ====
;


BASIC_START:
	;CALL RCLS	; CLS
	; get id code
	CALL PRINTMULTI
    db c_S,c_E,c_R,64 ;

	CALL SETCOMREGS
	;db ADDR_SELB+A_LCR,3	; write baud rate end, set wordlenght 8
	db ADDR_SELB+A_MCR,000H	; switch prescaler
	db ADDR_SELB+A_LCR,083H	;
	db ADDR_SELB+0,	0		; LSB of divisor, 0 for ID read
	db ADDR_SELB+1,	0		; MSB of divisor
    db 0FFH	; end

	LD A, ADDR_SELB+1	; ID when divider=0
	CALL READCOMREG
	LD A, ADDR_SELB+0	; ID REV when divider=0
	CALL READCOMREG

	CALL SETCOMREGS
	db ADDR_SELB+A_LCR,083H	; write baud rate
	db ADDR_SELB+0,	192		; LSB of divisor, 192 for 4800 MCR Bit-7=0, or 48 for 1
	db ADDR_SELB+1,	0		; MSB of divisor
	db ADDR_SELB+A_LCR,0BFH	; write Enhanced registers
	db ADDR_SELB+1,	40H		; FTCR - fifo count in scratchpad FCTR[6] = 1
	db ADDR_SELB+A_LCR,3	; write baud rate end, set wordlenght 8
	db ADDR_SELB+A_SCPAD,0	; EMSR (LCR[7] = 0, FCTR[6]=) RX Fifo = 0 or 2
	db ADDR_SELB+A_FCR,7	; enable and reset fifos
    db 0FFH	; end

	;LD A,c_NEWLINE
	;RST_PRTCHAR

	; send byte
	LD A, ADDR_SELB+A_THR
    OUT (COM_ADDR),A

	; dummy read
    ;IN A, (COM_DAT)
    IN A, (COM_DAT)
    IN A, (COM_DAT)

	LD A, 'O'
    OUT (COM_DAT),A
	LD A, 'K'
    OUT (COM_DAT),A

	; wait for input
WTINPLOOP1:
	LD A, ADDR_SELB+A_LSR
    OUT (COM_ADDR),A
WTINPLOOP2:
    IN A, (COM_DAT)
	AND 1			; bit 0 is RX data ready
	JR Z, WTINPLOOP2
	; have data

	LD A, ADDR_SELB+A_RHR
    OUT (COM_ADDR),A
    IN A, (COM_DAT)
	;CALL READCOMREG

	CP 'H'
	JR NZ, NOSWSP
	; Switch speed upon H
	CALL SETCOMREGS
	db ADDR_SELB+A_LCR,083H	; write baud rate
	db ADDR_SELB+0,	2		; LSB of divisor, 4 for 230.4 - 2 for 460.8k   -   MCR Bit-7=0
	db ADDR_SELB+1,	0		; MSB of divisor
	db ADDR_SELB+A_LCR,3	; write baud rate end, set wordlenght 8
	;db ADDR_SELB+A_FCR,7	; enable and reset fifos
    db 0FFH	; end
	JR WTINPLOOP1

NOSWSP:
	CP 'L'
	JR NZ, NOLOAD
	; LOAD a P file
LOADP:
	CALL FAST	; here we go
;	POP HL		; clean up leftover
;	LD HL, 0676H	; return address in NEXT-LINE like when LOADING
;	EX (SP),HL ; PUSH HL
	; copy loader code to some safe location
	LD HL, PLOADER
	;32719 is the highest possible for 29byte loader, allows 966 byte progs for 1k
	LD DE, 32719  ; move to area that possibly holds RAM, TODO find even better spot
	LD BC, PLOADEND-PLOADER
	LDIR
	; ok, go
	LD HL,ELINEHI
	INC (HL) ; make sure no match during load
	LD HL,4009h	; start of BASIC area to load
	JP 32719  ; +4000H?

NOLOAD:
	; send back what was received
	; we have jst read the data, so shold hav correct address
    OUT (COM_DAT),A
	;CALL PRINTHEX
	JR WTINPLOOP1


	
READCOMREG:
    OUT (COM_ADDR),A
    ; read scratch pad
    IN A, (COM_DAT)
    PUSH AF
	CALL PRINTHEX
	XOR A
	RST_PRTCHAR
	XOR A
	RST_PRTCHAR
	POP AF
	RET

	

SETCOMREGS:
	POP HL	; Ret-Adress
SETCOM2:
	LD A,(HL)
	INC HL
	CP  0FFh ; address FF to end
	JR Z,SETCOMEXIT
    OUT (COM_ADDR),A
	LD A,(HL)
	INC HL
    OUT (COM_DAT),A
	JR SETCOM2
SETCOMEXIT:
	JP (HL)



; Print characters after call until bit 6 set, 
;  USES HL
PRINTMULTI:
	POP HL	; Ret-Adress
PRINTMULT2:
	LD A,(HL)
	AND 0BFh
	RST_PRTCHAR
	BIT 6,(HL)
	INC HL
	JR Z,PRINTMULT2
	JP (HL)



; *
; * AUSGABE A IN HEX
; *
PRINTHEX:
	;PUSH HL
#ifdef DIAG
	PUSH BC
	LD C,A		; SAVE
	SRL A
	SRL A
	SRL A
	SRL A
	ADD A,1CH	; Offset to '0'
	RST 10H
	LD A,C
	AND	0FH		; MASK
	ADD A,1CH	; Offset to '0'
	RST 10H
	LD A,C
	POP BC
#endif
	;POP HL
	RET

 
   db $76   ;N/L 
 
line10:
   db 0,10  ;line number 
   dw dfile-$-2  ;line length 
   db $f5   ;PRINT 
   db $d4   ;USR 
   db $c5   ;VAL
   db $0b   ;"
   db $1d   ;1 
   db $22   ;6 
   db $21   ;5 
   db $1d   ;1 
   db $20   ;4 
   db $0b   ;"
   db $76   ;N/L 


   
;- Display file -------------------------------------------- 
 
dfile: 
   db $76 
   db $76,$76,$76,$76,$76,$76,$76,$76 
   db $76,$76,$76,$76,$76,$76,$76,$76 
   db $76,$76,$76,$76,$76,$76,$76,$76 
 
;- BASIC-Variables ---------------------------------------- 
 
var: 
   db $80 
 
;- End of program area ---------------------------- 

last: 
 
   end 
