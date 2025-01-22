from ctypes import *
import ctypes.util
import sys

# Basic type definitions matching ITR3800_radarAPI_basicTypes.h
class BasicTypes:
    # Map the radar's types to ctypes types
    bool_t = c_ushort
    float32_t = c_float
    sint8_t = c_byte
    uint8_t = c_ubyte
    sint16_t = c_short
    uint16_t = c_ushort
    sint32_t = c_int
    uint32_t = c_uint

# Constants from the header files
MAX_TRACKS = 0x3C
ITR3800_MAX_NR_OF_TRACKS = 256
ITR3800_MAX_NR_OF_DETECTIONS = 512
ITR3800_MAX_EVENT_MESSAGE_LENGTH = 128
ITR3800_MAX_NR_OF_EVENT_MESSAGES = 256

# Structure definitions using proper basic types
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

        # Set up function signatures
        self._setup_function_signatures()

    def _setup_function_signatures(self):
        """Set up the function signatures for the DLL functions."""
        # API Version
        self.radar_dll.ITR3800_getApiVersion.argtypes = [POINTER(BasicTypes.float32_t)]
        self.radar_dll.ITR3800_getApiVersion.restype = BasicTypes.uint32_t

        # System initialization
        self.radar_dll.ITR3800_initSystem.argtypes = [
            POINTER(c_void_p),
            BasicTypes.uint8_t, BasicTypes.uint8_t, 
            BasicTypes.uint8_t, BasicTypes.uint8_t
        ]
        self.radar_dll.ITR3800_initSystem.restype = BasicTypes.uint32_t

        # Object list retrieval
        self.radar_dll.ITR3800_getObjectList.argtypes = [
            c_void_p,
            POINTER(ITR3800_ObjectList)
        ]
        self.radar_dll.ITR3800_getObjectList.restype = BasicTypes.uint32_t

        # System exit
        self.radar_dll.ITR3800_exitSystem.argtypes = [c_void_p]
        self.radar_dll.ITR3800_exitSystem.restype = BasicTypes.uint32_t

    def get_api_version(self):
        """Get the API version of the radar system."""
        version = BasicTypes.float32_t()
        result = self.radar_dll.ITR3800_getApiVersion(byref(version))
        if result == 0:  # Assuming 0 is SUCCESS
            return version.value
        raise Exception(f"Failed to get API version. Error code: {result}")

    def init_system(self, ip_address):
        """
        Initialize the radar system.
        
        Args:
            ip_address (str): IP address of the radar system (e.g., "192.168.1.100")
        """
        ip_parts = [int(x) for x in ip_address.split('.')]
        handle = c_void_p()
        result = self.radar_dll.ITR3800_initSystem(
            byref(handle),
            BasicTypes.uint8_t(ip_parts[0]),
            BasicTypes.uint8_t(ip_parts[1]),
            BasicTypes.uint8_t(ip_parts[2]),
            BasicTypes.uint8_t(ip_parts[3])
        )
        
        if result == 0:
            self.handle = handle
            return True
        raise Exception(f"Failed to initialize radar system. Error code: {result}")

    def get_object_list(self):
        """Get the current list of tracked objects."""
        if not hasattr(self, 'handle'):
            raise Exception("Radar system not initialized")

        object_list = ITR3800_ObjectList()
        result = self.radar_dll.ITR3800_getObjectList(self.handle, byref(object_list))
        
        if result == 0:
            return {
                'timestamp_ms': object_list.timestamp_ms,
                'frame_id': object_list.frameID,
                'num_tracks': object_list.nrOfTracks,
                'objects': [{
                    'id': obj.ui32_objectID,
                    'position': {
                        'x': obj.f32_positionX_m,
                        'y': obj.f32_positionY_m
                    },
                    'velocity': {
                        'x': obj.f32_velocityX_mps,
                        'y': obj.f32_velocityY_mps,
                        'direction': obj.f32_velocityInDir_mps
                    },
                    'dimensions': {
                        'length': obj.f32_length_m,
                        'width': obj.f32_width_m
                    },
                    'quality': obj.f32_trackQuality,
                    'class_id': obj.classID.classID,
                    'age_count': obj.ui16_ageCount,
                    'static_count': obj.ui16_staticCount,
                    'event_zones': {
                        'motion': obj.si16_motion_eventZoneIndex,
                        'presence': obj.si16_presence_eventZoneIndex,
                        'loop': obj.si16_loop_eventZoneIndex
                    }
                } for obj in object_list.trackedObjects[:object_list.nrOfTracks]]
            }
        
        raise Exception(f"Failed to get object list. Error code: {result}")

    def exit_system(self):
        """Safely shut down the radar system."""
        if hasattr(self, 'handle'):
            result = self.radar_dll.ITR3800_exitSystem(self.handle)
            if result == 0:
                del self.handle
                return True
            raise Exception(f"Failed to exit system. Error code: {result}")
        return False

def example_usage():
    radar = RadarAPI("./Software/RadarAPI/library_v1.147/Windows_msvc_2017_x64/ITR3800_radarAPI.dll")
    try:
        # Get API version
        version = radar.get_api_version()
        print(f"Radar API Version: {version}")
        
        # Initialize the system
        radar.init_system("192.168.31.200")  # Replace with actual radar IP
        
        # Get and print object data
        data = radar.get_object_list()
        print(f"\nFrame {data['frame_id']} at {data['timestamp_ms']}ms")
        print(f"Detected {data['num_tracks']} objects:")
        
        for obj in data['objects']:
            print(f"\nObject ID: {obj['id']}")
            print(f"Position: ({obj['position']['x']:.2f}m, {obj['position']['y']:.2f}m)")
            print(f"Velocity: {obj['velocity']['direction']:.2f} m/s")
            print(f"Quality: {obj['quality']:.2f}")
            
    finally:
        radar.exit_system()

if __name__ == "__main__":
    example_usage()