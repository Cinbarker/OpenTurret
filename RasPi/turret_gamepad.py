# My Custom Gamepad Config File
# It is based on the Thrustmaster USB Joystick
# http://www.thrustmaster.com/en_US/products/usb-joystick
#

import Gamepad

class TM_joystick(Gamepad.Gamepad):
    def __init__(self, joystickNumber = 0):
        Gamepad.Gamepad.__init__(self, joystickNumber)
        self.axisNames = {
            0: 'JOY-X',
            1: 'JOY-Y',
            2: 'SLIDER',
            3: 'DPAD-X',
            4: 'DPAD-Y',
            5: 'NONE'
        }
        self.buttonNames = {
            0:  'TRIGGER',
            1:  'CENTER',
            2:  'BACK',
            3:  'RIGHT',
            4:  'NONE4',
            5:  'NONE5',
            6:  'NONE6',
            7:  'NONE7',
            8:  'NONE8',
            9:  'NONE9',
            10: 'NONE10',
            11: 'NONE11'
        }
        self._setupReverseMaps()
        
        