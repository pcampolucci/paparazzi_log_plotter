"""
Title: Main function for test visualization
Author: Pietro Campolucci
"""

# import functions
from raw_data_reader import mateksys_reader

# get dataframe
filename = "20_12_11__16_57_05"
matek_df = mateksys_reader(filename)


print(matek_df.head())


