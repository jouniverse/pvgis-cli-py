# import all from api_call.py
from api_call import *
from map_app import *


# Function for Off-grid PV systems
def off_grid(output_dir):
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    peakpower = float(input("Enter peak power (kWp): ") or 50)
    batterysize = float(input("Enter battery size (Ah): ") or 600)
    cutoff = float(input("Enter discharge cutoff limit (%): ") or 40)
    consumptionday = float(input("Enter daily consumption (Wh): ") or 300)
    angle = float(input("Enter angle/slope (default: 35): ") or 35)
    aspect = float(input("Enter aspect/azimuth (default: 0): ") or 0)
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "peakpower": peakpower,
        "batterysize": batterysize,
        "consumptionday": consumptionday,
        "cutoff": cutoff,
        "angle": angle,
        "aspect": aspect,
        "outputformat": outputformat,
    }
    data = make_api_call("SHScalc", params, output_dir)
    if data:
        plot_shcalc(data, output_dir)
    else:
        print("No data returned from SHScalc API call.")


# Function to plot data for SHScalc
def plot_shcalc(data, output_dir):
    # Assuming SHScalc returns similar structured data
    months = [item["month"] for item in data["outputs"]["monthly"]]
    energy_daily = [item["E_d"] for item in data["outputs"]["monthly"]]
    energy_daily_lost = [item["E_lost_d"] for item in data["outputs"]["monthly"]]

    lat = data["inputs"]["location"]["latitude"]
    lon = data["inputs"]["location"]["longitude"]

    plt.figure(figsize=(10, 5))
    plt.plot(months, energy_daily, marker="", color="g")
    plt.plot(months, energy_daily_lost, marker="", color="r")
    plt.title(f"Daily Avg Energy Production Monthly {lat}°N, {lon}°E  (SHScalc)")
    plt.xlabel("Month")
    plt.ylabel("Energy (kWh)")
    plt.xticks(months)
    # add legend
    plt.legend(["Daily Avg [E_d]", "Daily Lost [E_lost_d]"])
    # plt.grid()

    plt.savefig(os.path.join(output_dir, "SHScalc_plot.png"))
    plt.close()
    print("SHScalc plot saved.")
