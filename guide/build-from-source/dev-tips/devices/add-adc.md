# Adding a New ADC Device

ADC (Analog-to-Digital Converter) devices are used to convert analog signals (e.g., audio input) into digital data streams.
In this system, ADC devices operate over IP (usually Ethernet) and communicate using RTP (Real-Time Transport Protocol).

Currently, only the Audinate AVIO AI2 is supported.
However, the system is designed to make adding new devices simple — as long as the new device follows the same network audio specification.

### Device Requirements

A device can be integrated if it satisfies the following:

- ✅ Has an IPv4 address (typically used for Audio over Ethernet)
- ✅ Uses RTP (Real-Time Transport Protocol) for audio streaming

That’s all that’s required — no additional protocol changes or low-level modifications are needed.


### Integration Overview

All network audio devices are managed through a vendor-specific manager class that inherits from the abstract base class:

```python
class BaseVendor(abc.ABC):
"""Base class for all network audio device managers."""
```

To add a new ADC device, you must create a subclass of BaseVendor that implements the three required methods:
    
- `_scan_devices()` — the asynchronous discovery logic
- `scan_devices()` — the synchronous wrapper around _scan_devices()
- `to_device()` — the conversion from raw discovery data to the internal `Device` model


### Step-by-Step: Adding a New Vendor

#### 1. Create a New Vendor Class

Create a new Python class under the appropriate vendor module, for example:

```python
class MyVendorADC(BaseVendor):
    """Vendor manager for MyVendor ADC network audio devices."""

```


#### 2. Implement _scan_devices()

This asynchronous method performs the actual discovery of devices on the network.
It should return a list of raw device objects or data structures.

Example:

```python
@staticmethod
async def _scan_devices() -> List[TSource]:
    """
    Discover MyVendor ADC devices asynchronously.

    Returns:
        List[TSource]: Raw device information (e.g., IP, name, RTP stream data).
    """
    devices = await discover_myvendor_devices()  # Custom discovery logic
    return devices
```


#### 3. Implement scan_devices()

Provide a synchronous wrapper around `_scan_devices()` to make it usable in non-async contexts.

Example:

```python
@classmethod
def scan_devices(cls) -> List[TTarget]:
    """
    Synchronously discover MyVendor ADC devices.

    Returns:
        List[TTarget]: List of converted internal Device models.
    """
    return asyncio.run(cls._scan_devices())
```

#### 4. Implement to_device()

Convert the raw discovery data into the internal `Device` model expected by the system.

Example:

```python
@staticmethod
def to_device(device: TSource) -> Device:
    """
    Convert a discovered raw device into the internal Device model.

    Args:
        device (TSource): Raw device information.

    Returns:
        TTarget: Normalized Device model.
    """
    return ADCDevice(
        name=device.name,
        model=device.model_id,
        ipv4=str(device.ipv4),
        port=res.get("multicast_port"),
        multicast_ip=res.get("multicast_ip"),
        rtp_payload=res.get("rtp_payload"),
        interface=interface,
        clock_rate=48000,
    )
```

A device has the following structure:

```python
class ADCDevice:
    name: str
    model: str
    ipv4: str
    port: int
    multicast_ip: str
    rtp_payload: int
    interface: str
    clock_rate: int
```

### Example Directory Structure

```shell
├── adc_devices
│   └── vendors
│       ├── audinate
│       │    └── avio_ai2.py
│       └── base_vendor.py

```

#### Example

```python
class MyVendorADC(BaseVendor):
    """MyVendor ADC device integration."""

    @staticmethod
    async def _scan_devices() -> List[TSource]:
        # Replace with actual discovery code
        return [RawDevice(name="MyVendor ADC1", ip="192.168.1.20")]

    @classmethod
    def scan_devices(cls) -> List[TTarget]:
        devices = asyncio.run(cls._scan_devices())
        return [cls.to_device(d) for d in devices]

    @staticmethod
    def to_device(device: TSource) -> TTarget:
        return Device(
            name=device.name,
            ip_address=device.ip,
            protocol="RTP",
            vendor="MyVendor",
        )

```
