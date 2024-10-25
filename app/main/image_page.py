from flask import render_template, redirect
from rdflib import URIRef

from .links import Link
from .views import main_bp, ifixthat

@main_bp.route("/Image/<image>")
def image_page(image: str) -> str:
    """The image page"""
    from main.views import shacl_results

    image_instance = ifixthat.search_one(type=ifixthat.Image, iri=f"*#{image}")
    if image_instance is None:
        return redirect('/')
    
    uri = URIRef(image_instance.iri)
    errors = list(filter(lambda shacl_result: shacl_result.get('focusNode', None) == uri, shacl_results))

    url = image_instance.dataUrl[0]

    steps_for_item = ifixthat.search(type=ifixthat.Step, hasImage=image_instance)
    steps = [Link(step, 'http://ifixthat.org/hasImage', child_uri=image_instance.iri) for step in steps_for_item]

    tools_of_item = ifixthat.search(type=ifixthat.Tool, hasImage=image_instance)
    tools = [Link(tool, 'http://ifixthat.org/hasImage', child_uri=image_instance.iri) for tool in tools_of_item]

    return render_template('image.html', errors=errors, uri=image_instance.iri, url=url, steps=steps, tools=tools)
