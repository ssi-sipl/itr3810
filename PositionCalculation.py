import datetime

def parse_itr3810_data(data, radar_id="ITR3810", area_id="Zone 1", lat_radar=22.345678, lon_radar=73.123456):
    """
    Parses data from the ITR3810 radar (300m) and converts it into the desired format.
    Includes exception handling to catch missing or invalid data.
    """
    try:
        zone = data.get("zone")
        speed = data.get("speed")
        obj_class = data.get("class")
        direction = data.get("direction")
        timestamp = data.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")
        
        if zone is None or speed is None or obj_class is None or direction is None:
            raise ValueError("Missing required fields: 'zone', 'speed', 'class', or 'direction'.")
        
        if direction not in ["incoming", "outgoing"]:
            raise ValueError("Direction must be either 'incoming' or 'outgoing'.")
        
        # Map zones to average ranges (in meters)
        zone_to_range_map = {
            1: 50,
            2: 100,
            3: 150,
            4: 200,
            5: 250,
            6: 300
        }
        range_m = zone_to_range_map.get(zone, 150)  # Default to 150m if zone is unknown
        
        # Determine if object is detected
        object_detected = speed > 0
        
        result = {
            "radar_id": radar_id,
            "area_id": area_id,
            "timestamp": timestamp,
            "object_detected": object_detected,
            "classification": obj_class,
            "latitude": lat_radar,
            "longitude": lon_radar,
            "estimated_range_m": range_m,
            "direction": direction
        }
        return result

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except KeyError as ke:
        print(f"KeyError: {ke}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Example usage
data_input_300m = {
    "zone": 3,
    "speed": 5,
    "class": "truck",
    "direction": "incoming",
    "timestamp": "2025-01-06T12:45:30Z"
}

parsed_data_300m = parse_itr3810_data(data_input_300m)
print(parsed_data_300m)
