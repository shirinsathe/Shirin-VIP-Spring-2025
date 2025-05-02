import pandas as pd
import numpy as np
import requests
from pydub import AudioSegment
from pydub.playback import play
from pythonosc import udp_client
import tempfile
import os

# get the climate data from aws noaa
CSV_URL = "https://noaa-ghcn-pds.s3.amazonaws.com/csv/by_year/2023.csv"

def download_csv(url):
    print("Downloading NOAA climate data...")
    df = pd.read_csv(url)
    print("Data loaded successfully!")
    return df

# get data into pandas df
df = download_csv(CSV_URL)

# normalize the temps
df = df[df["ELEMENT"] == "TAVG"]
df["TEMP_C"] = df["DATA_VALUE"] / 10
df["TEMP_NORM"] = (df["TEMP_C"] - df["TEMP_C"].min()) / (df["TEMP_C"].max() - df["TEMP_C"].min())

# load in static bird sounds
BIRD_SOUNDS = [
    "bird1.wav", "bird2.wav", "bird3.wav", "bird4.wav", "bird5.wav"
]

# load in the samples to play
bird_samples = [AudioSegment.from_wav(sound) for sound in BIRD_SOUNDS]

# play bird sound based on temperature
def play_bird_sound(temp_value):
    index = int(temp_value * (len(bird_samples) - 1)) # map temp to index of birds
    print(f"Playing bird sound {index} for temperature {temp_value:.2f}")
    play(bird_samples[index])

# play the first bird sound
first_temp = df["TEMP_NORM"].iloc[0]
play_bird_sound(first_temp)

# send data to Max/MSP on localhost udp port 7400
client = udp_client.SimpleUDPClient("127.0.0.1", 7400)
client.send_message("/temperature", first_temp)

print("Data sent to Max")
