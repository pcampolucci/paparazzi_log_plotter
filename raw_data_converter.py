

# import packages
import os
from os import walk
from termcolor import colored

# import functions
from raw_data_reader import mateksys_reader

path = os.getcwd()

full = []
excel = []

for (dirpath, dirnames, filenames) in walk(f"{path}\logs_raw"):
    full.extend(filenames)
    break

for (dirpath, dirnames, filenames) in walk(f"{path}\logs_converted"):
    for file in filenames:
        if file[0] != "~":
            excel.append(file[:-5])
    break


for name in full:
    data_name = name[:-5]
    if data_name not in excel:
        mateksys_reader(data_name)
    else:
        print(colored(f"{data_name}: File already converted! Ignoring ...", 'green'))


