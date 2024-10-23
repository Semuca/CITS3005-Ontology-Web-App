"""Main route views"""

from typing import Self
from flask import Blueprint
import rdflib

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'item': 'category',
        'part': 'toys_and_games',
        'procedure': 'receipt_long',
        'step': 'stairs_2',
        'tool': 'construction',
    }

    def __init__(self: Self, uri: str, name: str, rdf_type: str, url: str) -> None:
        self.uri = uri

        # TODO: Remove this- URI has all the information we need
        self.name = name
        self.rdf_type = rdf_type
        self.url = url

        self.icon = self.type_to_icon_map.get(rdf_type, 'help')

domain = "http://ifixthat.org/"

g = rdflib.Graph()
g.parse("../graph.rdf", format="xml")
