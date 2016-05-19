# R2D2-in-the-sky

This is the core application for the R2D2 made in ISEN : a python application managing the robot who has to be deployed in a Beaglebone, and a Android application to control the robot by phone

##Configuration required
This project needs actually little tweaks et configurations to run smoothly. A bash script (lancement.sh) is already provided to speed up the tweaking, but let's talk a bit more about what it does.

###Software setup

####Video
This application stream video to the smartphone using the software avconv. If it's not installed, do it with a simple line (and a smile):

	sudo apt-get install avconv libav-utils

####Serial
To use this application, you need to enable your serial lines on your beaglebone. It can be done very easily by typing :
	
	echo BB-UART1 > /sys/devices/bone_capemgr.*/slots

This line actually enable the Serial 1. Change BB-UART1 by BB-UART2 to open the Serial 2, and so on.

This application needs a working implementation of Adafruit_BBIO and of pyserial in your python path. Without it, no communication over Serial lines, and no point in the application.

###Material Setup

####Clock setup
The Python application is heavily dependant of your system date ! To detect frames that took too long to transit in the network (time > 2s), the python application use the UTC system hour. 

#####Easy way:
Install ntp and ntpdate to update your system to a reliable (and shared by many devices) hour:

	sudo apt-get install ntp ntpdate

After that, you're good to go. Make sure the service ntpd is started, and if it's not, just type this line:

	sudo service ntp start

#####Hard way:
In our setup, we have our own network, not connected to any other network. So using ntp to synchronise our system clock time is not possible. So we do it the hard way, and make sure our changes stay at each reboot.

If you have to manually set your clock like us, follow this guide :

Begin by deleting the file /etc/adjtime

	sudo rm /etc/adjtime

Set your date at the correct setup :

	sudo date -s MM/JJ/AAAA
	sudo date -s HH:MM:SS

Then update your system to remember this hour:

	sudo hwclock --systohc --utc

This last command line save your actual hour and the difference in time between your BIOS time and your system time in the file /etc/adjtime. At each reboot, it's this file which is used to set your system time.

You shouldn't experiment any problems concerning the time after that.

####Network

We have created a little personalised setup for our lovely R2D2. This setup is made of a small Nano-router, linked by ethernet to the Beaglebone, which host a small LAN (172.17.0.0, netmask 255.255.255.248).

#####DHCP
The Nano router we used in our setup needed a dynamic IP for the ethernet link with the Beaglebone. Let's deploy a DHCP server on that card:

	sudo apt-get install isc-dhcp-server

When it's done, open the /etc/default/isc-dhcp-server.conf and change the line :

	INTERFACES=""

by:

	INTERFACES="eth0"

and change the file /etc/dhcp/dhcpd.conf by adding those lines:

	network 172.16.0.0 netmask 255.255.255.252{
		range 172.16.0.1-172.16.0.1;
		options router 172.16.0.1;
		options broadcasr 172.16.0.3;
	}

then, let the magic begin :

	sudo service isc-dhcp-server restart

#####Ethernet
The Ethernet interface eth0 needs to be configured in a special setup for easier use of the network and of the application. eth0 needs a static IP of 172.16.0.2 with a netmask of 255.255.255.252. You can change that by typing:

	ifdown eth0

then, going to the /etc/network/interfaces file, and change the line:

	#auto eth0
	#ip eth0 inet dhcp

by :

	auto eth0
	ip eth0 inet static
		address 172.16.0.2
		netmask 255.255.255.252
		options router 172.16.0.1

Then, let's make that visible on the network:

	ifup eth0

## How to install

Python application :
  1. Put the file lancement.sh, the file controleur.py and the folder classes in AppliPythonBeaglebone in your home directory
  2. Add the bash script to the crontab of your Beaglebone @reboot
  3. Congrats ! You now have a python script automatically launched and which will be restarted if a problem ever arise

Android Application:
  1. You can find the .apk in the release.
  2. After, install the .apk on your device
  3. You can control R2D2 !
