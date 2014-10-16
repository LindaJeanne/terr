import xml.etree.ElementTree as et

blockinfo = dict()
creatureinfo = dict()
iteminfo = dict()


class ObjDetails(object):

    def __init__(self, token, char):
        self.token = token
        self.char = char

    def as_tuple(self):
        return((self.token, self.char))


class BlockDetails(ObjDetails):

    def __init__(
        self,
        token,
        isPassable,
        isTransparent,
        char
    ):
        super().__init__(token, char)
        self.isPassable = isPassable
        self.isTransparent = isTransparent

    def as_tuple(self):
        return((
            self.token,
            self.isPassable,
            self.isTransparent,
            self.char))


class CreatureDetails(ObjDetails):
    pass
    #def __init__(self, token, char):
        #super().__init__(token, char):
        #self.token = token
        #self.char = char

    #def as_tuple(self):
        #return((
            #self.token,
            #self.char))


class ItemDetails(ObjDetails):
    pass
    #def __init__(self, token, char):
        #self.token = token
        #self.char = char

    #def as_tuple(self):
        #return((
            #self.token,
            #self.char))


def templXMLitr(xmlFile, roottag, elementtag):
    tree = et.parse(xmlFile)
    root = tree.getroot()

    #TODO: obviously, this needs better error handling than
    #just an assert
    assert(root.tag == roottag)

    return root.iter(elementtag)


def loadBlockXML(xmlFile):

    for blockel in templXMLitr(xmlFile, 'blockList', 'block'):
        blockinfo[blockel.attrib['token']] = BlockDetails(
            blockel.attrib['token'],
            (blockel.attrib['isPassable'] == 'True'),
            (blockel.attrib['isTransparent'] == 'True'),
            int(blockel.attrib['char']))


def loadItemXML(xmlFile):

    for itemel in templXMLitr(xmlFile, 'itemList', 'item'):
        iteminfo[itemel.attrib['token']] = ItemDetails(
            itemel.attrib['token'],
            int(itemel.attrib['char']))


def loadCreatureXML(xmlFile):

    for creatureel in templXMLitr(xmlFile, 'creatureList', 'creature'):
        creatureinfo[creatureel.attrib['token']] = CreatureDetails(
            creatureel.attrib['token'],
            int(creatureel.attrib['char']))
