; Server program for 16C2850 UART
; assumes that the UART is already initialized by the loader program
; 	GPL
; 	Oliver Lange
; 	Version 1.0.1

; Compile with "tasm -80 -b foo.asm foo.p"





 
#define db .byte ;  cross-assembler definitions 
#define dw .word 
#define ds .block 
#define org .org 
#define end .end 

;;#define VERBOSE 1

#define ELINE	4014h  ;
#define ELINEHI	4015h  ;

#define SHOW	0207h  ; ROM-Routinen
#define FAST	02E7h
#define RCLS	0A2Ah
#define GETKEY	02BBh
#define UPDATE	01FCh	; LOAD/SAVE adress update subroutine in ROM


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

#DEFINE COM_ADDR  0EFh
#DEFINE COM_DAT   06Fh

#DEFINE ADDR_LED  020h
#DEFINE ADDR_SELA 030h
#DEFINE ADDR_SELB 038h

#DEFINE A_RHR 00h
#DEFINE A_THR 00h
#DEFINE A_IER 01h
#DEFINE A_FCR 02h
#DEFINE A_ISR 02h
#DEFINE A_LCR 03h
#DEFINE A_MCR 04h
#DEFINE A_LSR 05h
#DEFINE A_MSR 06h
#DEFINE A_SCPAD 07h

#DEFINE ADDR_DISABLE 0

 
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

prbuf:
; ===== JUMP TABLE =====

	; CMD MULTIPOKE
    IN A, (COM_DAT) ; number of bytes
    LD B, A
    IN A, (COM_DAT) ; address low
    LD L, A
    IN A, (COM_DAT) ; address high
    LD H, A
    LD C, COM_DAT   ; prepares
    INIR
	JR ENTRYFAST

	; CMD PEEK
    IN A, (COM_DAT)
    LD L, A   ; address low
    IN A, (COM_DAT)
    LD H, A	  ; address high
    LD A, (HL)
    OUT (COM_DAT),A
	JR ENTRYFAST

	; CMD FAST
	CALL FAST
	JR ENTRYFAST

    ds 33-26-5  ;Print buffer
membot:
; relocatible loader code
   ds 30    ;Calculator´s memory area, used partially by com-init subprocedure
   ds 2     ;not used 
 
;= First BASIC line, asm code ================================== 
 
line0: 
   db 0,0   ;line number 
   dw line10-$-2 ;line length 
   db $ea   ; REM 


;
;   === Main entry point ====
;


BASIC_START:
	LD A, ADDR_SELB+A_THR
    OUT (COM_ADDR),A
	LD DE, JTBLFAST+1

	; CMD SYNC
CMD_SYNC:
	LD A,42
    OUT (COM_DAT),A

WAITFORCHUNK:
	LD B,42
	LD A, ADDR_SELB+A_SCPAD ; scratchpad has fifo level if configured
    ; read number of bytes in receiver
    OUT (COM_ADDR),A
WAITNLP:
    IN A, (COM_DAT)
	SUB B
	JR C, WAITNLP
    ; back to  data read/write
	LD A, ADDR_SELB+A_THR
    OUT (COM_ADDR),A

ENTRYFAST: ; MAINLOOP, also CMD NOP

    IN A, (COM_DAT)
	LD (DE),A  ; self modifying code
JTBLFAST:
	JR ENTRYFAST

; ===== JUMP TABLE =====
#ifdef DIAG

	; CMD MULTIPOKE
    IN A, (COM_DAT) ; number of bytes
    LD B, A
    IN A, (COM_DAT) ; address low
    LD L, A
    IN A, (COM_DAT) ; address high
    LD H, A
    LD C, COM_DAT   ; prepares
    INIR
	JR ENTRYFAST

	; CMD PEEK
    IN A, (COM_DAT)
    LD L, A   ; address low
    IN A, (COM_DAT)
    LD H, A	  ; address high
    LD A, (HL)
    OUT (COM_DAT),A
	JR ENTRYFAST


	; CMD OUT
    IN A, (COM_DAT)
    LD C, A   ; port address high
    IN A, (COM_DAT)
    LD B, A	   ; port address high
    IN A, (COM_DAT)
    OUT (C),A
	JR ENTRYFAST

	; CMD IN
    IN A, (COM_DAT)
    LD C, A   ; port
    IN A, (COM_DAT)
    LD B, A	   ; port address high
    IN A,(C)
    OUT (COM_DAT),A
	JR ENTRYFAST


; ===== END OF JUMP TABLE =====





;  #ifdef DIAG

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
	;POP HL
	RET
#endif
 
   db $76   ;N/L 
 
line10:
   db 0,10  ;line number 
   dw dfile-$-2  ;line length 
   db $f9   ;RAND
   db $d4   ;USR 
   db $1d   ;1 
   db $22   ;6 
   db $21   ;5
   db $1d   ;1
   db $20   ;4
   db $7e   ;FP mark
   db $8f   ;5 bytes FP number
   db $01   ;
   db $04   ;
   db $00   ;
   db $00   ;
   db $76   ;N/L 

   
;- Display file -------------------------------------------- 

dfile: 
   db $76

	db $20 ; Char in first pos
	ds 31
	db $76
	ds 32
	db $76
	ds 32
	db $76
	ds 32
	db $76

	ds 32	;4
	db $76
	ds 32
	db $76
	ds 32
	db $76
	ds 32
	db $76


	ds 32	;8
	db $76
	ds 32
	db $76
	ds 32
	db $76
	ds 32
	db $76

	ds 32	;12
	db $76
	ds 32
	db $76
	ds 32
	db $76
	ds 32
	db $76


	ds 32	;16
	db $76
	ds 32
	db $76
	ds 32
	db $76
	ds 32
	db $76

	ds 32	;20
	db $76
	ds 32
	db $76
	ds 32
	db $76
;	ds 1 ; 6 okay, 8 not
	db $76

 
;- BASIC-Variables ---------------------------------------- 
 
var: 
   db $80 

;- End of program area ---------------------------- 

last: 
 
   end 
