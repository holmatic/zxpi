; Compressed low res picture/movie viewer
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


#define SHOW	0207h  ; ROM-Routine
#define FAST	02E7h
#define RCLS	0A2Ah
#define GETKEY	02BBh
#define UPDATE	01FCh	; LOAD/SAVE adress update subroutine in ROM
#define RST_PRTCHAR RST 10H

;;#define VERBOSE 1
 
org     $4009 ; BASIC PROGRAMM
;= System variables ============================================ 
 
   db 0     	;VERSN 
   dw 0     	;E_PPC 
vdfile:
   dw dfile      ;D_FILE 
   dw dfile+1    ;DF_CC 
   dw var   	;VARS 
   dw 0     	;DEST 
eline:
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
   dw line10     ;NXTLIN   line10   dfile  autostart on/off
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


   ds 33    ;Print buffer

membot: 
   ds 30    ;Calculator´s memory area 
   ds 2     ;not used 
 
;= First BASIC line, asm code ================================== 
 
line0: 
   db 0,0   ;line number 
   dw line10-$-2 ;line length 
   db $ea   ; REM 


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
	JP VSTART
VDATA: ; compressed data
#ifdef TESTDATA
	db 071H,030h,078h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH

	db 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h,   01BH
	db 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h,   01BH
	db 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h,   01BH
	db 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h, 013H,014h,018h,014h,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH

	db 0F0H,0F0H,0F0H,0F0H,   01BH
	db 0F0H,0F0H,0F0H,0F0H,   01BH

	db 073H , 02Bh,01Ch , 02Bh,01Dh , 02Bh,01Eh, 02Bh,01Fh ,076H,   01BH


	db 03BH	; frame

	db 073H,034h,0F8h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 073H,034h,0F8h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH

	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH

	db 070H,070H,0F0H,070H,   01BH
	db 070H,070H,0F0H,070H,   01BH

	db 073H , 02Bh,01Ch , 02Bh,01Dh , 02Bh,01Eh, 02Bh,01Fh ,076H,   01BH
	db 03BH	; frame

	db 071H,030h,078h,030h,071H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 073H,034h,0F8h,034h,076H,   01BH
	db 071H,030h,078h,030h,071H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH

	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 071H,030h,0F8h,030h,071H,   01BH
	db 073H,034h,078h,034h,076H,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH
	db 016H,017h,018h,016h, 013H,012h,018h,010h, 013H,017h,017h,017h, 013H,013h,013h,014h,   01BH

	db 070H,070H,0F0H,070H,   01BH
	db 070H,070H,0F0H,070H,   01BH
	db 073H,034h,0F8h,034h,076H,   01BH

	db 073H , 02Bh,01Ch , 02Bh,01Dh , 02Bh,01Eh, 02Bh,01Fh ,076H,   01BH

#endif
	db 03BH	; frame
	db 04BH	; end


VSTART:
RESTART:
	LD DE,VDATA   ; read data
NEWFRAME:
	LD A,62	; dec, expire at 0
	LD (16436),A ; FRAMES
	LD HL,(vdfile) ; video bffer
	INC HL
CHARLOOP:
	LD A,(DE)	; get data
	INC DE
	LD B,A		; backup to B
	AND 08FH	; character to print
	LD C,A		; character to print
	CP 00BH		; one of the special chars
	JR Z,SPECIALCHAR
	; get number of reps
	LD A,B
	RRCA
	RRCA
	RRCA
	RRCA
	AND 7
	INC A
	LD B,A
	LD A,C
WRITELOOP:
	LD (HL),A
	INC HL
	DJNZ WRITELOOP
	JR CHARLOOP

SPECIALCHAR:
	LD A,B    ; get full code
	CP 01BH
	JR NZ,NOSKIPNEXT
	; skip newline
	INC HL
	JR CHARLOOP
NOSKIPNEXT:
	CP 02BH
	JR NZ,NOAPLHA
	; text
	LD A,(DE)	; get direct data
	INC DE
	LD (HL),A
	INC HL
	JR CHARLOOP
NOAPLHA:
	CP 03BH
	JR NZ,NOENDFRAME ; newline etc
	; end frame
	;LD HL,(vdfile) ; video bffer
	;INC HL
	;LD A,45
	;LD (HL),A
WAITTIMER:
	LD A,(16436) ; FRAMES
	CP 50
	JR C,NEWFRAME
	HALT
	JR WAITTIMER

NOENDFRAME:
	CP 04BH
	JR NZ,NORESTART ; newline etc
	; restart all
	HALT
	JR RESTART

NORESTART:
	JR CHARLOOP


 
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

	db $21 ; Char in first pos
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
	ds 32
	db $76
 
;- BASIC-Variables ---------------------------------------- 
 
var: 
   db $80 
 
;- End of program area ---------------------------- 

last: 
 
   end 
