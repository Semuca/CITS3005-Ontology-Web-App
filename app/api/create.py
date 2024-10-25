"""Defines endpoint for creating entries"""

from flask import request
from .bp import api_bp
from main.views import domain, ifixthat
from filelock import FileLock

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

@api_bp.route('/links', methods=['POST'])
def create_link():
    """Create a link between two instances"""
    # Parameters
    body = request.get_json()
    parentUri = body.get('parentUri')
    childUri = body.get('childUri')
    property = body.get('property')
    linkId = body.get('linkId')
    objectType = body.get('objectType')

    if (not parentUri and not childUri) or not property or not linkId or not objectType:
        return 'Subject, property, link ID or object type not provided', 400

    prop_name = ifixthat.search_one(iri=property).name
    if prop_name is None:
        return f'Property {property} not found', 404

    rdf_type_ref = getattr(ifixthat, objectType, None)
    if rdf_type_ref is None:
        return 'RDF type not found', 404

    try:
        if parentUri is None:
            parent_instance = ifixthat.search_one(is_a=rdf_type_ref, iri=f"*#{linkId}")
            child_instance = ifixthat.search_one(iri=childUri)
        else:
            parent_instance = ifixthat.search_one(iri=parentUri)
            child_instance = ifixthat.search_one(is_a=rdf_type_ref, iri=f"*#{linkId}")

        if prop_name == "hasStep":
            num_steps = len(parent_instance.hasStep)
            ordered_step_instance = ifixthat.OrderedStep()
            ordered_step_instance.details.append(child_instance)
            ordered_step_instance.order.append(num_steps)
            parent_instance.hasStep.append(ordered_step_instance)
        else:
            getattr(parent_instance, prop_name).append(child_instance)
    except Exception as e:
        return f"Error linking instances: {str(e)}", 500

    # Saving the ontology - using file lock to prevent file from wiping
    lock_path = "../ontology.owl.lock"
    file_lock = FileLock(lock_path)
    try:
        with file_lock:  # This ensures only one request can write at a time
            ifixthat.save(file="../ontology.owl", format="rdfxml")
    except Exception as e:
        return f"Error saving ontology: {str(e)}", 500

    return 'Link created', 201