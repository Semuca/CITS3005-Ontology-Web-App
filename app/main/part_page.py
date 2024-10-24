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

    itemsQuery = f"""
        SELECT ?item ?label
        WHERE {{
            {uri} props:partOf ?item .
            ?item rdfs:label ?label .
        }}
    """

    items = []
    for ref, item_label in g.query(itemsQuery):
        items.append(Link(ref, title=item_label))

    proceduresQuery = f"""
        SELECT ?procedure ?label
        WHERE {{
            ?procedure props:guideOf {uri} .
            ?procedure rdfs:label ?label .
        }}
    """

    procedures = []
    for ref, procedure_label in g.query(proceduresQuery):
        procedures.append(Link(ref, title=procedure_label))

    return render_template('part.html', label=label, items=items, procedures=procedures)