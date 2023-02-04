import argparse
import sys
import os
import stat
from stat import *

execcount = 0
filecount = 0
setuid_files = []
capabilities_files = []
def walktree(top, setuid, capabilities):
    '''recursively descend the directory tree rooted at top'''
    global filecount, execcount, setuid_files, capabilities_files
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.lstat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, setuid, capabilities)
        else:
            if os.access(pathname, os.X_OK):
                execcount +=1
                if setuid and (mode & stat.S_ISUID):
                    setuid_files.append(pathname)
                if capabilities:
                    print ('append to the capabilities list if capabilities is set')
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

walktree(options.path, options.setuid, options.capabilities)
print('Scanned ' + str(filecount) + ' files, found ' + str(execcount) + ' executables')
print('setuid executables:')
for x in setuid_files:
    print(x + '\n')

