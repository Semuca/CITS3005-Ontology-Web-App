"""Defines endpoint for creating entries"""

from flask import request
from rdflib import RDF, RDFS, Literal, URIRef
from .bp import api_bp
from main.views import g, domain

@api_bp.route('/', methods=['POST'])
def create_entry():
    """Create an entry"""

    body = request.get_json()
    rdf_type = body.get('rdf_type')
    label = body.get('label')

    if not rdf_type or not label:
        return 'RDF type or label not provided', 400
    
    uri = URIRef(f'{domain}{rdf_type.lower()}/{label}')

    g.add((uri, RDF.type, URIRef(f'{domain}properties/{rdf_type.capitalize()}')))
    g.add((uri, RDFS.label, Literal(label)))

    g.serialize('../graph.ttl', format='turtle')

    return 'Entry created', 201