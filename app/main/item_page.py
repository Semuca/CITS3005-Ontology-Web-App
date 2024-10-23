from flask import render_template
from .views import main_bp, Link, domain, g

@main_bp.route("/item/<item>")
def item_page(item: str) -> str:
    """The item page"""

    uri = f"<{domain}item/{item}>"

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    query = f"""
        SELECT ?procedure ?label
        WHERE {{
            ?procedure props:guideOf {uri} .
            ?procedure rdfs:label ?label .
        }}
    """

    procedures = []
    for ref, procedure_label in g.query(query):
        id = ref.split('/')[-1]
        procedures.append(Link(ref, procedure_label, 'Procedure', f'/procedure/{id}'))

    return render_template('item.html', label=label, procedures=procedures)