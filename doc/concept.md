

# Serial UART controls ZX81 via Python


### Next steps and to-do's:

* ! Transpose Cam
* ! Eliminate .. in path
* ! Make full 32x24 screen available by overlaying code
* Apps
  * Console
  * Dialog windows, lineditor etc
  * File system browser
  * Telnet etc
  * PiCam save pic as 768 bytes or as 1k Prog with just pause
* ! Load programs via tape or direct (hidden) UART loader
* KB read cycle connected to uppermost window!
* Save programs via `USR` loader
* p Loader as file, loader with break
* ! Loop in server 4800 baud mode to wait for 'OK' from sersrv, or 'SV' from pre-placed `USR` save routine 
* Link to DRIVE
* More generic Overlay for OUT, sound, etc
* Graph mode typing, graphics

zxroot
	USER-FILES				PICS DOCS PROGS
	ZXPI-MEDIA				VIDEO INTERNET SOUND 
	ZXPI-PROGRAMMING		ZX-PYTHON   Z80-ASSEMBLER
	ZXPI-CONTROL-CENTER		OS-SHELL  UPDATES
	
	ZX81-1K
	ZX81-DEMOS+GAMES
	ZX81-TOOLS
	DRIVES

### Pi Config

in boot/config.txt
dtoverlay=pi3-disable-bt
enable_uart=1

sudo cp -rf /media/pi/xxxxx/zxpi /opt/zxpi
sudo nano /etc/


### Next Hardware version
* Reset pushbutton
* plugs?

* IC3 text
* LED polarity
* Tantal smaller
* Pins