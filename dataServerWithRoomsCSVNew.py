#THis script parses sensors' names and assigns rooms to sensors respectively

import requests
from requests.auth import HTTPBasicAuth
import time
from flask import Flask, jsonify
import json
import keys
import pandas as pd
import csv
import threading
from threading import Thread

# Create a semaphore object
semaphore = threading.Semaphore(100)

# Create a shared flag for all threads
running = threading.Event()
running.set()  

# Create a lock
data_lock = threading.Lock()

password = keys.password
username = keys.username

app_data = Flask(__name__)

#context data
data = {"context": {"sensors": []}}
rooms = ["A01", "A02", "A03", "B03", "B04", "C01", "C02", "C03", "D01", "D02", "D03"]

def send_get_request(url, username, password):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an HTTPError for bad responses
        #time.sleep(5)  # Add a delay between each request
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def assign_rooms(sensor_name):
    for room in rooms:
        if room in sensor_name:
            return room
    return None

def parse_sensor_data(response_text):
    # Modify this function based on the actual structure of your response
    response_json = json.loads(response_text)
    name = response_json.get("displayName", "")
    present_value_dict = response_json.get("present-value", "")
    
    # Extract the value associated with the "value" key
    present_value = present_value_dict.get("value", "") if present_value_dict else ""
    
    # Assign a room based on the sensor name
    room = assign_rooms(name)
    
    return {"name": name, "present_value": present_value, "room": room}
        
def save_to_file(data_to_save, filename):
    with open(filename, 'w', newline='') as file:
        fieldnames = data_to_save[0].keys()  # Get the keys from the first dictionary
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(data_to_save)
            

def update_csv_file(filename, sensor_name, room_name, present_value):
    # Load the existing CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Find the row where the sensor name and room name match the given values
    mask = (df['name'] == sensor_name) & (df['room'] == room_name)

    if df[mask].empty:
        # If no existing row matches, append a new row
        new_row = pd.DataFrame({'name': [sensor_name], 'room': [room_name], 'present_value': [present_value]})
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        # Otherwise, update the value in the 'present_value' column of this row
        df.loc[mask, 'present_value'] = present_value

    # Write the DataFrame back to the CSV file
    df.to_csv(filename, index=False)
        

def get_data(api_name, url, username, password):
    while running.is_set():  # Check the flag in the loop condition
        semaphore.acquire()
        try:
            result = send_get_request(url, username, password)
            print("Server response:", result)  # Print the server's response

            parsed_data = parse_sensor_data(result)

            with data_lock:
                data["context"]["sensors"].append(parsed_data)
                if 'present_value' in parsed_data:
                    update_csv_file("all_sensor_data_present_values.csv", parsed_data['name'], parsed_data['room'], parsed_data['present_value'])
                else:
                    print(f"Warning: 'value' key not found in sensor_data: {parsed_data}")
        finally:
            semaphore.release()

def clean_data():
    # Stop all threads
    running.clear()

    # Clean the data dictionary
    data["context"]["sensors"] = []

    # Clear the CSV file
    with open("all_sensor_data_present_values.csv", "w") as f:
        f.write("")

        
@app_data.route("/get_data", methods=["GET"])
def provide_data():
    return jsonify(data)

if __name__ == "__main__":
    # Read the list of sensors from a file
    with open("sensors_list.txt", "r") as sensor_file:
        sensor_list = [line.strip() for line in sensor_file]

    # Define API parameters based on the sensor list
    apis = []
    for sensor in sensor_list:
        api = {
            "name": sensor,
            "url": f"https://link_here/{sensor}?alt=json",
            "username": username,
            "password": password,
        }
        apis.append(api)

    # Start the data fetching process for each API in a separate thread
    for api in apis:
        data_fetch_thread = Thread(target=get_data, args=(api["name"], api["url"], api["username"], api["password"]))
        data_fetch_thread.start()
        
    # Run the Flask app to provide data
    app_data.run(port=5002, debug=True)
