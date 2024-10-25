from flask import render_template, redirect
from rdflib import URIRef

from .views import main_bp, Link, ifixthat, shacl_results

@main_bp.route("/Procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""
    procedure_instance = ifixthat.search_one(type=ifixthat.Procedure, iri=f"*#{procedure}")
    if procedure_instance is None:
        return redirect('/')

    uri = URIRef(procedure_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    label = procedure_instance.label[0]
    parts = [Link(part) for part in procedure_instance.guideOf]
    tools = [Link(tool) for tool in procedure_instance.requiresTool]

    steps = []
    for step in procedure_instance.hasStep:
        step_ref = step.details[0]
        step_actions = step_ref.actions[0]
        step_images = [url for has_image in step_ref.hasImage for url in has_image.dataUrl]
        steps.append((step_ref, step_actions, step_images))

    steps.sort(key=lambda x: x[0].order)
    steps = [Link(step_ref, subtitle=step_actions, images=step_images) for step_ref, step_actions, step_images in steps]

    return render_template('procedure.html', errors=errors, uri=procedure_instance.iri, label=label, steps=steps, parts=parts, tools=tools)
