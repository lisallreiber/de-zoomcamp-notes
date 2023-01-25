
import os 
import pandas as pd

# for debugging print all the args in the system environment
# import sys
# print(sys.argv)
# day = sys.argv[1]

day = os.getenv("DAY")
# some fancy stuff with pandas

print(f'job finished successfully for day = {day}')