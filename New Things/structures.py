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

# Object information
class ITR3800_Object_t(ctypes.Structure):
    _fields_ = [
        ("objectID", ctypes.c_uint32),      # Unique object identifier
        ("x", ctypes.c_float),             # X-coordinate (meters)
        ("y", ctypes.c_float),             # Y-coordinate (meters)
        ("z", ctypes.c_float),             # Z-coordinate (meters)
        ("velocity", ctypes.c_float),      # Speed of the object (m/s)
        ("objectClass", ctypes.c_uint8),   # Object classification (e.g., pedestrian, vehicle)
        ("signalStrength", ctypes.c_float) # Signal strength (dB)
    ]

# Object list
class ITR3800_ObjectList_t(ctypes.Structure):
    _fields_ = [
        ("nrOfTracks", ctypes.c_uint32),              # Number of objects
        ("objects", ITR3800_Object_t * 256)          # Array of up to 256 objects
    ]

