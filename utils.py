#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import re

def remove_anchor(text):
    " hello, world.#string ==> hello, world"
    if not text:
        return text

    pos = text.find(u'#')
    if pos != -1:
        return text[0:pos]
    else:
        return text

def CachedProperty(func):
    """returns a cached property that is calculated by function func"""
    def get(self):
        try:
            return self._property_cache[func]
        except AttributeError:
            self._property_cache = { }
            x = self._property_cache[func] = func(self)
            return x
        except KeyError:
            x = self._property_cache[func] = func(self)
            return x

    return property(get)


def parseChmURL(url):
    '''
    url:unicode
    return: tuple(bool,unicode,unicode)
            first item tell if it's a url pointing to another .CHM
            second item is chm file,
            third item is page.
    '''
    assert isinstance(url, unicode)

    # [scheme]  ms-its:[chmpath]::[pagepath]
    pattern = re.compile(u'^ms-its:(.*)::(.*)$', re.I)
    match = pattern.search(url)
    if match:
        newchmfile = match.group(1)
        page = match.group(2)
        return (True, newchmfile, page)
    return (False, None, None)
