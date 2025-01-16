import socket
import datetime
import pytz
from datetime import datetime

ist_timezone = pytz.timezone('Asia/Kolkata')


LAT_RADAR = 22.345678
LONG_RADAR = 73.123456
RADAR_ID = "Radar-2"
AREA_ID = "Area-2"

def parse_itr3810_data(data):
    """
    Parses data from the ITR3810 radar (300m) and converts it into the desired format.
    Includes exception handling to catch missing or invalid data.
    """
    try:
        zone = data.get("zone")
        speed = data.get("speed")
        obj_class = data.get("class")
        direction = data.get("direction")
        timestamp = data.get("timestamp", datetime.now(ist_timezone))
        
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
        
       
        if (speed > 0) :

            target_info = {
            'radar_id': "radar-pune",
            'area_id': "area-1",
            'frame_id': 0, 
            'timestamp': str(timestamp),
            # 'signal_strength': round(signal_strength, 2),
            'range': round(range_m, 2),
            'speed': round(speed, 2),
            # 'aizmuth_angle': round(azimuth, 2),
            'distance': round(range_m, 2),
            'direction': direction,
            'classification': obj_class,
            'zone': zone,
            # 'x': round(x, 2),   
            # 'y': round(y, 2),
            # 'latitude': round(object_lat, 6),
            # 'longitude': round(object_lon, 6),
        }
            # object detected
            result = {
                "radar_id": RADAR_ID,
                "area_id": AREA_ID,
                "zone": zone,  # Zone included separately in the output
                "timestamp": timestamp,
                "classification": obj_class,
                "latitude": LAT_RADAR,
                "longitude": LONG_RADAR,
                "estimated_range_m": range_m,
                "direction": direction
            }
            return result
        
        return # object not detected

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return None
    except KeyError as ke:
        print(f"KeyError: {ke}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def read_data_continuously(ip_address, port, buffer_size=1024):
    """
    Connects to a TCP/IP server and continuously reads data.
    Parses the received data using the ITR3810 radar parsing function.
    
    :param ip_address: The IP address of the server (e.g., "192.168.31.200")
    :param port: The port number to connect to
    :param buffer_size: Size of the buffer to read data (default is 1024 bytes)
    """
    try:
        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        print(f"Connecting to {ip_address}:{port}...")
        client_socket.connect((ip_address, port))
        print("Connection established.")

        # Continuously read data
        print("Listening for data (press Ctrl+C to stop)...")
        while True:
            data = client_socket.recv(buffer_size)
            if not data:
                # Break the loop if the connection is closed
                print("Connection closed by the server.")
                break
            
            # Decode and parse the received data
            try:
                decoded_data = data.decode('utf-8')
                parsed_input = eval(decoded_data)  # Convert string to dictionary (use with caution)
                
                parsed_output = parse_itr3810_data(parsed_input)
                if parsed_output:
                    print("Parsed Data:")
                    print(parsed_output)
                else:
                    print("Failed to parse the received data.")
            except Exception as e:
                print(f"Error parsing data: {e}")

    except KeyboardInterrupt:
        print("\nTerminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        print("Closing the connection.")
        client_socket.close()


if __name__ == "__main__":
    # Configuration
    SERVER_IP = "192.168.31.200"  # IP address of the server
    SERVER_PORT = 62150           # Port number of the server


    # Read data continuously from the TCP/IP server
    read_data_continuously(SERVER_IP, SERVER_PORT)
