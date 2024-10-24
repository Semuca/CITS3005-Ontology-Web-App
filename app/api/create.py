"""Defines endpoint for creating entries"""

from flask import request
from .bp import api_bp
from main.views import domain, ifixthat
from filelock import FileLock

from random import randint

@api_bp.route('/', methods=['POST'])
def create_entry():
    """Create an entry"""
    # Parameters
    body = request.get_json()
    rdf_type = body.get('rdf_type')
    properties = body.get('properties')

    if not rdf_type:
        return 'RDF type not provided', 400

    # Making the new instance
    rdf_type_ref = getattr(ifixthat, rdf_type, None)
    if rdf_type_ref is None:
        return 'RDF type not found', 404

    instance_ns = ifixthat.get_namespace(domain + rdf_type)
    rdf_type_ref.lastIri[0] += 1
    instance_last_iri = rdf_type_ref.lastIri[0]

    new_instance = rdf_type_ref(str(instance_last_iri), instance_ns)

    # Setting the properties
    for prop, value in properties.items():
        prop_name = ""
        if prop == "http://www.w3.org/2000/01/rdf-schema#label":
            prop_name = "label"
        else:
            prop_name = ifixthat.search_one(iri=prop).name
            if prop_name is None:
                return f'Property {prop} not found', 404

        try:
            setattr(new_instance, prop_name, [value])
        except AttributeError:
            return f"Property '{prop_name}' not found on instance", 400

    # Saving the ontology - using file lock to prevent file from wiping
    lock_path = "../ontology.owl.lock"
    file_lock = FileLock(lock_path)
    try:
        with file_lock:  # This ensures only one request can write at a time
            ifixthat.save(file="../ontology.owl", format="rdfxml")
    except Exception as e:
        return f"Error saving ontology: {str(e)}", 500

    return 'Entry created', 201