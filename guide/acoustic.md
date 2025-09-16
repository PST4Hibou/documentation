# Acoustic specifications

### Connect the Hassebs

The Hasseb DAC provides 2 channels via broadcasts and is configurable via an IP address :
- Hasseb 1 : http://192.168.250.11/ with port 5004
- Hasseb 2 : http://192.168.250.12/ with port 5001

::: warning
Add an ip in the correct network to your computer

`sudo ip addr add 192.168.250.79/24 dev enp3s0`
:::

#### Configure the Hassebs with the following configuration :

Network settings
```
DHCP: Off
IP address: 192.168.250.11
Subnet mask: 255.255.255.0
Default gateway: 192.168.250.21
```

Stream Settings
```
Add IP address manually for the output stream: Checked
IP address: 192.168.250.255:5004
```

Test using GStreamer
```
gst-launch-1.0 -v udpsrc port=5004 caps="application/x-rtp, media=(string)audio, clock-rate=(int)48000, channels=(int)2, encoding-name=(string)L24, payload=(int)98" ! rtpjitterbuffer latency=50 ! rtpL24depay ! audioconvert ! autoaudiosink
```