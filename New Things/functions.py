import ctypes
from structures import ITR3800_GpsSatellitesInView_t, ITR3800_SystemInfo_t, ITR3800_ObjectList_t

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

def get_gps_coordinates(api, handle):
    """
    Retrieves and displays the GPS coordinates of the radar device.

    :param api: The loaded radar API DLL.
    :param handle: The initialized radar system handle.
    :return: A tuple containing (latitude, longitude) or None if no signal.
    """
    try:
        # Define variables for latitude and longitude
        lat = ctypes.c_float
        lng = ctypes.c_float

        # Call the API function
        result = api.ITR3800_getGpsCoordinates(handle, ctypes.byref(lat), ctypes.byref(lng))
        if result != 0:  # Check for errors
            raise RuntimeError(f"Error: ITR3800_getGpsCoordinates failed with error code {result}")

        # Check for no GPS signal
        if lat.value == 0.0 and lng.value == 0.0:
            print("GPS location: no signal")
            return None

        # Return the GPS coordinates
        print(f"GPS location: Latitude = {lat.value:.5f}°, Longitude = {lng.value:.5f}°")
        return lat.value, lng.value

    except Exception as e:
        print(f"An error occurred while retrieving GPS coordinates: {e}")
        return None

def get_object_list(api, handle):
    """
    Retrieves and displays the object list from the radar device.

    :param api: The loaded radar API DLL.
    :param handle: The initialized radar system handle.
    :return: A list of objects or an empty list if no objects are found.
    """
    try:
        # Create an instance of the object list structure
        object_list = ITR3800_ObjectList_t()

        # Call the API function
        result = api.ITR3800_getObjectList(handle, ctypes.byref(object_list))
        if result != 0:
            raise RuntimeError(f"Error: ITR3800_getObjectList failed with error code {result}")

        # Check if there are no objects
        if object_list.nrOfTracks == 0:
            print("No objects detected.")
            return []

        # Parse the object list
        objects = []
        print(f"Number of objects: {object_list.nrOfTracks}")
        for i in range(object_list.nrOfTracks):
            obj = object_list.objects[i]
            objects.append({
                "objectID": obj.objectID,
                "x": obj.x,
                "y": obj.y,
                "z": obj.z,
                "velocity": obj.velocity,
                "objectClass": obj.objectClass,
                "signalStrength": obj.signalStrength
            })

        return objects

    except Exception as e:
        print(f"An error occurred while retrieving the object list: {e}")
        return []

def remove_object(api, handle, object_id):
    """
    Removes a specific object from the radar's object list.

    :param api: The loaded radar API DLL.
    :param handle: The initialized radar system handle.
    :param object_id: The ID of the object to remove.
    """
    try:
        # Call the API function
        result = api.ITR3800_removeObject(handle, ctypes.c_uint32(object_id))
        if result != 0:
            raise RuntimeError(f"Error: ITR3800_removeObject failed with error code {result}")

        print(f"Object with ID {object_id} removed successfully.")

    except Exception as e:
        print(f"An error occurred while removing the object: {e}")