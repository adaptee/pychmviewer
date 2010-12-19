#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

" Provides the facility of parsing Index and ToC. "

from BeautifulSoup import BeautifulSoup

def parse_meta_tag(meta):
    " Parse <meta> tag"
    info = { }
    if meta:
        info[ meta["name"].lower().strip() ] = meta["content"]

    return info

def parse_param_tag(param):
    " Parse <param> tag"
    info = { }
    if param:
        # make it more tolerent with extra whitespaces
        # [use case]
        # <param name=" Name " value="4. Exception Handling">
        info [ param["name"].lower().strip() ] = param["value"]

    return info

def parse_object_tag(object):
    " Parse <object> tag"
    info = { }
    if object:
        params = object.findAll(name='param', recursive=False)
        for param in params:
            info.update( parse_param_tag(param) )

    return info

class Node(object):
    " Represent one item in the Index/ToC "
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
        " Unicode representation."
        def indent(text, level):
            "Help function to display node fitting with its depth."
            return u"  " * level + text

        result = u"[%s] [%s]\n" % (self.name, self.url)
        result = indent(result, self.depth)

        for child in self.children:
            result += unicode(child)

        return result

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def calcDepth(self):
        " Calc the depth of this node within the tree."
        self.depth = self.parent.depth + 1
        for child in self.children:
            child.calcDepth()

class Tree(Node):
    " Sepcial Node representing the root of Index/ToC "
    def __init__(self, children=() ):
        super(Tree, self).__init__( children=children,  )

        self.name = "Root"
        self.url  = "/"
        self.parent = self

        self.calcDepth()

def createNode(li):
    " Create one node representing one item of the Index/ToC."
    def get_sub_lis(li):
        " Obtain all <li> tags below this <li> tag, non-recursively."
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
    " Create one tree representing the Index/ToC."
    lis = root.findAll(name='li', recursive=False)
    children = [ createNode(li) for li in lis ]

    return Tree(children=children)

def parse(data):
    " Parse Index/ToC data."
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

