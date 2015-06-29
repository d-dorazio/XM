#!/bin/bash

# native hostapd, so only officially supported drivers will work
sudo apt-get install isc-dhcp-server hostapd

# backup
mkdir ./backup
cp /etc/dhcp/dhcpd.conf ./backup/
cp /etc/default/isc-dhcp-server ./backup/
cp /etc/network/interfaces ./backup/
cp /etc/default/hostapd ./backup/
cp /etc/hostapd/hostapd.conf ./backup/
cp /etc/sysctl.conf ./backup/
cp /etc/iptables.ipv4.nat ./backup/
cp /etc/default/ifplugd ./backup


# working
sudo cp ./files/dhcpd.conf /etc/dhcp/

sudo cp ./files/isc-dhcp-server /etc/default/


sudo ifconfig wlan0 down


sudo cp ./files/interfaces /etc/network/
sudo cp ./files/ifplugd /etc/default

sudo sh -c "echo DAEMON_CONF='/etc/hostapd/hostapd.conf' >> /etc/default/hostapd"

#ssid=XMnet
#wpa=2
#wpa_passphrase=xmnetpwd
sudo cp ./files/hostapd.conf /etc/default/hostapd.conf

sudo sh -c "echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf " 


sudo ifconfig wlan0 up


# NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT


sudo update-rc.d hostapd enable 
sudo update-rc.d isc-dhcp-server enable


sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"


sudo reboot