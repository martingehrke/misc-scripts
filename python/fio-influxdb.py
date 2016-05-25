#!/usr/bin/python

import influxdb
import argparse
import sys
from forecastiopy import *

def main(argv=None):

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--credentials", action='store',
                        help='file to read for nest credentials',
                        required=True, type=str, dest='cred_file')

    args = parser.parse_args(argv[1:])

    with open(args.cred_file) as f:
        api_key = f.readline().strip()

    lat = 41.080907
    lng = -80.065916

    fio = ForecastIO.ForecastIO(api_key, latitude=lat, longitude=lng)
    current = FIOCurrently.FIOCurrently(fio)
    temp = current.temperature
    humidity =  current.humidity * 100

    db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "climate")

    data = [
        {
            "measurement": "temperature",
            "fields": { "value": temp },
            "tags": { "device": "forecastio", "location": "outdoor", "type": "current" },
        },
        {
            "measurement":"humidity",
            "fields": { "value": humidity },
            "tags": { "location": "outdoor", "type":"current", "device":"forecastio" },
        },
    ]

    db.write_points(data)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
