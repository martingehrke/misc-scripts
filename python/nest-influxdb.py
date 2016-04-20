#!/usr/bin/python
#this was initiall copied from
#http://z3ugma.github.io/2014/12/13/influxdb-augments-my-homebrew-temperature-monitor/
#but will be/has been modified extensively as necessary

import nest_thermostat
import influxdb

nest = nest_thermostat.Nest("username", "password")
nest.login()
nest.get_status()

temp = nest.temp_out(nest.status["shared"][nest.serial]["current_temperature"])
mode = nest.status["shared"][nest.serial]["target_temperature_type"]
target = nest.temp_out(nest.status["shared"][nest.serial]["target_temperature"])

from influxdb import client as influxdb
db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "temperatures")

data = [
  {"points":[[temp, target, mode]],
   "name":"nest",
   "columns":["temperature", "target_temperature", "type"]
  }
]
db.write_points(data)
