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
    def __init__(self, token, char, hit, damage, dodge, soak):
        super().__init__(token, char)
        self.hit = hit
        self.damage = damage
        self.dodge = dodge
        self.soak = soak

    def as_tuple(self):
        return((
            self.token,
            self.char,
            self.hit,
            self.damage,
            self.dodge,
            self.soak))


class ItemDetails(ObjDetails):
    pass


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

        combat_info = creatureel.find('combat')

        creatureinfo[creatureel.attrib['token']] = CreatureDetails(
            creatureel.attrib['token'],
            int(creatureel.attrib['char']),
            int(combat_info.attrib['hit']),
            (
                int(combat_info.attrib['damage_low']),
                int(combat_info.attrib['damage_high'])),
            int(combat_info.attrib['dodge']),
            (
                int(combat_info.attrib['soak_low']),
                int(combat_info.attrib['soak_high'])))
