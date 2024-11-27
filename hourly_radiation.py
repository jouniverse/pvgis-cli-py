# import all from api_call.py
from api_call import *
from map_app import *


# Function for Hourly radiation
def hourly_radiation(output_dir):
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    # Year
    year = int(input("Enter year between 2005 and 2023 (default: 2020): ") or 2020)
    # if year is not between 2005 and 2023, set it to 2020
    if year < 2005 or year > 2023:
        year = 2020
    # Month range
    month_option = input("Do you want to specify month range? (y/n): ") or "n"
    if month_option == "y":
        month_start = int(input("Enter start month (1-12): ") or 1)
        if month_start < 1 or month_start > 12:
            month_start = 1
        month_end = int(input("Enter end month (1-12): ") or 12)
        if month_end < 1 or month_end > 12:
            month_end = 12
        if month_start > month_end:
            month_start, month_end = month_end, month_start
    # Mounting options
    mountingoptions = input("Do you want to specify mounting options? (y/n): ") or "n"
    if mountingoptions == "y":
        mountingplace = (
            input("Mounting options: Enter mounting place (default: free): ") or "free"
        )
        trackingtype = (
            input(
                "Mounting options: Enter tracking type - 0=fixed, 1=single horizontal axis aligned north-south, 2=two-axis tracking, 3=vertical axis tracking, 4=single horizontal axis aligned east-west, 5=single inclined axis aligned north-south (default: 0): "
            )
            or 0
        )
        if trackingtype == 0:
            optimalangles_option = input(
                "Mounting options - Fixed: Do you want to optimize angle/slope and aspect/azimuth? (y/n): "
            )
            if optimalangles_option == "y":
                optimalangles = 1
            else:
                optimalinclination_option = input(
                    "Mounting options - Fixed: Do you want to optimize inclination? (y/n): "
                )
                if optimalinclination_option == "y":
                    optimalinclination = 1
        #  3
        if trackingtype == 3:
            optimalinclination_option = input(
                "Mounting options - Vertical: Do you want to optimize inclination? (y/n): "
            )
            if optimalinclination_option == "y":
                optimalinclination = 1
            else:
                angle = (
                    input(
                        "Mounting options - Vertical: Enter angle/slope (default: 0): "
                    )
                    or 0
                )
        # 1 or 4 or 5
        if trackingtype == 1 or trackingtype == 4 or trackingtype == 5:
            optimalinclination_option = input(
                "Mounting options - Single axis: Do you want to optimize angle/slope ? (y/n): "
            )
            if optimalinclination_option == "y":
                optimalinclination = 1
            else:
                angle = (
                    input(
                        "Mounting options - Single axis: Enter inclination angle/slope (default: 0): "
                    )
                    or 0
                )
        # 2 -> two-axis no options
        # PV power
        pvcalculation_option = (
            input("Do you want to output the PV power? (y/n): ") or "n"
        )
        if pvcalculation_option == "y":
            pvcalculation = 1
            # "crystSi", "CIS", "CdTe" and "Unknown"
            pvtechchoice = (
                input("Enter PV technology (default: crystSi): ") or "crystSi"
            )
            peakpower = float(input("Enter peak power (kWp): ") or 1)
            loss = float(input("Enter system loss (%): ") or 14)
    components = input(
        "Do you want to output the beam, diffuse and reflected radiation components? (y/n): "
    )
    if components == "y":
        components = 1
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "outputformat": outputformat,
        "startyear": year,
        "endyear": year,
    }
    if mountingoptions == "y":
        params["mountingplace"] = mountingplace
        params["trackingtype"] = trackingtype
        if trackingtype == 0:
            if optimalangles_option == "y":
                params["optimalangles"] = optimalangles
            else:
                if optimalinclination_option == "y":
                    params["optimalinclination"] = optimalinclination
        if trackingtype == 3:
            if optimalinclination_option == "y":
                params["optimalinclination"] = optimalinclination
            else:
                params["angle"] = angle
        if trackingtype == 1 or trackingtype == 4 or trackingtype == 5:
            if optimalinclination_option == "y":
                params["optimalinclination"] = optimalinclination
            else:
                params["angle"] = angle
        if pvcalculation_option == "y":
            params["pvcalculation"] = pvcalculation
            params["pvtechchoice"] = pvtechchoice
            params["peakpower"] = peakpower
            params["loss"] = loss
    if components == "y":
        params["components"] = components
    data = make_api_call("seriescalc", params, output_dir)
    if data:
        plot_seriescalc(data, output_dir)
        if month_option == "y":
            data = filter_data_by_month(data, month_start, month_end)
            plot_seriescalc_range(data, output_dir)
    else:
        print("No data returned from seriescalc API call.")


