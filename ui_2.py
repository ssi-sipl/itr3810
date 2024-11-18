import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Define the function to parse the data string
def parse_mz_data(data_string):
    fields = [
        "MZ", "Timestamp", "Zone", "Speed", "Class", 
        "Direction", "Systemstate", "Outputnumber", 
        "Phasenumber", "ObjectID", "ETA"
    ]
    try:
        data_values = data_string.split(';')
        data = dict(zip(fields, data_values))
        timestamp = datetime.datetime.strptime(data["Timestamp"], "%Y.%m.%d_%H.%M.%S.%f")
        data["Timestamp"] = timestamp
        data["Zone"] = int(data["Zone"])
        data["Speed"] = float(data["Speed"])
        data["Class"] = int(data["Class"])
        data["Direction"] = int(data["Direction"])
        data["Systemstate"] = int(data["Systemstate"])
        data["Outputnumber"] = int(data["Outputnumber"])
        data["Phasenumber"] = int(data["Phasenumber"])
        data["ObjectID"] = int(data["ObjectID"])
        data["ETA"] = float(data["ETA"])
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
