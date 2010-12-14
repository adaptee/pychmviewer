#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


import sys
from BeautifulSoup import NavigableString
from BeautifulSoup import BeautifulSoup


def indent(text, level):
    return "  " * level + text


class Node(object):
    def __init__(self, name=u"Unknown", url=u"", children=( ) ):
        self.name     = name
        self.url      = url
        self.parent   = None
        self.level    = -1
        self.children = children

        for child in children:
            child.parent = self

    def __unicode__(self):
        result = u"[%s] [%s]\n" % (self.name, self.url)
        result = indent(result, self.level)

        for child in self.children:
            result += unicode(child)

        return result

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def calc_level(self):
        self.level = self.parent.level + 1
        for child in self.children:
            child.calc_level()

class Tree(Node):
    def __init__(self, children=() ):
        super(Tree, self).__init__( name=u'Root', url=u"", children=children)
        self.parent = self
        self.calc_level()

def parse(data):
    soup = BeautifulSoup(data)

    body  = soup.html.body
    style = body.object.param['value']
    root  = body.ul

    return style, createTree(root)


def createTree(root):

    lis = root.findAll(name='li', recursive=False)

    children = [ createNode(li) for li in lis ]

    return Tree(children=children)


def createNode(li):

    def get_sub_lis(li):
        results = []

        sub_uls = li.findAll(name='ul', recursive=False)

        for sub_ul  in sub_uls:
           results.extend( sub_ul.findAll(name='li', recursive=False ) )

        return results


    def get_value_by_name(params, name):
        for param in params:
            if param['name'].lower() == name.lower() :
                return param['value']

        return u""

    params = li.object.findAll(name='param', recursive=False)
    name = get_value_by_name(params, 'Name')
    url = get_value_by_name(params, 'Local')
    image_num = get_value_by_name(params, 'ImageNumber')

    children = [ ]
    #sub_lis = li.findAll(name='li', recursive=False)
    sub_lis = get_sub_lis(li)

    for sub_li in sub_lis:
        children.append( createNode(sub_li) )

    return Node( name=name, url=url, children=children)


################################################################################

def _parse_meta_tag(meta):
    info = { }
    if meta:
        print meta
        info[ meta["name"].lower() ] = meta["content"]
    return info


def _parse_param_tag(param):
    info = { }
    if param:
        info [ param["name"].lower() ] = param["value"]

    return info

def _parse_object_tag(object):
    info = { }
    if object:
        params = object.findAll(name='param', recursive=False)
        for param in params:
            info.update( _parse_param_tag(param) )

    return info


class NewNode(object):

    name_mappings = {
                        "name"        : "name" ,
                        "type"        : "type" ,
                        "url"         : "local",
                        "alternative" : "url",
                        "imagenum"    : "imagenumber"
                    }

    def __init__(self, children=( ), **kwargs ):
        self.children = children
        self.parent   = None
        self.level    = -1
        self._map     = kwargs

        for child in children:
            child.parent = self

        for name in self.name_mappings :
            setattr(self, name, self._map.get(name, "") )

    def __unicode__(self):
        result = u"[%s] [%s]\n" % (self.name, self.url)
        result = indent(result, self.level)

        for child in self.children:
            result += unicode(child)

        return result

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def calc_level(self):
        self.level = self.parent.level + 1
        for child in self.children:
            child.calc_level()

class NewTree(Node):
    def __init__(self, children=() ):
        super(NewTree, self).__init__( children=children,  )
        self.name = "Root"
        self.url  = "/"
        self.parent = self
        self.calc_level()

def NewcreateNode(li):

    def get_sub_lis(li):
        results = []

        sub_uls = li.findAll(name='ul', recursive=False)

        for sub_ul  in sub_uls:
           results.extend( sub_ul.findAll(name='li', recursive=False ) )

        return results

    object = li.find(name="object", recursive=False)
    info = _parse_object_tag(object)

    children = [ ]
    sub_lis = get_sub_lis(li)

    for sub_li in sub_lis:
        children.append( createNode(sub_li) )

    return NewNode( children=children, **info)

def NewcreateTree(root):

    lis = root.findAll(name='li', recursive=False)

    children = [ NewcreateNode(li) for li in lis ]

    return NewTree(children=children)




getMetaInfo   = _parse_meta_tag
getGlobalInfo = _parse_object_tag
getItemTree   = NewcreateTree



class Parser(object):
    def __init__(self):
        pass

    def parse(self, data):
        soup = BeautifulSoup(data)
        html = soup.html

        # mandatory
        meta = html.head.find( name="meta", recursive=False)

        # optional
        object = html.body.find( name="object", recursive=False)

        # mandatory
        root = html.body.find( name="ul", recursive=False)

        return getMetaInfo(meta), getGlobalInfo(object), getItemTree(root)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]

        data = open(filename).read()

        #style, tree = parse(data)
        #print(tree)

        parser = Parser()
        metainfo, globalinfo, tree = parser.parse(data)

        print (metainfo)
        print (globalinfo)
        print (tree)

