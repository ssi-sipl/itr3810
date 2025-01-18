import ctypes

# Load the DLL
dll_path = "./Software/RadarAPI/library_v1.147/Windows_msvc_2017_x64/ITR3800_radarAPI.dll"  # Replace with the actual path
radar_api = ctypes.WinDLL(dll_path)

print(type(radar_api))
print(dir(radar_api))

APIHandle_t = ctypes.c_void_p
ITR3800_Result_t = ctypes.c_int
uint8_t = ctypes.c_ubyte
float32_t = ctypes.c_float

class ITR3800_Object_t(ctypes.Structure):
    _fields_ = [
        ("objectID", ctypes.c_uint32),      # Unique object identifier
        ("x", ctypes.c_float),             # X-coordinate (meters)
        ("y", ctypes.c_float),             # Y-coordinate (meters)
        ("z", ctypes.c_float),             # Z-coordinate (meters)
        ("velocity", ctypes.c_float),      # Speed of the object (m/s)
        ("objectClass", ctypes.c_uint8),   # Object classification
        ("signalStrength", ctypes.c_float) # Signal strength (dB)
    ]

class ITR3800_ObjectList_t(ctypes.Structure):
    _fields_ = [
        ("nrOfTracks", ctypes.c_uint32),      # Number of detected objects
        ("objects", ITR3800_Object_t * 256)  # Array of up to 256 objects
    ]

# Define function prototypes
radar_api.ITR3800_initSystem.argtypes = [ctypes.POINTER(APIHandle_t), uint8_t, uint8_t, uint8_t, uint8_t]
radar_api.ITR3800_initSystem.restype = ITR3800_Result_t

radar_api.ITR3800_exitSystem.argtypes = [APIHandle_t]
radar_api.ITR3800_exitSystem.restype = ITR3800_Result_t

class ITR3800_SystemInfo_t(ctypes.Structure):
    _fields_ = [
        ("productcode", ctypes.c_int),       # Product code
        ("serialNumber", ctypes.c_int),     # Serial number
        ("swVersionMajor", ctypes.c_int),   # Major software version
        ("swVersionMinor", ctypes.c_int),   # Minor software version
    ]

radar_api.ITR3800_getSystemInfo.argtypes = [APIHandle_t, ctypes.POINTER(ITR3800_SystemInfo_t)]
radar_api.ITR3800_getSystemInfo.restype = ITR3800_Result_t


handle = APIHandle_t()
result = radar_api.ITR3800_initSystem(ctypes.byref(handle), 192, 168, 31, 200)
if result != 0:
    raise RuntimeError(f"Failed to initialize radar API: Error code {result}")
print("Radar system initialized successfully.")

# Retrieve system information
system_info = ITR3800_SystemInfo_t()
result = radar_api.ITR3800_getSystemInfo(handle, ctypes.byref(system_info))
if result == 0:
    print(f"Device:           ITR-{system_info.productcode}")
    print(f"Serial:           {system_info.serialNumber}")
    print(f"Software Version: {system_info.swVersionMajor}.{system_info.swVersionMinor:03d}")
else:
    print(f"Failed to retrieve system information: Error code {result}")


# Retrieve object list
try:
    object_list = ITR3800_ObjectList_t()
    result = radar_api.ITR3800_getObjectList(handle, ctypes.byref(object_list))
    if result != 0:
        raise RuntimeError(f"Failed to retrieve object list: Error code {result}")

    if object_list.nrOfTracks == 0:
        print("No objects detected.")
    else:
        print(f"Number of objects detected: {object_list.nrOfTracks}")
        for i in range(object_list.nrOfTracks):
            obj = object_list.objects[i]
            print(f"Object ID: {obj.objectID}, Position: ({obj.x}, {obj.y}, {obj.z}), "
                  f"Velocity: {obj.velocity}, Class: {obj.objectClass}, Signal Strength: {obj.signalStrength}")

except Exception as e:
    print(f"An error occurred while retrieving the object list: {e}")


# Clean up
result = radar_api.ITR3800_exitSystem(handle)
if result == 0:
    print("Radar system exited successfully.")
else:
    print(f"Failed to exit radar system: Error code {result}")

# Define Function Prototypes
# Example: ITR3800_getObjectList(handle, object_list)
# radar_api.ITR3800_getObjectList.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
# radar_api.ITR3800_getObjectList.restype = ctypes.c_int

# # Initialize Radar API
# handle = ctypes.c_void_p()
# result = radar_api.ITR3800_initSystem(ctypes.byref(handle))
# if result != 0:
#     raise RuntimeError(f"Failed to initialize radar API: Error code {result}")
# else:
#     print("Radar system initialized successfully.")

# # Retrieve Object List
# object_list = ctypes.c_void_p()
# result = radar_api.ITR3800_getObjectList(handle, ctypes.byref(object_list))
# if result == 0:
#     print("Successfully retrieved object list.")
# else:
#     print(f"Error retrieving object list: {result}")

# # Clean Up
# radar_api.ITR3800_exitSystem(handle)
# print("Radar system exited.")
