import os

controlled_data = os.path.join("data","private.csv")
public_data = os.path.join("data","example.csv")

if os.path.isfile(controlled_data):
    DATA_FILE = controlled_data
else:
    DATA_FILE = public_data

MAX_DF = 0.67
MIN_DF = 5
NO_OF_CLUSTERS = 6
NO_OF_MEMBERS = 8