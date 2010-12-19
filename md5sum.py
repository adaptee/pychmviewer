#!/usr/bin/python
# coding: utf8

" Provide convenient function for calculating md5sum "
import io
import hashlib

def md5sum(filename):
    " Return the hexdecimal md5sum of given file specified py path. "
    hasher = hashlib.md5()

    with io.FileIO(filename, 'rb') as stream:
        hasher.update( stream.readall() )

    return hasher.hexdigest()
