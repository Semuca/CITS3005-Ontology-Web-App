from typing import Self


class Link:

    type_to_icon_map = {
        'Item': 'category',
        'Part': 'toys_and_games',
        'Procedure': 'receipt_long',
        'Step': 'stairs_2',
        'Tool': 'construction',
    }

    def __init__(self: Self, thing: any, property_name: str, child_uri: str=None, parent_uri:str=None, title: str = None, subtitle: str = None, images: list[str] = [], hideContent: bool = False) -> None:
        self.ref = thing
        self.uri = thing.iri
        self.property_name = property_name
        self.child_uri = child_uri
        self.parent_uri = parent_uri
        self.hideDelete = child_uri is None and parent_uri is None

        self.images = images
        self.hideContent = hideContent

        self.rdf_type = thing.is_a[0].name
        self.url = "/" + self.rdf_type + "/" + thing.iri.split("#")[-1]
        self.name = thing.iri.split("#")[-1]

        self.title = title or (len(thing.label) > 0 and thing.label[0]) or self.name
        self.subtitle = subtitle or self.rdf_type.capitalize()

        self.icon = self.type_to_icon_map.get(self.rdf_type, 'help')