"""
Title: Raw Data Reader
Author: Pietro Campolucci
"""

# import packages
import os
import pandas as pd
from tqdm import tqdm
from progressbar import progressbar


# define function
def mateksys_reader(filename):
    """ This function reads the data file and gives a dataframe of the values"""

    # path and dataframe build
    path = os.getcwd()
    file_name = filename
    log_path = path + "\\logs_raw\\" + file_name + ".data"
    df = pd.DataFrame(columns=['motion quality', 'motion x', 'motion y', 'distance quality', 'distance', 'time'])
    datafile = open(log_path, "r")

    # parse data file and append
    for data in tqdm(datafile, f"{filename}"):
        data_split = data.split(" ")
        data_sensor = data_split[2]
        data_payload = data_split[3:]
        if data_sensor == "MATEKSYS_FLOW_LIDAR":
            motion_quality = float(data_payload[1])
            motion_x = float(data_payload[2])
            motion_y = float(data_payload[3])
            distance_quality = float(data_payload[4])
            distance = float(data_payload[5][:-1])
            time = float(data_split[0])
            if 200 > motion_x > -200 and 200 > motion_y > -200 and 2000 > distance > 0:
                df_row = [motion_quality, motion_x, motion_y, distance_quality, distance, time]
                df.loc[-1] = df_row
                df.index += 1
                df = df.sort_index()

    # write dataframe to excel for storage
    df.to_excel(f"{path}\logs_converted\{filename}.xlsx")

    return df


