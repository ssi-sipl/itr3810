import socket
import json

# Radar configuration
RADAR_IP = "192.168.31.200" # 192.168.1.1   
RADAR_PORT = 62150          # 62200s

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Request object list with all details enabled
request = {
    "Command": "RequestObjectList",
    "Parameters": {
        "EnableDetails": True,  # Request all available details
        # "ObjectListDetails": true,
        # "EventZoneDetails": true,s
        # "AllTracks": true
    }
}

# Send the request
try:
    print("Sending request to radar...")
    sock.sendto(json.dumps(request).encode(), (RADAR_IP, RADAR_PORT))

    # Receive response
    data, _ = sock.recvfrom(4096)  # Adjust buffer size if needed
    response = json.loads(data.decode())

    # Print the response
    print("Received data from radar:")
    print(json.dumps(response, indent=2))

except Exception as e:
    print(f"Error communicating with radar: {e}")

finally:
    # Close the socket
    sock.close()
