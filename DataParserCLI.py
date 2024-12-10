import socket

def read_data_continuously(ip_address, port, buffer_size=1024):
    """
    Connects to a TCP/IP server and continuously reads data.
    
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
            print(f"Data received: {data.decode('utf-8')}")

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
