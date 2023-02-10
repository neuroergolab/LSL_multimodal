import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyxdf as xdf


data_dir = 'T2.xdf'
streams, fileheader = xdf.load_xdf(data_dir)

streams_sort = {stream['info']['name'][0]: stream for stream in streams}

print(streams_sort.keys())


trigs = streams_sort['Trigger']
trigs_data = trigs['time_series']
trigs_time = trigs['time_stamps']
champ1 = streams_sort['actiCHamp-21050565']
champ1_time = champ1['time_stamps']

champ2 = streams_sort['actiCHamp-21040553']
champ2_time = champ2['time_stamps']

print(champ1_time[0])
print(champ2_time[0])

print(trigs_time[0])
trig_onset = []
for i in range(len(trigs_time)):
    trig_onset.append(trigs_time[i] - champ1_time[0])

print(len(trig_onset))



# save to onset file
with open('onset.txt', 'w') as f:
    f.write("latency\ttype\tposition\n")
    print("Latency\tType\tPosition\n")
    for i in range(len(trig_onset)):
        f.write(str(trig_onset[i]) + '\ttarget\t1\n')
        print(str(trig_onset[i]) + '\ttarget\t1\n')
    
    f.close()
