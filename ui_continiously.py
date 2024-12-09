import socket
import tkinter as tk
import datetime
import threading

# Global flag to handle disconnection
keep_reading = False

# Hardcoded IP and Port
IP_ADDRESS = "192.168.252.2"
PORT = 2050

# Function to parse the data string
def parse_mz_data(data_string):
    fields = ["Motion Zone", "Timestamp", "Zone", "Speed", "Class", "Direction"]
    class_mapping = {
        "02": "Others", "10": "Non-motorized", "30": "Car", "60": "Small Truck", "70": "Big Truck"
    }
    direction_mapping = {
        "1": "Incoming", "2": "Outgoing"
    }
    
    try:
        # Split data and map to fields
        data_values = data_string.split(';')
        data = dict(zip(fields, data_values[:6]))
        
        # Parse timestamp and convert speed and class
        data["Timestamp"] = datetime.datetime.strptime(data["Timestamp"], "%Y.%m.%d_%H.%M.%S.%f")
        data["Zone"] = int(data["Zone"])
        data["Speed"] = f"{float(data['Speed']):.2f} km/hr"
        data["Class"] = class_mapping.get(data["Class"], "Unknown Class")
        data["Direction"] = direction_mapping.get(data["Direction"], "Unknown Direction")
        
        return data
    except (ValueError, KeyError) as e:
        status_label.config(text=f"Error parsing data: {e}", foreground="red")
        return None

# Function to continuously read data from the socket
def read_data_continuously(buffer_size=1024):
    global keep_reading
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP_ADDRESS, PORT))
        status_label.config(text=f"Connected to {IP_ADDRESS}:{PORT}", foreground="green")

        while keep_reading:
            data = client_socket.recv(buffer_size)
            if not data:
                break
            data_string = data.decode('utf-8').strip()
            parsed_data = parse_mz_data(data_string)
            if parsed_data:
                display_parsed_data(parsed_data)

    except Exception as e:
        status_label.config(text=f"Connection Error: {e}", foreground="red")

    finally:
        client_socket.close()
        status_label.config(text="Disconnected", foreground="orange")

# Function to display parsed data in the GUI
def display_parsed_data(parsed_data):
    output_text.insert(tk.END, "Parsed Data:\n")
    for key, value in parsed_data.items():
        output_text.insert(tk.END, f"{key}: {value}\n")
    output_text.insert(tk.END, "\n")  # Add a newline for better readability
    output_text.yview(tk.END)  # Automatically scroll to the latest entry

# Function to clear the output text widget
def clear_output():
    output_text.delete("1.0", tk.END)

# Function to handle the "Connect/Disconnect" button click
def toggle_connection():
    global keep_reading
    if keep_reading:  # If currently connected, disconnect
        keep_reading = False
        status_label.config(text="Disconnected", foreground="orange")
        connect_button.config(text="Connect", bg="green", fg="white")
    else:  # If currently disconnected, connect
        keep_reading = True
        threading.Thread(target=read_data_continuously, daemon=True).start()
        status_label.config(text=f"Connecting to {IP_ADDRESS}:{PORT}...", foreground="blue")
        connect_button.config(text="Disconnect", bg="red", fg="white")

# Create the main window
root = tk.Tk()
root.title("300M Data Parser")
root.geometry("600x500")

# Input Frame (for Connect/Disconnect Button)
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=5)

# Connect/Disconnect Button
connect_button = tk.Button(button_frame, text="Connect", command=toggle_connection, bg="green", fg="white")
connect_button.pack(side=tk.LEFT, padx=5)

# Clear Button
clear_button = tk.Button(button_frame, text="Clear", command=clear_output)
clear_button.pack(side=tk.LEFT, padx=5)

# Status Label (to display connection status)
status_label = tk.Label(root, text="Not connected", foreground="red", anchor="center")
status_label.pack(fill=tk.X, pady=5)

# Output Frame (for displaying parsed data)
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, wrap=tk.WORD, height=15)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)

# Start the Tkinter main loop
root.mainloop()
