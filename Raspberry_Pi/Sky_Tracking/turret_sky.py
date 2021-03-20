from skyfield.api import Star, wgs84
from skyfield.data import hipparcos
from skyfield.iokit import Loader
import requests
import pandas as pd
import numpy as np
import wmm2020
import os

load = Loader(os.path.dirname(os.path.realpath(__file__)))  # Redefine loader to support other directories (skyfield loader removes this function)

planets = load('de440s.bsp')  # Load planets from spice kernel de440s.bsp
print('Loaded 8.5 planets, the sun, and moon')

stations_url = 'http://celestrak.com/NORAD/elements/active.txt'  # Load active satellites from NORAD
satellites = load.tle_file(stations_url)
print('Loaded {} satellites'.format(len(satellites)))

with load.open(hipparcos.URL) as f:  # Load stars from the Hipparcos Catalog
    df = hipparcos.load_dataframe(f)
    df = df[df['ra_degrees'].notnull()]  # Delete stars with NaN positions
print('Loaded {} stars'.format(len(df)))


def get_planet_altaz(planet, location, time):  # Get altaz of planets, the moon, and sun
    difference = planets[planet + ' barycenter'] - (planets['earth'] + location)
    topocentric = difference.at(time)
    alt, az, distance = topocentric.altaz()
    return alt.degrees, az.degrees, distance.au


def get_satellite_altaz(satellite, location, time):  # Get altaz of active satellites
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name[satellite]
    difference = satellite - location
    topocentric = difference.at(time)
    alt, az, distance = topocentric.altaz()
    return alt.degrees, az.degrees, distance.km


def get_star_altaz(star, location, time):
    star = Star.from_dataframe(df.loc[star])  # Star name must be input as HIP identifier
    delft = planets['earth'] + location
    astrometric = delft.at(time).observe(star).apparent()
    az, alt, distance = astrometric.altaz()
    return alt.degrees, az.degrees, distance.au


def get_mag_data(location, time):
    year, _, _, _, _, _ = time._utc_tuple(0)
    np.meshgrid()
    mag = wmm2020.wmm(location.latitude.degrees, location.longitude.degrees, location.elevation.km, year)
    decl = float(mag.data_vars.get('decl'))
    incl = float(mag.data_vars.get('incl'))
    total = float(mag.data_vars.get('total'))
    return decl, incl, total


class AirTraffic:
    lat_min = 0
    lon_min = 0
    lat_max = 0
    lon_max = 0
    vehicles_df = pd.DataFrame({'A' : []})

    def __init__(self, lat_min, lon_min, lat_max, lon_max):
        self.lat_min = lat_min
        self.lon_min = lon_min
        self.lat_max = lat_max
        self.lon_max = lon_max

    def update_airtraffic(self):
        # REST API QUERY ANONYMOUSLY
        url_data = 'https://opensky-network.org/api/states/all?' + 'lamin=' + str(self.lat_min) + '&lomin=' + str(
            self.lon_min) + '&lamax=' + str(self.lat_max) + '&lomax=' + str(self.lon_max)
        response = requests.get(url_data).json()

        # LOAD TO PANDAS DATAFRAME
        col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat',
                    'baro_altitude',
                    'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
                    'position_source']
        flight_df = pd.DataFrame(response['states'], columns=col_name)
        flight_df = flight_df.fillna('No Data')  # replace NAN with No Data
        flight_df.head()

        vehicles_df = flight_df[['callsign', 'lat', 'long', 'baro_altitude', 'velocity']]
        self.vehicles_df = vehicles_df[vehicles_df.ne('No Data').all(1)]

    def get_airvehicle_info(self, callsign):
        try:
            mask = self.vehicles_df['callsign'].str.contains(callsign)
        except IndexError:
            print('Invalid Callsign')
            return None
        vehicle = self.vehicles_df[mask]
        return tuple(vehicle.values.tolist()[0])

    def get_airvehicle_altaz(self, callsign, location, time):
        try:
            _, lat, long, alt, _ = self.get_airvehicle_info(callsign)
        except IndexError:
            print('Invalid Callsign')
            return None
        vehicle = wgs84.latlon(lat, long, alt)
        difference = vehicle - location
        topocentric = difference.at(time)
        alt, az, distance = topocentric.altaz()
        return alt.degrees, az.degrees, distance.km

    def get_airtraffic_callsigns(self, location, time):
        def get_distance(callsign):
            _, _, distance = self.get_airvehicle_altaz(callsign, location, time)
            return distance

        callsigns = self.vehicles_df['callsign'].values.tolist()
        callsigns = sorted([entry.strip() for entry in callsigns], key=get_distance)
        callsigns = list(filter(None, callsigns))
        return callsigns
