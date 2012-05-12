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
import howie.frontends.tty

    
class ChatBot():

    def Init(self):
        InitBotSubSystem()
        
    def Ask(self, user, question):
        self._sessionID = user
        import howie.core
        howie.core.kernel.setPredicate("secure", "yes", self._sessionID)
        response = self.submit(question, self._sessionID)
        #time.sleep(random.random() * 4)
        return response
   
        
    def submit(self, input, user):
      # must delay this import until now to prevent circular references
      import howie.core
      return howie.core.submit(input, user)

    
    
def InitBotSubSystem():
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
    bot = ChatBot()
    bot.Init()

    user='bruno'
    
    question = ''
    while question != 'bye':
        question = raw_input("> ")
        print bot.Ask(user, question)