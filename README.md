# Open Turret

An open sourced highly accurate pan-tilt system for anything that needs to be panned and tilted!\
My goal for this project is to make a pan tilt mechanism as precise yet low-cost as possible.

The hardware is still quite experimental, but I hope to refine it and release build instructions soon.

### To-Do

- [ ] Hardware
    - [ ] Add holes for pushing out bearings
    - [x] Make wiring rotation continuous (implement slipring)
    - [x] Add tripod mount
    - [x] Fix rigidity of pan axis
    - [ ] End-stops for tilt axis
    - [ ] Continuous tilt
    - [ ] Rotary encoder for positional feedback
    - [ ] Compass and accelerometer for positional feedback and calibration
- [ ] Document Hardware
- [ ] Explore using the Pi Zero or Wireless integrate electronics below tilt axis
- [x] Get joystick to control motors
- [ ] Make easy stepper coding interface
- [ ] Add zoom camera assembly
- [ ] Test whether the laser needs to be focussed to burn

### Code To-Do

- [ ] Add skipped step / stall error feedback
- [ ] Further optimise speed for equal steps
- [ ] Add tilt axis to all implementations
- [ ] Refractor I2C event methods
- [ ] Shutdown & Startup motion method
- [ ] Add config file

### Required Specifications

- Better than 0.1º accuracy in both pan and tilt axis
- 360º continuous pan and 135º tilt in either direction
- Support weight of a laser diode
- Have a standard mounting interface
- Be as quiet and cheap as possible
- Entirely made of off-shelf or 3D printed parts
- Safety Measures
    - IR Detection
    - Radar movement detection
    - Short Pulse duration
    - Guiding laser
    - Alert before firing
    - Kill switch
- Decent speed (~36º/s)
- Targeting System
    - Manual (joystick)
    - IR Laser guided
    - Sound Guided
    - Image guided
- On-board Status Display

### Milestones

- [x]  Implement joystick control of two axes and laser
- [ ]  Successfully move both axes with >=0.1º precision
- [ ]  Implement full system functionality including safety measures
- [ ]  Implement an automated detection and firing software

### Software Modes

- Full Manual: Control the turret and laser with a joystick
- Laser Guided: Autonomous Laser guided aiming of turret
- Sky Tracking: Use online data to track stars, planets, satellites, and air traffic. (For telescopes **NOT** lasers)

### Software Implementation Ideas

- [ ] Autonomous targeting and firing by means of image recognition
- [ ] Laser shape drawing mode
- [ ] Autonomous targeting and firing by means of acoustic triangulation

### Parts

- 2x NEMA17 Stepper Motors 0.9º 4.2 kg/cm
- 2x TMC2209 Stepper Drivers
- Joystick
- 1W Peak Laser Diode
- Bearings
- Axle Rods
- Various 3D Printed Parts
- Timing Belts
- Nuts n' Bolts

### Credit

Thank you to the following resources for making this project possible.

- Gamepad library by Piborg - https://github.com/piborg/Gamepad
- Skyfield library
- ESA, 1997, The Hipparcos and Tycho Catalogues, ESA SP-1200
- NORAD
    - CelesTrack database - https://celestrak.com/NORAD/elements/active.txt
- NAIF SPICE kernel 'de440s.bsp'
- The OpenSky Network, http://www.opensky-network.org
