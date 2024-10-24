"""Main route views"""

from typing import Self
from flask import Blueprint
from owlready2 import get_ontology, default_world

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'item': 'category',
        'part': 'toys_and_games',
        'procedure': 'receipt_long',
        'step': 'stairs_2',
        'tool': 'construction',
    }

    def __init__(self: Self, uri: str, title: str = None, subtitle: str = None) -> None:
        self.uri = uri
        url = self.uri.removeprefix(domain)

        self.url = '/' + url
        self.rdf_type = url.split('/')[0]
        self.name = url.removeprefix(f"{self.rdf_type}/")

        self.title = title or self.name
        self.subtitle = subtitle or self.rdf_type.capitalize()

        self.icon = self.type_to_icon_map.get(self.rdf_type, 'help')

get_ontology("../ontology.owl").load()
g = default_world.as_rdflib_graph()

domain = "http://ifixthat.org/"
g.bind("ifixthat", domain)
g.bind("procedure", f"{domain}Procedure#")
g.bind("item", f"{domain}Item#")
g.bind("part", f"{domain}Part#")
g.bind("tool", f"{domain}Tool#")
g.bind("step", f"{domain}Step#")
g.bind("image", f"{domain}Image#")
