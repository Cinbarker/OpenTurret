import os
cmd = './whereami'
so = os.popen(cmd).read()
print(so)