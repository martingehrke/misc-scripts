#!/usr/bin/python

import influxdb
import argparse
import sys
import os

SPEEDTEST_CMD = '/usr/local/bin/speedtest-cli'

def runSpeedTest(server=None):
    #this code was originally copied from
    # https://www.accelebrate.com/blog/pandas-bandwidth-python-tutorial-plotting-results-internet-speed-tests/
    '''
    Run test and parse results.
    Returns tuple of ping speed, download speed, and upload speed,
    or raises ValueError if unable to parse data.
    '''
    
    ping = download = upload = None

    if server==None:
        SPEEDTEST_CMD_LINE = SPEEDTEST_CMD + ' --simple'
    else:
        SPEEDTEST_CMD_LINE = SPEEDTEST_CMD + ' --simple' + ' --server ' + server

    with os.popen(SPEEDTEST_CMD_LINE) as speedtest_output:

        for line in speedtest_output:
            label, value, unit = line.split()
            if 'Ping' in label:
                ping = float(value)
            elif 'Download' in label:
                download = float(value)
            elif 'Upload' in label:
                upload = float(value)

        if all((ping, download, upload)): # if all 3 values were parsed
            return ping, download, upload
        else:
            raise ValueError('TEST FAILED')

def main(argv=None):

        ping, download, upload = runSpeedTest()

        db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "test")

        data = [
            {
                "measurement": "upload",
                "tags": { "device": "nest" },
                "fields": { "value": upload }
            },
            {
                "measurement":"download",
                "fields": { "value": download },
                "tags": { "location": "indoor" },
            },
            {
                "measurement":"ping",
                "fields": { "value": ping },
                "tags": { "location": "indoor" },
          },
        ]

        db.write_points(data)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
