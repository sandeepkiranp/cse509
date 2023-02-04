import argparse
import sys
import os
from stat import *

execcount = 0
filecount = 0
hello = 0
def walktree(top):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''
    global filecount, execcount
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.lstat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname)
        else:
            # Unknown file type, print a message
            if os.access(pathname, os.X_OK):
                 execcount +=1
            filecount +=1

parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true", dest="setuid")
parser.add_argument("-c", action="store_true", dest="capabilities")
parser.add_argument("-p", default="/",dest="path")

options = parser.parse_args()
if not len(sys.argv) > 1:
    print('No arguments passed')
    options.setuid = True
    options.capabilities = True
    options.path = "/"

if not options.setuid and not options.capabilities:
    options.setuid = True
    options.capabilities = True

print ('Argument setuid:', options.setuid)
print ('Argument capabilities:', options.capabilities)
print ('Argument path:', options.path)

walktree(options.path)
print('Scanned ' + str(filecount) + ' files, found ' + str(execcount) + ' executables')

