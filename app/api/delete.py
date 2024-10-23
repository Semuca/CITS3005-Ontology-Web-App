"""Defines endpoint for creating entries"""

from flask import request
import rdflib
from .bp import api_bp
from main.views import g

@api_bp.route('/', methods=['DELETE'])
def delete_entry():
    """Delete an entry"""

    body = request.get_json()
    uri = body.get('uri')

    if not uri:
        return 'URI not provided', 400

    g.remove((rdflib.URIRef(uri), None, None))

    g.serialize(destination="../graph.rdf", format="xml")

    return 'Entry deleted', 200