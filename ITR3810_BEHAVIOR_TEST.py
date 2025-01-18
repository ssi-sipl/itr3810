import socket
import json

# Radar configuration
RADAR_IP = "192.168.31.200"  # Replace with your radar's IP address
RADAR_PORT = 62150           # Replace with your radar's UDP port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((RADAR_IP, RADAR_PORT))
# Request object list with all details enabled
request = {
    "Command": "RequestObjectList",
    "Parameters": {
        "EnableDetails": True  # Request all available details
    }
}

# Send the request
try:
    print("Sending request to radar...")
    sock.sendto(json.dumps(request).encode(), (RADAR_IP, RADAR_PORT))

    
    
    with open("radar_response.json", "w") as f:
        # Start listening continuously
        while True:
            try:
                # Receive a packet
                print("Listening for packets...")
                data, _ = sock.recvfrom(1024)  # Adjust buffer size if needed
                response = json.loads(data.decode())
                
                # Print the response
                print("Received data:")
                print(json.dumps(response, indent=2))
                
                # Save the response to the JSON file
                json.dump(response, f, indent=2)
                f.write(",\n")  # Add a separator for each new packet
                
            except json.JSONDecodeError:
                print("Received invalid JSON data.")
            except KeyboardInterrupt:
                print("\nStopping listening...")
                break  # Exit the loop when interrupted (Ctrl+C)

except Exception as e:
    print(f"Error communicating with radar: {e}")

finally:
    # Close the socket
    sock.close()
    print("Socket closed.")
