#!/usr/bin/python
import pygop
from optparse import OptionParser
import sys

def logOnOff(name, onoff):
	if (onoff == 1):
		print 'Turning \'' + str(name) + '\' on.'
	else:
		print 'Turning \'' + str(name) + '\' off.'

def logLevel(name, level):
	print 'Setting dim level ' + str(level) + ' on \'' + str(name) + '\'.'

# set up parser and options
usage = "%prog [-p]"
description = "Command Line Utility for the pygop module"
version = "%prog " + pygop.__version__
parser = OptionParser(usage=usage, description=description, version=version)
parser.add_option("-p", "--print-info", action="store_true", default=False,
			dest="printInfo", help="Print rooms and devices to the console")
parser.add_option("-s", "--set", action="store", type="int", dest="onoff",
			help="Set the bulb/fixture on - 1 or off - 0", default=-1)
parser.add_option("-l", "--level", action="store", type="int", dest="level",
			help="Set the dim level of the bulb/fixture (1-100)", default=-1)
parser.add_option("-d", "--did", action="store", type="int", dest="did",
			help="Specify the did (device identifier)")
parser.add_option("-r", "--rid", action="store", type="int", dest="rid",
			help="Specify the rid (room identifier)")
parser.add_option("-n", "--name", action="store", type="string", dest="name",
			help="Specify the name of the bulb/fixture")
parser.add_option("-m", "--rname", action="store", type="string", dest="rname",
			help="Specify the name of the room")

# parse arguments
(options, args) = parser.parse_args()

# if no arguments print usage
if ((options.printInfo is False) and (options.onoff == -1) 
	and (options.level == -1) and (options.did is None) and (options.rid is None)
	and (options.name is None) and (options.rname is None)):
	parser.print_help()
	sys.exit()

if(options.did and options.rid):
	parser.error('Please choose only one (did,rid)')
if(options.did and options.name):
	parser.error('Please choose only one (did,name)')
if(options.did and options.rname):
	parser.error('Please choose only one (did,rname)')
if(options.rid and options.name):
	parser.error('Please choose only one (rid,name)')
if(options.rid and options.rname):
	parser.error('Please choose only one (rid,rname)')
if(options.name and options.rname):
	parser.error('Please choose only one (name,rname)')

if (options.did and (options.onoff == -1) and (options.level == -1)):
	parser.error('Please choose an action (set,level)')
if (options.rid and (options.onoff == -1) and (options.level == -1)):
	parser.error('Please choose an action (set,level)')
if (options.name and (options.onoff == -1) and (options.level == -1)):
	parser.error('Please choose an action (set,level)')
if (options.rname and (options.onoff == -1) and (options.level == -1)):
	parser.error('Please choose an action (set,level)')

pygop = pygop.pygop()

if (options.printInfo):
	pygop.printHouseInfo()

if (options.onoff != -1):
	if (options.onoff < 0 or options.onoff > 1):
		parser.error("Set value out of bounds (0 or 1)")
	else:
		if (options.did):
			if (pygop.setBulbLevelByDid(options.did, options.onoff, 0)):
				logOnOff(options.did, options.onoff)
		elif (options.rid):
			if (pygop.setRoomLevelByRid(options.rid, options.onoff, 0)):
				logOnOff(options.rid, options.onoff)
		elif (options.name):
			if (pygop.setBulbLevelByName(options.name, options.onoff, 0)):
				logOnOff(options.name, options.onoff)
		elif (options.rname):
			if (pygop.setRoomLevelByName(options.rname, options.onoff, 0)):
				logOnOff(options.rname, options.onoff)
		else:
			parser.error('Name or did required to set bulb/fixture on or off.')

if (options.level != -1):
	if(options.level < 1 or options.level > 100):
		parser.error("Dim level out of bounds (1-100)")
	else:
		if (options.did):
			if (pygop.setBulbLevelByDid(options.did, 0, options.level)):
				logLevel(options.did, options.level)
		elif (options.rid):
			if (pygop.setRoomLevelByRid(options.rid, 0, options.level)):
				logLevel(options.rid, options.level)
		elif (options.name):
			if (pygop.setBulbLevelByName(options.name, 0, options.level)):
				logLevel(options.name, options.level)
		elif (options.rname):
			if (pygop.setRoomLevelByName(options.rname, 0, options.level)):
				logLevel(options.rname, options.level)
		else:
			parser.error('Name or did required to set bulb/fixture dim level.')
