# itr3810

## Table of Contents

1. [Overview](#overview)
2. [Radar Config](#radar-config)
3. [Important Files](#important-files)
4. [Configuration](#configuration)
5. [Usage](#usage)

## Overview

This repository contains scripts to interface with the radar device, parse its data, and display it using both CLI and GUI interfaces.

## Radar Config

- **IP Address:** 192.168.31.200
- **Port:** 61250

## Important Files

- **main.py**: The main script to run the radar interface.
- **config.py**: Contains configuration variables for the radar.
- **subscriber.py**: Subscribes to radar data and processes it.
- **setup.sh**: Sets the Static IP

## Configuration

The `config.py` file contains variables that can be adjusted to configure the radar and its data parsing behavior. Below are the key variables:

### MQTT Configuration

- `SEND_MQTT`: Boolean flag to enable or disable sending data via MQTT.
- `MQTT_BROKER`: The IP address of the MQTT broker.
- `MQTT_PORT`: The port number to connect to the MQTT broker.
- `MQTT_CHANNEL`: The MQTT channel to publish radar data.
- `MQTT_BROKER_SUBSCRIBER`: The IP address of the MQTT broker for the subscriber.

### Radar Configuration

- `RADAR_IP`: The IP address of the radar device.
- `RADAR_ID`: The unique identifier for the radar device.
- `AREA_ID`: The identifier for the area being monitored by the radar.
- `RADAR_LAT`: The latitude coordinate of the radar's location.
- `RADAR_LONG`: The longitude coordinate of the radar's location.

### Output Configuration

- `OUTPUT_FILE`: The file where detected targets data will be saved.

## Usage

1. **Run setup.sh**:

   ```sh
   chmod +x setup.sh
   ./setup.sh
   ```

1. **Run Main Script**: Execute `main.py` to start the radar interface.

   ```sh
   python main.py
   ```

1. **Configuration**: Adjust settings in `config.py` as needed.

1. **Subscriber**: Use `subscriber.py` to handle radar data subscriptions.
   ```sh
   python subscriber.py
   ```
