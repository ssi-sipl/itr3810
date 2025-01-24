from ctypes import *
import ctypes.util
import sys
import time

# Basic type definitions matching ITR3800_radarAPI_basicTypes.h
class BasicTypes:
    bool_t = c_ushort
    float32_t = c_float
    sint8_t = c_byte
    uint8_t = c_ubyte
    sint16_t = c_short
    uint16_t = c_ushort
    sint32_t = c_int
    uint32_t = c_uint

# Constants
MAX_TRACKS = 0x3C
ITR3800_MAX_NR_OF_TRACKS = 256
ITR3800_MAX_NR_OF_DETECTIONS = 512
ITR3800_MAX_EVENT_MESSAGE_LENGTH = 128
ITR3800_MAX_NR_OF_EVENT_MESSAGES = 256

# Error descriptions
ITR3800_ERRORS = {
    0x200: "No connection available.",
    0x201: "No valid socket.",
    0x202: "iSYS software version not supported.",
    0x203: "Raw data: No first valid frame.",
    0x204: "Object list size: Metric and imperial mismatch.",
    0x205: "Firmware version incompatible."
}

# Structure definitions
class ITR3800_EventMessage(Structure):
    _fields_ = [
        ("c_eventMessage", BasicTypes.uint8_t * ITR3800_MAX_EVENT_MESSAGE_LENGTH),
        ("ui8_eventMessageLength", BasicTypes.uint8_t)
    ]

class ITR3800_EventMessageList(Structure):
    _fields_ = [
        ("eventMessages", ITR3800_EventMessage * ITR3800_MAX_NR_OF_EVENT_MESSAGES),
        ("nrOfMessages", BasicTypes.uint8_t)
    ]

class ITR3800_TrackClass_u(Union):
    _fields_ = [
        ("classID", BasicTypes.uint32_t)
    ]

class ITR3800_ObjectListError_u(Union):
    _fields_ = [
        ("error", BasicTypes.uint32_t)
    ]

class ITR3800_TrackedObject(Structure):
    _fields_ = [
        ("ui32_objectID", BasicTypes.uint32_t),
        ("ui16_ageCount", BasicTypes.uint16_t),
        ("ui16_predictionCount", BasicTypes.uint16_t),
        ("ui16_staticCount", BasicTypes.uint16_t),
        ("f32_trackQuality", BasicTypes.float32_t),
        ("classID", ITR3800_TrackClass_u),
        ("si16_motion_eventZoneIndex", BasicTypes.sint16_t),
        ("si16_presence_eventZoneIndex", BasicTypes.sint16_t),
        ("si16_loop_eventZoneIndex", BasicTypes.sint16_t),
        ("f32_positionX_m", BasicTypes.float32_t),
        ("f32_positionY_m", BasicTypes.float32_t),
        ("f32_velocityX_mps", BasicTypes.float32_t),
        ("f32_velocityY_mps", BasicTypes.float32_t),
        ("f32_velocityInDir_mps", BasicTypes.float32_t),
        ("f32_directionX", BasicTypes.float32_t),
        ("f32_directionY", BasicTypes.float32_t),
        ("f32_distanceToFront_m", BasicTypes.float32_t),
        ("f32_distanceToBack_m", BasicTypes.float32_t),
        ("f32_length_m", BasicTypes.float32_t),
        ("f32_width_m", BasicTypes.float32_t)
    ]

class ITR3800_ObjectList(Structure):
    _fields_ = [
        ("protocolVersion", BasicTypes.uint16_t),
        ("reserved_0", BasicTypes.uint8_t),
        ("configurationChanged", BasicTypes.uint8_t),
        ("systemState", BasicTypes.uint32_t),
        ("error", ITR3800_ObjectListError_u),
        ("timestamp_ms", BasicTypes.uint32_t),
        ("frameID", BasicTypes.uint16_t),
        ("nrOfTracks", BasicTypes.uint16_t),
        ("trackedObjects", ITR3800_TrackedObject * ITR3800_MAX_NR_OF_TRACKS),
        ("eventMessages", ITR3800_EventMessageList),
        ("reserved0", BasicTypes.float32_t),
        ("reserved1", BasicTypes.float32_t),
        ("reserved2", BasicTypes.float32_t),
        ("reserved3", BasicTypes.float32_t)
    ]

