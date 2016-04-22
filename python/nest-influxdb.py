#!/usr/bin/python
#this was initiall copied from
#http://z3ugma.github.io/2014/12/13/influxdb-augments-my-homebrew-temperature-monitor/
#but will be/has been modified extensively as necessary

import nest_thermostat
import influxdb

with open("/home/martin/configs/nest.txt") as f:
    credentials = [x.strip().split(" ") for x in f.readlines()]

nest = nest_thermostat.Nest(credentials[0][0], credentials[0][1], index=0, units="F")
nest.login()
nest.get_status()

temp = nest.temp_out(nest.status["shared"][nest.serial]["current_temperature"])
mode = nest.status["shared"][nest.serial]["target_temperature_type"]
target = nest.temp_out(nest.status["shared"][nest.serial]["target_temperature"])

from influxdb import client as influxdb
db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "test")

data = [
    {
        "measurement": "temperature",
        "tags": { "device": "nest", "location": "indoor", "type": "current" },
        "fields": { "value": temp }
    },
    {
        "measurement":"temperature",
        "fields": { "value": target },
        "tags": { "location": "indoor", "type":"target", "device":"nest" },
    },
    {
        "measurement":"mode",
        "fields": { "value": mode },
        "tags": { "location": "indoor", "type":"mode", "device":"nest" },
  },
]

    
db.write_points(data)
