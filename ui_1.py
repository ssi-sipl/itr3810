import datetime

# Define a function to parse the data string
def parse_mz_data(data_string):
    # Define the format fields
    fields = [
        "MZ", "Timestamp", "Zone", "Speed", "Class", 
        "Direction", "Systemstate", "Outputnumber", 
        "Phasenumber", "ObjectID", "ETA"
    ]
    
    # Split the data string by semicolon
    data_values = data_string.split(';')
    
    # Map the fields to their corresponding values
    data = dict(zip(fields, data_values))
    
    # Convert the timestamp to a readable datetime object
    try:
        timestamp = datetime.datetime.strptime(data["Timestamp"], "%Y.%m.%d_%H.%M.%S.%f")
        data["Timestamp"] = timestamp
    except ValueError:
        print("Error: Invalid timestamp format.")
        return None
    
    # Convert numeric fields to appropriate types
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

# Example data string
data_string = "MZ;2024.11.18_14.53.20.894;01;33.56;30;1;0;0;0;851;0.00"

# Parse the data
parsed_data = parse_mz_data(data_string)

# Display the parsed data
if parsed_data:
    print("Parsed Data:")
    for key, value in parsed_data.items():
        print(f"{key}: {value}")
