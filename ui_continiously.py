import socket
import tkinter as tk
from tkinter import ttk
import datetime
import threading

# Global flag to handle disconnection
keep_reading = True

# Function to parse the data string
def parse_mz_data(data_string):
    fields = ["Motion Zone", "Timestamp", "Zone", "Speed", "Class", "Direction"]
    
    class_mapping = {
        "02": "Others",
        "10": "Non-motorized",
        "30": "Car",
        "60": "Small Truck",
        "70": "Big Truck"
    }
    
    direction_mapping = {
        "1": "Incoming",
        "2": "Outgoing"
    }
    
    try:
        data_values = data_string.split(';')
        data = dict(zip(fields, data_values[:6]))
        
        timestamp = datetime.datetime.strptime(data["Timestamp"], "%Y.%m.%d_%H.%M.%S.%f")
        data["Timestamp"] = timestamp
        data["Zone"] = int(data["Zone"])
        data["Speed"] = float(data["Speed"])
        
        data["Speed"] = f"{data['Speed']} km/hr"
        data["Class"] = class_mapping.get(data["Class"], "Unknown Class")
        data["Direction"] = direction_mapping.get(data["Direction"], "Unknown Direction")
        
        return data
    except (ValueError, KeyError) as e:
        status_label.config(text=f"Error parsing data: {e}", foreground="red")
        return None

# Function to continuously read data from the socket
def read_data_continuously(ip_address, port, buffer_size=1024):
    global keep_reading
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        status_label.config(text=f"Connected to {ip_address}:{port}", foreground="green")

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

# Function to handle the "Connect" button click
def start_tcp_connection():
    global keep_reading
    keep_reading = True
    ip_address = ip_entry.get()
    port = int(port_entry.get())
    threading.Thread(target=read_data_continuously, args=(ip_address, port), daemon=True).start()

# Function to handle the "Disconnect" button click
def stop_tcp_connection():
    global keep_reading
    keep_reading = False
    status_label.config(text="Disconnected", foreground="orange")

# Create the main window
root = tk.Tk()
root.title("MZ Data Parser")
root.geometry("600x500")

# Input Frame (for IP and Port)
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill=tk.X)

ip_label = ttk.Label(input_frame, text="IP Address:")
ip_label.pack(side=tk.LEFT, padx=5)

ip_entry = ttk.Entry(input_frame, width=20)
ip_entry.pack(side=tk.LEFT, padx=5)

port_label = ttk.Label(input_frame, text="Port:")
port_label.pack(side=tk.LEFT, padx=5)

port_entry = ttk.Entry(input_frame, width=10)
port_entry.pack(side=tk.LEFT, padx=5)

connect_button = ttk.Button(input_frame, text="Connect", command=start_tcp_connection)
connect_button.pack(side=tk.LEFT, padx=5)

disconnect_button = ttk.Button(input_frame, text="Disconnect", command=stop_tcp_connection)
disconnect_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(input_frame, text="Clear", command=clear_output)
clear_button.pack(side=tk.LEFT, padx=5)

# Status Label (to display connection status)
status_label = ttk.Label(root, text="Not connected", foreground="red", anchor="center")
status_label.pack(fill=tk.X, pady=5)

# Output Frame (for displaying parsed data)
output_frame = ttk.Frame(root, padding=10)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, wrap=tk.WORD, height=15)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)

# Start the Tkinter main loop
root.mainloop()
