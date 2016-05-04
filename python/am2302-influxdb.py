#!/usr/bin/python

import influxdb
import argparse
import sys
import os
import Adafruit_DHT

def main(argv=None):

	pin = 4
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, pin)

	#convert temp to F
	temperature = temperature * 9/5.0 + 32

        db = influxdb.InfluxDBClient("192.168.1.105", 8086, "root", "root", "climate")

        data = [
            {
                "measurement": "temperature",
                "fields": { "value": temperature },
                "tags": { "device": "cerberus-rpi-am2302", "location":"basement", "type":"current" }
            },
            {
                "measurement":"humidity",
                "fields": { "value": humidity },
                "tags": { "device": "cerberus-rpi-am2302", "location":"basement", "type":"current" }
            },
        ]

	if humidity is not None and temperature is not None:
            db.write_points(data)
	else:
	    print('Failed to get reading. Try again!')
	    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
