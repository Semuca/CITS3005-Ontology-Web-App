"""Defines endpoint for creating entries"""
# By Heidi Leow (23643117) and James Frayne (23372032)

from flask import request
from .bp import api_bp
from main.views import ifixthat
from owlready2 import destroy_entity
from filelock import FileLock

@api_bp.route('/', methods=['DELETE'])
def delete_entry():
    """Delete an entry"""

    body = request.get_json()
    uri = body.get('uri')

    if not uri:
        return 'URI not provided', 400

    instance = ifixthat.search_one(iri=uri)

    if instance.is_a[0].name == "Procedure":
        for ordered_step in instance.hasStep:
            destroy_entity(ordered_step)
    if instance.is_a[0].name == "Step":
        for ordered_step in ifixthat.search(is_a=ifixthat.OrderedStep, details=instance):
            procedure_instance = ifixthat.search_one(is_a=ifixthat.Procedure, hasStep=ordered_step)
            order = ordered_step.order[0]
            for step in procedure_instance.hasStep[order:]:
                step.order[0] -= 1
            destroy_entity(ordered_step)

    destroy_entity(instance)

    ifixthat.save(file="../ontology.owl")

    return 'Entry deleted', 200

@api_bp.route('/links', methods=['DELETE'])
def delete_link():
    """Delete a link between two instances"""
    # Parameters
    body = request.get_json()
    parentUri = body.get('parentUri')
    childUri = body.get('childUri')
    uri = body.get('uri')
    property = body.get('property')

    # Getting instances
    if (not parentUri and not childUri) or not property or not uri:
        return 'URI, property, or new value not provided', 400

    prop_name = ifixthat.search_one(iri=property).name
    if prop_name is None:
        return f'Property {property} not found', 404

    if parentUri is None:
        parentUri = uri
    if childUri is None:
        childUri = uri

    parent_instance = ifixthat.search_one(iri=parentUri)
    child_instance = ifixthat.search_one(iri=childUri)

    # Removing the link
    if prop_name == "hasStep":
        found_step = False
        for step in parent_instance.hasStep:
            if step.details[0] == child_instance:
                parent_instance.hasStep.remove(step)
                destroy_entity(step)
                found_step = True
            elif found_step:
                step.order[0] -= 1
    else:
        getattr(parent_instance, prop_name).remove(child_instance)

    # Saving the ontology - using file lock to prevent file from wiping
    lock_path = "../ontology.owl.lock"
    file_lock = FileLock(lock_path)
    try:
        with file_lock:  # This ensures only one request can write at a time
            ifixthat.save(file="../ontology.owl", format="rdfxml")
    except Exception as e:
        return f"Error saving ontology: {str(e)}", 500

    ifixthat.save(file="../ontology.owl")

    return 'Link deleted', 200