
import matplotlib.pyplot as plt
import numpy as np

# import the CSV file using numpy
path = '../../../data/ekg/mitdb_201.csv'

# load data in matrix from CSV file; skip first two rows

ekg_data = np.loadtxt(path, skiprows=2, delimiter=',')

# save each vector as own variable

time = ekg_data[:, 0]
voltage = ekg_data[:, 2]

# use matplot lib to generate a single

plt.plot(time, voltage)
plt.title('Heartbeats over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (mV)')

plt.show()
