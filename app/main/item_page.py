from flask import render_template
import rdflib
from .views import main_bp, Link, domain

@main_bp.route("/item/<item>")
def item_page(item: str) -> str:
    """The item page"""

    uri = f"<{domain}item/{item}>"

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    query = f"""
        SELECT ?procedure
        WHERE {{
            ?procedure props:guideOf {uri} .
        }}
    """

    procedures = []
    for result in g.query(query):
        ref = result[0]
        id = ref.split('/')[-1]
        procedures.append(Link(ref, id, 'Procedure', f'/procedure/{id}'))

    return render_template('item.html', label=label, procedures=procedures)