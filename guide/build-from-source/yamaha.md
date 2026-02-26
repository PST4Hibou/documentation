# Yamaha Tio1608-D Controller

## Manuel Officiel

[Download Yamaha Tio1608-D Owner's Manual (CA)](https://ca.yamaha.com/en/download/files/2323669/)

## JSON Configuration Fields Breakdown

| Field                             | Value             | Role in Hibou                                                                     |
| -------                           | -------           | ---------------                                                                   |
| `ha_gains`                        | `[30,30,30,30]`   | Fixed preamp gains                                                                |
| `multicast_ip`                    | `239.69.250.255`  | GStreamer RX target: `udpsrc port=5005 address=239.69.250.255`                    |
| `clock_rate`                      | `48000`           | Audio sync for drone AI datasets processing                                       |
| `interface`                       | `enp3s0`          | `ip maddr add 239.69.250.255 dev enp3s0` for IGMP multicast                       |
| `nb_channels`                     | `4`               | Active audio channels from Tio1608                                                |
| `rtp_payload`                     | `99`              | RTP payload type                                                                  |
| `port`                            | `5005`            | RTP/UDP port for multicast audio reception                                        |
| `model`                           | `"1966"`          | Dante device ID uniquely identifying Tio1608-D hardware                           |

```json
{
    "controllers": [
        {
            "name": "YamahaTio1608",
            "ip": "192.168.250.15",
            "ha_gains": [30, 30, 30, 30],
            "devices": [
                {
                    "name": "Y001-Yamaha-Tio1608-D2-8f6e69",
                    "model": "1966",
                    "ipv4": "192.168.250.16",
                    "port": 5005,
                    "nb_channels": 4,
                    "multicast_ip": "239.69.250.255",
                    "rtp_payload": 99,
                    "interface": "enp3s0",
                    "clock_rate": 48000
                }
            ]
        }
    ]
}
```
