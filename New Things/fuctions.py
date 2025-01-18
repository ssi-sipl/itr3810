import ctypes
from structure import ITR3800_GpsSatellitesInView_t

def get_gps_satellites_in_view(api, handle):
    """
    Retrieves and displays GPS satellites in view using the ITR3800 API.

    :param api: The loaded radar API DLL.
    :param handle: The initialized radar system handle.
    """
    try:
        # Create an instance of the satellites structure
        satellites_info = ITR3800_GpsSatellitesInView_t()

        # Call the ITR3800_getGpsSatellitesInView function
        result = api.ITR3800_getGpsSatellitesInView(handle, ctypes.byref(satellites_info))
        if result != 0:  # Check for errors
            print(f"Error: ITR3800_getGpsSatellitesInView failed with error code {result}")
            return

        # Print the number of satellites
        print(f"Number of satellites in view: {satellites_info.count}")

        # Print details of each satellite
        for i in range(satellites_info.count):
            satellite = satellites_info.satellites[i]
            print(f"Satellite {i + 1}:")
            print(f"  ID: {satellite.satelliteID}")
            print(f"  Signal Strength: {satellite.signalStrength:.2f} dB")
            print(f"  Elevation: {satellite.elevation:.2f}°")
            print(f"  Azimuth: {satellite.azimuth:.2f}°")
            print()

    except Exception as e:
        print(f"An error occurred while retrieving GPS satellites: {e}")
