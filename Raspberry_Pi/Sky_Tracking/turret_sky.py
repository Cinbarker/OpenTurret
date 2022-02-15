import time

from skyfield.api import Star, wgs84
from skyfield.data import hipparcos
from skyfield.iokit import Loader
import requests
import pandas as pd
import numpy as np
import os

import platform
if platform.system() == 'Linux':  # TODO: Relative path issue. The current solution is quick and dirty.
    from CustomExceptions import *
else:
    from Raspberry_Pi.CustomExceptions import *



load = Loader(os.path.dirname(
    os.path.realpath(__file__)))  # Redefine loader to support other directories (skyfield loader removes this function)

starsFile = os.path.dirname(os.path.realpath(__file__))
starsFile += '/Common_Stars.txt'

planets = load('de440s.bsp')  # Load planets from spice kernel de440s.bsp
print('Loaded 8.5 planets, the sun, and moon')
objects = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun',
           'Moon']

stations_url = 'http://celestrak.com/NORAD/elements/active.txt'  # Load active satellites from NORAD
satellites = load.tle_file(stations_url)
print('Loaded {} satellites'.format(len(satellites)))

with load.open(hipparcos.URL) as f:  # Load stars from the Hipparcos Catalog
    df = hipparcos.load_dataframe(f)
    df = df[df['ra_degrees'].notnull()]  # Delete stars with NaN positions
print('Loaded {} stars'.format(len(df)))


def get_objects():
    """
    Get a list of solar system objects.
    """
    return objects


def get_planet_altaz(planet, location, time):
    """
    Get altaz of planets, the moon, and sun.

    :param planet: name of object of interest
    :type planet: str
    :param location: reference point location
    :type location: skyfield.toposlib.GeographicPosition
    :param time: time for which the altaz should be calculated
    :type time: skyfield.timelib.Timescale
    :return: tuple(alt, az, distance) in degrees, degrees, au
    """
    difference = planets[planet + ' barycenter'] - (planets['earth'] + location)
    topocentric = difference.at(time)
    alt, az, distance = topocentric.altaz()
    return alt.degrees, az.degrees, distance.au


def get_satellites():
    """
    Get a list of active satellites.
    """
    return list({sat.name: sat for sat in satellites})


def get_satellite_altaz(satellite, location, time):
    """
    Get altaz of active satellites.

    :param satellite: name of satellite of interest
    :type satellite: str
    :param location: reference point location
    :type location: skyfield.toposlib.GeographicPosition
    :param time: time for which the altaz should be calculated
    :type time: skyfield.timelib.Timescale
    :return: tuple(alt, az, distance) in degrees, degrees, km
    """
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name[satellite]
    difference = satellite - location
    topocentric = difference.at(time)
    alt, az, distance = topocentric.altaz()
    return alt.degrees, az.degrees, distance.km


def get_stars():
    """
    Get a list of a few common stars.
    """
    names, hips = [], []
    with open(starsFile, 'r') as file:
        file.seek(0, 2)
        eof = file.tell()
        file.seek(0, 0)
        file.readline()
        nextLine = True
        while nextLine:
            name, hip = file.readline().split('\t')
            names.append(name)
            hips.append(hip)
            if file.tell() == eof:
                nextLine = False
    file.close()
    return names, hips


def get_star_altaz(star, location, time):
    """
    Get altaz of stars in the hipparcos catalog.

    :param star: name of star of interest
    :type star: str
    :param location: reference point location
    :type location: skyfield.toposlib.GeographicPosition
    :param time: time for which the altaz should be calculated
    :type time: skyfield.timelib.Timescale
    :return: tuple(alt, az, distance) in degrees, degrees, au
    """
    star = Star.from_dataframe(df.loc[star])  # Star name must be input as HIP identifier
    delft = planets['earth'] + location
    astrometric = delft.at(time).observe(star).apparent()
    az, alt, distance = astrometric.altaz()
    return alt.degrees, az.degrees, distance.au


