#!/usr/bin/env python

from tempfile import mkstemp

import os

def CreateTemporaryFile():
    '''Return the name of a temporary file.
    '''
    fd,pathname = mkstemp(dir = ".")
    os.close(fd)
    return pathname
    
def RemoveFile(filename):
    try:
        os.remove(filename)
    except OSError as e:
        print >> stderr, "Removal of %s failed: %s" % (filename, e)
        exit(1)
