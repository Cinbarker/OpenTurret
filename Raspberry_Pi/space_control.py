# Must install pandas: pip3 install pandas
import Space_Tracking.turret_space as space
from skyfield.api import load, wgs84

delft = wgs84.latlon(+51.99737, +4.35430, +60)  # Create earth position

ts = load.timescale()
t = ts.now()  # Get current time

print('Planet:', space.get_planet_altaz('mars', delft, t))
print('Satellite:', space.get_satellite_altaz('ISS (ZARYA)', delft, t))
print('Star:', space.get_star_altaz(11767, delft, t))

print('Air Traffic:', space.get_airtraffic_callsigns(51,2,54,8))
print('Enter callsign:')
callsign = input()
print('Vehicle:', space.get_airtraffic_altaz(callsign, delft, t))