class AirTraffic:
    """ Air Traffic data from the Opensky Network: https://opensky-network.org """
    lat_min = 0
    lon_min = 0
    lat_max = 0
    lon_max = 0
    vehicles_df = pd.DataFrame({'A': []})

    def __init__(self, lat_min, lon_min, lat_max, lon_max):
        self.lat_min = lat_min
        self.lon_min = lon_min
        self.lat_max = lat_max
        self.lon_max = lon_max

    def update_airtraffic(self):
        """ Update airtraffic data. """
        # REQUEST API QUERY ANONYMOUSLY
        url_data = 'https://opensky-network.org/api/states/all?' + 'lamin=' + str(self.lat_min) + '&lomin=' + str(
            self.lon_min) + '&lamax=' + str(self.lat_max) + '&lomax=' + str(self.lon_max)
        response = requests.get(url_data, timeout=5).json()
        cleaned_response = [i[0:17] for i in response["states"]]

        # LOAD TO PANDAS DATAFRAME
        col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat',
                    'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
                    'squawk', 'spi', 'position_source']
        flight_df = pd.DataFrame(cleaned_response, columns=col_name)
        flight_df = flight_df.fillna('No Data')  # replace NAN with No Data
        flight_df.head()

        vehicles_df = flight_df[['icao24', 'callsign', 'lat', 'long', 'baro_altitude', 'velocity']]
        self.vehicles_df = vehicles_df[vehicles_df.ne('No Data').all(1)]

    def get_airtraffic_info(self, callsign):
        """
        Retrieve information about airtraffic

        Note: Does not update airtraffic data.
            Use update_airtraffic() to do so.

        :param callsign: name of callsign of interest
        :type callsign: str
        :return: tuple(icao, callsign, lat, long, alt, velocity)
        """
        mask = self.vehicles_df['callsign'].str.contains(callsign)
        if True not in mask.values:
            raise InvalidCallsignError('Invalid Callsign')
        vehicle = self.vehicles_df[mask]
        return tuple(vehicle.values.tolist()[0])

    def get_airtraffic_altaz(self, callsign, location, time):
        """
        Get altaz of Air Traffic.

        :param callsign: name of callsign of interest
        :type callsign: str
        :param location: reference point location
        :type location: skyfield.toposlib.GeographicPosition
        :param time: time for which the altaz should be calculated
        :type time: skyfield.timelib.Timescale
        :return: tuple(alt, az, distance) in degrees, degrees, km
        """
        _, _, lat, long, alt, _ = self.get_airtraffic_info(callsign)
        vehicle = wgs84.latlon(lat, long, alt)
        difference = vehicle - location
        topocentric = difference.at(time)
        alt, az, distance = topocentric.altaz()
        return alt.degrees, az.degrees, distance.km

    def get_airtraffic_callsigns(self, location, time):
        """
        Get air traffic callsigns sorted by distance from close to far.

        :param location: reference point location
        :type location: skyfield.toposlib.GeographicPosition
        :param time: time for which the altaz should be calculated
        :type time: skyfield.timelib.Timescale
        :return: list of callsigns sorted by distance
        """
        def get_distance(callsign):
            """ Get distance of each callsign """
            _, _, distance = self.get_airtraffic_altaz(callsign, location, time)
            return distance

        callsigns = self.vehicles_df['callsign'].values.tolist()
        callsigns = sorted([entry.strip() for entry in callsigns], key=get_distance)
        callsigns = list(filter(None, callsigns))
        return callsigns

    def fast_callsign_altaz(self, callsign, location, time):
        """
        Get altaz of just one aircraft.
        This method is much faster than get_airtraffic_callsigns() as it only updates the value of the aircraft of interest.

        :param callsign: name of callsign of interest
        :type callsign: str
        :param location: reference point location
        :type location: skyfield.toposlib.GeographicPosition
        :param time: time for which the altaz should be calculated
        :type time: skyfield.timelib.Timescale
        :return: tuple(alt, az, distance) in degrees, degrees, km
        """

        # Get altaz for just one aircraft
        # Get icao24 from callsign
        mask = self.vehicles_df['callsign'].str.contains(callsign)
        if True not in mask.values:
            raise InvalidCallsignError('Invalid Callsign')
        vehicle = self.vehicles_df[mask]
        icao24 = vehicle.values[0][0]

        url_data = 'https://opensky-network.org/api/states/all?' + '&icao24=' + str(icao24)
        try:
            response = requests.get(url_data, timeout=5).json()
            lat, long, alt = response['states'][0][6], response['states'][0][5], response['states'][0][7]
            self.vehicles_df.loc[[vehicle.index.values[0]], ('lat', 'long', 'baro_altitude')] = (lat, long, alt)
        except requests.exceptions.ReadTimeout:
            _, _, lat, long, alt, _ = self.get_airtraffic_info(
                callsign)  # Fall back on previous data if server is unavailable

        vehicle = wgs84.latlon(lat, long, alt)
        difference = vehicle - location
        topocentric = difference.at(time)
        alt, az, distance = topocentric.altaz()
        return alt.degrees, az.degrees, distance.km