def filter_data_by_month(data, month_start, month_end):
    filtered_data = []
    for entry in data["outputs"]["hourly"]:
        month = int(entry["time"][4:6])  # Extract month from time string
        if month_start <= month <= month_end:  # Check if month is in range
            filtered_data.append(entry)
    return filtered_data


def plot_seriescalc_range(data, output_dir):
    print("Plotting seriescalc range...")
    time = []
    # global irradiation
    radiation_values_gi = []
    # temperature
    t2m = []
    month = []

    # save range data
    output_file = os.path.join(output_dir, f"seriescalc_range.json")
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {output_file}")

    year = data[0]["time"][:4]

    for entry in data:
        time.append(entry["time"])
        radiation_values_gi.append(entry["G(i)"])
        t2m.append(entry["T2m"])
    plt.figure(figsize=(12, 6))
    time = [t[4:] for t in time]
    plt.hist(
        time,
        bins=len(time),
        weights=radiation_values_gi,
        color="b",
        histtype="bar",
        rwidth=0.8,
    )
    plt.title(f"Hourly Global Irradiation in {year} (Seriescalc)")
    plt.xlabel("Timestamp/Hour")
    plt.ylabel("Irradiation (W/m²) [G(i)]")
    # tick every 438 hours
    plt.xticks(
        ticks=range(0, len(time), 438), labels=time[::438], rotation=45, fontsize=6
    )
    # plot temperature values on another y-axis, very thin line
    plt.twinx()
    plt.plot(time, t2m, color="r", linewidth=0.5)
    plt.ylabel("Temperature (°C)")
    plt.savefig(os.path.join(output_dir, "Seriescalc_plot_range.png"))
    plt.close()
    print("Seriescalc plot range saved.")


def plot_seriescalc(data, output_dir):
    print("Plotting seriescalc...")
    time = []
    # global irradiation
    radiation_values_gi = []
    # temperature
    t2m = []

    year = data["outputs"]["hourly"][0]["time"][:4]

    for entry in data["outputs"]["hourly"]:
        time.append(entry["time"])
        radiation_values_gi.append(entry["G(i)"])
        t2m.append(entry["T2m"])
    plt.figure(figsize=(12, 6))
    plt.hist(
        time,
        bins=len(time),
        weights=radiation_values_gi,
        color="b",
        histtype="bar",
        rwidth=0.8,
    )
    plt.title(f"Hourly Global Irradiation in {year} (Seriescalc)")
    plt.xlabel("Timestamp/Hour")
    plt.ylabel("Irradiation (W/m²) [G(i)]")
    # tick every 438 hours
    plt.xticks(
        ticks=range(0, len(time), 438), labels=time[::438], rotation=45, fontsize=6
    )
    # plot temperature values on another y-axis, very thin line
    plt.twinx()
    plt.plot(time, t2m, color="r", linewidth=0.5)
    plt.ylabel("Temperature (°C)")
    plt.savefig(os.path.join(output_dir, "Seriescalc_plot.png"))
    plt.close()
    print("Seriescalc plot saved.")
