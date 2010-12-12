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
            if param['name'] == name :
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

if __name__ == '__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]

        style, tree = parse( open(filename).read() )

        print ("style: %s" % style)
        print (tree)

