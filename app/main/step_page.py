from flask import render_template

from .views import main_bp, Link, ifixthat

@main_bp.route("/Step/<step>")
def step_page(step: str) -> str:
    """The step page"""
    step_instance = ifixthat.search_one(type=ifixthat.Step, iri=f"*{step}")

    actions = step_instance.actions[0]
    tools = [Link(tool) for tool in step_instance.usesTool]

    orderedsteps_with_step = ifixthat.search(type=ifixthat.OrderedStep, details=step_instance)

    procedures = []
    for orderedstep in orderedsteps_with_step:
        procedure = ifixthat.search_one(type=ifixthat.Procedure, hasStep=orderedstep)
        procedures.append(Link(procedure))

    return render_template('step.html', actions=actions, procedures=procedures, tools=tools)
