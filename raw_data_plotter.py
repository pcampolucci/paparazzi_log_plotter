"""
Title: Raw Data Plotter
Author: Pietro Campolucci
"""

# import packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import walk
import math
import numpy as np


# design menu function
def let_user_pick(options, pick_type):
    """ gives the user a list of excel files that he can plot """
    print(f"Please choose [{pick_type}]:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)-1
    except len(options) == 0:
        pass
    return None


# get files from the converted folder
excel_files = []
path = os.getcwd()

for (dirpath, dirnames, filenames) in walk(f"{path}\logs_converted"):
    for file in filenames:
        if file[0] != "~":
            excel_files.append(file[:-5])
    break


# initialize menu
choice = let_user_pick(excel_files, "DATA")
motion = let_user_pick(["Circlular Motion", "Linear Motion"], "MOTION")
filename = excel_files[choice] + ".xlsx"


# open dataframe
matek_df = pd.read_excel(f"{path}\logs_converted\{filename}", engine='openpyxl')
matek_df["motion x adjusted"] = matek_df["distance"] * matek_df["motion x"].apply(lambda x: math.sin(x*math.pi/180))
matek_df["motion y adjusted"] = matek_df["distance"] * matek_df["motion y"].apply(lambda x: math.sin(x*math.pi/180))


def plot_circular_cnc(diameter, speed, time):
    """ estimate x and y velocity in [mm/sec] """
    speed_new = speed / 60
    radius_new = (diameter/2)
    angular_frequency = speed_new/radius_new
    angle_at_time = (angular_frequency*time)
    x_velocity = -speed_new*math.sin(angle_at_time)
    y_velocity = speed_new*math.cos(angle_at_time)
    return x_velocity, y_velocity


def plot_step_cnc(length, speed, time):
    """ estimate x velocity in a straight line """
    speed_new = speed / 60
    time_for_one = length/speed_new
    if int(time/time_for_one)%2 == 0:
        velocity = speed_new
    else:
        velocity = -speed_new
    return velocity


# set parameters for ground truth
start = 0
end = -1
shift = 20
shift2 = 40
diameter = 300
length = 900
speed = 4000
time_circle = np.arange(shift, 130-shift)
x_motion_circle = [plot_circular_cnc(diameter, speed, t + shift2)[0] for t in time_circle]
y_motion_circle = [plot_circular_cnc(diameter, speed, t + shift2)[1] for t in time_circle]
x_motion_straight = [plot_step_cnc(length, speed, t + shift2) for t in time_circle]

# plot data
plt.figure(figsize=[10,5])
plt.title(f"LOG: {filename[:-5]}.data")
sns.lineplot(matek_df['time'][start:end], matek_df['motion y adjusted'][start:end])
sns.lineplot(matek_df['time'][start:end], matek_df['motion x adjusted'][start:end])
sns.lineplot(matek_df['time'][start:end], matek_df['motion quality'][start:end])
if motion == 0:
    sns.lineplot(time_circle, y_motion_circle)
if motion == 1:
    sns.lineplot(time_circle, x_motion_straight)
plt.show()

