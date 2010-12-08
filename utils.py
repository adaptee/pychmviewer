#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

def remove_comment(text):
    " hello, world.#string ==> hello, world"
    if not text:
        return text

    pos = text.find(u'#')
    if pos != -1:
        return text[0:pos]
    else:
        return text
