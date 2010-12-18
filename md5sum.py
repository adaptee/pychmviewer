#!/usr/bin/python
# coding: utf8

import io
import hashlib

def md5sum2(filename):
    hasher = hashlib.md5()

    with io.FileIO(filename, 'rb') as stream:
        hasher.update( stream.readall() )

    return hasher.hexdigest()
