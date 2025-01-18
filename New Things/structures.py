import ctypes

# Satellite information
class SatelliteInfo(ctypes.Structure):
    _fields_ = [
        ("satelliteID", ctypes.c_uint32),    # Unique satellite identifier
        ("signalStrength", ctypes.c_float), # Signal strength in dB
        ("elevation", ctypes.c_float),      # Elevation in degrees
        ("azimuth", ctypes.c_float),        # Azimuth in degrees
    ]

# GPS Satellites in view
class ITR3800_GpsSatellitesInView_t(ctypes.Structure):
    _fields_ = [
        ("count", ctypes.c_uint32),         # Number of satellites in view
        ("satellites", SatelliteInfo * 32)  # Array of up to 32 satellites
    ]

# System information
class ITR3800_SystemInfo_t(ctypes.Structure):
    _fields_ = [
        ("productcode", ctypes.c_uint32),    # Product code
        ("serialNumber", ctypes.c_uint32),  # Serial number
        ("swVersionMajor", ctypes.c_uint32),# Major software version
        ("swVersionMinor", ctypes.c_uint32),# Minor software version
    ]
