"""Defines endpoint for creating entries"""

from flask import request
from .bp import api_bp
from main.views import ifixthat
from filelock import FileLock

@api_bp.route('/', methods=['PUT'])
def edit_entry():
    """Edit an entry"""
    # Parameters
    body = request.get_json()
    uri = body.get('uri')

    property = body.get('property')
    new_value = body.get('new_value')

    # Getting relevant instances
    if not uri or not property or not new_value:
        return 'URI, property, or new value not provided', 400

    property_name = ifixthat.search_one(iri=property).name
    if property_name is None:
        return 'Property not found', 404

    instance = ifixthat.search_one(iri=uri)
    if instance is None:
        return 'URI not found', 404

    # Setting the new value
    try:
        setattr(instance, property_name, [new_value])
    except AttributeError:
        return f"Property '{property_name}' not found on instance", 400


    # Saving the ontology - using file lock to prevent file from wiping
    lock_path = "../ontology.owl.lock"
    file_lock = FileLock(lock_path)
    try:
        with file_lock:  # This ensures only one request can write at a time
            ifixthat.save(file="../ontology.owl", format="rdfxml")
    except Exception as e:
        return f"Error saving ontology: {str(e)}", 500

    return 'Entry edited', 200