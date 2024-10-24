from flask import render_template
from .views import main_bp, Link, domain, g

@main_bp.route("/part/<part>")
def part_page(part: str) -> str:
    """The part page"""

    uri = f"<{domain}part/{part}>"

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    query = f"""
        SELECT ?procedure ?label
        WHERE {{
            {uri} props:partOf ?procedure .
            ?procedure rdfs:label ?label .
        }}
    """

    procedures = []
    for ref, procedure_label in g.query(query):
        procedures.append(Link(ref, title=procedure_label))

    return render_template('part.html', label=label, procedures=procedures)