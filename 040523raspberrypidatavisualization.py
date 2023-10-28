import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

x_time = []
y_run = []
y_trip = []
y_pressure = []

with open('/home/reubengoh/Documents/datalogger/data/data.csv', 'r') as csvfile:
    lines = csv.reader(csvfile,delimiter=',')
    for row in lines:
        x_time.append(row[0])
        y_run.append(row[1])
        y_trip.append(row[2])
        y_pressure.append(row[3])
        
x_time = x_time[::10] #select every 10th element

plt.scatter(x_time,y_run[::10], color = 'g', marker = 'o', label = "Run")
plt.scatter(x_time,y_trip[::10], color = 'b', marker = 'o', label = "Trip")
plt.plot(x_time,y_pressure[::10], color = 'r', linestyle = 'dashed', marker = '.', label = "Pressure")

plt.xticks(rotation = 25)
plt.xlabel ('Time')
plt.ylabel ('Status')
plt.title ('Booster System Monitoring', fontsize = 20)
plt.grid()
plt.legend()
plt.show()
