from flask import render_template
import rdflib
from .views import main_bp, Link, domain

@main_bp.route("/part/<part>")
def part_page(part: str) -> str:
    """The part page"""

    uri = f"<{domain}part/{part}>"

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
            {uri} props:partOf ?procedure .
        }}
    """

    procedures = []
    for result in g.query(query):
        ref = result[0]
        id = ref.split('/')[-1]
        procedures.append(Link(ref, id, 'Procedure', f'/procedure/{id}'))

    return render_template('part.html', label=label, procedures=procedures)