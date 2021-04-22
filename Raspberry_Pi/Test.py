import os

cmd = './whereami'
so = os.popen(cmd).read()
print(so)

import Sky_Tracking.turret_sky as sky

print(sky.objects)
