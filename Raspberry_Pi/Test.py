import os
cmd = './whereami'
so = os.popen(cmd).read()
print(so)

import Sky_Tracking.turret_sky as sky
from skyfield.api import load, wgs84
from Sky_Tracking.turret_sky import AirTraffic

currentLocation = wgs84.latlon(+51.99737, +4.35430, +60)  # Coordinates of turret earth position

lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8  # Define air traffic scanning region

ts = load.timescale()
time = ts.now()  # Get current time

at = AirTraffic(lat_min, lon_min, lat_max, lon_max)
at.update_airtraffic()
callsigns = at.get_airtraffic_callsigns(currentLocation, time)