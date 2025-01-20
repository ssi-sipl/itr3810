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



handle = APIHandle_t()

# --------------------------------------------------------------------------
# Define function prototypes
radar_api.ITR3800_initSystem.argtypes = [ctypes.POINTER(APIHandle_t), uint8_t, uint8_t, uint8_t, uint8_t]
radar_api.ITR3800_initSystem.restype = ITR3800_Result_t

result = radar_api.ITR3800_initSystem(ctypes.byref(handle), 192, 168, 31, 200)
print("Init Result: ", result)
if result != 0:
    raise RuntimeError(f"Failed to initialize radar API: Error code {result}")
    exit()
print("Radar system initialized successfully.")
print(handle.value)

#-----------------------------------------------------------------------------

class ITR3800_SystemInfo_t(ctypes.Structure):
    _fields_ = [
        ("productcode", ctypes.c_int),       # Product code
        ("serialNumber", ctypes.c_int),     # Serial number
        ("swVersionMajor", ctypes.c_int),   # Major software version
        ("swVersionMinor", ctypes.c_int),   # Minor software version
    ]

radar_api.ITR3800_getSystemInfo.argtypes = [APIHandle_t, ctypes.POINTER(ITR3800_SystemInfo_t)]
radar_api.ITR3800_getSystemInfo.restype = ITR3800_Result_t

# Retrieve system information
system_info = ITR3800_SystemInfo_t()
result = radar_api.ITR3800_getSystemInfo(handle, ctypes.byref(system_info))
print("System Info Result: ", result)
if result == 0:
    print(f"Device:           ITR-{system_info.productcode}")
    print(f"Serial:           {system_info.serialNumber}")
    print(f"Software Version: {system_info.swVersionMajor}.{system_info.swVersionMinor:03d}")
else:
    print(f"Failed to retrieve system information: Error code {result}")

#-----------------------------------------------------------------------------

version = ctypes.c_float()

radar_api.ITR3800_getApiVersion.argtypes = [ctypes.POINTER(ctypes.c_float)]
radar_api.ITR3800_getApiVersion.restype = ITR3800_Result_t

result = radar_api.ITR3800_getApiVersion(ctypes.byref(version))
print("getAPIVersion Result: ", result)
if result == 0:  # Assuming ITR3800_API_ERR_OK = 0
    print(f"API Version: {version.value}")
else:
    print(f"Error occurred: {result}")

#-----------------------------------------------------------------------------

class ITR3800_Description_t(ctypes.Structure):
    _fields_ = [("description", ctypes.c_char * 256),  # Assuming 256 as max length for description
                ("descriptionLength", ctypes.c_int8)]  # uint8_t is an unsigned 8-bit integer


radar_api.ITR3800_getDescription.argtypes = [APIHandle_t, ctypes.POINTER(ITR3800_Description_t)]
radar_api.ITR3800_getDescription.restype = ITR3800_Result_t

description = ITR3800_Description_t()

result = radar_api.ITR3800_getDescription(APIHandle_t,ctypes.byref(description))
print("Description Result: ", result)

if result == 0:
    print(f"Description: {description.description.decode('utf-8')}")
    print(f"Description Length: {description.descriptionLength}")
else:
    print(f"Error occurred: {result}")

#-----------------------------------------------------------------------------



radar_api.ITR3800_exitSystem.argtypes = [APIHandle_t]
radar_api.ITR3800_exitSystem.restype = ITR3800_Result_t
# Clean up
result = radar_api.ITR3800_exitSystem(handle)
print("Exit Result: ", result)
if result == 0:
    print("Radar system exited successfully.")
else:
    print(f"Failed to exit radar system: Error code {result}")

#-----------------------------------------------------------------------------


