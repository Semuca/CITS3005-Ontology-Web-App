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

    def __init__(self: Self, uri: str, title: str = None, subtitle: str = None) -> None:
        self.uri = uri
        url = self.uri.removeprefix("http://ifixthat.org/")

        self.url = '/' + url
        self.rdf_type = url.split('/')[0]
        self.name = url.removeprefix(f"{self.rdf_type}/")

        self.title = title or self.name
        self.subtitle = subtitle or self.rdf_type.capitalize()

        self.icon = self.type_to_icon_map.get(self.rdf_type, 'help')

domain = "http://ifixthat.org/"

g = rdflib.Graph()
g.parse("../graph.rdf", format="xml")
