from flask import render_template
import rdflib
from .views import main_bp, Link, domain

@main_bp.route("/part/<part>")
def part_page(part: str) -> str:
    """The part page"""

    g = rdflib.Graph()
    g.parse("../graph.rdf", format="xml")

    query = f"""
        SELECT ?procedure
        WHERE {{
            <{domain}part/{part}> props:stepOf ?procedure .
        }}
    """

    procedures = []
    for result in g.query(query):
        uri = result[0]
        id = uri.split('/')[-1]
        procedures.append(Link(id, 'Procedure', f'/procedure/{id}'))

    return render_template('part.html', procedures=procedures)