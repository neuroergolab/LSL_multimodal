"""
Python script to send a trigger to LSL for EEG and fNIRS data acquisition
author: @nimrobotics
"""

import sys
import getopt
import time
import datetime
from random import random as rand
from pylsl import StreamInfo, StreamOutlet, local_clock
import os

# imports for keyboard
import tty
import sys
import termios


# write a function to write a csv file
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
    #pylsl params
    srate = 10.2 # sampling rate in Hz
    name = 'Trigger' # name of trigger, same as in montage config
    type = 'Markers'
    n_channels = 16 # number of channels
    sid = 'Aurora'

    # first create a new stream info (here we set the name to BioSemi,
    info = StreamInfo(name, type, n_channels, srate, 'float32', sid)

    # next make an outlet
    outlet = StreamOutlet(info)

    # print the stream info to the console
    print("\nStream Info:")
    print("Name of the stream: ", info.name())
    print("Type of the stream: ", info.type())
    print("Number of channels: ", info.channel_count())
    print("Sampling rate: ", info.nominal_srate())
    print("Stream ID: ", info.source_id())
    print("\nReady to send data...")
    print("Press a key to send a stim...\n")


    # create a dictinary of key and associated stim number
    stims = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16}

    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    x = 0
    filename = "./LSLLOGS/LSL_" + str(time.time()) + ".csv"
    # create the directory if it doesn't exist
    
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    
    while True: # ESC
        x=sys.stdin.read(1)[0]
        unixTime = time.time()
        print(unixTime, ' | ', datetime.datetime.fromtimestamp(unixTime), end=" | ")
        print("You pressed: ", x, end=" | ")
        markers=" you pressed: "+str(x)+"  "

        
        try:
            print('Sending stim: %s' % stims[x])
            sendStim(outlet, stims[x], n_channels)
            write_csv(filename, unixTime, stims[x])
        except KeyError:
            print('Invalid key')
            write_csv(filename, unixTime, 'InvalidKey')
            pass

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    
