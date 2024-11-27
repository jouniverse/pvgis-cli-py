# import all from api_call.py
from api_call import *
from map_app import *


# Function for Monthly radiation
def monthly_radiation(output_dir):
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    year = input("Enter year (leave empty for all years 2005-2023): ") or ""
    mr_dni_option = (
        input("Do you want to output direct normal irradiation? (y/n): ") or "n"
    )
    if mr_dni_option == "y":
        mr_dni = 1
    selectrad_option = input("Do you want to select irradiation angle? (y/n): ") or "n"
    if selectrad_option == "y":
        selectrad = 1
        angle = input("Enter angle/slope (default: 0): ") or 0
    # the ratio of diffuse to global radiation
    d2g_option = (
        input("Do you want to output the ratio of diffuse to global radiation? (y/n): ")
        or "n"
    )
    if d2g_option == "y":
        d2g = 1
    # temperature
    avtemp_option = (
        input("Do you want to output the average monthly temperature? (y/n): ") or "n"
    )
    if avtemp_option == "y":
        avtemp = 1
    # optional output values
    outputformat = input("Enter output format (default: json): ") or "json"

    if year:
        year = int(year)  # Convert to int if a year is provided
        params = {
            "lat": latitude,
            "lon": longitude,
            "horirrad": 1,
            "outputformat": outputformat,
            "startyear": year,
            "endyear": year,
        }
    else:
        # If no year is provided, set the range from 2005 to 2023 = all years
        params = {
            "lat": latitude,
            "lon": longitude,
            "horirrad": 1,
            "outputformat": outputformat,
            "startyear": 2005,
            "endyear": 2023,
        }
    if mr_dni_option == "y":
        params["mr_dni"] = mr_dni
    if selectrad_option == "y":
        params["selectrad"] = selectrad
        params["angle"] = angle
    if d2g_option == "y":
        params["d2g"] = d2g
    if avtemp_option == "y":
        params["avtemp"] = avtemp
    data = make_api_call("MRcalc", params, output_dir)
    if data:
        plot_mrcalc(data, output_dir)
    else:
        print("No data returned from MRcalc API call.")


def plot_mrcalc(data, output_dir):
    months = []
    radiation_values = []

    lat = data["inputs"]["location"]["latitude"]
    lon = data["inputs"]["location"]["longitude"]
    # elevation = data["inputs"]["location"]["elevation"]

    # Extract data from the JSON response
    for entry in data["outputs"]["monthly"]:
        year = entry["year"]
        month = entry["month"]
        radiation = entry["H(h)_m"]

        months.append(f"{year}-{month:02d}")  # Format as YYYY-MM
        radiation_values.append(radiation)

    plt.figure(figsize=(12, 6))
    plt.plot(months, radiation_values, marker="", color="b")
    plt.title(f"Monthly Average Solar Irradiation {lat}°N, {lon}°E, (MRcalc)")
    plt.xlabel("Month")
    plt.ylabel("Irradiation (kWh/m²) [H(h)_m]")
    if len(months) > 12:
        plt.xticks(
            ticks=range(0, len(months), 12),
            labels=months[::12],
            rotation=45,
            fontsize=8,
        )
    else:
        plt.xticks(ticks=range(0, len(months)), labels=months, rotation=45, fontsize=8)
    plt.tight_layout()
    # plt.grid()

    # Save the plot
    plt.savefig(os.path.join(output_dir, "MRcalc_plot.png"))
    plt.close()
    print("MRcalc plot saved.")
