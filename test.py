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

result = radar_api.ITR3800_getDescription(handle,ctypes.byref(description))
print("Description Result: ", result)

if result == 0:
    print(f"Description Length: {description.descriptionLength}")
    print(f"Description: {description.description.decode('utf-8', 'ignore')}")
else:
    print(f"Error occurred: {result}")

#-----------------------------------------------------------------------------
print("Newwwwwwwww")

class ITR3800_TrackClass_u(ctypes.Union):
    _fields_ = [
        ("ITR3800_TrackClass", ctypes.c_uint32),
        ("dummy", ctypes.c_uint32)
    ]

print("Newwwwwwwww2")


class ITR3800_TrackedObject_t(ctypes.Structure):
    _fields_ = [
        ("ui32_objectID", ctypes.c_uint32),
        ("ui16_ageCount", ctypes.c_uint16),
        ("ui16_predictionCount", ctypes.c_uint16),
        ("ui16_staticCount", ctypes.c_uint16),
        ("f32_trackQuality", ctypes.c_float),
        ("classID", ITR3800_TrackClass_u),
        ("si16_motion_eventZoneIndex", ctypes.c_int16),
        ("si16_presence_eventZoneIndex", ctypes.c_int16),
        ("si16_loop_eventZoneIndex", ctypes.c_int16),
        ("f32_positionX_m", ctypes.c_float),
        ("f32_positionY_m", ctypes.c_float),
        ("f32_velocityX_mps", ctypes.c_float),
        ("f32_velocityY_mps", ctypes.c_float),
        ("f32_velocityInDir_mps", ctypes.c_float),
        ("f32_directionX", ctypes.c_float),
        ("f32_directionY", ctypes.c_float),
        ("f32_distanceToFront_m", ctypes.c_float),
        ("f32_distanceToBack_m", ctypes.c_float),
        ("f32_length_m", ctypes.c_float),
        ("f32_width_m", ctypes.c_float),
    ]
    _pack_ = 1

print("Newwwwwwwww3")


class ITR3800_EventMessage_t(ctypes.Structure):
    _fields_ = [
        ("c_eventMessage", ctypes.c_char * 256),  # Assuming max length
        ("ui8_eventMessageLength", ctypes.c_uint8)
    ]

print("Newwwwwwwww4")


class ITR3800_EventMessageList_t(ctypes.Structure):
    _fields_ = [
        ("eventMessages", ITR3800_EventMessage_t * 10),  # Assuming max 10 messages
        ("nrOfMessages", ctypes.c_uint8)
    ]

print("Newwwwwwwww5")


class ITR3800_ObjectListError_u(ctypes.Union):
    _fields_ = [
        ("ITR3800_ObjectListError", ctypes.c_uint32),
        ("dummy", ctypes.c_uint32)
    ]

print("Newwwwwwwww6")


class ITR3800_ObjectList_t(ctypes.Structure):
    _fields_ = [
        ("protocolVersion", ctypes.c_uint16),
        ("reserved_0", ctypes.c_uint8),
        ("configurationChanged", ctypes.c_uint8),
        ("systemState", ctypes.c_uint32),
        ("error", ITR3800_ObjectListError_u),
        ("timestamp_ms", ctypes.c_uint32),
        ("frameID", ctypes.c_uint16),
        ("nrOfTracks", ctypes.c_uint16),
        ("trackedObjects", ITR3800_TrackedObject_t * 50),  # Assuming max 50 tracked objects
        ("eventMessages", ITR3800_EventMessageList_t),
        ("reserved0", ctypes.c_float),
        ("reserved1", ctypes.c_float),
        ("reserved2", ctypes.c_float),
        ("reserved3", ctypes.c_float),
    ]

print("Newwwwwwwww7")


object_list = ITR3800_ObjectList_t()
 # Create a new object list structure
# Set the argument and return types for the function

print("Newwwwwwwww8")



radar_api.ITR3800_getObjectList.argtypes = [APIHandle_t, ctypes.POINTER(object_list)]
radar_api.ITR3800_getObjectList.restype = ctypes.c_int


print("Newwwwwwwww9")

print(f"Handle value before calling ITR3800_getObjectList: {handle.value}")
print(f"Object list before calling: {object_list}")


try:

    result = radar_api.ITR3800_getObjectList(handle, ctypes.byref(object_list))
    print("Newwwwwwwww10")
    print("Object List: ", result)
        
        # Check the result code
    if result != 0:  # Assuming 0 means success
        print(f"Error: Unable to get object list, error code: {result}")
    else:
        # Check the number of tracked objects
        if object_list.nrOfTracks > 0:
            print(f"Number of objects: {object_list.nrOfTracks}")
            # Process the object list (example of accessing tracked objects)
            for obj in object_list.trackedObjects[:object_list.nrOfTracks]:  # Slice based on actual number of objects
                print(f"Object ID: {obj.ui32_objectID}")
                print(f"Position: ({obj.f32_positionX_m}, {obj.f32_positionY_m})")
                print(f"Velocity: ({obj.f32_velocityX_mps}, {obj.f32_velocityY_mps})")
        else:
            print("No objects in the list.")
except Exception as e:
    print(e)

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


