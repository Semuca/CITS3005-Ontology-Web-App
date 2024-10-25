from flask import render_template, redirect
from .views import main_bp, Link, ifixthat

@main_bp.route("/Image/<image>")
def image_page(image: str) -> str:
    """The image page"""
    image_instance = ifixthat.search_one(type=ifixthat.Image, iri=f"*#{image}")
    if image_instance is None:
        return redirect('/')

    url = image_instance.dataUrl[0]

    steps_for_item = ifixthat.search(type=ifixthat.Step, hasImage=image_instance)
    steps = [Link(step) for step in steps_for_item]

    tools_of_item = ifixthat.search(type=ifixthat.Tool, hasImage=image_instance)
    tools = [Link(tool) for tool in tools_of_item]

    return render_template('image.html', uri=image_instance.iri, url=url, steps=steps, tools=tools)
