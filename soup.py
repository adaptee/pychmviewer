#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from BeautifulSoup import BeautifulSoup


def parse_meta_tag(meta):
    info = { }
    if meta:
        info[ meta["name"].lower() ] = meta["content"]

    return info

def parse_param_tag(param):
    info = { }
    if param:
        info [ param["name"].lower() ] = param["value"]

    return info

def parse_object_tag(object):
    info = { }
    if object:
        params = object.findAll(name='param', recursive=False)
        for param in params:
            info.update( parse_param_tag(param) )

    return info

class Node(object):
    name_mappings = {
                        "name"        : "name" ,
                        "keyword"     : "keyword" ,
                        "url"         : "local",
                        "type"        : "type" ,
                        "imagenum"    : "imagenumber" ,
                    }

    def __init__(self, children=( ), **kwargs ):
        self.children = children
        self.parent   = None
        self._info    = kwargs
        self.depth    = -1

        for child in children:
            child.parent = self

        for attr, key  in self.name_mappings.iteritems() :
            setattr(self, attr, self._info.get(key, u"") )

    def __unicode__(self):
        def indent(text, level):
            return u"  " * level + text

        result = u"[%s] [%s]\n" % (self.name, self.url)
        result = indent(result, self.depth)

        for child in self.children:
            result += unicode(child)

        return result

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def calcDepth(self):
        self.depth = self.parent.depth + 1
        for child in self.children:
            child.calcDepth()

class Tree(Node):
    def __init__(self, children=() ):
        super(Tree, self).__init__( children=children,  )

        self.name = "Root"
        self.url  = "/"
        self.parent = self

        self.calcDepth()

def createNode(li):

    def get_sub_lis(li):
        results = []

        sub_uls = li.findAll(name='ul', recursive=False)

        for sub_ul  in sub_uls:
            results.extend( sub_ul.findAll(name='li', recursive=False ) )

        return results

    object = li.find(name="object", recursive=False)
    info = parse_object_tag(object)

    children = [ ]
    sub_lis = get_sub_lis(li)

    for sub_li in sub_lis:
        children.append( createNode(sub_li) )

    return Node( children=children, **info)

def createTree(root):
    lis = root.findAll(name='li', recursive=False)
    children = [ createNode(li) for li in lis ]

    return Tree(children=children)

def parse(data):

    soup = BeautifulSoup(data)

    html = soup.html

    # mandatory
    meta = html.head.find( name="meta", recursive=False)

    # optional
    object = html.body.find( name="object", recursive=False)

    # mandatory
    root = html.body.find( name="ul", recursive=False)

    meta_info = parse_meta_tag(meta)
    global_info = parse_object_tag(object)
    tree = createTree(root)

    return meta_info, global_info, tree

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        data = open(filename).read()

        meta_info, global_info, tree = parse(data)
        print (meta_info)
        print (global_info)
        print (tree)

