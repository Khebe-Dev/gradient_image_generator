import sys 
from struct import *

print(sys.byteorder) 
# little-endian backwards

# byte size of integers 
print(calcsize("i"))