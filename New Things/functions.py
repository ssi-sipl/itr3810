import ctypes
from structures import ITR3800_GpsSatellitesInView_t, ITR3800_SystemInfo_t

def get_system_info(api, handle):
    """
    Retrieves and displays radar system information using the ITR3800 API.
    """
    try:
        system_info = ITR3800_SystemInfo_t()
        result = api.ITR3800_getSystemInfo(handle, ctypes.byref(system_info))
        if result != 0:
            print(f"Error: ITR3800_getSystemInfo failed with error code {result}")
            return

        print(f"Device:           ITR-{system_info.productcode}")
        print(f"Serial Number:    {system_info.serialNumber}")
        print(f"Software Version: {system_info.swVersionMajor}.{system_info.swVersionMinor:03d}")

    except Exception as e:
        print(f"An error occurred while retrieving system info: {e}")

def get_gps_satellites_in_view(api, handle):
    """
    Retrieves and displays GPS satellites in view using the ITR3800 API.
    """
    try:
        satellites_info = ITR3800_GpsSatellitesInView_t()
        result = api.ITR3800_getGpsSatellitesInView(handle, ctypes.byref(satellites_info))
        if result != 0:
            print(f"Error: ITR3800_getGpsSatellitesInView failed with error code {result}")
            return

        print(f"Number of satellites in view: {satellites_info.count}")
        for i in range(satellites_info.count):
            satellite = satellites_info.satellites[i]
            print(f"Satellite {i + 1}:")
            print(f"  ID: {satellite.satelliteID}")
            print(f"  Signal Strength: {satellite.signalStrength:.2f} dB")
            print(f"  Elevation: {satellite.elevation:.2f}°")
            print(f"  Azimuth: {satellite.azimuth:.2f}°")

    except Exception as e:
        print(f"An error occurred while retrieving GPS satellites: {e}")