class RadarAPI:
    def __init__(self, dll_path):
        """Initialize the RadarAPI with the path to the DLL."""
        try:
            self.radar_dll = CDLL(dll_path)
        except OSError as e:
            raise Exception(f"Failed to load radar DLL: {e}")

        self._setup_function_signatures()

    def _setup_function_signatures(self):
        self.radar_dll.ITR3800_getApiVersion.argtypes = [POINTER(BasicTypes.float32_t)]
        self.radar_dll.ITR3800_getApiVersion.restype = BasicTypes.uint32_t
        self.radar_dll.ITR3800_initSystem.argtypes = [
            POINTER(c_void_p),
            BasicTypes.uint8_t, BasicTypes.uint8_t, BasicTypes.uint8_t, BasicTypes.uint8_t
        ]
        self.radar_dll.ITR3800_initSystem.restype = BasicTypes.uint32_t
        self.radar_dll.ITR3800_getObjectList.argtypes = [c_void_p, POINTER(ITR3800_ObjectList)]
        self.radar_dll.ITR3800_getObjectList.restype = BasicTypes.uint32_t
        self.radar_dll.ITR3800_exitSystem.argtypes = [c_void_p]
        self.radar_dll.ITR3800_exitSystem.restype = BasicTypes.uint32_t

    def handle_error(self, error_code):
        """Translate error code into a human-readable message."""
        return ITR3800_ERRORS.get(error_code, f"Unknown error code: {error_code}")

    def get_api_version(self):
        version = BasicTypes.float32_t()
        result = self.radar_dll.ITR3800_getApiVersion(byref(version))
        if result != 0:
            raise Exception(self.handle_error(result))
        return version.value

    def init_system(self, ip_address):
        ip_parts = [int(x) for x in ip_address.split('.')]
        handle = c_void_p()
        result = self.radar_dll.ITR3800_initSystem(
            byref(handle),
            BasicTypes.uint8_t(ip_parts[0]),
            BasicTypes.uint8_t(ip_parts[1]),
            BasicTypes.uint8_t(ip_parts[2]),
            BasicTypes.uint8_t(ip_parts[3])
        )
        if result != 0:
            raise Exception(self.handle_error(result))
        self.handle = handle

    def get_object_list(self):
        if not hasattr(self, 'handle'):
            raise Exception("Radar system not initialized")
        object_list = ITR3800_ObjectList()
        result = self.radar_dll.ITR3800_getObjectList(self.handle, byref(object_list))
        if result != 0:
            raise Exception(self.handle_error(result))
        
        return object_list

    def exit_system(self):
        if hasattr(self, 'handle'):
            result = self.radar_dll.ITR3800_exitSystem(self.handle)
            if result != 0:
                raise Exception(self.handle_error(result))
            del self.handle

def example_usage():
    radar = RadarAPI("./Software/RadarAPI/library_v1.147/Windows_msvc_2017_x64/ITR3800_radarAPI.dll")
    try:
        print(f"Radar API Version: {radar.get_api_version()}")
        radar.init_system("192.168.31.200")
        time.sleep(1)      
        objects = radar.get_object_list()
        if objects.nrOfTracks > 0:
            print(f"Number of objects: {objects.nrOfTracks}")
            # Process the object list (example of accessing tracked objects)
            for obj in objects.trackedObjects[:objects.nrOfTracks]:  # Slice based on actual number of objects
                print(f"Object ID: {obj.ui32_objectID}")
                print(f"Position: ({obj.f32_positionX_m}, {obj.f32_positionY_m})")
                print(f"Velocity: ({obj.f32_velocityX_mps}, {obj.f32_velocityY_mps})")
        else:
            print("No objects in the list.")
    finally:
        radar.exit_system()

if __name__ == "__main__":
    example_usage()
