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

