# import all from api_call.py
from api_call import *
from map_app import *


def tmy(output_dir):
    # TMY = typical meteorological year
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    startyear = 2005
    endyear = 2023
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "outputformat": outputformat,
        "startyear": startyear,
        "endyear": endyear,
    }
    data = make_api_call("tmy", params, output_dir)
    if data:
        plot_tmy(data, output_dir)
    else:
        print("No data returned from tmy API call.")


def plot_tmy(data, output_dir):
    print("Plotting TMY...")
    time = []
    radiation_values_gh = []
    radiation_values_gb = []
    radiation_values_gd = []
    radiation_values_ir = []

    for entry in data["outputs"]["tmy_hourly"]:
        time.append(entry["time(UTC)"])
        radiation_values_gh.append(entry["G(h)"])
        radiation_values_gb.append(entry["Gb(n)"])
        radiation_values_gd.append(entry["Gd(h)"])
        radiation_values_ir.append(entry["IR(h)"])

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs[0, 0].hist(
        time, bins=len(time), weights=radiation_values_gh, color="b", label="Global"
    )
    axs[0, 0].set_title("Global Irradiation [G(h)]")
    axs[0, 0].set_xlabel("Timestamp/Hour")
    axs[0, 0].set_ylabel("Irradiation (W/m²)")
    axs[0, 0].legend()
    # Adjusting xticks to show only month and year
    axs[0, 0].set_xticks(range(0, len(time), 438))
    axs[0, 0].tick_params(axis="x", labelsize=6, rotation=45)
    axs[0, 0].set_xticklabels(
        [entry["time(UTC)"][4:] for entry in data["outputs"]["tmy_hourly"][::438]]
    )

    axs[0, 1].hist(
        time, bins=len(time), weights=radiation_values_gb, color="g", label="Direct"
    )
    axs[0, 1].set_title("Direct Irradiation [Gb(n)]")
    axs[0, 1].set_xlabel("Timestamp/Hour")
    axs[0, 1].set_ylabel("Irradiation (W/m²)")
    axs[0, 1].legend()
    axs[0, 1].set_xticks(range(0, len(time), 438))
    axs[0, 1].tick_params(axis="x", labelsize=6, rotation=45)
    axs[0, 1].set_xticklabels(
        [entry["time(UTC)"][4:] for entry in data["outputs"]["tmy_hourly"][::438]]
    )

    axs[1, 0].hist(
        time, bins=len(time), weights=radiation_values_gd, color="r", label="Diffuse"
    )
    axs[1, 0].set_title("Diffuse Irradiation [Gd(h)]")
    axs[1, 0].set_xlabel("Timestamp/Hour")
    axs[1, 0].set_ylabel("Irradiation (W/m²)")
    axs[1, 0].legend()
    axs[1, 0].set_xticks(range(0, len(time), 438))
    axs[1, 0].tick_params(axis="x", labelsize=6, rotation=45)
    axs[1, 0].set_xticklabels(
        [entry["time(UTC)"][4:] for entry in data["outputs"]["tmy_hourly"][::438]]
    )

    axs[1, 1].hist(
        time, bins=len(time), weights=radiation_values_ir, color="y", label="IR"
    )
    axs[1, 1].set_title("IR Irradiation [IR(h)]")
    axs[1, 1].set_xlabel("Timestamp/Hour")
    axs[1, 1].set_ylabel("Irradiation (W/m²)")
    axs[1, 1].legend()
    axs[1, 1].set_xticks(range(0, len(time), 438))
    axs[1, 1].tick_params(axis="x", labelsize=6, rotation=45)
    axs[1, 1].set_xticklabels(
        [entry["time(UTC)"][4:] for entry in data["outputs"]["tmy_hourly"][::438]]
    )

    plt.tight_layout()
    plt.suptitle(
        f"TMY for {data['inputs']['location']['latitude']}°N, {data['inputs']['location']['longitude']}°E"
    )
    # move the suptitle up a few pixels
    plt.subplots_adjust(top=0.92)
    plt.savefig(os.path.join(output_dir, "TMY_plot.png"))
    plt.close()
    print("TMY plot saved.")
