from flask import render_template

from .views import main_bp, Link, ifixthat

@main_bp.route("/Procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""
    procedure_instance = ifixthat.search_one(type=ifixthat.Procedure, iri=f"*{procedure}")

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

    return render_template('procedure.html', uri=procedure_instance.iri, label=label, steps=steps, parts=parts, tools=tools)
