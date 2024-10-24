from flask import render_template

from .views import main_bp, Link, domain, g

@main_bp.route("/procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""

    uri = f"<{domain}procedure/{procedure}>"
    print(uri)

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
        steps.append(Link(ref, subtitle=actions))

    subjectQuery = f"""
        SELECT ?subject ?type
        WHERE {{
            {uri} props:guideOf ?subject .
            ?subject rdf:type ?type .
        }}
    """

    parts = []
    for ref, rdf_type in g.query(subjectQuery):
        if str(rdf_type) == f'{domain}properties/Part':
            parts.append(Link(ref))
        else:
            parts.append(Link(ref))

    toolsQuery = f"""
        SELECT ?tool ?label
        WHERE {{
            {uri} props:requiresTool ?tool .
            ?tool rdfs:label ?label .
        }}
    """

    tools = []
    for ref, tool_label in g.query(toolsQuery):
        tools.append(Link(ref, title=tool_label))

    return render_template('procedure.html', label=label, steps=steps, parts=parts, tools=tools)