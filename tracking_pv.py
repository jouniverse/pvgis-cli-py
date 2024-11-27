# import all from api_call.py
from api_call import *
from map_app import *


def tracking_pv(output_dir):
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
    trackingoptions = input("Do you want to specify tracking options? (y/n): ") or "n"
    if trackingoptions == "y":
        inclinedaxis_option = (
            input(
                "Tracking options: Do you want to output a single inclined axis system? (y/n): "
            )
            or "n"
        )
        if inclinedaxis_option == "y":
            inclined_axis = 1
            optimise_inclination = (
                input("Inclined axis: Do you want to optimize inclination? (y/n): ")
                or "n"
            )
            if optimise_inclination == "y":
                inclined_optimum = 1
            else:
                inclinedaxisangle = (
                    input("Inclined axis: Enter angle/slope (default: 0)") or 0
                )
        verticalaxis_option = (
            input(
                "Tracking options: Do you want to output a single vertical axis system? (y/n): "
            )
            or "n"
        )
        if verticalaxis_option == "y":
            verticalaxis = 1
            optimise_vertical = (
                input("Vertical axis: Do you want to optimize vertical axis? (y/n): ")
                or "n"
            )
            if optimise_vertical == "y":
                vertical_optimum = 1
            else:
                verticalaxisangle = (
                    input("Vertical axis: Enter angle/slope (default: 0)") or 0
                )
        twoaxis_option = (
            input("Tracking options: Do you want to output a two axis system? (y/n): ")
            or "n"
        )
        if twoaxis_option == "y":
            twoaxis = 1
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "pvtechchoice": pvtechnology,
        "peakpower": peakpower,
        "loss": loss,
        "outputformat": outputformat,
    }
    if trackingoptions == "y":
        if inclinedaxis_option == "y":
            params["inclined_axis"] = inclined_axis
            if optimise_inclination == "y":
                params["inclined_optimum"] = inclined_optimum
            else:
                params["inclinedaxisangle"] = inclinedaxisangle
        if verticalaxis_option == "y":
            params["verticalaxis"] = verticalaxis
            if optimise_vertical == "y":
                params["vertical_optimum"] = vertical_optimum
            else:
                params["verticalaxisangle"] = verticalaxisangle
        if twoaxis_option == "y":
            params["twoaxis"] = twoaxis
    data = make_api_call("PVcalc", params, output_dir)
    if data:
        plot_trackingcalc(data, output_dir)
    else:
        print("No data returned from trackingcalc API call.")


def plot_trackingcalc(data, output_dir):
    months = [item["month"] for item in data["outputs"]["monthly"]["fixed"]]
    energy_monthly = [item["E_m"] for item in data["outputs"]["monthly"]["fixed"]]
    energy_daily = [item["E_d"] for item in data["outputs"]["monthly"]["fixed"]]

    lat = data["inputs"]["location"]["latitude"]
    lon = data["inputs"]["location"]["longitude"]

    plt.figure(figsize=(10, 5))
    plt.plot(months, energy_monthly, marker="", color="b")
    plt.plot(months, energy_daily, marker="", color="g")
    plt.title(f"Monthly Energy Production {lat}°N, {lon}°E (Trackingcalc)")
    plt.xlabel("Month")
    plt.ylabel("Energy (kWh)")
    plt.xticks(months)
    # add legend
    plt.legend(["Monthly Avg [E_m]", "Daily Avg [E_d]"])
    # plt.grid()

    plt.savefig(os.path.join(output_dir, "PVcalc_Trackingcalc_plot.png"))
    plt.close()
    print("Trackingcalc plot saved.")
