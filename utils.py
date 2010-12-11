#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import globalvalue

def remove_comment(text):
    " hello, world.#string ==> hello, world"
    if not text:
        return text

    pos = text.find(u'#')
    if pos != -1:
        return text[0:pos]
    else:
        return text

def getchmfile():
    return globalvalue.chmfile

def setchmfile(chmfile):
    globalvalue.chmfile = chmfile

