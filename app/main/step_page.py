from flask import render_template
import rdflib

from .views import main_bp, Link, domain

@main_bp.route("/step/<step>")
def step_page(step: str) -> str:
    """The step page"""

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

    uri = f"<{domain}step/{step}>"

    actions = list(g.query(f"""
        SELECT ?actions
        WHERE {{
            {uri} props:actions ?actions .
        }}
    """))[0][0]

    procedureQuery = f"""
        SELECT ?procedure
        WHERE {{
            {uri} props:stepOf ?procedure .
        }}
    """

    procedures = []
    for result in g.query(procedureQuery):
        ref = result[0]
        id = ref.split('/')[-1]
        procedures.append(Link(ref, id, 'Procedure', f'/procedure/{id}'))

    toolQuery = f"""
        SELECT ?tool
        WHERE {{
            {uri} props:usesTool ?tool .
        }}
    """

    tools = []
    for result in g.query(toolQuery):
        ref = result[0]
        id = ref.split('/')[-1]
        tools.append(Link(ref, id, 'Tool', f'/tool/{id}'))

    return render_template('step.html', actions=actions, procedures=procedures, tools=tools)