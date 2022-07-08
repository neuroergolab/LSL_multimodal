"""Example program to demonstrate how to send a multi-channel time series to
LSL."""
# imports for pylsl
import sys
import getopt
import time
import datetime
from random import random as rand
from pylsl import StreamInfo, StreamOutlet, local_clock


# imports for keyboard
import tty
import sys
import termios

# write a function to write a csv file
def write_csv(filename, data):
    with open(filename, 'w') as f:
        for row in data:
            f.write(','.join(str(col) for col in row))
            f.write('\n')

def sendStim(outlet, stim, n_channels):
    payload = [stim]*n_channels
    outlet.push_sample(payload)


if __name__ == '__main__':
    #pylsl params
    srate = 10.2 # sampling rate in Hz
    name = 'Trigger' # name of trigger, same as in montage config
    type = 'EEG'
    n_channels = 19 # number of channels
    sid = 'Aurora'

    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)
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
    while True: # ESC
        x=sys.stdin.read(1)[0]
        unixTime = time.time()
        print(unixTime, ' | ', datetime.datetime.fromtimestamp(unixTime), end=" | ")
        print("You pressed: ", x, end=" | ")

        try:
            print('Sending stim: %s' % stims[x])
            sendStim(outlet, stims[x], n_channels)
        except KeyError:
            print('Invalid key')
            pass

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    