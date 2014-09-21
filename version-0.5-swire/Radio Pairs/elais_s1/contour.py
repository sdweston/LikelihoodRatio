
import math 

sqrt2=math.sqrt(2)

n=1
rms=20.0 * 10 ** -6
level=rms 

# take max level to be max(sint) from atlas table4

while (level < 200.0):
      level=rms * 3* sqrt2 ** n
      n=n+1
      print '%.7f' % level
