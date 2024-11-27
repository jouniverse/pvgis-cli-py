# PVGIS API CLI

## Description

**PVGIS API CLI** is a small Python module that fetches data from the PVGIS API<sup>1,2</sup> outputting the energy production and other relevant parameters of a PV system, depending on the user's choice of input parameters. The module is designed to be used as a CLI. The original PVGIS Tool is available [here](https://re.jrc.ec.europa.eu/pvg_tools/en/#TMY).

## Requirements

Python version:

- Python 3.10+ (the application was developed with v3.12)

Install the required packages:

```
pip install -r requirements.txt
```

_Google Chrome_ with _Selenium_ is used to take a screenshot of a web page for the PV installation site map, which is an area map around the chosen latitude and longitude, so _Google Chrome_ must be installed.

## Features

- Grid-connected PV
- Tracking PV
- Off-grid PV
- Monthly radiation
- Daily radiation
- Hourly radiation
- TMY (typical meteorological year)
- Horizon profile

## Usage

The main menu is launched by running:

```
python pvgis.py
```

The user is prompted to select the desired feature, select the location as latitude and longitude, and set other input parameters. The output is saved in the `outputs` folder in a timestamped folder. The outputs are the raw data from the API, a map of the PV installation site, and a plot of selected parameters.

The module has very little error correction and therefore the user should be careful to enter valid parameters. It cannot be used while drunk or while in a hurry, or if you are generally a careless person. Better yet, it can be used, but your contractor might be fuming, if you provide a design for a PV system in Southern France while the PV system site is in Northern Sweden.

The module can be modified to run batch jobs, i.e. to calculate a large number of scenarios automatically. This will depend on the user's needs and it will require some modifications in the scripts.

### Usage details

The module is designed to be used as a CLI, but it can be modified to be used as a GUI. The GUI can be, for example, a simple Tkinter GUI.

Map zoom level is hard-coded to 15. It can be modified at `map_app.py` line 9:

```
m = folium.Map(location=[lat, lon], zoom_start=15)
```

Output folder is hard-coded to `outputs/{timestamp}`. It can be modified at `api_call.py` lines 9-14, within the function `create_output_directory()`.

Chrome WebDriver is hardcoded in `map_app.py` line 31:

```
driver = webdriver.Chrome()
```

Where it can be changed to some other browser, e.g. Firefox, by changing the line to:

```
driver = webdriver.Firefox()
```

## License

MIT License.

<sup>1</sup> [PVGIS](https://ec.europa.eu/jrc/en/pvgis)
<sup>2</sup> [PVGIS API](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en)
