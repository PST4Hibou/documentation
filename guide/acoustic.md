# Acoustic specifications

### Connect the Hassebs

The Hasseb DAC provides 2 channels via multicast and is configurable via an IP address :
- Hasseb 1 : http://192.168.250.11/
- Hasseb 2 : http://192.168.250.12/

Multicast addresses:
- Hasseb 1 : 192.168.250.255:5001
- Hasseb 2 : 192.168.250.255:5004

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
gst-launch-1.0 -v udpsrc address=192.168.250.255 port=5004 multicast-iface=eth0 caps="application/x-rtp, media=(string)audio, clock-rate=(int)48000, channels=(int)2, encoding-name=(string)L24, payload=(int)98" ! rtpjitterbuffer latency=50 ! rtpL24depay ! audioconvert ! autoaudiosink
```

::: info
Notice the UDP & RTP settings must match exactly. __48000Hz__, __2__ channels, __L24__ (PCM 24) encoding, RTP payload dynamic __98__.
:::

### Connect the Dantes

The Dante/Audinate DAC also provides 2 channels via multicast, but Dante Controller application is required to edit the configuration.
As well as for the Hassebs, you need to be on the same network as the Dante devices.
Dante only supports 48kHz of sample rate when using RTP/AES67. Dante AVIO Analog Input Adapter does not support phantom power, which means that your
MICs may require an additional power supply, which is not the case of the Hassebs.

Dante does not let you use any IP prefix you want. 

Multicast addresses:
- Hasseb 1 : 239.69.250.255:5002
- Hasseb 2 : 239.69.250.255:5003

#### Configure the Dantes with the following configuration :

Network settings, in Dante Controller: Vue du dispositif > Configuration réseau:
```
Configurer manuellement une adresse IP: checked
IP address: 192.168.250.13
Subnet mask: 255.255.255.0
DNS: 1.1.1.1
Gateway: 192.168.250.21
```

Stream Settings, Vue du dispositif > Configuration AES67:
```
Mode AES67: Activé
Préfixe multicast RTP: Par défaut
```

Stream Settings, Vue du dispositif > Transmission:
```
Transmission mode: RTP/AES67
All channels: checked
Multicast port: 5003
Multicast IP: 239.69.250.255
```

Test using GStreamer
```
gst-launch-1.0 -v udpsrc address=239.69.250.255 port=5003 multicast-iface=eth0 caps="application/x-rtp, media=(string)audio, clock-rate=(int)48000, channels=(int)2, encoding-name=(string)L24, payload=(int)98" ! rtpjitterbuffer latency=50 ! rtpL24depay ! audioconvert ! autoaudiosink
```

::: info
Notice the UDP & RTP settings must match exactly. __48000Hz__, __2__ channels, __L24__ (PCM 24) encoding, RTP payload dynamic __97__.
:::
