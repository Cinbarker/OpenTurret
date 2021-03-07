# Must install pandas: pip3 install pandas
import Space_Tracking.turret_space as space
from skyfield.api import load, wgs84
from Space_Tracking.turret_space import AirTraffic

currentLocation = wgs84.latlon(+51.99737, +4.35430, +60)  # Coordinates of turret earth position

lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8  # Define air traffic scanning region

ts = load.timescale()
t = ts.now()  # Get current time

at = AirTraffic(lat_min, lon_min, lat_max, lon_max)

print('Planet:', space.get_planet_altaz('mars', currentLocation, t))
print('Satellite:', space.get_satellite_altaz('STARLINK-1099', currentLocation, t))
print('Star:', space.get_star_altaz(11767, currentLocation, t))

at.update_airtraffic()
print('Air Traffic:', at.get_airtraffic_callsigns(currentLocation, t))
print('Enter callsign:')
callsign = input()
print('Vehicle:', at.get_airvehicle_altaz(callsign, currentLocation, t))

