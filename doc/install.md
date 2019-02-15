

# Serial UART controls ZX81 via Python


### Next steps and to-do's:

* ! Make full 32x24 screen available by overlaying code
* Apps
    * Console
    * Dialog windows, lineditor etc
    * File system browser
    * Telnet etc
* ! Load programs via tape or direct (hidden) UART loader
* KB read cycle connected to uppermost window!
* Save programs via `USR` loader
* ! Loop in server 4800 baud mode to wait for 'OK' from sersrv, or 'SV' from pre-placed `USR` save routine 
* PiCam save pic etc
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


### Pi Config


cp -rf /media/pi/xxxxx/zxpi ~/

 sudo nano /boot/config.txt 

dtoverlay=pi3-disable-bt
enable_uart=1

 sudo nano /etc/rc.local 
 
 git remote add origin https://github.com/holmatic/zxpi
 git pull origin master 
 cd /home/pi/zxpi/zxroot ln -s /media/pi drives

 cd /home/pi/zxpi/src && sudo -u pi python3 main.py & 


### Next Hardware version
* Reset pushbutton
* plugs?

* IC3 text
* LED polarity
* Tantal smaller
* Pins