from flask import render_template

from .views import main_bp, Link, domain, g

@main_bp.route("/procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""

    uri = f"<{domain}procedure/{procedure}>"

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    stepsQuery = f"""
        SELECT ?step
        WHERE {{
            ?step props:stepOf {uri} .
        }}
    """

    steps = []
    for result in g.query(stepsQuery):
        ref = result[0]
        id = ref.split('/')[-1]
        steps.append(Link(ref, id, 'Step', f'/step/{id}'))

    partsQuery = f"""
        SELECT ?part
        WHERE {{
            {uri} props:guideOf ?part .
        }}
    """

    parts = []
    for result in g.query(partsQuery):
        ref = result[0]
        id = ref.split('/')[-1]
        parts.append(Link(ref, id, 'Part', f'/part/{id}'))

    toolsQuery = f"""
        SELECT ?tool
        WHERE {{
            {uri} props:requiresTool ?tool .
        }}
    """

    tools = []
    for result in g.query(toolsQuery):
        ref = result[0]
        id = ref.split('/')[-1]
        tools.append(Link(ref, id, 'Tool', f'/tool/{id}'))

    return render_template('procedure.html', label=label, steps=steps, parts=parts, tools=tools)