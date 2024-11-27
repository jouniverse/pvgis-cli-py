# import all from api_call.py
from api_call import *
from map_app import *


# Function for Daily radiation
def daily_radiation(output_dir):
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    month = int(input("Enter month (1-12, default: 7): ") or 7)
    if month < 1 or month > 12:
        month = 7
    tracking = input("Do you want to specify tracking options? (y/n): ") or "n"
    if tracking == "y":
        angle = input("Tracking: Enter angle/slope (default: 0): ") or 0
        aspect = input("Tracking: Enter aspect/azimuth (default: 0): ") or 0
    glob_2axis_option = (
        input(
            "Do you want to output the global, direct and diffuse two-axis tracking irradiances? (y/n): "
        )
        or "n"
    )
    if glob_2axis_option == "y":
        glob_2axis = 1
    clearsky_option = (
        input("Do you want to output the global clear-sky irradiance? (y/n): ") or "n"
    )
    if clearsky_option == "y":
        clearsky = 1
    clearsky_2axis_option = (
        input(
            "Do you want to output the global clear-sky two-axis tracking irradiance? (y/n): "
        )
        or "n"
    )
    if clearsky_2axis_option == "y":
        clearsky_2axis = 1
    showtemperatures_option = (
        input("Do you want to output the average monthly temperature? (y/n): ") or "n"
    )
    if showtemperatures_option == "y":
        showtemperatures = 1
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "month": month,
        "global": 1,
        "outputformat": outputformat,
    }
    if tracking == "y":
        params["angle"] = angle
        params["aspect"] = aspect
    if glob_2axis_option == "y":
        params["glob_2axis"] = glob_2axis
    if clearsky_option == "y":
        params["clearsky"] = clearsky
    if clearsky_2axis_option == "y":
        params["clearsky_2axis"] = clearsky_2axis
    if showtemperatures_option == "y":
        params["avtemp"] = showtemperatures
    data = make_api_call("DRcalc", params, output_dir)
    if data:
        plot_drcalc(data, output_dir)
    else:
        print("No data returned from DRcalc API call.")


def plot_drcalc(data, output_dir):
    hours = []
    radiation_values_gi = []
    radiation_values_gb = []
    radiation_values_gd = []

    lat = data["inputs"]["location"]["latitude"]
    lon = data["inputs"]["location"]["longitude"]

    month = data["outputs"]["daily_profile"][0]["month"]
    # month name
    month_name = datetime(1, month, 1).strftime("%B")

    for entry in data["outputs"]["daily_profile"]:
        hours.append(entry["time"])
        radiation_values_gi.append(entry["G(i)"])
        radiation_values_gb.append(entry["Gb(i)"])
        radiation_values_gd.append(entry["Gd(i)"])

    plt.figure(figsize=(12, 6))
    plt.plot(hours, radiation_values_gi, marker="", color="b")
    plt.plot(hours, radiation_values_gb, marker="", color="g")
    plt.plot(hours, radiation_values_gd, marker="", color="r")

    plt.title(
        f"Hourly Global, Direct and Diffuse Irradiation in {month_name} - {lat}°N, {lon}°E (DRcalc)"
    )
    plt.xlabel("Timestamp/Hour")
    plt.ylabel("Irradiation (W/m²)")
    plt.xticks(hours, fontsize=6)
    plt.legend(["Global [G(i)]", "Direct [Gb(i)]", "Diffuse [Gd(i)]"])
    plt.savefig(os.path.join(output_dir, "DRcalc_plot.png"))
    plt.close()
    print("DRcalc plot saved.")
