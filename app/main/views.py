"""Main route views"""

from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

class Link:

    type_to_icon_map = {
        'Item': 'category',
        'Part': 'toys_and_games',
        'Procedure': 'receipt_long',
        'Step': 'stairs_2',
        'Tool': 'construction',
    }

    def __init__(self, name: str, rdf_type: str, url: str) -> None:
        self.name = name
        self.rdf_type = rdf_type
        self.url = url

        self.icon = self.type_to_icon_map.get(rdf_type, 'help')

domain = "http://ifixthat.org/"
