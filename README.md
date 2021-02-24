# Open Turret

An open sourced highly accurate pan-tilt system for anything that needs to be panned and tilted!

### To-Do:

- [ ]  Hardware
    - [ ]  Add holes for pushing out bearings
    - [ ]  Make wiring rotation continuous (implement slipring)
    - [ ]  Add tripod mount
    - [ ]  Fix rigidity of pan axis
- [ ]  Document Hardware
- [ ]  Explore using the Pi Zero or Wireless integrate electronics below tilt axis
- [x]  Get joystick to control motors
- [ ]  Make easy stepper coding interface
- [ ]  Add zoom camera assembly
- [ ]  Test whether I need to focus the laser

### Code To-Do:

- [ ] Add skipped step / stall error feedback
- [ ] Further optimise speed for equal steps
- [ ] Return to home button
- [ ] D-pad steps
- [ ] D-pad Speed modes
- [ ] Send zero signal from pi before exiting code on exit button (reset method) => exithandler atexit
- [x] Fix thread error when firing laser

### Specifications:

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

- [ ]  Successfully move both axes with 0.1º precision
- [ ]  Implement an automated detection and firing software

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
