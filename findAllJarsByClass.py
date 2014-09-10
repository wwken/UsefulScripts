#!/usr/bin/python 

""" README 
Author: Ken Wu

This script is to find all jars that contain the given class name inside a given location

Parameters:
1)	directory location to be searched from
2)	class name that is to be searched

Usage: 
1) To find all jar files in the location /home/kwu/ 
	./findAllJarsByClass.py /home/kwu/ ConsumerProcess

"""

##### Start: Standard libraries ################################################################################################################
import ConfigParser
import argparse
import collections
import datetime
import logging
import os
import re
import shutil
import stat
import sys
import tarfile
import tempfile
import time
import traceback
import urllib
import commands
import decimal
import datetime
import time 
import md5
##### End: Standard libraries ###################################################################################################################

##### Start: Customized libraries ################################################################################################################
import lib.printings
import lib.commands
##### End: Customized libraries ##################################################################################################################

################################################################################################################################################

logging.basicConfig(format="%(asctime)-15s %(levelname)s: %(message)s")
logger = logging.getLogger('com.kwu.utilities')
logger.setLevel(logging.DEBUG)
debug = False

###### Start: Customized functions #############################################################################################################
###### End:   Customized functions #############################################################################################################

thisFileName=os.path.basename(__file__)
dirLoc=sys.argv[1]
className=sys.argv[2]

findCommand= "for f in `find "+dirLoc+" -name \"*.jar\" -exec ls -lrt \"{}\" + | awk '{ print $NF}' | xargs grep "+className+".class | awk '{print $3}'`; do ls -lrt $f | awk '{print $(NF-1), $(NF-2), $(NF-3), $NF} '; done"

#print findCommand;

out = lib.commands.execCommand (findCommand);
lib.printings.printResults(out)




