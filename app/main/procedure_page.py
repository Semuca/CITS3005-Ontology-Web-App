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
        SELECT ?step ?actions
        WHERE {{
            ?step props:stepOf {uri} .
            ?step props:actions ?actions .
        }}
    """

    steps = []
    for ref, actions in g.query(stepsQuery):
        id = ref.split('/')[-1]
        steps.append(Link(ref, actions, 'Step', f'/step/{id}'))

    subjectQuery = f"""
        SELECT ?subject ?type
        WHERE {{
            {uri} props:guideOf ?subject .
            ?subject rdf:type ?type .
        }}
    """

    parts = []
    for ref, rdf_type in g.query(subjectQuery):
        id = ref.split('/')[-1]
        if str(rdf_type) == f'{domain}properties/Part':
            parts.append(Link(ref, id, 'Part', f'/part/{id}'))
        else:
            parts.append(Link(ref, id, 'Item', f'/item/{id}'))

    toolsQuery = f"""
        SELECT ?tool ?label
        WHERE {{
            {uri} props:requiresTool ?tool .
            ?tool rdfs:label ?label .
        }}
    """

    tools = []
    for ref, tool_label in g.query(toolsQuery):
        id = ref.split('/')[-1]
        tools.append(Link(ref, tool_label, 'Tool', f'/tool/{id}'))

    return render_template('procedure.html', label=label, steps=steps, parts=parts, tools=tools)