"""Defines endpoint for creating entries"""

from flask import request
from .bp import api_bp
from main.views import ifixthat
from owlready2 import destroy_entity

@api_bp.route('/', methods=['DELETE'])
def delete_entry():
    """Delete an entry"""

    body = request.get_json()
    uri = body.get('uri')

    if not uri:
        return 'URI not provided', 400

    instance = ifixthat.search_one(iri=uri)
    destroy_entity(instance)

    ifixthat.save(file="../ontology.owl")

    return 'Entry deleted', 200