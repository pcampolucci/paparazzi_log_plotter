"""
Title: Main function for test visualization
Author: Pietro Campolucci
"""

from os import walk
from bs4 import BeautifulSoup
import os
import pandas as pd
from tqdm import tqdm
from termcolor import colored
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math as m


class Converter:

    def __init__(self):
        self.body = BeautifulSoup(self.read_data(), "xml")
        self.path = os.getcwd()
        self.msg = "OPTICAL_FLOW" # self.get_msg_list()[(self.let_user_pick(self.get_msg_list(), "MESSAGE"))]
        self.conv_library = self.get_conv_library()  # list of names of the already converted files
        self.raw_library = self.get_raw_library()  # list of names of the raw files

    @staticmethod
    def let_user_pick(options, pick_type):
        """ gives the user a list of items to choose """

        print(f"Please choose [{pick_type}]:")
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))
        i = input("Enter number: ")
        try:
            if 0 < int(i) <= len(options):
                return int(i) - 1
        except len(options) == 0:
            pass
        return None

    @staticmethod
    def read_data():

        with open('messages.xml', 'r') as f:
            data = f.read()

        return data

    def get_msg_list(self):

        msg_list = []

        for i in self.body.find_all("message"):
            msg_list.append(i["name"])

        return msg_list

    def get_item_msg(self):

        item_lst = []

        for i in self.body.find('message', {'name': self.msg}).find_all("field"):
            item_lst.append(i["name"])

        return item_lst

    def get_conv_library(self):
        conv_lib = []

        for (dirpath, dirnames, filenames) in walk(f"{self.path}/logs_converted"):
            for file in filenames:
                if file[0] != "~":
                    conv_lib.append(file[:-4])
            break

        return conv_lib

    def get_raw_library(self):

        raw_lib = []

        for (dirpath, dirnames, filenames) in walk(f"{self.path}/logs_raw"):
            raw_lib.extend(filenames)
            break

        return raw_lib

    def convert(self):

        for name in self.raw_library:
            data_name_w_msg = name[:-5] + f"_{self.msg}"
            data_name = name[:-5]
            if data_name_w_msg not in self.conv_library:
                print(colored(f"{data_name_w_msg}: File to be converted. Conversion started ...", 'blue'))
                self.logs_reader(data_name)
            else:
                print(colored(f"{data_name_w_msg}: File already converted! Ignoring ...", 'yellow'))

    def logs_reader(self, filename):
        """ This function reads the data file and gives a dataframe of the values"""

        # path and dataframe build
        file_name = filename
        log_path = self.path + "/logs_raw/" + file_name + ".data"
        msg_list = self.get_item_msg()
        df = pd.DataFrame(columns=msg_list)
        datafile = open(log_path, "r")

        # parse data file and append
        for data in tqdm(datafile, f"{filename}"):
            data_split = data.split(" ")
            data_sensor = data_split[2]
            data_payload = data_split[3:]
            if data_sensor == self.msg:
                df_row = np.zeros(len(msg_list))
                for value in range(len(msg_list)):
                    df_row[value] = float(data_payload[value])

                df.loc[-1] = df_row
                df.index += 1
                df = df.sort_index()

        # write dataframe to csv for storage
        df.to_csv(f"{self.path}/logs_converted/{filename}_{self.msg}.csv")
        print(colored(f"File written to {self.path}/logs_converted/{filename}_{self.msg}.csv", 'green'))

        return df

    def plot(self, start, end):

        # let the user pick the file from the library
        file_choice = self.let_user_pick(self.conv_library, "DATAFILE")

        filename = self.conv_library[file_choice] + ".csv"

        dataframe = pd.read_csv(f"{self.path}/logs_converted/{filename}")
        diff_dataframe = dataframe.diff()
        len_dataframe = len(dataframe.index)
        start = int(start*len_dataframe)
        end = int(end*len_dataframe)

        # build derived values
        dataframe["velocity_x"] = dataframe["ground_distance"] * np.tan(np.radians(dataframe["flow_x"]))
        dataframe["velocity_y"] = dataframe["ground_distance"] * np.tan(np.radians(dataframe["flow_y"]))

        print(f"The file contains data on:\n{list(dataframe.columns)[1:]}\n ... and contains {len(dataframe.index)} samples")

        sns.set_style('whitegrid')

        plt.figure(figsize=[10, 5])
        plt.title(f"LOG: {filename[:-4]}.data - flow in deg/sec")
        # sns.lineplot(x=dataframe['time_sec'][start:end], y=dataframe['flow_x'][start:end], label="Motion X")
        # sns.lineplot(x=dataframe['time_sec'][start:end], y=dataframe['flow_y'][start:end], label="Motion Y")
        # sns.lineplot(x=dataframe['time_sec'][start:end], y=dataframe['ground_distance'][start:end] * 100, label="AGL [cm]")
        # sns.lineplot(x=dataframe['time_sec'][start:end], y=dataframe['velocity_x'][start:end] * 100, label="Velocity X [mm/sec]")
        # sns.lineplot(x=dataframe['time_sec'][start:end], y=dataframe['velocity_y'][start:end] * 100, label="Velocity Y [mm/sec]")

        sns.lineplot(x=dataframe['time_sec'][start:end], y=diff_dataframe['time_sec'][start:end]*-10**(-9), label="Delta time [sec]")

        plt.show()


#################################################################

conv = Converter()
# conv.convert()
conv.plot(0.05, 0.3)


