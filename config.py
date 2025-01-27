#MQTT Configuration
SEND_MQTT = False
MQTT_BROKER = "localhost"  # Change to your broker's IP address if needed
MQTT_PORT = 1883
MQTT_CHANNEL = "radar_surveillance"

# Radar Configuration
RADAR_ID = "radar-itr3810"
AREA_ID = "area-2"
RADAR_LAT = 34.011125  #  radar latitude
RADAR_LONG = 74.01219  #  radar longitude
RADAR_IP = "192.168.31.200"

# Output Configuration
OUTPUT_FILE = "detected_targets.json"
