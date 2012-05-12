#!/usr/bin/python


import getopt
import os
import random
import string
import sys
import time

# Add the current directory to the python search path
sys.path.append(os.getcwd())

import howie.configFile
import howie.core	

def usage():
	"Prints a usage message."
	print __doc__

def main():
	random.seed()

	# Process command-line arguments
	try:
		opts,args = getopt.getopt(sys.argv[1:], "hlf:v",
					  ["help","local","config-file","verbose"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	localMode = "no"
	configFile = "howie.ini"
	verboseMode = "no"
	for o,a in opts:
		if o in ["-h","--help"]:
			usage()
			sys.exit(2)
		elif o in ["-v","--verbose"]:
			verboseMode = "yes"
		elif o in ["-f","--config-file"]:
			configFile = a
		elif o in ["-l","--local"]:
			localMode = "yes"
	
	# Read config file
	config = howie.configFile.load(configFile)

	# Add config data from command-line arguments to the "cla" group.
	# TODO: find a clean way to iterate over the destination variables in
	# options, so the following code can be used instead:
	## for k,v in options.dict:
	##	config["cla.%s" % k] = str(v)
	for k in ["localMode", "configFile", "verboseMode"]:
		config["cla.%s" % k] = str( eval("%s" % k) )

	# Bootstrap the AI.
	howie.core.init()

# if this file is run directly, call main.
if __name__ == "__main__":
	main()
