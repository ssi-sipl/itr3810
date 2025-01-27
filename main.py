from ctypes import *
import ctypes.util
import sys
import time
import math
import json
import signal
import paho.mqtt.client as mqtt
from config import *

targets_data = []  # List to store valid targets

mqtt_client = mqtt.Client()

if SEND_MQTT:
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print("Channel: ", MQTT_CHANNEL)
        print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        sys.exit(1)

def publish_target(target):
    try:
        mqtt_client.publish(MQTT_CHANNEL, json.dumps(target))
        # print(f"Published target: {target}")
    except Exception as e:
        print(f"Failed to publish target: {e}")

def save_to_json():
    with open(OUTPUT_FILE, "w") as file:
        json.dump(targets_data, file, indent=4)
    print(f"Data saved to {OUTPUT_FILE}")

def signal_handler(sig, frame):
    print("\nCtrl+C detected! Saving data and exiting...")
    save_to_json()
    # print("Disconnecting from MQTT broker...")
    # mqtt_client.loop_stop()
    # mqtt_client.disconnect()
    sys.exit(0)

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

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

ITR3800_TrackClass = {
    2: "OTHERS",
    10: "PEDESTRIAN",
    12: "BICYCLE",
    30: "CAR",
    60: "SMALL_TRUCK",
    70: "BIG_TRUCK"
}

# Combined classification mapping
ITR3800_TrackClass_Mapped = {
    "VEHICLE": [30, 60, 70],  # CAR, SMALL_TRUCK, BIG_TRUCK
    "PERSON": [10, 12],       # PEDESTRIAN, BICYCLE
    "OTHERS": [2]             # OTHERS
}

# Reverse the mapping for easy lookup
classification_mapping = {}
for category, keys in ITR3800_TrackClass_Mapped.items():
    for key in keys:
        classification_mapping[key] = category


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

        self.radar_dll.ITR3800_getSimulation.argtypes = [c_void_p, POINTER(BasicTypes.uint8_t)]
        self.radar_dll.ITR3800_getSimulation.restype = BasicTypes.uint32_t

        self.radar_dll.ITR3800_setSimulation.argtypes = [c_void_p, BasicTypes.uint8_t]
        self.radar_dll.ITR3800_setSimulation.restype = BasicTypes.uint32_t

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

    def get_simulation(self):
        if not hasattr(self, 'handle'):
            raise Exception("Radar system not initialized")
        simulation = BasicTypes.uint8_t()
        result = self.radar_dll.ITR3800_getSimulation(self.handle, byref(simulation))
        if result != 0:
            raise Exception(self.handle_error(result))
        return simulation.value
    
    def set_simulation(self, value):
        if not hasattr(self, 'handle'):
            raise Exception("Radar system not initialized")
        result = self.radar_dll.ITR3800_setSimulation(self.handle, BasicTypes.uint8_t(value))
        if result != 0:
            raise Exception(self.handle_error(result))
        
        return self.handle_error(result)

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

def get_class(class_id):
    return classification_mapping.get(class_id, "UNKNOWN")

def calculate_azimuth(x, y):
    angle_radians = math.atan2(y, x)
    angle_degrees = math.degrees(angle_radians)
    # Ensure the angle is in the range [0, 360)
    if angle_degrees < 0:
        angle_degrees += 360
    
    return angle_degrees

def parse_object_list(object_list):
    if object_list.nrOfTracks > 0:
        print("-"*40)
        frame_id = object_list.frameID
        timestamp = object_list.timestamp_ms

        print(f"Frame ID: {object_list.frameID}")
        print(f"Timestamp: {object_list.timestamp_ms}")
        print(f"Number of objects: {object_list.nrOfTracks}")
        print(f"Frame ID: {frame_id}")
        print("Detected Targets:")
        print(f"{'Serial':<8} {'Signal Strength (%)':<25} {'Range (m)':<15} {'Velocity (m/s)':<25} {'Direction':<15} {'Azimuth (Deg)':<25} {'x (m) y (m)':<25} {'Latitude':<25} {'Longitude':<25} {'Classification':<25}")

        
        for obj in object_list.trackedObjects[:object_list.nrOfTracks]:  # Slice based on actual number of objects
            velocity = obj.f32_velocityInDir_mps
            signal_strength = obj.f32_trackQuality
            range = obj.f32_distanceToFront_m
            distance = obj.f32_distanceToFront_m
            classification = get_class(obj.classID.classID)
            x = obj.f32_positionX_m
            y = obj.f32_positionY_m
            idx = obj.ui32_objectID

            radar_lat_rad = math.radians(RADAR_LAT) # Convert radar latitude to radians
        
            # Calculate change in latitude and longitude in degrees
            delta_lat_deg = y / 111139
            delta_lon_deg = x / (111139 * math.cos(radar_lat_rad))
            
            # Final coordinates of the object
            object_lat = RADAR_LAT + delta_lat_deg
            object_lon = RADAR_LONG + delta_lon_deg

            azimuth = calculate_azimuth(x, y)

            target_info = {
            'radar_id': RADAR_ID,
            'area_id': AREA_ID,
            'frame_id': frame_id,
            'timestamp': str(timestamp),
            'signal_strength': round(signal_strength, 2),
            'range': round(range, 2),
            'speed': round(velocity, 2),
            'aizmuth_angle': round(azimuth, 2),
            'distance': round(distance, 2),
            'direction': "Static" if velocity == 0 else "Incoming" if velocity > 0 else "Outgoing",
            'classification': classification, # ['vehicle', 'person', 'bicycle', 'others']
            'zone': 0,
            'x': round(x, 2),   
            'y': round(y, 2),
            'latitude': round(object_lat, 6),
            'longitude': round(object_lon, 6),
            }

            targets_data.append(target_info)

            if SEND_MQTT:
                publish_target(target_info)

            print(f"{idx:<8} {target_info['signal_strength']:<25} {target_info['range']:<15} {target_info['speed']:<25} {target_info['direction']:<15} {target_info['aizmuth_angle']:<25} {target_info['x']} {target_info['y']:<25} {target_info['latitude']:<25} {target_info['longitude']:<25} {target_info['classification']}")

        print("-"*40)

def main():
    # radar = RadarAPI("./Software/RadarAPI/library_v1.147/Windows_msvc_2017_x64/ITR3800_radarAPI.dll")

    radar = RadarAPI("./Software/RadarAPI/library_v1.147/Linux_x64/libITR3800_radarAPI.so")
    try:
        print(f"Radar API Version: {radar.get_api_version()}")
        radar.init_system("192.168.31.200")
        time.sleep(1)

        # radar.set_simulation(0)
        print("Simulation mode: ", "True" if radar.get_simulation() == 1 else "False")

        while True:      
            objects = radar.get_object_list()
            parse_object_list(objects)
            time.sleep(0.1)
        
    finally:
        radar.exit_system()

if __name__ == "__main__":
    main()
