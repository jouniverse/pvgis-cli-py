# import all from api_call.py
from api_call import *
from map_app import *


# Function for Grid-connected PV systems
def grid_connected(output_dir):
    # obligatory parameters
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    # "crystSi", "CIS", "CdTe" and "Unknown"
    pvtechnology = input("Enter PV technology (default: crystSi): ") or "crystSi"
    peakpower = float(input("Enter peak power (kWp): ") or 0.5)
    loss = float(input("Enter system loss (%): ") or 14)
    mountingoptions = input("Do you want to specify mounting options? (y/n): ") or "n"
    if mountingoptions == "y":
        # free, building
        mountingplace = (
            input("Mounting options: Enter mounting place (default: free): ") or "free"
        )
        optimal = (
            input(
                "Mounting options: Do you want to optimize angle/slope and aspect/azimuth? (y/n): "
            )
            or "n"
        )
        if optimal == "y":
            optimalinclination = 1
            optimalangles = 1
        else:
            # optimize angle only
            optimizeangle = (
                input("Mounting options: Do you want to optimize angle/slope? (y/n): ")
                or "n"
            )
            if optimizeangle == "y":
                optimalangles = 1
            else:
                angle = input("Mounting options: Enter angle/slope (default: 0): ") or 0
                aspect = (
                    input("Mounting options: Enter aspect/azimuth (default: 0): ") or 0
                )
    price = input("Do you want to specify the price options? (y/n): ") or "n"
    if price == "y":
        pvprice = 1
        lifetime = int(input("Price options: Enter lifetime (default: 25): ") or 25)
        systemcost = float(
            input("Price options: Enter system cost (default: 0): ") or 0
        )
        interest = float(input("Price options: Enter interest (%): ") or 0)
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "pvtechnology": pvtechnology,
        "peakpower": peakpower,
        "loss": loss,
        "outputformat": outputformat,
    }
    if mountingoptions == "y":
        params["mountingplace"] = mountingplace
        if optimal == "y":
            params["optimalinclination"] = optimalinclination
            params["optimalangles"] = optimalangles
        else:
            if optimizeangle == "y":
                params["optimalangles"] = optimalangles
            else:
                params["angle"] = angle
            params["aspect"] = aspect
    if price == "y":
        params["lifetime"] = lifetime
        params["pvprice"] = pvprice
        params["systemcost"] = systemcost
        params["interest"] = interest
    data = make_api_call("PVcalc", params, output_dir)
    if data:
        plot_pvcalc(data, output_dir)
    else:
        print("No data returned from PVcalc API call.")


# Function to plot data for PVcalc
def plot_pvcalc(data, output_dir):
    months = [item["month"] for item in data["outputs"]["monthly"]["fixed"]]
    energy_monthly = [item["E_m"] for item in data["outputs"]["monthly"]["fixed"]]
    energy_daily = [item["E_d"] for item in data["outputs"]["monthly"]["fixed"]]

    lat = data["inputs"]["location"]["latitude"]
    lon = data["inputs"]["location"]["longitude"]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    color = "tab:red"
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Monthly Energy (kWh) [E_m]", color=color)
    ax1.plot(months, energy_monthly, color=color)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_xticks(months)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = "tab:green"
    ax2.set_ylabel(
        "Daily Energy (kWh) [E_d]", color=color
    )  # we already handled the x-label with ax1
    ax2.plot(months, energy_daily, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title(f"Monthly and Daily Energy Production {lat}°N, {lon}°E (PVcalc)")
    # move plot up 10%
    plt.subplots_adjust(top=0.92)

    plt.savefig(os.path.join(output_dir, "PVcalc_plot.png"))
    plt.close()
    print("PVcalc plot saved.")
