import ctypes
from functions import get_system_info, get_gps_satellites_in_view
from structures import ITR3800_GpsSatellitesInView_t

# Load the radar API DLL
dll_path = "../Software/RadarAPI/library_v1.147/Windows_msvc_2017_x64/ITR3800_radarAPI.dll"  # Replace with the correct path
radar_api = ctypes.WinDLL(dll_path)

# Define types
APIHandle_t = ctypes.c_void_p
ITR3800_Result_t = ctypes.c_int

# Define function prototypes
radar_api.ITR3800_initSystem.argtypes = [ctypes.POINTER(APIHandle_t), ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte]
radar_api.ITR3800_initSystem.restype = ITR3800_Result_t

radar_api.ITR3800_exitSystem.argtypes = [APIHandle_t]
radar_api.ITR3800_exitSystem.restype = ITR3800_Result_t

radar_api.ITR3800_getSystemInfo.argtypes = [APIHandle_t, ctypes.POINTER(ITR3800_SystemInfo_t)]
radar_api.ITR3800_getSystemInfo.restype = ITR3800_Result_t

radar_api.ITR3800_getGpsSatellitesInView.argtypes = [APIHandle_t, ctypes.POINTER(ITR3800_GpsSatellitesInView_t)]
radar_api.ITR3800_getGpsSatellitesInView.restype = ITR3800_Result_t

# Initialize the radar system
handle = APIHandle_t()
result = radar_api.ITR3800_initSystem(ctypes.byref(handle), 192, 168, 31, 200)  # Replace with your radar's IP
if result != 0:
    raise RuntimeError(f"Failed to initialize radar API: Error code {result}")
print("Radar system initialized successfully.")

# Get system information
get_system_info(radar_api, handle)

# Get GPS satellites in view
get_gps_satellites_in_view(radar_api, handle)

# Clean up
result = radar_api.ITR3800_exitSystem(handle)
if result != 0:
    print(f"Failed to clean up radar system: Error code {result}")
else:
    print("Radar system exited successfully.")
