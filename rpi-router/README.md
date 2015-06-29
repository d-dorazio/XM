Rpi-Router
===========
Turn your boring Raspberry PI into a fully working WiFi router.
It hasn't got anything to do with XM actually, it's here just to
simplify the build process. The Raspberry PI should have Raspbian as OS.


Use
=====
To apply the config just do:
```bash
sudo ./apply-config.sh
```
and wait until it finishes rebooting.


Hostapd
=========
It uses [hostapd](http://w1.fi/hostapd/) to create an access point. 
Obviously Raspberry PI doesn't come with a wireless network interface so
we need to buy a WiFi dongle. Be careful with the dongle you want to
use because not every dongle can act as an access point and the actual 
configuration works with cfg80211 based drivers(using nl80211 interface).
If you have got a dongle with another driver refer to the 
[hostapd documentation](https://wireless.wiki.kernel.org/en/users/documentation/hostapd).


Network configuration
=======================

##Access Point
By default it will create a wpa2 network with ssid XMnet and password xmnetpwd. 
We highly suggest changing the password for obvious reasons. To change these settings
just search for ssid, wpa_passphrase and wpa [here](files/hostapd.conf) and feel free to modify them.

##DHCP
The created network will be 192.168.0.0/24 and the Raspberry PI
will have a static IP(192.168.0.1) assigned on its wlan interface. DHCP is enabled
and it will serve IPs from 192.168.0.2 to 192.168.0.50.
The clients will use the google servers and the Raspberry PI itself(even though it's
not yet implemented) as DNS servers.
To modify dhcp settings modify [this](files/dhcpd.conf).

##Nat
This configuration also sets up NAT between wlan0 and eth0. The IP of the last one
is obtained by DHCP.
