from flask import render_template

from .views import main_bp, Link, domain, g

@main_bp.route("/step/<step>")
def step_page(step: str) -> str:
    """The step page"""

    uri = f"<{domain}step/{step}>"

    actions = list(g.query(f"""
        SELECT ?actions
        WHERE {{
            {uri} props:actions ?actions .
        }}
    """))[0][0]

    procedureQuery = f"""
        SELECT ?procedure ?label
        WHERE {{
            {uri} props:stepOf ?procedure .
            ?procedure rdfs:label ?label .
        }}
    """

    procedures = []
    for ref, label in g.query(procedureQuery):
        id = ref.split('/')[-1]
        procedures.append(Link(ref, label, 'Procedure', f'/procedure/{id}'))

    toolQuery = f"""
        SELECT ?tool ?label
        WHERE {{
            {uri} props:usesTool ?tool .
            ?tool rdfs:label ?label .
        }}
    """

    tools = []
    for ref, label in g.query(toolQuery):
        id = ref.split('/')[-1]
        tools.append(Link(ref, label, 'Tool', f'/tool/{id}'))

    return render_template('step.html', actions=actions, procedures=procedures, tools=tools)