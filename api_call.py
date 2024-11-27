import os
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def create_output_directory():
    # Create output directory based on timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_dir = f"outputs/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


# Define the base URL for the PVGIS API
base_url = "https://re.jrc.ec.europa.eu/api"


# Function to make API calls and save results
def make_api_call(endpoint, params, output_dir):
    url = f"{base_url}/{endpoint}"

    response = requests.get(url, params=params)

    if response.status_code == 200:
        if params["outputformat"] == "csv" or params["outputformat"] == "basic":
            # Handle CSV response
            output_file = os.path.join(output_dir, f"{endpoint}.csv")
            with open(output_file, "w") as csv_file:
                csv_file.write(response.text)  # Write the raw CSV response directly

            print(f"Data saved to {output_file}")

            # Change output format to JSON for plotting
            params["outputformat"] = "json"
            response = requests.get(url, params=params)
            return response.json()

        else:
            # Handle JSON response
            try:
                data = response.json()  # Attempt to decode JSON
            except json.JSONDecodeError:
                print(f"Error decoding JSON from response: {response.text}")
                return None

            output_file = os.path.join(output_dir, f"{endpoint}.json")
            with open(output_file, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data saved to {output_file}")
            return data  # Return the data for plotting
    else:
        print(f"Failed to fetch data from {endpoint}: {response.status_code}")
        return None
