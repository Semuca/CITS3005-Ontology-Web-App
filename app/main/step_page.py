from flask import render_template, redirect
from rdflib import URIRef

from .links import Link
from .views import main_bp, ifixthat

@main_bp.route("/Step/<step>")
def step_page(step: str) -> str:
    """The step page"""
    from main.views import shacl_results

    step_instance = ifixthat.search_one(type=ifixthat.Step, iri=f"*#{step}")
    if step_instance is None:
        return redirect('/')

    uri = URIRef(step_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    actions = step_instance.actions[0]
    tools = [Link(tool, 'http://ifixthat.org/usesTool', parent_uri=step_instance.iri) for tool in step_instance.usesTool]

    ordered_steps_with_step = ifixthat.search(type=ifixthat.OrderedStep, details=step_instance)

    procedures = []
    for ordered_step in ordered_steps_with_step:
        procedure = ifixthat.search_one(type=ifixthat.Procedure, hasStep=ordered_step)
        procedures.append(Link(procedure, 'http://ifixthat.org/hasStep', child_uri=step_instance.iri, images=[image.dataUrl for image in procedure.hasImage]))

    images = [Link(has_image, 'http://ifixthat.org/hasImage', parent_uri=step_instance.iri, images=has_image.dataUrl, hideContent=True) for has_image in step_instance.hasImage]

    return render_template('step.html', errors=errors, uri=step_instance.iri, images=images, actions=actions, procedures=procedures, tools=tools)
