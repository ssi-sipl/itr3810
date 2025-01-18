import ctypes

class SatelliteInfo(ctypes.Structure):
    _fields_ = [
        ("satelliteID", ctypes.c_uint32),   # Unique satellite identifier
        ("signalStrength", ctypes.c_float),  # Signal strength in dB
        ("elevation", ctypes.c_float),      # Elevation in degrees
        ("azimuth", ctypes.c_float),        # Azimuth in degrees
    ]

class ITR3800_GpsSatellitesInView_t(ctypes.Structure):
    _fields_ = [
        ("count", ctypes.c_uint32),          # Number of satellites in view
        ("satellites", SatelliteInfo * 32),  # Array of up to 32 satellites
    ]
