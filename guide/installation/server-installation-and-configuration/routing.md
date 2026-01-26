# Routing

You must have an ip on the same network as the devices.

```bash
sudo ip addr add 192.168.250.11/24 dev enp3s0
```

## Auto discovery

For the Yamaha autodiscovery to work, you need to be in the same subnet as the device and have the broadcast route set up with the correct source IP.

```bash
sudo ip route add 224.0.0.0/4 dev enp3s0 src 192.168.250.11
```