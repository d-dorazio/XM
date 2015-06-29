XM(eXaM)
================
XM is a platform for building robots and in particular whatever can be
compared to a rover. It uses a Raspberry PI acting as a router and web server
and an Arduino to control motors and in general hardware.


Install
========
To install the software for Arduino the only simple way is to use the official
IDE. You could try with [Ino](http://inotool.org/) at your own risk.

To install the API we provide basic instructions for Raspbian(therefore a 
Debian based distro).

```bash
git clone https://github.com/d-dorazio/XM.git ~/XM
cd ~/XM

cd rpi-router/
sudo ./apply-config.sh      # access point setup

cd ../api

# api dependencies
sudo ./install_motion-jpeg.sh
sudo apt-get install espeak
sudo pip3 install -r requirements.txt

cd ..

# adjust XMAPI in xm.sh if the user isn't pi
sudo cp ./xm.sh /etc/init.d/
sudo update-rc.d xm.sh
sudo service xm.sh start

```



Project structure
===================
Every subfolder relative to this file contains a module that can
be used and substituted easily without corrupting the entire project.
Every module has a separate README for your happiness!


What a strange name, isn't it?
===============================
XM is named the way it is because it's my thesis for my high school exam
and because in some way it reminds me to some Asimov's novels.


TODO
=======
- [x] Let a Raspberry PI power up into a WiFi router!
- [ ] Make the Raspberry PI as a DNS Server too!
- [ ] Design the electronic schema of the rover
- [x] Design the most flexible and easy to use protocol between Arduino and Raspberry PI
- [x] Implement the protocol Arduino side
- [x] Implement the protocol Raspberry PI side  
- [ ] Have fun :smile:!
