import sys
import os
import time
import datetime
from random import random as rand
from pylsl import StreamInfo, StreamOutlet, local_clock
import msvcrt  # Windows-specific module for capturing keypresses

def write_csv(filename, unixTime, stim):
    '''
    Write a csv file with the following columns: UNIX time, date, time, stim
    '''
    with open(filename, 'a') as f:
        f.write(','.join(str(col) for col in [unixTime, datetime.datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d'), datetime.datetime.fromtimestamp(unixTime).strftime('%H:%M:%S.%f'), stim]))
        f.write('\n')

def sendStim(outlet, stim, n_channels):
    payload = [stim]*n_channels
    outlet.push_sample(payload)

if __name__ == '__main__':
    srate = 10.2 # sampling rate in Hz
    name = 'Trigger' # name of trigger, same as in montage config
    type = 'Markers'
    n_channels = 16 # number of channels
    sid = 'Aurora'

    # Create a new stream info
    info = StreamInfo(name, type, n_channels, srate, 'float32', sid)

    # Create an outlet
    outlet = StreamOutlet(info)

    # Print the stream info
    print("\nStream Info:")
    print("Name of the stream: ", info.name())
    print("Type of the stream: ", info.type())
    print("Number of channels: ", info.channel_count())
    print("Sampling rate: ", info.nominal_srate())
    print("Stream ID: ", info.source_id())
    print("\nReady to send data...")
    print("Press a key to send a stim...\n")

    stims = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16}

    # File to log events
    filename = "./LSLLOGS/LSL_" + str(time.time()) + ".csv"
    
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    while True:
        if msvcrt.kbhit():  # Check if a key has been pressed
            x = msvcrt.getch().decode('utf-8')  # Get the key press
            unixTime = time.time()
            print(unixTime, ' | ', datetime.datetime.fromtimestamp(unixTime), end=" | ")
            print("You pressed: ", x, end=" | ")
            markers = " you pressed: "+str(x)+"  "

            try:
                print('Sending stim: %s' % stims[x])
                sendStim(outlet, stims[x], n_channels)
                write_csv(filename, unixTime, stims[x])
            except KeyError:
                print('Invalid key')
                write_csv(filename, unixTime, 'InvalidKey')
                pass
