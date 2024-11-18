import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Define the function to parse the data string
def parse_mz_data(data_string):
    # Define the fields we want to parse
    fields = ["Motion Zone", "Timestamp", "Zone", "Speed", "Class", "Direction"]
    
    # Mapping Class codes to descriptions
    class_mapping = {
        "02": "Others",
        "10": "Non-motorized",
        "30": "Car",
        "60": "Small Truck",
        "70": "Big Truck"
    }
    
    # Mapping Direction codes to descriptions
    direction_mapping = {
        "1": "Incoming",
        "2": "Outgoing"
    }
    
    try:
        # Split the data string by semicolon
        data_values = data_string.split(';')
        
        # Ensure we only get the relevant fields
        data = dict(zip(fields, data_values[:6]))  # Only take first 6 fields
        
        # Convert the timestamp to a readable datetime object
        timestamp = datetime.datetime.strptime(data["Timestamp"], "%Y.%m.%d_%H.%M.%S.%f")
        data["Timestamp"] = timestamp
        
        # Convert numeric fields to appropriate types
        data["Zone"] = int(data["Zone"])
        data["Speed"] = float(data["Speed"])
        data["Class"] = data["Class"]
        data["Direction"] = data["Direction"]
        
        # Append the unit to Speed
        data["Speed"] = f"{data['Speed']} km/hr"
        
        # Map Class code to its description
        class_code = data["Class"]
        data["Class"] = class_mapping.get(class_code, "Unknown Class")
        
        # Map Direction code to its description
        direction_code = data["Direction"]
        data["Direction"] = direction_mapping.get(direction_code, "Unknown Direction")
        
        return data
    except (ValueError, KeyError) as e:
        messagebox.showerror("Parsing Error", f"Failed to parse data: {e}")
        return None

# Define the function for the button click
def parse_and_display():
    data_string = input_entry.get()
    parsed_data = parse_mz_data(data_string)
    if parsed_data:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Parsed Data:\n")
        for key, value in parsed_data.items():
            output_text.insert(tk.END, f"{key}: {value}\n")

# Create the main window
root = tk.Tk()
root.title("MZ Data Parser")
root.geometry("500x400")

# Input Frame
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill=tk.X)

input_label = ttk.Label(input_frame, text="Data String:")
input_label.pack(side=tk.LEFT, padx=5)

input_entry = ttk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

parse_button = ttk.Button(input_frame, text="Parse", command=parse_and_display)
parse_button.pack(side=tk.LEFT, padx=5)

# Output Frame
output_frame = ttk.Frame(root, padding=10)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, wrap=tk.WORD, height=15)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)

# Start the Tkinter main loop
root.mainloop()
