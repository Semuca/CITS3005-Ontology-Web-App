from flask import render_template

from .views import main_bp, domain, Link, g

@main_bp.route("/tool/<tool>")
def tool_page(tool: str) -> str:
    """The tool page"""

    uri = f"<{domain}tool/{tool}>"

    label = list(g.query(f"""
        SELECT ?label
        WHERE {{
            {uri} rdfs:label ?label .
        }}
    """))[0][0]

    supplier_url = list(g.query(f"""
        SELECT ?supplierUrl
        WHERE {{
            {uri} props:supplierUrl ?supplierUrl .
        }}
    """))[0][0]

    query = f"""
        SELECT ?procedure ?label
        WHERE {{
            ?procedure props:requiresTool {uri} .
            ?procedure rdfs:label ?label .
        }}
    """

    procedures = []
    for ref, tool_label in g.query(query):
        id = ref.split('/')[-1]
        procedures.append(Link(ref, tool_label, 'Procedure', f'/procedure/{id}'))

    return render_template('tool.html', label=label, supplier_url=supplier_url, procedures=procedures)