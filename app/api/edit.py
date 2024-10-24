"""Defines endpoint for creating entries"""

from flask import request
from rdflib import Literal, URIRef
from .bp import api_bp
from main.views import g

@api_bp.route('/', methods=['PUT'])
def edit_entry():
    """Edit an entry"""

    body = request.get_json()
    uri = URIRef(body.get('uri'))
    property = URIRef(body.get('property'))
    new_value = Literal(body.get('new_value'))

    matching_triples = list(g.triples((uri, property, None)))
    g.remove(matching_triples[0])

    g.add((uri, property, new_value))

    g.serialize('../ontology.owl', format='xml')

    return 'Entry edited', 200