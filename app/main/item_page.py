from flask import render_template
import rdflib
from .views import main_bp, Link, domain

@main_bp.route("/item/<item>")
def item_page(item: str) -> str:
    """The item page"""

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

    query = f"""
        SELECT ?procedure
        WHERE {{
            ?procedure props:guideOf <{domain}item/{item}> .
        }}
    """

    procedures = []
    for result in g.query(query):
        uri = result[0]
        id = uri.split('/')[-1]
        procedures.append(Link(id, 'Procedure', f'/procedure/{id}'))

    return render_template('item.html', procedures=procedures)