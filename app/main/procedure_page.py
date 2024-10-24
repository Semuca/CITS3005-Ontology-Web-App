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
        steps.append(Link(step_ref, subtitle=step_actions))

    return render_template('procedure.html', label=label, steps=steps, parts=parts, tools=tools)
