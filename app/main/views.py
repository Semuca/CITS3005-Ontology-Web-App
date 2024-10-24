"""Main route views"""

from typing import Self
from flask import Blueprint
from owlready2 import get_ontology, default_world

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'Item': 'category',
        'Part': 'toys_and_games',
        'Procedure': 'receipt_long',
        'Step': 'stairs_2',
        'Tool': 'construction',
    }

    def __init__(self: Self, thing: any, title: str = None, subtitle: str = None) -> None:
        self.ref = thing
        self.uri = thing.iri

        self.rdf_type = thing.is_a[0].name
        self.url = "/" + self.rdf_type + "/" + thing.iri.split("#")[-1]
        self.name = thing.iri.split("#")[-1]

        self.title = title or (len(thing.label) > 0 and thing.label[0]) or self.name
        self.subtitle = subtitle or self.rdf_type.capitalize()

        self.icon = self.type_to_icon_map.get(self.rdf_type, 'help')

ifixthat = get_ontology("../ontology.owl").load()

g = default_world.as_rdflib_graph()

domain = "http://ifixthat.org/"
g.bind("ifixthat", domain)
g.bind("procedure", f"{domain}Procedure#")
g.bind("item", f"{domain}Item#")
g.bind("part", f"{domain}Part#")
g.bind("tool", f"{domain}Tool#")
g.bind("step", f"{domain}Step#")
g.bind("image", f"{domain}Image#")
