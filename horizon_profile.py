# import all from api_call.py
from api_call import *
from map_app import *


# Function for Horizon profile
def horizon_profile(output_dir):
    latitude = float(input("Enter latitude: ") or 37.2435)
    longitude = float(input("Enter longitude: ") or -115.8115)
    # save map
    print("Saving map...")
    create_map(latitude, longitude, output_dir)
    print("Map saved.")
    # output format
    outputformat = input("Enter output format (default: json): ") or "json"

    params = {
        "lat": latitude,
        "lon": longitude,
        "outputformat": outputformat,
    }
    data = make_api_call("printhorizon", params, output_dir)
    if data:
        horizon_profile_plot(data, output_dir)
    else:
        print("No data returned from horizon profile API call.")


# horizon_profile -> Azimuth, Horizon height
# winter_solstice -> Sun Azimuth, Sun height
# summer_solstice -> Sun Azimuth, Sun height
def horizon_profile_plot(data, output_dir):
    horizon_profile_A = []
    horizon_profile_H_hor = []

    winter_solstice_A = []
    winter_solstice_H_sun = []

    summer_solstice_A = []
    summer_solstice_H_sun = []

    for entry in data["outputs"]["horizon_profile"]:
        horizon_profile_A.append(entry["A"])
        horizon_profile_H_hor.append(entry["H_hor"])

    for entry in data["outputs"]["winter_solstice"]:
        winter_solstice_A.append(entry["A_sun(w)"])
        winter_solstice_H_sun.append(entry["H_sun(w)"])

    for entry in data["outputs"]["summer_solstice"]:
        summer_solstice_A.append(entry["A_sun(s)"])
        summer_solstice_H_sun.append(entry["H_sun(s)"])

    # plot and save the figure
    plt.figure(figsize=(10, 5))
    plt.plot(horizon_profile_A, horizon_profile_H_hor, label="Horizon Profile")
    plt.plot(winter_solstice_A, winter_solstice_H_sun, label="Winter Solstice")
    plt.plot(summer_solstice_A, summer_solstice_H_sun, label="Summer Solstice")
    plt.legend()
    # plot title data["inputs"]["location"][latitude]
    plt.title(
        f"Horizon profile: {data['inputs']['location']['latitude']}°N, {data['inputs']['location']['longitude']}°E"
    )
    plt.savefig(os.path.join(output_dir, "horizon_profile_plot.png"))
    plt.close()
    print("Horizon profile plot saved.")
