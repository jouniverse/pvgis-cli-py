import folium
from selenium import webdriver
import time
import os


def create_map(lat, lon, output_dir):
    # Create a map centered at the specified location
    m = folium.Map(location=[lat, lon], zoom_start=15)

    # Add a marker for the specified location
    folium.Marker([lat, lon], popup="Marker").add_to(m)

    # Save the map to an HTML file
    map_file = "map.html"
    m.save(map_file)

    # Get the absolute path to the map.html file
    map_file = os.path.abspath(map_file)

    # Use Selenium to take a screenshot of the map
    take_screenshot(map_file, output_dir)


def take_screenshot(map_file, output_dir, prefix="PV_installation_site_map"):
    # Check if the file exists
    if not os.path.exists(map_file):
        print(f"Error: The file {map_file} does not exist.")
    else:
        # Set up Selenium WebDriver
        driver = webdriver.Chrome()  # or the appropriate driver for your browser

        # Load the map HTML file
        driver.get(f"file://{map_file}")  # Use the correct path to your map.html

        # Wait for the map to load completely
        time.sleep(5)  # Adjust the sleep time as necessary

        # Take a screenshot
        driver.save_screenshot(os.path.join(output_dir, f"{prefix}.png"))

        # Close the browser
        driver.quit()
