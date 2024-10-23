from flask import render_template
import rdflib

from .views import main_bp, Link, domain

@main_bp.route("/procedure/<procedure>")
def procedure_page(procedure: str) -> str:
    """The procedure page"""

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

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
        id = result[0].split('/')[-1]
        steps.append(Link(id, 'Step', f'/step/{id}'))

    itemsQuery = f"""
        SELECT ?item
        WHERE {{
            {uri} props:guideOf ?item .
        }}
    """

    items = []
    for result in g.query(itemsQuery):
        id = result[0].split('/')[-1]
        items.append(Link(id, 'Item', f'/item/{id}'))

    partsQuery = f"""
        SELECT ?part
        WHERE {{
            {uri} props:guideOf ?part .
        }}
    """

    parts = []
    for result in g.query(partsQuery):
        id = result[0].split('/')[-1]
        parts.append(Link(id, 'Part', f'/part/{id}'))

    toolsQuery = f"""
        SELECT ?tool
        WHERE {{
            {uri} props:requiresTool ?tool .
        }}
    """

    tools = []
    for result in g.query(toolsQuery):
        id = result[0].split('/')[-1]
        tools.append(Link(id, 'Tool', f'/tool/{id}'))

    return render_template('procedure.html', label=label, steps=steps, items=items, parts=parts, tools=tools)