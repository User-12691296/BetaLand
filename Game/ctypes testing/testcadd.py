import sys, platform
import ctypes, ctypes.util

# Find the library and load it
mylib_path = ctypes.util.find_library("./libcadd")
if not mylib_path:
    print("Unable to find the specified library.")
    sys.exit()

try:
    cadd = ctypes.CDLL(mylib_path)
except OSError as err:
    print("Unable to load the system C library: ", err)
    sys.exit()
