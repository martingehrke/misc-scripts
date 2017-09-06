#!/usr/bin/python

import influxdb
import argparse
import sys
import urllib3
import json

urllib3.disable_warnings()

def main(argv=None):

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--credentials", action='store',
                        help='file to read for nest credentials',
                        required=True, type=str, dest='cred_file')

    args = parser.parse_args(argv[1:])

    URL = "https://api.particle.io/v1/devices/%(DEV)s/%(VAR)s?access_token=%(AT)s"

    with open(args.cred_file) as f:
        credentials = [x.strip().split(";") for x in f.readlines()]


    devices = {}
    for credential in credentials:
        devices[credential[1]] = credential[0]

    http = urllib3.PoolManager()

    URL = "https://api.particle.io/v1/devices/%(DEV)s/%(VAR)s?access_token=%(AT)s"

    for device in devices.keys():
        device_id = device
        access_token = devices[device_id]

	r = http.request('GET', "https://api.particle.io/v1/devices/%s?access_token=%s" % (device_id, access_token))
	jdata = json.loads(r.data)
	name = jdata["name"]

        #get humidity
        r = http.request('GET', URL % {"DEV":device_id, "AT":access_token, "VAR":"humidity"})
        jdata = json.loads(r.data)
        humidity = float(jdata["result"])

        #get temperature
        r = http.request('GET', URL % {"DEV":device_id, "AT":access_token, "VAR":"temperature"})
        jdata = json.loads(r.data)
        temp = float(jdata["result"])

        db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "test")

        data = [
                {
                        "measurement": "temperature",
                        "fields": { "value": temp },
                        "tags": { "device": name, "location": "upstairs", "type": "current" },
                },
                {
                        "measurement":"humidity",
                        "fields": { "value": humidity },
                        "tags": { "device": name, "location": "upstairs", "type": "current" },
                },
        ]
	
	print data
        #db.write_points(data)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
