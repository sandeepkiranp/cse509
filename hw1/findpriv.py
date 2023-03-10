import argparse
import sys
import os
import stat
from stat import *

execcount = 0
filecount = 0
setuid_files = []
capabilities_files = {}
def walktree(top, setuid, capabilities):
    '''recursively descend the directory tree rooted at top'''
    global filecount, execcount, setuid_files, capabilities_files
    try:
        for f in os.listdir(top):
            try:
                pathname = os.path.join(top, f)
                mode = os.lstat(pathname).st_mode
                if S_ISDIR(mode):
                    # It's a directory, recurse into it
                    walktree(pathname, setuid, capabilities)
                else:
                    if S_ISLNK(mode):
                        # not following links
                        pass
                    elif (mode & S_IXUSR or mode & S_IXGRP or mode & S_IXOTH) :
                        execcount +=1
                        if setuid and (mode & stat.S_ISUID):
                            setuid_files.append(pathname)
                        if capabilities:
                            import subprocess
                            result = subprocess.run(['getcap', pathname], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                            if result.stdout:
                                output = result.stdout.decode('ascii')
                                capabilities_files[output.split()[0]] = output.split()[1].split('=')[0]
                    filecount +=1
            except:
                pass
    except:
        pass

parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true", dest="setuid")
parser.add_argument("-c", action="store_true", dest="capabilities")
parser.add_argument("-p", default="/",dest="path")

options = parser.parse_args()
if not len(sys.argv) > 1:
    #print('No arguments passed')
    options.setuid = True
    options.capabilities = True
    options.path = "/"

if not options.setuid and not options.capabilities:
    options.setuid = True
    options.capabilities = True

options.path = os.path.abspath(options.path)

#print ('Argument setuid:', options.setuid)
#print ('Argument capabilities:', options.capabilities)
#print ('Argument path:', options.path)

walktree(options.path, options.setuid, options.capabilities)
print('Scanned ' + str(filecount) + ' files, found ' + str(execcount) + ' executables')
options.setuid and print('setuid executables:')
for x in setuid_files:
    print(x)
options.capabilities and print('capability-aware executables:')
for x in capabilities_files.keys():
    print(x.ljust(20) + '\t' + capabilities_files[x])

