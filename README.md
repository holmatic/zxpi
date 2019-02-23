# zxpi

This is a small experimental project connecting a ZX81 computer to a Raspberry Pi via
serial interface. The project mainly uses Python3 on the PI but also uses Z80 code
for interfacing (ZX81 as terminal). It can demonstrate things like loading of ZX81 programs,
low-res-camera and internet usage.

***The project is in a very early stage.*** 



## Getting started

First part is about preparing the Raspberry Pi. It is written for the Zero W(H), other models may differ
in terms of what is needed to configure the serial port.

### Configuration of your Raspberry Pi and Installation

This project uses the GPIO serial interface of the Pi. For the Pi Zero W(H), this port is initially used by the
blutooth interface, and thus we have to change the configuration a little. Assuming `nano` as an text editor:

    sudo nano /boot/config.txt 

In the configuration, the following lines have to be changed or added:

    dtoverlay=pi3-disable-bt

    enable_uart=1

Afterwards, a reboot is required to apply the changes

## Installing the project

First, make sure your Pi has access to the internet. This allows to just use `git` to get the latest version.

In the home directory of the `pi`user, apply

	git init
 
    git remote add origin https://github.com/holmatic/zxpi

    git pull origin master 

This should create the `zxpi` project. It is started by

    cd /home/pi/zxpi/src
   
    python3 main.py & 


## Auto-start

If you want it to auto-start the Raspberry Pi side of the software

    sudo nano /etc/rc.local 

And add the start command at the end (but still before `exit`)

    cd /home/pi/zxpi/src && sudo -u pi python3 main.py & 

## The Zeddy side

On the _ZX81_, just enter `LOAD ""` (on a ZX81NU, use `LOAD "-"`)    
    
    