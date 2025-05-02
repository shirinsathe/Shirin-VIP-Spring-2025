import pandas as pd
import numpy as np
from MAxPy import maxpy

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def process_data(data):
    year = data['year'].values
    temperature = data['temperature'].values
    return year, temperature

def normalize_data(temp, min_freq=100, max_freq=1000):
    min_temp = np.min(temp)
    max_temp = np.max(temp)
    
    frequencies = np.interp(temp, (min_temp, max_temp), (min_freq, max_freq))
    return frequencies

class ClimateToSound(maxpy):
    def __init__(self, file_path):
        super().__init__()
        self.data = load_data(file_path)
        self.time, self.temperature = process_data(self.data)
        self.frequencies = normalize_data(self.temperature)
        
        self.time_index = 0

    def bang(self):
        if self.time_index < len(self.time):
            freq = self.frequencies[self.time_index]
            self.output_frequency(freq)
            self.time_index += 1

    def output_frequency(self, frequency):
        self.send(frequency)
'''
if __name__ == '__main__':
    # need to add once i export all data to a csv
    climate_sound = ClimateToSound(".csv")
    
    # a basic example: using bang to periodicially update the sound
    climate_sound.bang()
'''