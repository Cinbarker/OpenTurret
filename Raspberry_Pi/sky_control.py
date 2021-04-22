# Must install pandas: pip3 install pandas
import Sky_Tracking.turret_sky as sky
from skyfield.api import load, wgs84
from Sky_Tracking.turret_sky import AirTraffic
from time import sleep

currentLocation = wgs84.latlon(+51.99737, +4.35430, +60)  # Coordinates of turret earth position

lat_min, lon_min, lat_max, lon_max = 51, 2, 54, 8  # Define air traffic scanning region

ts = load.timescale()
time = ts.now()  # Get current time

at = AirTraffic(lat_min, lon_min, lat_max, lon_max)

if __name__ == '__main__':
    # print('Mag Data:', sky.get_mag_data(currentLocation, time))
    print('Planet:', sky.get_planet_altaz('mars', currentLocation, time))
    print('Satellite:', sky.get_satellite_altaz('STARLINK-1099', currentLocation, time))
    print('Star:', sky.get_star_altaz(11767, currentLocation, time))

    at.update_airtraffic()
    print('Air Traffic:', at.get_airtraffic_callsigns(currentLocation, time))
    callsign = input('Enter callsign: ')
    print('Vehicle:', at.get_airtraffic_altaz(callsign, currentLocation, time))
    while True:
        print(at.fast_callsign_altaz(callsign, currentLocation, time))
